#!/usr/bin/env python3
"""
Fetch YouTube channel playlists and videos using the official YouTube Data API v3.
Requires an API key from Google Cloud Console.
"""

import os
import sys
import json
import requests
from typing import List, Dict, Any, Optional
from datetime import datetime


class YouTubeAPIClient:
    """Client for interacting with YouTube Data API v3."""

    BASE_URL = "https://www.googleapis.com/youtube/v3"

    def __init__(self, api_key: str):
        """
        Initialize the YouTube API client.

        Args:
            api_key: YouTube Data API v3 key from Google Cloud Console
        """
        self.api_key = api_key
        self.session = requests.Session()

    def _make_request(self, endpoint: str, params: Dict[str, Any]) -> Dict[str, Any]:
        """
        Make a request to the YouTube API.

        Args:
            endpoint: API endpoint (e.g., 'channels', 'playlists', 'playlistItems')
            params: Query parameters

        Returns:
            JSON response from the API
        """
        params['key'] = self.api_key
        url = f"{self.BASE_URL}/{endpoint}"

        try:
            response = self.session.get(url, params=params, timeout=30)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as e:
            print(f"API request error: {e}", file=sys.stderr)
            if hasattr(e, 'response') and e.response is not None:
                print(f"Response: {e.response.text}", file=sys.stderr)
            return {}

    def get_channel_by_username(self, username: str) -> Optional[Dict[str, Any]]:
        """
        Get channel information by username (handle).

        Args:
            username: Channel username/handle (without @)

        Returns:
            Channel information dict or None
        """
        # Try with forUsername first
        params = {
            'part': 'snippet,contentDetails,statistics',
            'forUsername': username
        }

        data = self._make_request('channels', params)

        if data.get('items'):
            return data['items'][0]

        # If not found, try with handle (newer format)
        params = {
            'part': 'snippet,contentDetails,statistics',
            'forHandle': username if not username.startswith('@') else username
        }

        data = self._make_request('channels', params)

        if data.get('items'):
            return data['items'][0]

        return None

    def get_channel_by_id(self, channel_id: str) -> Optional[Dict[str, Any]]:
        """
        Get channel information by channel ID.

        Args:
            channel_id: YouTube channel ID

        Returns:
            Channel information dict or None
        """
        params = {
            'part': 'snippet,contentDetails,statistics',
            'id': channel_id
        }

        data = self._make_request('channels', params)

        if data.get('items'):
            return data['items'][0]

        return None

    def get_channel_playlists(self, channel_id: str, max_results: int = 50) -> List[Dict[str, Any]]:
        """
        Get all playlists from a channel.

        Args:
            channel_id: YouTube channel ID
            max_results: Maximum number of playlists to fetch

        Returns:
            List of playlist dicts
        """
        playlists = []
        params = {
            'part': 'snippet,contentDetails',
            'channelId': channel_id,
            'maxResults': min(max_results, 50)  # API max is 50 per request
        }

        while True:
            data = self._make_request('playlists', params)

            if not data or 'items' not in data:
                break

            playlists.extend(data['items'])

            # Check if there are more results
            next_page_token = data.get('nextPageToken')
            if next_page_token and len(playlists) < max_results:
                params['pageToken'] = next_page_token
            else:
                break

        return playlists[:max_results]

    def get_playlist_videos(self, playlist_id: str, max_results: int = 50) -> List[Dict[str, Any]]:
        """
        Get videos from a playlist.

        Args:
            playlist_id: YouTube playlist ID
            max_results: Maximum number of videos to fetch

        Returns:
            List of video dicts
        """
        videos = []
        params = {
            'part': 'snippet,contentDetails',
            'playlistId': playlist_id,
            'maxResults': min(max_results, 50)
        }

        while True:
            data = self._make_request('playlistItems', params)

            if not data or 'items' not in data:
                break

            videos.extend(data['items'])

            # Check if there are more results
            next_page_token = data.get('nextPageToken')
            if next_page_token and len(videos) < max_results:
                params['pageToken'] = next_page_token
            else:
                break

        return videos[:max_results]

    def search_channel_videos(self, channel_id: str, query: str = "", max_results: int = 50) -> List[Dict[str, Any]]:
        """
        Search for videos in a channel.

        Args:
            channel_id: YouTube channel ID
            query: Search query
            max_results: Maximum number of videos to fetch

        Returns:
            List of video dicts
        """
        videos = []
        params = {
            'part': 'snippet',
            'channelId': channel_id,
            'type': 'video',
            'order': 'date',  # Most recent first
            'maxResults': min(max_results, 50)
        }

        if query:
            params['q'] = query

        while True:
            data = self._make_request('search', params)

            if not data or 'items' not in data:
                break

            videos.extend(data['items'])

            # Check if there are more results
            next_page_token = data.get('nextPageToken')
            if next_page_token and len(videos) < max_results:
                params['pageToken'] = next_page_token
            else:
                break

        return videos[:max_results]

    def get_video_details(self, video_ids: List[str]) -> List[Dict[str, Any]]:
        """
        Get detailed information about videos.

        Args:
            video_ids: List of video IDs

        Returns:
            List of video detail dicts
        """
        if not video_ids:
            return []

        videos = []
        # API allows up to 50 IDs per request
        for i in range(0, len(video_ids), 50):
            batch = video_ids[i:i+50]
            params = {
                'part': 'snippet,contentDetails,statistics',
                'id': ','.join(batch)
            }

            data = self._make_request('videos', params)

            if data and 'items' in data:
                videos.extend(data['items'])

        return videos


