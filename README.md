# YouTube Cooking Watch List Project

Complete beginner's guide to learning how to cook using YouTube content from Ethan Chlebowski and Joshua Weissman.

## Files in This Repository

### 📖 Main Resources

**[DETAILED_COOKING_WATCHLIST.md](DETAILED_COOKING_WATCHLIST.md)** ⭐ **START HERE**
- Complete 6-month learning path from absolute beginner to confident cook
- Specific video search terms and topics
- Organized by learning phases (Setup → Techniques → Recipes → Advanced)
- Includes tracking checklists and practice guidance
- Week-by-week schedule

**[cooking-watchlist.md](cooking-watchlist.md)**
- Original comprehensive overview with learning stages
- Motivation and mindset guidance
- General structure for self-paced learning

### 🔧 Automated Data Fetching

**[fetch_youtube_api.py](fetch_youtube_api.py)** ⭐ **RECOMMENDED**
- Official YouTube Data API v3 implementation
- Most reliable method for fetching playlists and videos
- Requires free API key (see setup guide below)
- Fetches complete channel data, playlists, and videos
- Generates comprehensive reports

**[YOUTUBE_API_SETUP.md](YOUTUBE_API_SETUP.md)** 📖 **Setup Guide**
- Step-by-step instructions to get a free YouTube API key
- No credit card required for typical usage
- 10,000 free API calls per day
- Security best practices

**[run_fetcher.sh](run_fetcher.sh)** 🚀 **Easy Run Script**
- Simple wrapper to run the API fetcher
- Checks dependencies
- User-friendly output

**Alternative Methods:**

**[fetch_youtube_playlists.py](fetch_youtube_playlists.py)**
- Uses yt-dlp (may be blocked by network restrictions)
- No API key needed

**[fetch_youtube_rss.py](fetch_youtube_rss.py)**
- Uses YouTube RSS feeds (limited to ~15 recent videos)
- No API key needed

**[youtube_cooking_videos.md](youtube_cooking_videos.md)**
- Auto-generated overview of playlist series
- Search terms for finding content

**[youtube_cooking_data.json](youtube_cooking_data.json)**
- Structured data about channels and playlists
- Useful for programmatic processing

## Quick Start (Manual Approach)

1. **Read** [DETAILED_COOKING_WATCHLIST.md](DETAILED_COOKING_WATCHLIST.md)
2. **Go to YouTube** and visit:
   - [Ethan Chlebowski](https://youtube.com/@ethanchlebowski)
   - [Joshua Weissman](https://youtube.com/@joshuaweissman)
3. **Start with Week 1**: Kitchen Organization
4. **Follow the phases** at your own pace

## Quick Start (Automated Approach)

Want to automatically fetch all playlists and videos? Use the YouTube API:

1. **Get a free API key**: Follow [YOUTUBE_API_SETUP.md](YOUTUBE_API_SETUP.md)
2. **Run the fetcher**:
   ```bash
   export YOUTUBE_API_KEY='your-key-here'
   ./run_fetcher.sh
   ```
3. **Check the results**: `YOUTUBE_API_RESULTS.md` will contain all playlists and videos
4. **Start learning**: Use the generated data alongside the detailed watch list

**Benefits of API approach:**
- ✅ Get all playlists automatically
- ✅ See video counts and descriptions
- ✅ Get recent uploads
- ✅ Search for specific topics
- ✅ Completely free (10,000 API calls/day)

## About the Channels

### Ethan Chlebowski
- **Focus:** Cooking fundamentals and food science
- **Style:** Clear explanations of WHY techniques work
- **Best for:** Understanding the principles behind cooking
- **Founder of:** CookWell platform

### Joshua Weissman
- **Focus:** Restaurant-quality home cooking
- **Series:** "But Better," "But Cheaper," "But Faster"
- **Style:** Professional techniques made accessible
- **Best for:** Building confidence and variety

## Learning Philosophy

This watch list is designed for someone with **zero cooking experience**:
- No prior kitchen knowledge assumed
- Starts with organizing and equipping your kitchen
- Builds fundamental skills before recipes
- Progressive difficulty
- Emphasizes understanding over memorization

## Tools & Equipment Needed

### Essential (Week 1-2):
- 8-inch chef's knife
- Cutting board
- 12-inch skillet
- Medium pot
- Basic utensils (spatula, wooden spoon, tongs)
- Measuring cups/spoons

### Budget: $130-230 to start

Full equipment guide in the detailed watch list.

## Expected Timeline

- **Week 1:** Kitchen setup and organization
- **Week 2:** Knife skills and safety
- **Week 3-4:** Basic cooking techniques
- **Week 5-8:** Simple recipes and budget cooking
- **Week 9-12:** Quick meals and building repertoire
- **Month 4+:** Advanced techniques and improvisation
- **Month 6:** Cooking confidently without always needing recipes

## Fetching Methods Comparison

| Method | Pros | Cons | Best For |
|--------|------|------|----------|
| **YouTube API** ⭐ | Complete data, reliable, official | Requires API key setup | Most users |
| **Manual search** | No setup, always works | Time-consuming | Quick start |
| **yt-dlp script** | No API key needed | May be blocked by network | Advanced users |
| **RSS feeds** | No API key needed | Limited to recent videos | Quick checks |

**Recommendation:** Use the YouTube API method for the best experience. It's free and takes just 5 minutes to set up.

## License & Usage

These resources are for personal learning. The video content belongs to the respective creators (Ethan Chlebowski and Joshua Weissman).

## Contributing

This is a personal learning project, but suggestions for additional resources or organization improvements are welcome.

---

**Start your cooking journey today! 🍳**
