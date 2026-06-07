# UnfranchisedFC Data Architecture

## Overview

UnfranchisedFC is powered by a **multi-source data pipeline** that connects:
- **Live match data** (standings, results)
- **Global sports context** (World Cup 2026 base camps)
- **Cultural sentiment** (Reddit fan discussions)
- **News & announcements** (RSS feeds, Twitter)
- **Club eligibility metrics** (Wikipedia)

This creates a rich foundation for generating authentic, data-driven content about USL pro/rel.

---

## Data Sources

### 1. Live Match Data: API-Football / Sportmonks

**Purpose:** Get real-time standings, results, and statistics for USL Championship.

**Endpoint:** API-Football via RapidAPI  
**Cost:** Free tier available; Pro tier ~$15-30/month for production use  
**Update Frequency:** Live (as matches happen)

**What you get:**
- Current league standings
- Recent match results
- Team statistics (goals, assists, clean sheets)
- Player performance data

**LLM Integration:**  
The orchestrator pulls current standings and generates content like:
- "San Diego Loyal extends lead with 3-0 victory"
- "Chattanooga FC moves into Pro/Rel contention zone"

**Setup:**
```bash
# 1. Go to https://rapidapi.com/api-sports/api/api-football
# 2. Subscribe (free tier: 100 requests/day)
# 3. Copy API key to .env as API_FOOTBALL_KEY
# 4. Python will handle the rest
```

---

### 2. Club Eligibility Data: Wikipedia API

**Purpose:** Verify USL Pro/Rel eligibility for clubs (stadium capacity, ownership net worth).

**Endpoint:** Wikipedia API (free, no authentication)  
**Cost:** Free  
**Update Frequency:** Monthly or on-demand

**USL Premier Requirements:**
- Minimum 15,000-seat stadium
- Minimum $70M ownership net worth
- Professional league operation

**What you get:**
- Club Wikipedia summaries
- Stadium capacity
- Ownership information
- Historical context

**LLM Integration:**
The orchestrator checks club eligibility and generates content like:
- "Sacramento Republic meets ALL requirements for promotion"
- "Detroit City FC aims for $70M ownership threshold"

**Setup:**
```bash
# Wikipedia API is FREE and requires no authentication
# Python's requests library handles it automatically
# Add club names to the consolidate_data() function
```

---

### 3. Cultural Sentiment: Reddit API (PRAW)

**Purpose:** Capture authentic fan voice from r/USLPRO and r/MLS.

**Endpoint:** Reddit API via PRAW  
**Cost:** Free (Reddit OAuth is free)  
**Update Frequency:** Weekly (on-demand)

**What you get:**
- Top weekly posts from r/USLPRO
- Top comments with sentiment
- Fan debate and arguments
- Current narrative (e.g., "pro/rel speculation", "franchise model critiques")

**LLM Integration:**
The LLM adopts the tone of real fan comments to write scripts:

```
Reddit comment sample:
"Pro/rel would be the best thing to happen to American soccer. 
 The franchise model is a monopoly."

LLM prompt:
"Using this tone from r/USLPRO: [paste comment], 
 write a 60-second script about why pro/rel matters."

Result:
"The franchise model is strangling American soccer. 
 Pro/rel isn't just about competition—it's about giving 
 communities a real stake in their clubs..."
```

**Setup:**
```bash
# 1. Go to https://www.reddit.com/prefs/apps
# 2. Create a "script" type app
# 3. Get Client ID and Client Secret
# 4. Add to .env as REDDIT_CLIENT_ID and REDDIT_CLIENT_SECRET
# 5. pip install praw
```

---

### 4. News & Updates: RSS Feeds

**Purpose:** Real-time access to USL official announcements and team news.

**Endpoints:** RSS feeds (free)  
**Cost:** Free  
**Update Frequency:** Real-time

**What you get:**
- USL official announcements
- Stadium expansion news
- Ownership changes
- Promotion/relegation speculation

**Supported Feeds:**
- USL Championship official
- Individual club feeds (Sacramento, Chattanooga, Pittsburgh, Detroit, etc.)
- Sports journalism sites

**LLM Integration:**
The orchestrator can detect breaking news and auto-generate:
- "New stadium announced in El Paso"
- "Sacramento Republic eyes 2028 promotion"

**Setup:**
```bash
# 1. pip install feedparser
# 2. RSS feeds are free and need no authentication
# 3. Add feed URLs to fetch_rss_feeds() function
```

---

### 5. World Cup Base Camps: Static JSON

**Purpose:** Connect global superpowers to local USL clubs.

**Data File:** `data/base_camps.json`  
**Cost:** Free (static data)  
**Update Frequency:** Pre-tournament (2026)

