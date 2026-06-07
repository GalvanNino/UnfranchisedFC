# GitHub Actions Deployment Guide for UnfranchisedFC

This document explains how to set up GitHub Actions to run the AMF (Against Modern Football) pipeline automatically.

## Workflow Overview

**Workflow File**: `.github/workflows/deploy-amf-pipeline.yml`

**Schedule**: Runs daily at 10 AM UTC (6 AM EST, 3 AM PST)

**Steps**:
1. Checkout code from main branch
2. Set up Python 3.14 environment
3. Install FFmpeg (via Homebrew on macOS)
4. Install Python dependencies from `requirements-minimal.txt`
5. Create `.env` file from GitHub secrets
6. Run closed-loop test (validation)
7. Run full orchestrator pipeline (`src/orchestrator.py`)
8. Upload video artifacts
9. Post results to GitHub Actions summary
10. (Optional) Send Slack notification

## GitHub Secrets Setup

You must configure these secrets in your GitHub repository for the pipeline to function:

### 1. Navigate to GitHub Repository Settings
- Go to `https://github.com/GalvanNino/UnfranchisedFC`
- Click **Settings** → **Secrets and variables** → **Actions**

### 2. Create Repository Secrets

Create each of these as a **New repository secret**:

| Secret Name | Description | Example |
|---|---|---|
| `ELEVENLABS_API_KEY` | ElevenLabs TTS API key (optional if using silent fallback) | `sk_827d928...` |
| `TOGETHER_API_KEY` | Together.ai LLM API key for Llama 3 (optional) | Get from together.ai |
| `API_FOOTBALL_KEY` | API-Football API key for standings/matches (optional) | Get from api-football.com |
| `REDDIT_CLIENT_ID` | Reddit API client ID (optional) | Get from reddit.com/dev |
| `REDDIT_CLIENT_SECRET` | Reddit API client secret (optional) | Get from reddit.com/dev |
| `TWITTER_BEARER_TOKEN` | Twitter API v2 bearer token (optional) | Get from twitter.com/dev |
| `INSTAGRAPI_USERNAME` | Instagram username for posting (optional) | Your Instagram handle |
| `INSTAGRAPI_PASSWORD` | Instagram password or app token (optional) | Use app-specific password |
| `SLACK_WEBHOOK_URL` | Slack webhook for notifications (optional) | Get from Slack workspace |

**Note**: All API keys are optional. The pipeline gracefully falls back to:
- Silent audio if ElevenLabs unavailable
- Local LLM calls if Together.ai unavailable
- Static JSON data if external APIs unavailable
- No Instagram posting if credentials unavailable

### 3. Setting Secrets (CLI Alternative)

If using GitHub CLI:

```bash
gh secret set ELEVENLABS_API_KEY --body "sk_827d928..."
gh secret set TOGETHER_API_KEY --body "your_key_here"
# ... etc
```

## Workflow Triggers

### Automatic Schedule
Pipeline runs automatically at **10 AM UTC** every day.

### Manual Trigger
Trigger manually from GitHub Actions UI:
1. Go to **Actions** tab
2. Click **UnfranchisedFC AMF Pipeline**
3. Click **Run workflow**
4. (Optional) Select post number (1-9) or leave as "auto"
5. Click **Run workflow**

### Workflow Dispatch via CLI
```bash
gh workflow run deploy-amf-pipeline.yml
```

## Monitoring Pipeline Execution

### View Workflow Results
1. Go to **Actions** tab in GitHub
2. Click latest workflow run
3. View logs in **deploy-amf-pipeline** job
4. Download video artifacts if available

### Check Job Summary
After execution, GitHub Actions displays:
- ✅ Pipeline status (success/failure)
- 🎬 Video artifacts available for download
- 📊 Execution details and logs

### Slack Notifications (Optional)
If `SLACK_WEBHOOK_URL` is configured, you'll receive:
- Pipeline status notification
- Link to GitHub Actions run
- AMF manifesto reminder: *"Against Modern Football. Pro/Rel for the People."*

## Artifact Storage

Generated videos are stored as **GitHub Actions artifacts**:
- **Name**: `amf-videos`
- **Location**: `output/video/*.mp4`
- **Retention**: 7 days (configurable in workflow)
- **Download**: Via GitHub Actions UI → Artifacts

## Customizing the Schedule

To change the daily run time, edit `.github/workflows/deploy-amf-pipeline.yml`:

```yaml
on:
  schedule:
    # Change this cron expression (UTC timezone)
    - cron: '0 10 * * *'  # Currently: 10 AM UTC
```

Common cron times:
- `'0 10 * * *'` = 10 AM UTC (6 AM EST, 3 AM PST)
- `'0 14 * * *'` = 2 PM UTC (10 AM EST, 7 AM PST)
- `'0 2 * * *'` = 2 AM UTC (9 PM EST previous day, 6 PM PST previous day)
- `'0 * * * *'` = Every hour

[Cron Expression Reference](https://crontab.guru/)

## Environment Variables

The workflow automatically sets:
- `GITHUB_ACTIONS=true` (for conditional logic in orchestrator)
- `PYTHON_VERSION=3.14`
- `FFMPEG_VERSION=8.1.1`

## Troubleshooting

### Workflow fails to run
- Check that `.github/workflows/deploy-amf-pipeline.yml` is in main branch
- Verify branch is set to `main` in repository settings
- Check Actions are enabled in repository settings

### Missing API keys
- Secrets are optional; pipeline gracefully degrades
- Check `.env` file creation step in logs
- Silent audio will be used if TTS unavailable
- External APIs won't be queried if keys missing

### Video artifacts not generated
- Check logs for errors in `orchestrator.py`
- Run `python3 closed_loop_test.py` locally to validate pipeline
- Verify FFmpeg is installed (GitHub Actions handles this automatically)

### Can't find artifacts
- Artifacts expire after 7 days
- Download before expiration from Actions tab
- Modify `retention-days` in workflow file to extend

## Deployment Workflow

1. **Push to main branch**:
   ```bash
   git add .
   git commit -m "Deploy AMF pipeline with GitHub Actions"
   git push origin main
   ```

2. **Verify workflow file**:
   - Go to `.github/workflows/deploy-amf-pipeline.yml` in GitHub
   - Confirm it's present and readable

3. **Configure secrets**:
   - Go to **Settings → Secrets and variables → Actions**
   - Add all required secrets (listed above)

4. **Test manually**:
   - Go to **Actions** tab
   - Click **UnfranchisedFC AMF Pipeline**
   - Click **Run workflow**

5. **Monitor first run**:
   - Check logs for errors
   - Download artifacts if available
   - Adjust cron schedule as needed

## Ethos & Automation

This workflow embeds the **Against Modern Football (AMF)** manifesto directly into automated media creation:

- **System Prompt**: Anti-corporate, pro-community, pro-pyramid language
- **Visual Aesthetic**: Brutalist (yellow text on dark, Impact font, UPPERCASE)
- **Content Strategy**: 9-post campaign targeting structural inequality in soccer
- **Automation**: Daily posts on a schedule, no manual intervention required

*"Against Modern Football. Pro/Rel for the People."*

## Support

For issues or questions:
1. Check GitHub Actions logs for error details
2. Run `closed_loop_test.py` locally to validate
3. Check `.env` configuration
4. Verify API keys are correctly set in secrets

---

**Last Updated**: June 7, 2026  
**Workflow Version**: 1.0  
**Python Version**: 3.14  
**Required Tools**: FFmpeg 8.1.1+
