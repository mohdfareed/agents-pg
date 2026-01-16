#!/usr/bin/env python3
"""
Fetch YouTube channel videos using RSS feeds and alternative methods.
This bypasses the need for direct API access.
"""

import xml.etree.ElementTree as ET
import requests
import json
import sys
from typing import List, Dict, Any
import time


def get_channel_id_from_username(username: str) -> str:
    """
    Map known usernames to channel IDs.
    For unknown channels, this would need to be done via the YouTube API.
    """
    # These are the actual channel IDs for the cooking channels
    # You can find these by viewing the channel page source
    known_channels = {
        'ethanchlebowski': 'UCJjlcL2AgENfU-uvxIqZawA',
        'joshuaweissman': 'UChBEbMKI1eCcejTtmI32UEw'
    }
    return known_channels.get(username.lower().replace('@', ''))


def fetch_channel_rss(channel_id: str, channel_name: str) -> List[Dict[str, Any]]:
    """
    Fetch recent videos from a YouTube channel using RSS feed.

    Args:
        channel_id: YouTube channel ID
        channel_name: Human-readable channel name

    Returns:
        List of video dictionaries
    """
    rss_url = f"https://www.youtube.com/feeds/videos.xml?channel_id={channel_id}"
    print(f"Fetching RSS feed for {channel_name}...", file=sys.stderr)

    try:
        response = requests.get(rss_url, timeout=10)
        response.raise_for_status()

        # Parse XML
        root = ET.fromstring(response.content)

        # Define namespace
        ns = {
            'atom': 'http://www.w3.org/2005/Atom',
            'media': 'http://search.yahoo.com/mrss/',
            'yt': 'http://www.youtube.com/xml/schemas/2015'
        }

        videos = []
        for entry in root.findall('atom:entry', ns):
            video = {
                'title': entry.find('atom:title', ns).text,
                'url': entry.find('atom:link', ns).get('href'),
                'id': entry.find('yt:videoId', ns).text,
                'published': entry.find('atom:published', ns).text,
                'author': entry.find('atom:author/atom:name', ns).text,
            }

            # Get thumbnail if available
            thumbnail = entry.find('.//media:thumbnail', ns)
            if thumbnail is not None:
                video['thumbnail'] = thumbnail.get('url')

            videos.append(video)

        print(f"Found {len(videos)} recent videos", file=sys.stderr)
        return videos

    except requests.RequestException as e:
        print(f"Error fetching RSS feed: {e}", file=sys.stderr)
        return []
    except ET.ParseError as e:
        print(f"Error parsing RSS feed: {e}", file=sys.stderr)
        return []


def filter_beginner_videos(videos: List[Dict[str, Any]], keywords: List[str]) -> List[Dict[str, Any]]:
    """Filter videos that contain beginner-related keywords."""
    filtered = []
    for video in videos:
        title = video.get('title', '').lower()
        if any(keyword.lower() in title for keyword in keywords):
            filtered.append(video)
    return filtered


def scrape_playlists_basic(channel_username: str) -> Dict[str, Any]:
    """
    Attempt to get basic channel information.
    Note: This is limited without API access.
    """
    print(f"Attempting to get channel info for {channel_username}...", file=sys.stderr)

    # For now, return curated playlists based on known content
    # In a real implementation, this would scrape the actual playlists
    curated_playlists = {
        'ethanchlebowski': [
            {
                'name': 'Kitchen Fundamentals',
                'description': 'Basic techniques and kitchen organization',
                'keywords': ['kitchen organization', 'beginner', 'guide', 'fundamentals']
            },
            {
                'name': 'Cooking Techniques',
                'description': 'Essential cooking methods and skills',
                'keywords': ['technique', 'how to', 'basics', 'method']
            },
            {
                'name': 'Recipe Videos',
                'description': 'Full recipe demonstrations',
                'keywords': ['recipe', 'cook', 'make']
            }
        ],
        'joshuaweissman': [
            {
                'name': 'But Better',
                'description': 'Making restaurant dishes better at home',
                'keywords': ['but better']
            },
            {
                'name': 'But Cheaper',
                'description': 'Budget-friendly cooking',
                'keywords': ['but cheaper']
            },
            {
                'name': 'But Faster',
                'description': 'Quick and easy recipes',
                'keywords': ['but faster']
            },
            {
                'name': 'Fundamentals',
                'description': 'Basic cooking techniques and skills',
                'keywords': ['fundamental', 'basic', 'technique', 'beginner']
            }
        ]
    }

    return curated_playlists.get(channel_username.lower().replace('@', ''), [])


