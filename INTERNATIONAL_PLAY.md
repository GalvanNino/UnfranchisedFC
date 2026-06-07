# International Play & Global Transfer Tracking

## Overview

UnfranchisedFC now tracks **global player movement** and **World Cup connections** to tell the ultimate pro/rel narrative: **"The open system builds better players for the global stage."**

This requires three integrated systems:
1. **World Cup Live Feed** - Real-time USMNT/MXMNT match tracking
2. **Global Transfer Market** - Player movement between USL, MLS, and Europe
3. **USL-to-World-Cup Cross-Reference** - Connecting domestic talent to international stages

---

## 1. World Cup Live Feed Integration

### The Module: `world_cup_tracker.py`

Tracks USMNT and Mexico national teams during World Cup 2026 (or any tournament).

```python
from world_cup_tracker import fetch_world_cup_matches

matches = fetch_world_cup_matches(team_ids=[1, 84])  # USA, Mexico
```

**Data Flow:**

```
GitHub Actions (evening during tournament)
    ↓
fetch_world_cup_matches()
    ↓ (via API-Football)
Live match score, goals, possession, lineup
    ↓
cross_reference_usl_players()
    ↓
"USMNT player from [USL club] started vs [country]"
    ↓
LLM generates "World Cup Check-In" Reel
```

### Configuration

Add to `.env`:
```bash
# API-Football already configured
API_FOOTBALL_KEY=your_key

# League ID for World Cup 2026 (verify with API docs)
WORLD_CUP_LEAGUE_ID=25
```

### Example Output

**Match Data:**
```json
{
  "match": {
    "home_team": "USA",
    "away_team": "Mexico",
    "score": "2-1",
    "goalscorers": ["Reyna (23')", "Sargent (67')"],
    "possession": {"USA": 58, "Mexico": 42},
    "date": "2026-06-15T20:00:00Z"
  },
  "usl_connection": {
    "player": "Gio Reyna",
    "usl_club": "Development pathway (via LAFC)",
    "national_team": "USA",
    "position": "Midfielder"
  }
}
```

**LLM Prompt:**
```
USMNT beat Mexico 2-1 in World Cup 2026.

Gio Reyna scored—he came through the development pathway 
connected to LA FC's academy (part of the USL ecosystem).

Write a 60-second script about how independent player development 
through open leagues creates global talent. Mention the pro/rel advantage.

Tone: Analytical but celebratory
```

**LLM Output:**
```
"Gio Reyna just scored for the USMNT in the World Cup.
 He's one of millions of American players developed outside 
 the closed MLS franchise system. The open pathway? 
 Through academies, USL clubs, and real market competition.
 This is what promotion and relegation builds.
 Not franchises. Not draft restrictions.
 Talent on the global stage."
```

---

## 2. Global Transfer Market Tracking

### The Data: `transfers.json`

Tracks player movement between:
- **USL → Europe** (young talent going directly to Europe)
- **USL ↔ MLS** (player movement within US system)
- **Europe → USL** (international veterans choosing the open league)

### Real Example: Ramiz Hamouda

```json
{
  "player_name": "Ramiz Hamouda",
  "from_club": "Birmingham Legion FC",
  "from_league": "USL Championship",
  "to_club": "Werder Bremen",
  "to_league": "Bundesliga",
  "age_at_transfer": 18,
  "transfer_fee": "€500,000",
  "narrative": "18-year-old bypasses MLS draft, goes directly from USL to German first division"
}
```

### Why This Matters for Pro/Rel Narrative

**Franchise System (MLS):**
- Young players drafted by MLS clubs
- Must stay in franchise system or sit on bench
- Club owns player rights
- Limited international options

**Pro/Rel System (USL Premier):**
- Young players developed by independent clubs
- Clubs can sell players freely on open market
- Direct access to European teams
- Global market mechanics

### Transfer Alert Categories

The `world_cup_tracker.py` automatically flags:

1. **Youth-to-Europe** (age < 22)
   ```python
   {
     "type": "youth_to_europe",
     "player": "Ramiz Hamouda",
     "age": 18,
     "narrative": "USL club sells young talent directly to Bundesliga"
   }
   ```

