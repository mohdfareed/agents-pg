#!/usr/bin/env python3
"""
Fetch YouTube channel playlists and videos for cooking watch list.
Uses yt-dlp to extract playlist and video information without API keys.
"""

import json
import subprocess
import sys
from typing import Dict, List, Any


def run_ytdlp(url: str, extract_flat: bool = True) -> Dict[str, Any]:
    """
    Run yt-dlp to extract information from YouTube URL.

    Args:
        url: YouTube channel or playlist URL
        extract_flat: If True, only extract playlist info without individual videos

    Returns:
        Dictionary containing extracted information
    """
    cmd = [
        'yt-dlp',
        '--dump-json',
        '--no-warnings',
        '--quiet',
    ]

    if extract_flat:
        cmd.append('--flat-playlist')

    cmd.append(url)

    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            check=True
        )

        # yt-dlp outputs one JSON object per line for playlists
        lines = result.stdout.strip().split('\n')
        if len(lines) == 1:
            return json.loads(lines[0])
        else:
            return [json.loads(line) for line in lines if line]

    except subprocess.CalledProcessError as e:
        print(f"Error running yt-dlp: {e}", file=sys.stderr)
        print(f"stderr: {e.stderr}", file=sys.stderr)
        return {}
    except json.JSONDecodeError as e:
        print(f"Error parsing JSON: {e}", file=sys.stderr)
        return {}


def get_channel_playlists(channel_url: str) -> List[Dict[str, Any]]:
    """
    Get all playlists from a YouTube channel.

    Args:
        channel_url: YouTube channel URL (e.g., https://youtube.com/@channelname)

    Returns:
        List of playlist dictionaries with id, title, and other metadata
    """
    playlists_url = f"{channel_url}/playlists"
    print(f"Fetching playlists from: {playlists_url}", file=sys.stderr)

    result = run_ytdlp(playlists_url, extract_flat=True)

    if isinstance(result, dict) and 'entries' in result:
        return result['entries']
    elif isinstance(result, list):
        return result
    else:
        return []


def get_playlist_videos(playlist_url: str, max_videos: int = 50) -> List[Dict[str, Any]]:
    """
    Get videos from a YouTube playlist.

    Args:
        playlist_url: YouTube playlist URL
        max_videos: Maximum number of videos to fetch

    Returns:
        List of video dictionaries with title, url, duration, etc.
    """
    print(f"Fetching videos from playlist: {playlist_url}", file=sys.stderr)

    result = run_ytdlp(playlist_url, extract_flat=True)

    videos = []
    if isinstance(result, dict) and 'entries' in result:
        videos = result['entries'][:max_videos]
    elif isinstance(result, list):
        videos = result[:max_videos]

    return videos


def get_channel_videos(channel_url: str, search_terms: List[str] = None, max_videos: int = 20) -> List[Dict[str, Any]]:
    """
    Get recent videos from a channel, optionally filtered by search terms.

    Args:
        channel_url: YouTube channel URL
        search_terms: List of terms to search for in video titles
        max_videos: Maximum number of videos to fetch

    Returns:
        List of video dictionaries
    """
    videos_url = f"{channel_url}/videos"
    print(f"Fetching recent videos from: {videos_url}", file=sys.stderr)

    result = run_ytdlp(videos_url, extract_flat=True)

    videos = []
    if isinstance(result, dict) and 'entries' in result:
        videos = result['entries']
    elif isinstance(result, list):
        videos = result

    # Filter by search terms if provided
    if search_terms:
        filtered = []
        for video in videos:
            title = video.get('title', '').lower()
            if any(term.lower() in title for term in search_terms):
                filtered.append(video)
        videos = filtered

    return videos[:max_videos]


def format_video_info(video: Dict[str, Any]) -> str:
    """Format video information for display."""
    title = video.get('title', 'Unknown')
    video_id = video.get('id', '')
    url = f"https://youtube.com/watch?v={video_id}" if video_id else video.get('url', '')
    duration = video.get('duration', 0)

    # Format duration if available
    duration_str = ""
    if duration:
        minutes = int(duration) // 60
        seconds = int(duration) % 60
        duration_str = f" ({minutes}:{seconds:02d})"

    return f"- [{title}]({url}){duration_str}"


def main():
    """Main function to fetch and display cooking channel information."""

    # Check if yt-dlp is installed
    try:
        subprocess.run(['yt-dlp', '--version'], capture_output=True, check=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("Error: yt-dlp is not installed. Install it with: pip install yt-dlp")
        sys.exit(1)

    channels = {
        'Ethan Chlebowski': 'https://youtube.com/@ethanchlebowski',
        'Joshua Weissman': 'https://youtube.com/@joshuaweissman'
    }

    # Keywords for beginner cooking content
    beginner_keywords = [
        'beginner', 'basics', 'fundamental', 'guide', 'kitchen organization',
        'knife skills', 'essential', 'tips', 'how to', 'mistakes',
        'pantry', 'equipment', 'tools', 'setup'
    ]

    all_data = {}

    for channel_name, channel_url in channels.items():
        print(f"\n{'='*60}", file=sys.stderr)
        print(f"Processing: {channel_name}", file=sys.stderr)
        print(f"{'='*60}\n", file=sys.stderr)

        channel_data = {
            'url': channel_url,
            'playlists': [],
            'beginner_videos': []
        }

        # Get playlists
        print(f"Fetching playlists...", file=sys.stderr)
        playlists = get_channel_playlists(channel_url)
        channel_data['playlists'] = playlists[:15]  # Limit to 15 playlists

        print(f"Found {len(playlists)} playlists", file=sys.stderr)

        # Get videos related to beginner content
        print(f"Searching for beginner-friendly videos...", file=sys.stderr)
        beginner_videos = get_channel_videos(channel_url, beginner_keywords, max_videos=30)
        channel_data['beginner_videos'] = beginner_videos

        print(f"Found {len(beginner_videos)} beginner-related videos", file=sys.stderr)

        all_data[channel_name] = channel_data

    # Save raw data to JSON
    output_file = 'youtube_cooking_data.json'
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(all_data, f, indent=2, ensure_ascii=False)

    print(f"\n{'='*60}", file=sys.stderr)
    print(f"Data saved to: {output_file}", file=sys.stderr)
    print(f"{'='*60}\n", file=sys.stderr)

    # Generate markdown report
    markdown_file = 'youtube_cooking_data.md'
    with open(markdown_file, 'w', encoding='utf-8') as f:
        f.write("# YouTube Cooking Channels - Playlists and Videos\n\n")
        f.write("*This data was automatically fetched from YouTube*\n\n")

        for channel_name, data in all_data.items():
            f.write(f"\n## {channel_name}\n\n")
            f.write(f"Channel: [{channel_name}]({data['url']})\n\n")

            # Write playlists
            if data['playlists']:
                f.write("### Available Playlists\n\n")
                for playlist in data['playlists']:
                    title = playlist.get('title', 'Unknown Playlist')
                    playlist_id = playlist.get('id', '')
                    url = f"https://youtube.com/playlist?list={playlist_id}" if playlist_id else playlist.get('url', '')
                    video_count = playlist.get('playlist_count', '?')
                    f.write(f"- [{title}]({url}) - {video_count} videos\n")
                f.write("\n")

            # Write beginner videos
            if data['beginner_videos']:
                f.write("### Beginner-Friendly Videos\n\n")
                for video in data['beginner_videos']:
                    f.write(format_video_info(video) + "\n")
                f.write("\n")

    print(f"Markdown report saved to: {markdown_file}", file=sys.stderr)
    print("\nDone!", file=sys.stderr)


if __name__ == '__main__':
    main()
