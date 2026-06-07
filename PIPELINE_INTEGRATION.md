## PIPELINE INTEGRATION GUIDE

UnfranchisedFC is fully integrated. Every stage of the pipeline now embeds the anti-corporate, pro-community, working-class ethos.

---

## Pipeline Stages (5 → 8 after integration)

### Stage 1: Data Aggregation (7 sources)
**Module**: `data_fetcher.py`

Consolidates:
- API-Football (standings, results)
- Wikipedia API (stadium capacity, club eligibility)
- PRAW (Reddit r/USLPRO sentiment)
- RSS feeds (USL news, club announcements)
- Twitter API v2 (40+ USL handles)
- Static JSON (base camps, player rosters)
- World Cup tracker (international play)

**Output**: `raw_data` dict with `sources` key containing all 7 data sources.

---

### Stage 1b: Accessibility Metrics (NEW)
**Module**: `accessibility_metrics.py`

Adds inequality data to support manifesto messaging:
- Ticket price comparison (MLS $125 vs USL $22)
- Youth academy costs (MLS $8,000/year vs USL free)
- Beer prices, jersey costs
- Ownership structure (billionaire vs community-owned)
- Pro/rel accessibility case statement

**Output**: `raw_data["accessibility_metrics"]` — ammunition for LLM content generation.

**When used**: Whenever generating content about barriers to entry, cost of supporting a club, or inequality narratives.

---

### Stage 1c: Content Ethos Filtering (NEW)
**Module**: `culture_club_priority.py`

Filters content by UnfranchisedFC ethos and assigns priority:

**Priority Tier 1 (HIGHEST)**: Street Soccer
- Keywords: "street soccer", "futsal", "grassroots", "pickup", "community courts"
- Gets `priority=10` and celebratory tone

**Priority Tier 2**: Culture Clubs (tied at 10)
- Detroit City FC, Atlético Dallas, Oakland Roots, Forward Madison, Chattanooga FC, Louisville City, Vermont Green
- Atlético Dallas = Street soccer connection (Latinx, grassroots roots)

**Priority Tier 3**: Generic USL content (priority 4)
- Reframed through pro/rel lens

**Critique Tier**: Billionaire franchises (priority 8)
- LAFC, Inter Miami — exposed as corporate exploitation

**Output**: `raw_data["content_ethos"]` — tells LLM how to handle this specific piece of content.

---

### Stage 2: LLM Content Generation
**Module**: `llm_formatter.py`

**CRITICAL INTEGRATION**: System prompt embedding.

Every LLM call now receives:
```python
messages = [
    {"role": "system", "content": UNFRANCHISED_SYSTEM_PROMPT},
    {"role": "user", "content": prompt}
]
```

The system prompt:
- Defines tone: "gritty, rebellious, fiercely pro-community"
- Forbids: Corporate jargon, ESPN neutrality, both-sides framing
- Demands: Direct confrontation, naming inequality, working-class celebration
- Inspiration: FC St. Pauli, Rayo Vallecano, Detroit City FC

**Output**: JSON with:
- `voiceover`: 60-90 word script (TTS-ready)
- `on_screen_text`: Bold, punchy overlay (max 10 words)
- `caption`: Instagram caption with hashtags
- `tone`: "gritty/rebellious/manifesto"

---

### Stage 3: Audio Generation (NEW - Multi-Strategy)
**Module**: `audio_strategy.py`

Three audio strategies (user selects via `AUDIO_STRATEGY` env var):

#### Strategy A: Raw Matchday Chants (PRIMARY - Authenticity 10/10)
- Live recordings from grassroots/pro/rel clubs
- Sources: St. Pauli ultras, Rayo Vallecano, DCFC, Oakland Roots
- Mixing: Chants at 0-3dB, voiceover drops underneath at -12dB
- Cost: Free (YouTube/supporter archives)

#### Strategy B: Protest Soundtrack / Barrio y Rebeldía (SECONDARY - Authenticity 9/10)
- Curated playlists of anti-establishment music
- Artists: Residente, Violeta, Los Chiquibum, Molotov, Cultura Profética
- Mixing: Music at -6dB, dynamic drops for voiceover
- Cost: ~$0.005/stream (Spotify licensing)