2. **High-Value Transfers** (fee > $500k)
   ```python
   {
     "type": "high_value",
     "fee": "€2,500,000",
     "narrative": "Sacramento Republic FC commands major transfer fee"
   }
   ```

3. **International-to-USL** (veteran joins)
   ```python
   {
     "type": "international_to_usl",
     "player": "Marcus Brown",
     "from": "Norwich City (Championship)",
     "narrative": "English veteran chooses USL over MLS franchise"
   }
   ```

### How to Track Transfers

**Option A: Transfermarkt Web Scraping** (Recommended)

```bash
# Install transfermarkt scraper
pip install git+https://github.com/dcaribou/transfermarkt-scraper.git

# In world_cup_tracker.py, add:
from transfermarkt.club import Club

def scrape_usl_transfers():
    for club_id in USL_CLUB_IDS:
        club = Club(club_id, "2025-2026")
        return club.get_transfers()
```

**Option B: Manual API Updates**

Update `data/transfers.json` when you see transfers in the news:

```bash
# Add transfer to data/transfers.json
git add data/transfers.json
git commit -m "Transfer: Player Name from Club A to Club B"
```

The orchestrator will pick it up automatically.

---

## 3. USL-to-World-Cup Cross-Reference

### The Data: `usl_world_cup_players.json`

A curated list of USL-connected players in World Cup 2026.

```json
{
  "player_name": "Folarin Balogun",
  "usl_club": "Louisville City FC",
  "usl_years": "2023-2025",
  "national_team": "USMNT",
  "position": "Forward",
  "usl_stats": {
    "goals": 24,
    "assists": 8,
    "appearances": 52
  },
  "world_cup_squad": true,
  "narrative": "From USL Championship leading scorer to USMNT forward"
}
```

### How It Works

During World Cup 2026:

```
1. Match happens: USMNT vs [Team]
2. Lineups released
3. world_cup_tracker.py checks lineups against usl_world_cup_players.json
4. Match found: "Balogun starts for USA"
5. Pull his USL stats: "24 goals in 52 appearances for Louisville"
6. Generate content hook:
   
   "The USMNT's leading goal scorer in Qatar?
    He was USL Championship's best last season.
    Louisville City FC developed him.
    Open leagues. Global talent. Pro/rel advantage."
```

### Maintaining the List

1. **Pre-tournament:** Review rosters of nations with USL players
2. **During tournament:** Update as players get called up/sent home
3. **Post-tournament:** Archive for retrospectives

**To add a player:**

```json
{
  "id": "uslp_009",
  "name": "[Player Name]",
  "birth_year": 2000,
  "usl_club": "[USL Club Name]",
  "usl_years": "2023-2025",
  "national_team": "[National Team]",
  "position": "[Position]",
  "usl_stats": {
    "goals": 0,
    "assists": 0,
    "appearances": 0
  },
  "world_cup_squad": true,
  "squad_number": 0,
  "narrative": "[Your narrative hook]"
}
```

---

## Integration with Main Pipeline

### Orchestrator Changes

Update `src/orchestrator.py`:

```python
from src.world_cup_tracker import fetch_international_data

def main():
    # ... existing code ...
    
    # Stage 1b: Fetch international data (NEW)
    logger.info("🌍 Stage 1b: Fetching international data...")
    international_data = fetch_international_data()
    
    # Stage 2: Include international context in LLM prompt
    raw_data["international"] = international_data
    post_content = generate_post_content(raw_data)
```

### LLM Prompt Updates

The LLM now receives:

```
AVAILABLE DATA:
- USL standings (domestic)
- World Cup matches (international)
- Transfer alerts (market dynamics)
- USL players in World Cup (cross-reference)

NARRATIVE FRAMEWORK:
Connect local to global. Show how pro/rel creates players 
who compete on the world stage. Contrast with franchise system.
```

---

## Example Content Calendar

### Week 1: World Cup Begins

