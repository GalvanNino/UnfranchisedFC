# Automated USL Instagram Pipeline

A fully deterministic, programmatic pipeline for generating and posting automated USL Championship content to Instagram using **free open-weight LLMs (OpenCode Zen)**, GitHub Actions, and standard media generation tools.

## Architecture

```
GitHub Actions (Scheduled)
    ↓
[1] Data Fetch (APIs, Web Scraping, Twitter/X)
    ↓
[2] LLM Formatting (OpenCode Zen FREE or Together.ai)
    ├→ Voiceover text
    ├→ On-screen text
    └→ Caption + hashtags
    ↓
[3] Media Generation
    ├→ TTS Audio (ElevenLabs)
    └→ Video Rendering (MoviePy)
    ↓
[4] Merge & Stitch (ffmpeg)
    ↓
[5] Instagram Posting (instagrapi or Meta Graph API)
```

## Why Programmatic > Multi-Agent

- **Deterministic:** You control every step. No hallucinations between handoffs.
- **Cheap:** GitHub Actions is free. LLM via OpenCode Zen is free. Total: ~$0.11/post.
- **Reliable:** Each stage has clear inputs/outputs. Errors are logged and traceable.
- **Maintainable:** Single Python script, not multiple competing bots.
- **Private (optional):** Use local Ollama for 100% private inference.

## Cost Breakdown

| Component | Cost |
|-----------|------|
| LLM (OpenCode Zen) | $0 FREE |
| TTS (30s) | $0.10 |
| GitHub Actions | $0.01 |
| **Per post** | **~$0.11** |
| **2x/week** | **$11.44/year** |

*Note: Costs shown are for ElevenLabs TTS. You can reduce to $0 by using free TTS APIs.*

## Setup

### 1. Clone & Install Dependencies

```bash
git clone <repo>
cd FLIG
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Get API Keys

#### PRIMARY: OpenCode Zen (FREE!)

No setup required! Just install the VS Code extension:

1. Open VS Code
2. Go to **Extensions** (Cmd+Shift+X)
3. Search "OpenCode"
4. Install the official extension
5. Done! You now have free access to:
   - Big Pickle
   - MiniMax M2.5 Free
   - MiMo V2 Pro Free
   - Nemotron 3 Super Free

**See [OPENCODE_SETUP.md](OPENCODE_SETUP.md) for details.**

#### SECONDARY: Other APIs (Optional)

| Service | Purpose | Cost | Sign Up |
|---------|---------|------|---------|
| **Together.ai** | LLM fallback | ~$0.0008 per 1K tokens | [together.ai](https://www.together.ai/) |
| **ElevenLabs** | Text-to-Speech | ~$0.30 per 1K chars | [elevenlabs.io](https://elevenlabs.io/) |
| **Instagram** | Posting (Personal) | Free | Meta account required |
| **Meta** | Posting (Business) | Free | [developers.facebook.com](https://developers.facebook.com/) |

### 3. Configure Environment

```bash
# Copy the example
cp .env.example .env

# Edit .env with your API keys
# OpenCode will auto-detect from VS Code extension
# Only need Twitter bearer token, ElevenLabs key, Instagram creds
nano .env
```

Default setup uses **OpenCode Zen** (free). Change to Together.ai if preferred:

```bash
export LLM_BACKEND=together
export TOGETHER_API_KEY=your_key_here
```

### 4. Local Testing

```bash
# Test the full pipeline locally
python src/orchestrator.py
```

Output will be in `./output/`:
```
output/
├── raw_data/
│   ├── raw_input.json
│   └── llm_output.json
├── audio/
│   └── voiceover.mp3
├── video/
│   └── final_video.mp4
└── final/
    └── (merged video ready to post)
```

### 5. Deploy to GitHub

#### Step 5a: Add Repository Secrets

Go to **Settings → Secrets and variables → Actions** and add:

For OpenCode Zen (local):
- `OPENCODE_API_URL=http://localhost:8000` (only if using self-hosted runner)

For Together.ai fallback:
- `TOGETHER_API_KEY` (needed for GitHub Actions, as Zen runs locally)
- `ELEVENLABS_API_KEY`
- `INSTAGRAM_USERNAME`
- `INSTAGRAM_PASSWORD`
- (Optional) `META_ACCESS_TOKEN`, `IG_BUSINESS_ACCOUNT_ID`