#### Strategy C: Documentary Narrator (FALLBACK - Authenticity 5/10)
- ElevenLabs TTS with harsh voice settings
- Fast delivery, clipped phrases
- Cost: Included in TTS API

**Output**: MP3 audio file with selected strategy.

---

### Stage 4: Video Rendering with Brutalist Aesthetic
**Module**: `media_generator.py`

#### Step 1: Generate Base Video
- Size: 1080x1920 (Instagram Reel, 9:16 vertical)
- Background: Pure black (stark, dramatic)
- Text: Arial-Black, 90pt, white, centered
- Duration: Matches audio length

#### Step 2: Apply Visual Brutalism
**Function**: `apply_visual_brutalism()`

FFmpeg filter chain:
```
eq=contrast=1.4,hue=s=1.2,noise=alls=0.04:allf=t,vignette=ratio=2:thickness=0.15
```

Effects:
- **Contrast boost (1.4x)**: Make blacks deeper, whites brighter (high contrast)
- **Saturation boost (1.2x)**: Punchy colors (red, yellow pop)
- **Film grain (noise=0.04)**: Raw, printed texture (not digital polish)
- **Vignette**: Darkened edges (drawing focus to center)

**Philosophy**: Raw > polished. Looks like protest banners, not corporate broadcast.

**Output**: MP4 video with brutal aesthetic, audio baked in.

---

### Stage 5: Instagram Posting
**Module**: `instagram_poster.py`

Posts video + caption to Instagram.

Supports:
- `instagrapi` (personal account)
- Meta Graph API (business account)

---

## Environment Variables

```bash
# LLM Backend
LLM_BACKEND=opencode              # "opencode", "together", or "auto"
OPENCODE_API_URL=http://localhost:8000
OPENCODE_TOKEN=<optional>
TOGETHER_API_KEY=<if using Together.ai fallback>

# Audio Strategy
AUDIO_STRATEGY=raw_chants         # "raw_chants", "protest_soundtrack", or "tts"

# Instagram Credentials
INSTAGRAM_USERNAME=<username>
INSTAGRAM_PASSWORD=<password>
# OR
INSTAGRAM_BUSINESS_ACCOUNT_ID=<id>
INSTAGRAM_ACCESS_TOKEN=<token>

# Data Sources
API_SPORTS_KEY=<key>
ELEVENLABS_API_KEY=<key>
REDDIT_CLIENT_ID=<id>
REDDIT_CLIENT_SECRET=<secret>
TWITTER_BEARER_TOKEN=<token>

# Paths
OUTPUT_DIR=./output
```

---

## Data Flow Diagram

```
┌─────────────────────────────────────────────────┐
│ Stage 1: Data Fetcher (7 sources)              │
│ - API Sports, Wikipedia, Reddit, RSS, Twitter  │
│ - Base camps, World Cup players, transfers     │
└──────────────────┬──────────────────────────────┘
                   │ raw_data
┌──────────────────▼──────────────────────────────┐
│ Stage 1b: Accessibility Metrics                │
│ - Inequality data (ticket prices, ownership)   │
│ - Pro/rel case statements                      │
└──────────────────┬──────────────────────────────┘
                   │ raw_data + metrics
┌──────────────────▼──────────────────────────────┐
│ Stage 1c: Culture Club Priority Filter         │
│ - Detect street soccer, culture clubs          │
│ - Assign priority tier & tone                  │
└──────────────────┬──────────────────────────────┘
                   │ raw_data + content_ethos
┌──────────────────▼──────────────────────────────┐
│ Stage 2: LLM Formatter (with System Prompt)    │
│ - Embedded UNFRANCHISED_SYSTEM_PROMPT          │
│ - Generate: voiceover, text, caption, tone     │
└──────────────────┬──────────────────────────────┘
                   │ post_content (JSON)
         ┌─────────┴─────────┐
         │                   │
    ┌────▼────┐       ┌─────▼──────┐
    │ Stage 3 │       │ Stage 4    │
    │ Audio   │       │ Video      │
    │ TTS     │       │ Brutalist  │
    │ +Chants │       │ Aesthetic  │
    └────┬────┘       └──────┬─────┘
         │ .mp3             │ .mp4
         └──────┬───────────┘
                │
         ┌──────▼──────────┐
         │ Stage 5:        │
         │ Instagram Post  │
         │ Video + Caption │
         └─────────────────┘
```