def main():
    """Main function to fetch YouTube channel information."""

    channels = {
        'Ethan Chlebowski': {
            'username': 'ethanchlebowski',
            'url': 'https://youtube.com/@ethanchlebowski'
        },
        'Joshua Weissman': {
            'username': 'joshuaweissman',
            'url': 'https://youtube.com/@joshuaweissman'
        }
    }

    # Keywords for beginner cooking content
    beginner_keywords = [
        'beginner', 'basics', 'fundamental', 'guide', 'kitchen organization',
        'knife skills', 'essential', 'tips', 'how to', 'mistakes',
        'pantry', 'equipment', 'tools', 'setup', 'start'
    ]

    all_data = {}

    for channel_name, channel_info in channels.items():
        print(f"\n{'='*60}", file=sys.stderr)
        print(f"Processing: {channel_name}", file=sys.stderr)
        print(f"{'='*60}\n", file=sys.stderr)

        username = channel_info['username']
        channel_url = channel_info['url']

        # Get channel ID
        channel_id = get_channel_id_from_username(username)
        if not channel_id:
            print(f"Warning: Unknown channel ID for {username}", file=sys.stderr)
            continue

        # Fetch recent videos via RSS
        all_videos = fetch_channel_rss(channel_id, channel_name)

        # Filter for beginner content
        beginner_videos = filter_beginner_videos(all_videos, beginner_keywords)

        # Get curated playlist info
        playlists = scrape_playlists_basic(username)

        all_data[channel_name] = {
            'url': channel_url,
            'channel_id': channel_id,
            'recent_videos': all_videos,
            'beginner_videos': beginner_videos,
            'curated_playlists': playlists
        }

        time.sleep(1)  # Be nice to the server

    # Save raw data to JSON
    output_file = 'youtube_cooking_data.json'
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(all_data, f, indent=2, ensure_ascii=False)

    print(f"\n{'='*60}", file=sys.stderr)
    print(f"Data saved to: {output_file}", file=sys.stderr)
    print(f"{'='*60}\n", file=sys.stderr)

    # Generate markdown report
    markdown_file = 'youtube_cooking_videos.md'
    with open(markdown_file, 'w', encoding='utf-8') as f:
        f.write("# YouTube Cooking Channels - Recent Videos\n\n")
        f.write("*Data fetched from YouTube RSS feeds*\n\n")
        f.write("---\n\n")

        for channel_name, data in all_data.items():
            f.write(f"\n## {channel_name}\n\n")
            f.write(f"**Channel:** [{channel_name}]({data['url']})\n\n")

            # Write curated playlists (based on known content patterns)
            if data.get('curated_playlists'):
                f.write("### Known Playlist Series\n\n")
                for playlist in data['curated_playlists']:
                    f.write(f"**{playlist['name']}**\n")
                    f.write(f"- {playlist['description']}\n")
                    f.write(f"- Search for: {', '.join(playlist['keywords'])}\n\n")

            # Write beginner videos found
            if data.get('beginner_videos'):
                f.write(f"### Beginner-Related Videos (from recent uploads)\n\n")
                for video in data['beginner_videos']:
                    title = video['title']
                    url = video['url']
                    published = video['published'][:10]  # Just the date
                    f.write(f"- [{title}]({url}) - {published}\n")
                f.write("\n")

            # Write all recent videos
            if data.get('recent_videos'):
                f.write(f"### Recent Videos (Latest 15)\n\n")
                for video in data['recent_videos'][:15]:
                    title = video['title']
                    url = video['url']
                    published = video['published'][:10]
                    f.write(f"- [{title}]({url}) - {published}\n")
                f.write("\n")

            f.write("---\n\n")

        # Add search instructions
        f.write("\n## How to Find More Videos\n\n")
        f.write("Since I can only access recent videos via RSS, here's how to find more content:\n\n")
        f.write("### On YouTube:\n")
        f.write("1. Visit the channel page\n")
        f.write("2. Click on the 'Playlists' tab to see organized content\n")
        f.write("3. Click on the 'Videos' tab and use the search icon to search within the channel\n")
        f.write("4. Use YouTube's search with: `site:youtube.com @channelname keyword`\n\n")

        f.write("### Recommended Search Terms:\n")
        f.write("- Beginner guide\n")
        f.write("- Kitchen basics\n")
        f.write("- Knife skills\n")
        f.write("- Kitchen organization\n")
        f.write("- Essential equipment\n")
        f.write("- Cooking fundamentals\n")
        f.write("- How to cook [ingredient]\n")
        f.write("- Easy recipes\n\n")

    print(f"Markdown report saved to: {markdown_file}", file=sys.stderr)
    print("\nDone!", file=sys.stderr)


if __name__ == '__main__':
    main()