**What you get:**
- World Cup 2026 base camp locations
- Corresponding USL Championship club
- Connection narrative

**Examples:**
```json
{
  "country": "Spain",
  "base_camp_city": "Chattanooga",
  "usl_club": "Chattanooga FC",
  "narrative": "Spain's technical excellence meets the rising USL Championship"
}

{
  "country": "Brazil",
  "base_camp_city": "Los Angeles",
  "usl_club": "LA Galaxy, LAFC",
  "narrative": "Brazil's Seleção trains where American soccer dreams are built"
}
```

**LLM Integration:**
The orchestrator can generate cross-cultural content:

```
Prompt: "Germany's World Cup team is preparing in Philadelphia. 
         FC Cincinnati is climbing the USL Championship. 
         Write a 60-second script about the intersection of global and grassroots soccer."

Result: [Authentic narrative connecting German excellence with American pro/rel]
```

**Setup:**
```bash
# No setup needed - data/base_camps.json is pre-populated
# Add more base camps as needed for different tournaments
```

---

### 6. Twitter/X Feeds: Real-time Updates

**Purpose:** Breaking news and real-time reactions from USL accounts.

**Endpoint:** Twitter API v2  
**Cost:** Free tier available (450 requests/15-min window)  
**Update Frequency:** Real-time

**What you get:**
- Latest tweets from 40+ USL accounts
- Fan reactions
- Official announcements
- Analyst insights

**Pre-configured Handles:**
- Official: @USLChampionship, @USLLeagueOne, etc.
- Analysts: @BackHeeledUSL, @USLTactics
- Journalists: @grahamruthven, @jeffrueter, etc.
- Clubs: @SanDiegoLoyal, @DetCityFC, etc.

---

## Data Flow Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    DATA AGGREGATION LAYER                   │
└─────────────────────────────────────────────────────────────┘

    ↓

┌──────────────────┐ ┌──────────────────┐ ┌──────────────────┐
│ Live API Data    │ │ Static Context   │ │ Cultural Data    │
│─────────────────│ │─────────────────│ │─────────────────│
│ - Standings     │ │ - Base Camps     │ │ - Reddit Posts   │
│ - Results       │ │ - Club Info      │ │ - Fan Comments   │
│ - Player Stats  │ │ - Stadium Data   │ │ - Sentiment      │
└──────────────────┘ └──────────────────┘ └──────────────────┘

    ↓

┌──────────────────┐ ┌──────────────────┐ ┌──────────────────┐
│ News Data        │ │ Real-time Data   │ │ Combined JSON    │
│─────────────────│ │─────────────────│ │─────────────────│
│ - RSS Feeds      │ │ - Twitter/X      │ │ All sources      │
│ - Announcements  │ │ - Breaking News  │ │ in one object    │
│ - Press Releases │ │ - Live Updates   │ │ for LLM          │
└──────────────────┘ └──────────────────┘ └──────────────────┘

    ↓

┌─────────────────────────────────────────────────────────────┐
│              CONSOLIDATED DATA STRUCTURE                    │
│  (Single JSON object with all sources + metadata)           │
└─────────────────────────────────────────────────────────────┘

    ↓

┌─────────────────────────────────────────────────────────────┐
│                    LLM PROMPT                               │
│  (with instructions to adopt Reddit tone, use base camps,   │
│   reference current standings, incorporate fan sentiment)   │
└─────────────────────────────────────────────────────────────┘

    ↓

┌─────────────────────────────────────────────────────────────┐
│              LLM OUTPUT (JSON)                              │
│  - Voiceover script (authentic tone)                       │
│  - On-screen text (data-driven)                            │
│  - Caption (with hashtags)                                 │
└─────────────────────────────────────────────────────────────┘

    ↓

┌─────────────────────────────────────────────────────────────┐
│           MEDIA GENERATION & POSTING                        │
│  - TTS audio                                               │
│  - Video rendering                                         │
│  - Instagram upload                                        │
└─────────────────────────────────────────────────────────────┘
```

---

## Configuration

All data source credentials are managed in `.env`:

```bash
# API Keys
API_FOOTBALL_KEY=...
REDDIT_CLIENT_ID=...
TWITTER_BEARER_TOKEN=...

# LLM & Media
LLM_BACKEND=opencode
ELEVENLABS_API_KEY=...