---

## Example: Full Pipeline Execution

```bash
# Set environment
export LLM_BACKEND=opencode
export AUDIO_STRATEGY=raw_chants
export INSTAGRAM_USERNAME=unfranchisedfc
export INSTAGRAM_PASSWORD=<password>

# Run
python src/orchestrator.py
```

**Output logs**:
```
🚀 Starting automated USL Instagram pipeline (UnfranchisedFC)...
🔥 Ethos: Anti-corporate. Pro-community. Working-class megaphone.

📊 Stage 1: Fetching USL data...
✓ Data fetched and saved

📊 Stage 1b: Consolidating accessibility metrics...
✓ Added 4 inequality metrics

🏘️ Stage 1c: Filtering content by UnfranchisedFC ethos...
✓ Content filtered: culture_club (priority: 10)

📝 Stage 2: Generating copy via LLM (with UnfranchisedFC system prompt)...
✓ LLM generated content:
  Voiceover: "Detroit City FC proved it: communities own soccer better than billionaires..."
  Caption: "Pro/rel is justice. Accessibility is democracy. #DCFC #ProRel..."

🎵 Stage 3: Generating audio...
   Using audio strategy: raw_chants
✓ Audio generated: output/audio/voiceover.mp3

🎬 Stage 4: Rendering video with brutalist aesthetic...
   Applying: High contrast, film grain, punk-rock energy
✓ Video generated: output/video/final_video.mp4

📱 Stage 5: Posting to Instagram...
✓ Successfully posted to Instagram!

✅ Pipeline complete!
🔥 UnfranchisedFC: Soccer from the streets. Pro/rel is justice.
```

---

## Module Dependencies

| Module | Imports | Purpose |
|--------|---------|---------|
| `orchestrator.py` | All others + strategy modules | Coordinates pipeline |
| `data_fetcher.py` | requests, praw, feedparser | Aggregates data |
| `llm_formatter.py` | requests, together | Generates copy with system prompt |
| `media_generator.py` | elevenlabs, moviepy, ffmpeg | Audio + video with effects |
| `instagram_poster.py` | instagrapi OR requests | Posts to Instagram |
| `world_cup_tracker.py` | requests, json | International play tracking |
| `accessibility_metrics.py` | dataclasses | Inequality data |
| `culture_club_priority.py` | dataclasses | Ethos filtering |
| `audio_strategy.py` | dataclasses | Audio options |
| `visual_style.py` | dataclasses | Brutalist aesthetic config |

---

## Testing the Pipeline

### Unit Tests
```bash
# Test data fetcher
python -c "from src.data_fetcher import fetch_usl_data; data = fetch_usl_data(); print(list(data['sources'].keys()))"

# Test LLM formatter (requires API)
python -c "from src.llm_formatter import generate_post_content; print(generate_post_content({'sources': {}}))"

# Test audio strategy
python src/audio_strategy.py

# Test visual style
python src/visual_style.py

# Test culture club priority
python src/culture_club_priority.py
```

### End-to-End Test
```bash
# Dry run (no Instagram post)
export INSTAGRAM_USERNAME=test
export INSTAGRAM_PASSWORD=test
python src/orchestrator.py
```

---

## Next Steps

1. **Set up GitHub Actions**: Schedule pipeline to run daily
2. **Test with real API keys**: Verify all data sources work
3. **Monitor early Reels**: Validate that content matches manifesto ethos
4. **Iterate on prompts**: Refine UNFRANCHISED_SYSTEM_PROMPT based on outputs
5. **Expand audio sources**: Build library of grassroots chants
6. **Add content analytics**: Track which narratives resonate

---

## The Ethos

```
Football belongs to the working class, immigrants, and marginalized communities.
Not billionaires. Not franchises. Not corporate stadiums.

Promotion & Relegation creates accountability.
Bad ownership = demotion.
Bad pricing = no fans = demotion.

The franchise system creates the opposite:
Billionaires can charge whatever they want.
Fans have nowhere else to go.

Until they build something new.
Until they own it themselves.

USL is that something.
Pro/rel is the mechanism.
Accessibility is justice.

This is UnfranchisedFC.
```

---

**Last Updated**: June 7, 2026
**Status**: 🔥 FULL PIPELINE INTEGRATED
