# YouTube API Setup Guide

This guide will help you get a YouTube Data API v3 key to fetch playlists and videos programmatically.

## Step 1: Create a Google Cloud Project

1. **Go to Google Cloud Console**
   - Visit: https://console.cloud.google.com/

2. **Sign in** with your Google account

3. **Create a new project**
   - Click the project dropdown at the top
   - Click "New Project"
   - Enter a project name (e.g., "YouTube Cooking List")
   - Click "Create"

## Step 2: Enable YouTube Data API v3

1. **Navigate to APIs & Services**
   - In the Google Cloud Console, go to "APIs & Services" > "Library"
   - Or visit: https://console.cloud.google.com/apis/library

2. **Search for YouTube Data API**
   - In the search box, type "YouTube Data API v3"
   - Click on "YouTube Data API v3"

3. **Enable the API**
   - Click the "Enable" button
   - Wait for it to be enabled (takes a few seconds)

## Step 3: Create API Credentials

1. **Go to Credentials**
   - Navigate to "APIs & Services" > "Credentials"
   - Or visit: https://console.cloud.google.com/apis/credentials

2. **Create credentials**
   - Click "+ CREATE CREDENTIALS" at the top
   - Select "API key"

3. **Copy your API key**
   - A dialog will appear with your new API key
   - **IMPORTANT:** Copy this key and save it securely
   - It will look something like: `AIzaSyD...` (39 characters)

4. **Restrict your API key (Recommended)**
   - Click "Edit API key" or the key name
   - Under "API restrictions":
     - Select "Restrict key"
     - Check "YouTube Data API v3"
   - Click "Save"

## Step 4: Understand API Quotas

**Free Tier Limits:**
- **10,000 units per day** (default quota)
- Reading playlists costs ~1 unit each
- Reading videos costs ~1 unit each
- You can easily fetch all the data needed within the free quota

**What this means:**
- You can fetch hundreds of playlists and thousands of videos daily
- Perfect for this cooking watchlist project
- No credit card required for this usage level

## Step 5: Use the API Key

### Option 1: Environment Variable (Recommended)

```bash
# Linux/Mac
export YOUTUBE_API_KEY='your-api-key-here'
python3 fetch_youtube_api.py

# Windows (Command Prompt)
set YOUTUBE_API_KEY=your-api-key-here
python fetch_youtube_api.py

# Windows (PowerShell)
$env:YOUTUBE_API_KEY='your-api-key-here'
python fetch_youtube_api.py
```

### Option 2: Command Line Argument

```bash
python3 fetch_youtube_api.py YOUR_API_KEY_HERE
```

### Option 3: Create a .env file

1. Create a file named `.env` in the project directory:

```bash
YOUTUBE_API_KEY=your-api-key-here
```

2. Add `.env` to `.gitignore` to avoid committing your key:

```bash
echo ".env" >> .gitignore
```

3. Modify the script to load from .env (or use python-dotenv package)

## Step 6: Run the Fetcher Script

Once you have your API key set up:

```bash
python3 fetch_youtube_api.py
```

**Expected output:**
- `youtube_api_data.json` - Raw JSON data with all playlists and videos
- `YOUTUBE_API_RESULTS.md` - Formatted markdown report with links

## Security Best Practices

### ✅ DO:
- Keep your API key private
- Add `.env` to `.gitignore`
- Restrict your API key to only YouTube Data API v3
- Regenerate your key if it's ever exposed publicly

### ❌ DON'T:
- Commit API keys to Git repositories
- Share your API key publicly
- Use the same key for multiple unrelated projects
- Leave API keys unrestricted

## Troubleshooting

### "API key not valid" error

**Solution:**
1. Make sure you enabled the YouTube Data API v3
2. Wait a few minutes after creating the key (propagation time)
3. Check that you copied the entire key (should be 39 characters)

### "Quota exceeded" error

**Solution:**
- You've hit the daily limit of 10,000 units
- Wait until midnight Pacific Time for reset
- Or request a quota increase (requires billing account, but won't be charged unless you exceed free tier)

### "Access Not Configured" error

**Solution:**
- Make sure YouTube Data API v3 is enabled in your project
- Go to APIs & Services > Library and enable it

### Network/Proxy errors

**Solution:**
- Check your internet connection
- If behind a corporate firewall, you may need to configure proxy settings
- Try from a different network

## Alternative: No API Key Needed

If you don't want to set up an API key, you can still use the watch list effectively:

1. **Use the manual guides:**
   - `DETAILED_COOKING_WATCHLIST.md` has specific search terms
   - Manually search on YouTube using the provided terms
   - No programming needed

2. **Limited RSS access:**
   - `fetch_youtube_rss.py` doesn't need an API key
   - Only gets recent videos (last ~15)
   - May not work in all network environments

## Cost Breakdown

**YouTube Data API v3 is FREE for typical usage:**

| Operation | Cost (units) | How many you can do daily |
|-----------|--------------|---------------------------|
| List playlists | 1 | 10,000 |
| List playlist items | 1 | 10,000 |
| Search videos | 100 | 100 |
| Get video details | 1 | 10,000 |

**For this project:**
- Fetching both channels' data: ~200-500 units
- Well within the 10,000 free daily quota
- **Cost: $0.00**

## Running the Script

Once set up, the script will:

1. ✅ Fetch channel statistics (subscribers, views, etc.)
2. ✅ Get all playlists from both channels
3. ✅ Search for beginner-friendly videos
4. ✅ Get recent uploads
5. ✅ Generate JSON data file
6. ✅ Create formatted markdown report with links

**Output files:**
- `youtube_api_data.json` - Complete data dump
- `YOUTUBE_API_RESULTS.md` - Human-readable report

## Quick Start Summary

```bash
# 1. Get API key from Google Cloud Console
# 2. Enable YouTube Data API v3
# 3. Set environment variable
export YOUTUBE_API_KEY='your-key-here'

# 4. Run the script
python3 fetch_youtube_api.py

# 5. Check the output
cat YOUTUBE_API_RESULTS.md
```

That's it! You'll have all the playlists and videos fetched automatically.

---

## Need Help?

- **Google Cloud Console:** https://console.cloud.google.com/
- **YouTube API Documentation:** https://developers.google.com/youtube/v3
- **API Key Help:** https://support.google.com/googleapi/answer/6158862

If you run into issues, check the troubleshooting section above or search for the specific error message.