# Instagram
INSTAGRAM_USERNAME=...
INSTAGRAM_PASSWORD=...
```

Sensitive credentials should be **GitHub Secrets**, not in `.env`.

---

## Cost Breakdown

| Source | Cost | Frequency | Required? |
|--------|------|-----------|-----------|
| API-Football | Free tier (100/day) or $15-30/mo | Live | ✅ Yes |
| Wikipedia | FREE | On-demand | ✅ Yes |
| Reddit (PRAW) | FREE | Weekly | ✅ Yes |
| RSS Feeds | FREE | Real-time | ✅ Yes |
| Base Camps JSON | FREE (static) | N/A | ✅ Yes |
| Twitter API | FREE tier | Real-time | ✅ Yes |
| **TOTAL** | **~$15-30/mo** | — | — |

All major sources are free or very cheap. You're not paying for the data—you're paying for API infrastructure.

---

## Example: Generating a Single Post

### Scenario: Chattanooga FC vs. San Diego Loyal, Saturday night

#### Step 1: Fetch Data

```python
data = fetch_usl_data()
```

The orchestrator calls:
- API-Football → Gets live standings + Chattanooga beat San Diego 2-1
- Wikipedia → Chattanooga Stadium capacity: 6,000 (below 15k threshold)
- Reddit → Top comment: "CFC is the soul of American soccer, but they'll never go pro with that stadium"
- World Cup → Chattanooga is Spain's base camp (2026)
- RSS → "Chattanooga FC announces stadium expansion plans"

#### Step 2: Build LLM Prompt

```
You are writing a 60-second Instagram Reel for UnfranchisedFC.

MATCH RESULT: Chattanooga 2-1 San Diego

STANDINGS:
- Chattanooga FC: 2nd place, 45 pts (eligible for pro/rel promotion)
- San Diego: 4th place, 40 pts

CULTURAL CONTEXT (from Reddit):
"CFC is the soul of American soccer, but they'll never go pro with a 6,000 stadium"

WORLD CUP CONNECTION:
Spain's World Cup base camp is in Chattanooga (2026)

PRO/REL ELIGIBILITY:
- Stadium capacity: 6,000 (NEEDS: 15,000+)
- Ownership net worth: $30M (NEEDS: $70M+)

TONE (from Reddit fans):
Optimistic but frustrated about structural barriers to pro/rel

WRITE A 60-SECOND VOICEOVER SCRIPT

Output as JSON:
{
  "voiceover": "...",
  "on_screen_text": "...",
  "caption": "..."
}
```

#### Step 3: LLM Output

```json
{
  "voiceover": "Chattanooga FC just beat San Diego Loyal 2-1. They're fighting for promotion in the USL Championship. But there's a catch. The nation's most authentic soccer fans play in a 6,000-seat stadium. Spain's World Cup team will train here in 2026. And yet, the pro/rel door stays closed. Not because of talent. Not because of heart. But because American soccer's franchise system demands a 15,000-seat stadium. This is what pro/rel denial looks like: excellence without opportunity.",
  "on_screen_text": "Chattanooga 2-1 San Diego\n2nd Place | 45 Points",
  "caption": "Chattanooga FC fights for pro/rel promotion. But the stadium size says otherwise. 🔴⚪ #CFC #ProRel #USLPRO #UnfranchisedFC #PromotionAndRelegation"
}
```

#### Step 4: Generate Video

1. TTS: Convert voiceover to MP3 (30s audio)
2. Manim: Render standings animation + on-screen text
3. FFmpeg: Combine audio + video
4. Instagram: Post with caption

**Total time:** 2 minutes (automated)  
**Total cost:** ~$0.11  
**Authenticity:** High (real data + Reddit tone + World Cup context)

---

## Next Steps

1. **Populate .env** with API keys
2. **Install dependencies**: `pip install -r requirements.txt`
3. **Test data aggregation**: `python -c "from src.data_fetcher import fetch_usl_data; import json; print(json.dumps(fetch_usl_data(), indent=2))"`
4. **Run full pipeline**: `python src/orchestrator.py`
5. **Deploy to GitHub**: Push and set up CI/CD

---

## Advanced: Custom Data Sources

You can add more data sources by:

1. Creating a new function in `src/data_fetcher.py`:
```python
def fetch_custom_source() -> Dict[str, Any]:
    """Fetch custom data"""
    ...

2. Adding it to `consolidate_data()`:
```python
consolidated["sources"]["custom"] = fetch_custom_source()
```

3. Documenting it in `.env.example.data`

Examples:
- **Player trades/signings:** Parse ESPN API
- **Stadium attendance:** Scrape official websites
- **Weather data:** OpenWeather API
- **Injury updates:** Custom RSS monitor
- **Social media sentiment:** Sentiment analysis on Twitter

---

**UnfranchisedFC is powered by data. Every post is grounded in real statistics, real fan voices, and real context.**