| Date | Content Type | Hook | Source |
|------|---|---|---|
| Mon | "Tournament Preview" | USL players to watch | usl_world_cup_players.json |
| Wed | "USMNT Match Check-In" | Balogun scores for USA | API-Football + cross-ref |
| Fri | "Transfer Rumor" | European club eyes USL star | transfers.json alert |

### Week 2: Mid-Tournament

| Date | Content Type | Hook | Source |
|------|---|---|---|
| Mon | "Head-to-Head" | Mexico's USL-connected player vs USA's | cross-ref |
| Wed | "Academy Success Story" | Young player from USL in World Cup | usl_world_cup_players.json |
| Fri | "Market Watch" | Teen sells for €500k to Europe | transfer alert |

---

## Advanced: Automating Transfer Detection

### Option 1: RSS Monitoring

Add RSS feeds for transfer news:

```python
RSS_FEEDS = [
    "https://www.transfermarkt.com/feed",
    "https://www.worldfootball.net/feed",
    "https://soccer.espn.com/feed"
]

# In fetch_rss_feeds(), scan for keywords:
keywords = ["USL", "transfer", "Birmingham", "Sacramento"]
```

### Option 2: Twitter Monitoring

Track transfer news accounts:

```
@Transfermarkt
@RumorsTransfers
@FutbolBomba
@DeadlineDay
```

GitHub Actions can monitor these and auto-add to `transfers.json`.

### Option 3: AI-Powered Detection

Use your LLM to scan sports news:

```python
news_articles = fetch_news_feeds()
for article in news_articles:
    # Send to LLM: "Is this a USL transfer? Extract details."
    transfer_candidate = llm_extract_transfer(article)
    if transfer_candidate:
        add_to_transfers_json(transfer_candidate)
```

---

## Metrics & Content Hooks

### Trackable Metrics

- ✅ USL players in World Cup squad
- ✅ Transfers involving USL clubs
- ✅ Market value of USL-developed talent
- ✅ International call-ups
- ✅ Youth-to-Europe ratio

### Content Hooks Generated

1. **"Local to Global"** - USL player in World Cup
2. **"Market Forces"** - Transfer deal announced
3. **"Development Pipeline"** - Academy player moving up
4. **"Independence Advantage"** - Player sold freely (vs. draft)
5. **"Global Talent Pool"** - International veteran joining USL

---

## Cost & Infrastructure

### API Costs

| Service | Cost | Usage |
|---------|------|-------|
| API-Football | Free tier (100/day) or paid | World Cup matches |
| Transfermarkt | Free (web scrape) | Transfer tracking |
| Twitter API | Free tier | Transfer news |
| **Total** | ~$0 - $15/mo | — |

### GitHub Actions

```yaml
# .github/workflows/international_tracker.yml
name: International Data Sync
on:
  schedule:
    - cron: '0 21 * * *'  # 9 PM UTC daily (catch World Cup matches)
jobs:
  track:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Fetch World Cup data
        run: python -c "from src.world_cup_tracker import fetch_international_data; fetch_international_data()"
```

---

## FAQ

**Q: What if there's no World Cup happening?**

A: The pipeline gracefully handles no matches. It will still track:
- Player transfers
- International friendlies
- National team qualifiers
- Youth tournaments

**Q: Can I customize the player list?**

A: Yes! Edit `data/usl_world_cup_players.json` anytime. Add/remove players as they transfer.

**Q: How often should I update transfers.json?**

A: During transfer windows (summer, winter). Real-time updates happen automatically if you set up RSS/Twitter monitoring.

**Q: Will this work for women's soccer?**

A: Absolutely. Add women's teams and players to the JSON files. The pipeline is gender-agnostic.

**Q: Can I track MLS players too?**

A: Yes. The system is flexible. Just add MLS club data to the configs.

---

## Resources

- **API-Football Docs:** https://www.api-football.com/documentation
- **Transfermarkt:** https://www.transfermarkt.com/
- **Transfermarkt Scraper:** https://github.com/dcaribou/transfermarkt-scraper
- **World Cup 2026:** https://www.fifa.com/fifaplus/en/tournaments/mens/worldcup/2026

---

**UnfranchisedFC now tells the complete story: local talent → global stage → proof that pro/rel works.**
