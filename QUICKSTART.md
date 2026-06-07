#!/usr/bin/env python3
"""
Quick Setup Guide - Get your USL Instagram pipeline running in 10 minutes.

This script walks you through the essential setup steps.
"""

import os
import subprocess
from pathlib import Path

def run_command(cmd, description=""):
    """Run a shell command."""
    if description:
        print(f"\n→ {description}")
    print(f"  $ {cmd}")
    result = subprocess.run(cmd, shell=True)
    return result.returncode == 0


def main():
    print("""
╔════════════════════════════════════════════════════════════╗
║     FLIG - Faceless Instagram + USL Pipeline               ║
║     Quick Setup Guide                                       ║
╚════════════════════════════════════════════════════════════╝

This guide will get you from zero to deployed in ~10 minutes.

PREREQUISITES:
  - Python 3.11+ installed
  - Git installed
  - ffmpeg installed (brew install ffmpeg on macOS)
  - GitHub account (for Actions deployment)

═══════════════════════════════════════════════════════════════
    """)
    
    # Step 1: Create virtual environment
    print("STEP 1: Create Python Virtual Environment")
    print("─" * 50)
    if not Path("venv").exists():
        run_command("python -m venv venv", "Creating venv...")
    
    # Step 2: Install dependencies
    print("\nSTEP 2: Install Dependencies")
    print("─" * 50)
    activate = "source venv/bin/activate" if os.name != "nt" else "venv\\Scripts\\activate"
    run_command(f"{activate} && pip install -r requirements.txt", 
               "Installing packages...")
    
    # Step 3: Get API Keys
    print("\nSTEP 3: Get LLM (FREE or Cheap)")
    print("─" * 50)
    print("""
OPTION A: OpenCode Zen (RECOMMENDED - FREE!)
  1. Install VS Code extension "OpenCode"
  2. Done! You have free LLM models
  3. See OPENCODE_SETUP.md for details
  
OPTION B: Together.ai Fallback (Cheap - ~$0.0008/1K tokens)
  → Go to: https://www.together.ai/
  → Sign up → Copy API key
  
Then get these:

1. ElevenLabs (TTS - ~$0.30 per 1K characters)
   → Go to: https://elevenlabs.io/
   → Sign up → Copy API key
   
2. Instagram (for test posting)
   → Use your personal account or create test account
   → Have username + password ready

═══════════════════════════════════════════════════════════════
    """)
    
    # Step 4: Configure .env
    print("\nSTEP 4: Create .env File")
    print("─" * 50)
    
    env_template = """# Use free OpenCode Zen models (just need VS Code extension)
LLM_BACKEND=opencode

# OR use Together.ai if you prefer (costs ~$0.0008 per 1K tokens)
# TOGETHER_API_KEY=sk_abc123...

ELEVENLABS_API_KEY=sk_abc123...
INSTAGRAM_USERNAME=your_username
INSTAGRAM_PASSWORD=your_password
"""
    
    if not Path(".env").exists():
        print("Creating .env file...")
        env_path = Path(".env")
        env_path.write_text(env_template)
        print("""✓ .env created with template values.
        
EDIT THIS FILE NOW:
  For OpenCode Zen (FREE):
    - Just set LLM_BACKEND=opencode (no API key needed!)
    - Install VS Code extension "OpenCode" for local LLM
  
  For Together.ai:
    - Uncomment TOGETHER_API_KEY and add your key
  
  Always add:
    - ELEVENLABS_API_KEY
    - INSTAGRAM_USERNAME and INSTAGRAM_PASSWORD
  
  nano .env
        """)
    else:
        print("✓ .env already exists")
    
    # Step 5: Test locally
    print("\nSTEP 5: Test Pipeline Locally")
    print("─" * 50)
    run_command(f"{activate} && python test_pipeline.py",
               "Running diagnostic tests...")
    
    # Step 6: Run orchestrator
    print("\nSTEP 6: Generate Sample Content")
    print("─" * 50)
    run_command(f"{activate} && python src/orchestrator.py",
               "Running full pipeline...")
    
    # Step 7: Deploy to GitHub
    print("\nSTEP 7: Deploy to GitHub Actions")
    print("─" * 50)
    print("""
Ready to deploy? Follow these steps:

1. Initialize Git (if not already):
   $ git init
   $ git add .
   $ git commit -m "Initial commit: FLIG pipeline"
   $ git branch -M main
   
2. Create GitHub repository:
   → Go to https://github.com/new
   → Create new repo (e.g., 'flig-instagram')
   → Do NOT initialize with README (we have one)
   
3. Push to GitHub:
   $ git remote add origin https://github.com/YOUR_USERNAME/flig-instagram.git
   $ git push -u origin main
   
4. Add Secrets to GitHub:
   → Go to Settings → Secrets and variables → Actions
   → Click "New repository secret"
   → Add these secrets:
     • TOGETHER_API_KEY
     • ELEVENLABS_API_KEY
     • INSTAGRAM_USERNAME
     • INSTAGRAM_PASSWORD
   
5. Test the workflow:
   → Go to Actions tab
   → Click "Generate and Post USL Content"
   → Click "Run workflow" button
   → Monitor the logs in real-time

═══════════════════════════════════════════════════════════════

✅ DONE! Your pipeline is now automated.

Next runs will happen on schedule (Tuesday & Thursday at 10 AM UTC).
You can manually trigger anytime from the Actions tab.

═══════════════════════════════════════════════════════════════

TROUBLESHOOTING:

  • LLM not generating text?
    → Check TOGETHER_API_KEY is valid
    → Try different prompt in src/llm_formatter.py
  
  • Audio not generating?
    → Check ELEVENLABS_API_KEY is valid
    → Script will use silent audio for testing
  
  • Video rendering slow?
    → Lower video resolution in config
    → Use faster codec (mpeg4 instead of libx264)
  
  • Instagram posting fails?
    → Try logging in manually to account
    → Some accounts require app-specific passwords
    → Consider using Meta Graph API instead

═══════════════════════════════════════════════════════════════

Questions? Check README.md or see inline code comments.
    """)


if __name__ == "__main__":
    main()
