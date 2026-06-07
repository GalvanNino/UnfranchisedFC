# Using OpenCode Zen Models with FLIG

## What is OpenCode Zen?

**OpenCode Zen** is a free tier of open-weight LLM models integrated into VS Code (via the OpenCode extension). It provides:

- ✅ **Zero Setup:** No API keys, no local GPU required
- ✅ **Multiple Models:** Big Pickle, MiniMax M2.5, MiMo V2 Pro, Nemotron 3
- ✅ **VS Code Native:** Works directly in your editor
- ✅ **Free:** No credit card needed

## The Privacy Tradeoff

⚠️ **Important:** Free Zen models are cloud-based. The providers **may use your code snippets and prompts for training purposes**.

**For sensitive/proprietary code, choose:**
1. **OpenCode Go** ($10/month) - Better privacy, top-tier models
2. **Local Ollama** - Run models locally (requires GPU)
3. **Together.ai** - Paid tier with privacy guarantees

## Setup Guide

### Step 1: Install OpenCode Extension

1. Open VS Code
2. Go to **Extensions** (Cmd+Shift+X on Mac)
3. Search for "OpenCode"
4. Click **Install** (look for official OpenCode extension)

### Step 2: Verify Installation

1. Open the integrated terminal in VS Code
2. You should see an OpenCode chat panel on the right
3. Type `/models` and press Enter
4. You'll see available models:
   - **Big Pickle** - General coding (recommended)
   - **MiniMax M2.5 Free** - Long context, strong reasoning
   - **MiMo V2 Pro** - Xiaomi's coding model
   - **Nemotron 3 Super** - NVIDIA's fast model

### Step 3: Test the Connection (Optional)

```bash
# Local test to ensure OpenCode is accessible
curl http://localhost:8000/models

# Should return list of available models
```

If this fails, the VS Code extension will handle it automatically.

### Step 4: Configure FLIG to Use OpenCode

Edit `src/orchestrator.py`:

```python
# At the top of main()
from config.config import config

# Pass the LLM backend
post_content = generate_post_content(raw_data, backend="opencode")
```

Or use the environment variable:

```bash
export LLM_BACKEND=opencode
```

### Step 5: Run the Pipeline

```bash
python src/orchestrator.py
```

The pipeline will:
1. Try OpenCode Zen first (free)
2. Fall back to Together.ai if OpenCode unavailable
3. Log which model was used

## How It Works Technically

### Local OpenCode Server

The VS Code extension runs a lightweight server on `localhost:8000` that provides:
- `/models` - List available models
- `/chat/completions` - OpenAI-compatible chat endpoint
- Automatic authentication (VS Code handles it)

### Cloud Models

The actual LLM inference runs on OpenCode's infrastructure. Your prompts are sent to their servers, which is why the privacy caveat exists.

### Fallback Chain

```
OpenCode Zen (free, cloud)
    ↓ (if unavailable)
Together.ai (cheap, cloud)
    ↓ (if unavailable)
Local Ollama (optional, your GPU)
```

## Choosing the Right Model for USL Content

| Model | Speed | Reasoning | Cost | Best For |
|-------|-------|-----------|------|----------|
| **Big Pickle** | ⚡⚡⚡ | ⭐⭐ | FREE | Quick, casual posts |
| **MiniMax M2.5** | ⚡⚡ | ⭐⭐⭐ | FREE | Complex analysis |
| **MiMo V2 Pro** | ⚡⚡ | ⭐⭐⭐ | FREE | Long context (tweets) |
| **Nemotron 3** | ⚡⚡⚡ | ⭐⭐ | FREE | Real-time updates |
| Together.ai Llama 3 | ⚡ | ⭐⭐⭐⭐ | $0.0008/1K | Production quality |

**Recommendation for USL:** Start with **Big Pickle** for speed, upgrade to **MiniMax M2.5** if you need better reasoning about standings/stats.

## Advanced: Self-Hosting in GitHub Actions

To run OpenCode in GitHub Actions (limited), you can:

1. Use a **self-hosted runner** with OpenCode installed locally
2. Or use a cloud OpenCode instance (not yet public)

For now, GitHub Actions will use **Together.ai** as the backend. You can configure this:

```yaml
# .github/workflows/generate_and_post.yml
env:
  LLM_BACKEND: "together"  # Use Together.ai in Actions
  TOGETHER_API_KEY: ${{ secrets.TOGETHER_API_KEY }}
```

For local testing, use:

```bash
LLM_BACKEND=opencode python src/orchestrator.py
```

## Troubleshooting

### "OpenCode API not accessible"

```
Error: Could not connect to http://localhost:8000
```

**Solution:**
- Ensure VS Code with OpenCode extension is running
- Check port 8000 is not blocked by firewall
- Falls back to Together.ai automatically

### "Model not found"

```
Error: Model 'big-pickle' not available
```

**Solution:**
- Run `/models` in OpenCode chat to see available options
- Update model name in config
- Default models should always be available

### "Response exceeds token limit"

```
Error: Generated text too long
```

**Solution:**
- Reduce prompt length in `build_prompt()`
- Use a faster model (Nemotron 3)
- Shorten the input data

## Privacy FAQ

**Q: Will OpenCode use my USL data for training?**

A: Free Zen models may log your prompts. For a public sports account, this is acceptable. For sensitive work, use OpenCode Go ($10/month).

**Q: Can I disable privacy logging?**

A: Not for free models. Upgrade to OpenCode Go or use a local Ollama instance.

**Q: What about GitHub Actions?**

A: GitHub Actions will use Together.ai (or your configured backend). It's cloud-based but has explicit privacy terms you control.

## Resources

- [OpenCode Documentation](https://opencode.dev/docs)
- [VS Code Extension Marketplace](https://marketplace.visualstudio.com)
- [Zen Models Comparison](https://opencode.dev/zen)
- [OpenCode Go (Paid Tier)](https://opencode.dev/pricing)
- [Local Ollama Setup](https://ollama.ai/)

---

**Next:** Run your pipeline locally with OpenCode Zen, then deploy to GitHub Actions with Together.ai as backup.

```bash
# Local: Uses OpenCode Zen
LLM_BACKEND=opencode python src/orchestrator.py

# GitHub Actions: Uses Together.ai
# (Set TOGETHER_API_KEY in secrets)
```