**Note:** GitHub Actions uses **Together.ai** as the backend (not OpenCode Zen, since it's local to VS Code). You can override this in `.github/workflows/generate_and_post.yml`:

```yaml
env:
  LLM_BACKEND: "together"  # Use Together.ai in cloud runner
  TOGETHER_API_KEY: ${{ secrets.TOGETHER_API_KEY }}
```

#### Step 5b: Push to GitHub

```bash
git add .
git commit -m "Initial commit: automated USL pipeline"
git push origin main
```

#### Step 5c: Verify Workflow

- Go to **Actions** tab on GitHub
- Click **Generate and Post USL Content**
- Click **Run workflow**
- Monitor logs in real-time

## Configuration

### LLM Backend Selection

You can choose your LLM backend for text generation:

```bash
# Use OpenCode Zen (DEFAULT - Free, cloud)
export LLM_BACKEND=opencode

# Use Together.ai (Cheap - ~$0.0008/1K tokens)
export LLM_BACKEND=together
export TOGETHER_API_KEY=your_key

# Try OpenCode first, fall back to Together.ai
export LLM_BACKEND=auto
```

**Privacy Note:** OpenCode Zen (free tier) may log data for training. Use paid options for sensitive code. See [OPENCODE_SETUP.md](OPENCODE_SETUP.md).

### Data Sources Configuration

The pipeline aggregates data from:

**Official USL Accounts:**
- @USLChampionship, @USLLeagueOne, @USLLeagueTwo

**Analysis & Tactics:**
- @BackHeeledUSL, @USLTactics, @ManagerTactical, @USLL1Review

**Podcasts & Shows:**
- @USLRdio, @TheUSLShow, @TotalSoccerShow, @11Yanks

**Journalists & Analysts:**
- @grahamruthven, @jeffrueter, @ByDougMcIntyre, @BrianSciaretta, @WillParchman

**Team Accounts:**
- @AkronCityFC, @ChattanoogaFC, @LexSporting, @mplscitysc, @dallastrinityfc, @GainbridgeSL, @atleticodallas, @ForwardMSNFC

**Regional Coverage:**
- @BigDSoccer, @PrepSoccerTX, @ESPNFC, @MASLarena

To customize, edit `src/data_fetcher.py` and update the `handles` list in `fetch_from_twitter_accounts()`.

### Adjust Schedule

Edit `.github/workflows/generate_and_post.yml`:

```yaml
schedule:
  - cron: '0 10 * * 2,4'  # Tuesday (2) and Thursday (4) at 10 AM UTC
```

[Cron syntax reference](https://crontab.guru)

### Customize LLM

#### OpenCode Zen Models

Edit `src/llm_formatter.py` to choose which free model to use:

```python
response = call_llm_opencode_zen(
    prompt,
    model="big-pickle"  # Options:
    # - "big-pickle" (fastest, recommended for sports)
    # - "minimax-m2.5-free" (best reasoning)
    # - "mimo-v2-pro-free" (long context)
    # - "nemotron-3-super-free" (balanced)
)
```

#### Together.ai Models

If using Together.ai as backend:

```python
response = client.complete(
    model="meta-llama/Llama-3-70b-chat-hf",  # 70B, most accurate
    # OR
    model="mistralai/Mistral-7B-Instruct-v0.1",  # 7B, faster
    # OR
    model="meta-llama/Llama-2-13b-chat-hf",  # Older, cheaper
    ...
)

### Add Data Sources

In `src/data_fetcher.py`, expand the functions:

- `fetch_from_api_sports()` - Add your sports API
- `fetch_from_usl_website()` - Customize web scraping selectors
- `fetch_from_twitter_accounts()` - Add your Twitter handles
- `fetch_news_feeds()` - Configure news sources

### Customize Video Style

In `src/media_generator.py`, modify:

```python
# Change background color
background = ColorfulVideoClip(
    size=(1080, 1920),
    color=(25, 45, 85)  # RGB: Dark blue
).set_duration(duration)

# Change text style
text_clip = TextClip(
    text,
    fontsize=80,
    color="white",
    font="Arial-Bold",
    ...
)
```

## Troubleshooting

### LLM API Errors

#### OpenCode Zen Issues

```
Error: Could not connect to http://localhost:8000
```
→ Ensure VS Code with OpenCode extension is running. The extension runs a local server.
→ Falls back to Together.ai automatically if unavailable.

```
Error: Model 'big-pickle' not available
```
→ Run `/models` in OpenCode chat to see available options.
→ Check your internet connection (models are cloud-hosted).

#### Together.ai Issues

```
TOGETHER_API_KEY not set
```
→ Check GitHub secrets are configured. Locally, ensure `.env` is in the root directory.

```
Failed to parse LLM response as JSON
```
→ The LLM didn't return valid JSON. Try adjusting the prompt in `build_prompt()`.

### Audio Generation Fails

```
ELEVENLABS_API_KEY not set
```
→ The script will generate silent audio for testing. Set the key to enable real TTS.

### Video Rendering Issues

```
MoviePy error: ffmpeg not found
```
→ Install ffmpeg:
- **macOS:** `brew install ffmpeg`
- **Linux:** `sudo apt install ffmpeg`
- **Windows:** Download from [ffmpeg.org](https://ffmpeg.org/download.html)

### Instagram Posting Fails

**Option 1: instagrapi (Personal Account)**
- Issue: "Login failed"
- Solution: Try logging in manually to your account first. Some accounts require app-specific passwords.
- Alternative: Use Meta Graph API (official method).

**Option 2: Meta Graph API (Business Account)**
- Follow [this guide](https://developers.facebook.com/docs/instagram-api/getting-started) to set up a Business Account with Graph API access.

## Cost Breakdown (Per Post)

| Component | Cost |
|-----------|------|
| LLM (Llama 3, ~200 tokens) | $0.0002 |
| TTS (ElevenLabs, ~30 seconds) | $0.10 |
| GitHub Actions (compute) | ~$0.01 |
| **Total per post** | **~$0.11** |

**2x per week = $11.44/year** 🎉

## Next Steps

1. **Test locally** with dummy data
2. **Deploy to GitHub** with test account
3. **Monitor logs** for the first few posts
4. **Iterate on LLM prompts** to refine content quality
5. **Scale** by scheduling additional content types

## Documentation

- **[README.md](README.md)** - You are here
- **[QUICKSTART.md](QUICKSTART.md)** - 10-minute setup guide
- **[OPENCODE_SETUP.md](OPENCODE_SETUP.md)** - Free LLM integration
- **[DATA_ARCHITECTURE.md](DATA_ARCHITECTURE.md)** - Comprehensive data pipeline (NEW)

The **[DATA_ARCHITECTURE.md](DATA_ARCHITECTURE.md)** document explains the complete data infrastructure:
- Live API data (API-Football, Wikipedia)
- Cultural sentiment (Reddit)
- News & updates (RSS feeds, Twitter)
- Static context (World Cup 2026 base camps)
- How they all connect for authenticity

## License

This project is provided as-is. Use at your own risk and ensure compliance with Instagram's TOS and local laws.

---

**Made with 🤖 + 📹 + ☁️**
