#!/bin/bash
# Simple wrapper script to run the YouTube API fetcher

set -e

echo "============================================"
echo "YouTube Cooking Channels Data Fetcher"
echo "============================================"
echo ""

# Check if API key is set
if [ -z "$YOUTUBE_API_KEY" ]; then
    echo "❌ Error: YOUTUBE_API_KEY environment variable not set"
    echo ""
    echo "Please set your YouTube API key first:"
    echo ""
    echo "  export YOUTUBE_API_KEY='your-api-key-here'"
    echo ""
    echo "Or pass it as an argument:"
    echo ""
    echo "  ./run_fetcher.sh YOUR_API_KEY"
    echo ""
    echo "Need help getting an API key?"
    echo "  📖 Read: YOUTUBE_API_SETUP.md"
    echo "  🌐 Visit: https://console.cloud.google.com/apis/credentials"
    echo ""

    # Check if API key was passed as argument
    if [ $# -eq 1 ]; then
        echo "Using API key from command line argument..."
        export YOUTUBE_API_KEY="$1"
    else
        exit 1
    fi
fi

echo "✅ API key found"
echo ""

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    echo "❌ Error: python3 not found"
    echo "Please install Python 3"
    exit 1
fi

echo "✅ Python 3 found"
echo ""

# Check if requests library is installed
if ! python3 -c "import requests" 2>/dev/null; then
    echo "⚠️  requests library not found, installing..."
    pip install requests
    echo ""
fi

echo "✅ Dependencies OK"
echo ""

# Run the fetcher
echo "🚀 Fetching YouTube data..."
echo ""

python3 fetch_youtube_api.py

echo ""
echo "============================================"
echo "✨ Done!"
echo "============================================"
echo ""
echo "Output files:"
echo "  📄 youtube_api_data.json - Raw JSON data"
echo "  📄 YOUTUBE_API_RESULTS.md - Formatted report"
echo ""
echo "Next steps:"
echo "  1. Read YOUTUBE_API_RESULTS.md for all playlists"
echo "  2. Start with DETAILED_COOKING_WATCHLIST.md for guided learning"
echo ""