def format_duration(duration: str) -> str:
    """
    Convert ISO 8601 duration to readable format.

    Args:
        duration: ISO 8601 duration string (e.g., 'PT15M30S')

    Returns:
        Formatted duration (e.g., '15:30')
    """
    import re

    match = re.match(r'PT(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?', duration)
    if not match:
        return "Unknown"

    hours, minutes, seconds = match.groups()
    hours = int(hours) if hours else 0
    minutes = int(minutes) if minutes else 0
    seconds = int(seconds) if seconds else 0

    if hours > 0:
        return f"{hours}:{minutes:02d}:{seconds:02d}"
    else:
        return f"{minutes}:{seconds:02d}"


def filter_beginner_videos(videos: List[Dict[str, Any]], keywords: List[str]) -> List[Dict[str, Any]]:
    """Filter videos that contain beginner-related keywords in title or description."""
    filtered = []
    for video in videos:
        snippet = video.get('snippet', {})
        title = snippet.get('title', '').lower()
        description = snippet.get('description', '').lower()

        if any(keyword.lower() in title or keyword.lower() in description for keyword in keywords):
            filtered.append(video)

    return filtered


def main():
    """Main function to fetch YouTube cooking channel data."""

    # Get API key from environment or command line
    api_key = os.environ.get('YOUTUBE_API_KEY')

    if not api_key:
        if len(sys.argv) > 1:
            api_key = sys.argv[1]
        else:
            print("Error: YouTube API key required!", file=sys.stderr)
            print("\nUsage:", file=sys.stderr)
            print("  1. Set environment variable: export YOUTUBE_API_KEY='your-key'", file=sys.stderr)
            print("  2. Or pass as argument: python fetch_youtube_api.py YOUR_API_KEY", file=sys.stderr)
            print("\nGet an API key from:", file=sys.stderr)
            print("  https://console.cloud.google.com/apis/credentials", file=sys.stderr)
            sys.exit(1)

    print(f"Using YouTube Data API v3", file=sys.stderr)

    # Initialize API client
    client = YouTubeAPIClient(api_key)

    # Channel information
    channels = {
        'Ethan Chlebowski': {
            'id': 'UCJjlcL2AgENfU-uvxIqZawA',
            'username': 'ethanchlebowski',
            'url': 'https://youtube.com/@ethanchlebowski'
        },
        'Joshua Weissman': {
            'id': 'UChBEbMKI1eCcejTtmI32UEw',
            'username': 'joshuaweissman',
            'url': 'https://youtube.com/@joshuaweissman'
        }
    }

    # Keywords for beginner content
    beginner_keywords = [
        'beginner', 'basics', 'fundamental', 'guide', 'kitchen organization',
        'knife skills', 'essential', 'tips', 'how to', 'mistakes',
        'pantry', 'equipment', 'tools', 'setup', 'start', 'easy'
    ]

    all_data = {}

    for channel_name, channel_info in channels.items():
        print(f"\n{'='*60}", file=sys.stderr)
        print(f"Processing: {channel_name}", file=sys.stderr)
        print(f"{'='*60}\n", file=sys.stderr)

        channel_id = channel_info['id']

        # Get channel details
        print("Fetching channel information...", file=sys.stderr)
        channel_details = client.get_channel_by_id(channel_id)

        if not channel_details:
            print(f"Warning: Could not fetch channel details for {channel_name}", file=sys.stderr)
            continue

        # Get playlists
        print("Fetching playlists...", file=sys.stderr)
        playlists = client.get_channel_playlists(channel_id, max_results=50)
        print(f"Found {len(playlists)} playlists", file=sys.stderr)

        # Search for beginner videos
        print("Searching for beginner-friendly videos...", file=sys.stderr)
        beginner_search_results = []

        # Search with different beginner-related terms
        for keyword in ['beginner guide', 'basics', 'fundamentals', 'kitchen organization', 'knife skills']:
            results = client.search_channel_videos(channel_id, query=keyword, max_results=10)
            beginner_search_results.extend(results)

        # Remove duplicates based on video ID
        seen_ids = set()
        unique_beginner_videos = []
        for video in beginner_search_results:
            video_id = video.get('id', {}).get('videoId')
            if video_id and video_id not in seen_ids:
                seen_ids.add(video_id)
                unique_beginner_videos.append(video)

        print(f"Found {len(unique_beginner_videos)} beginner-related videos", file=sys.stderr)

        # Get recent videos
        print("Fetching recent videos...", file=sys.stderr)
        recent_videos = client.search_channel_videos(channel_id, max_results=30)
        print(f"Found {len(recent_videos)} recent videos", file=sys.stderr)

        # Store data
        all_data[channel_name] = {
            'url': channel_info['url'],
            'channel_id': channel_id,
            'channel_details': channel_details,
            'playlists': playlists,
            'beginner_videos': unique_beginner_videos,
            'recent_videos': recent_videos
        }

    # Save raw data to JSON
    output_file = 'youtube_api_data.json'
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(all_data, f, indent=2, ensure_ascii=False)

    print(f"\n{'='*60}", file=sys.stderr)
    print(f"Data saved to: {output_file}", file=sys.stderr)
    print(f"{'='*60}\n", file=sys.stderr)

    # Generate markdown report
    markdown_file = 'YOUTUBE_API_RESULTS.md'
    with open(markdown_file, 'w', encoding='utf-8') as f:
        f.write("# YouTube Cooking Channels - API Results\n\n")
        f.write(f"*Data fetched via YouTube Data API v3 on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*\n\n")
        f.write("---\n\n")

        for channel_name, data in all_data.items():
            channel_details = data.get('channel_details', {})
            snippet = channel_details.get('snippet', {})
            statistics = channel_details.get('statistics', {})

            f.write(f"\n## {channel_name}\n\n")
            f.write(f"**Channel:** [{channel_name}]({data['url']})\n\n")

            # Channel stats
            if statistics:
                subscriber_count = statistics.get('subscriberCount', 'Hidden')
                video_count = statistics.get('videoCount', 'Unknown')
                view_count = statistics.get('viewCount', 'Unknown')

                f.write("### Channel Statistics\n\n")
                f.write(f"- **Subscribers:** {subscriber_count:,} (if not hidden)\n")
                f.write(f"- **Total Videos:** {video_count:,}\n")
                f.write(f"- **Total Views:** {view_count:,}\n\n")

            # Description
            description = snippet.get('description', '')
            if description:
                f.write("### About\n\n")
                # Limit description length
                desc_preview = description[:300] + "..." if len(description) > 300 else description
                f.write(f"{desc_preview}\n\n")

            # Playlists
            playlists = data.get('playlists', [])
            if playlists:
                f.write(f"### Playlists ({len(playlists)} total)\n\n")
                for playlist in playlists:
                    pl_snippet = playlist.get('snippet', {})
                    pl_title = pl_snippet.get('title', 'Unknown')
                    pl_id = playlist.get('id', '')
                    pl_url = f"https://youtube.com/playlist?list={pl_id}"
                    pl_video_count = playlist.get('contentDetails', {}).get('itemCount', '?')

                    f.write(f"**[{pl_title}]({pl_url})**\n")
                    f.write(f"- {pl_video_count} videos\n")

                    pl_desc = pl_snippet.get('description', '')
                    if pl_desc:
                        desc_preview = pl_desc[:150] + "..." if len(pl_desc) > 150 else pl_desc
                        f.write(f"- {desc_preview}\n")
                    f.write("\n")

            # Beginner videos
            beginner_videos = data.get('beginner_videos', [])
            if beginner_videos:
                f.write(f"### Beginner-Friendly Videos ({len(beginner_videos)} found)\n\n")
                for video in beginner_videos[:20]:  # Limit to 20
                    vid_snippet = video.get('snippet', {})
                    vid_title = vid_snippet.get('title', 'Unknown')
                    vid_id = video.get('id', {}).get('videoId', '')
                    vid_url = f"https://youtube.com/watch?v={vid_id}"
                    vid_published = vid_snippet.get('publishedAt', '')[:10]

                    f.write(f"- [{vid_title}]({vid_url})")
                    if vid_published:
                        f.write(f" - {vid_published}")
                    f.write("\n")
                f.write("\n")

            # Recent videos
            recent_videos = data.get('recent_videos', [])
            if recent_videos:
                f.write(f"### Recent Videos ({len(recent_videos[:15])} shown)\n\n")
                for video in recent_videos[:15]:
                    vid_snippet = video.get('snippet', {})
                    vid_title = vid_snippet.get('title', 'Unknown')
                    vid_id = video.get('id', {}).get('videoId', '')
                    vid_url = f"https://youtube.com/watch?v={vid_id}"
                    vid_published = vid_snippet.get('publishedAt', '')[:10]

                    f.write(f"- [{vid_title}]({vid_url})")
                    if vid_published:
                        f.write(f" - {vid_published}")
                    f.write("\n")
                f.write("\n")

            f.write("---\n\n")

    print(f"Markdown report saved to: {markdown_file}", file=sys.stderr)
    print("\n✅ Done!", file=sys.stderr)


if __name__ == '__main__':
    main()
