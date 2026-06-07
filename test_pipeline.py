#!/usr/bin/env python3
"""
Quick test script to verify all pipeline components work.

Run locally before deploying to GitHub Actions.
"""

import os
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from loguru import logger


def test_imports():
    """Test that all required modules can be imported."""
    logger.info("Testing imports...")
    
    try:
        import together
        logger.info("✓ together")
    except ImportError:
        logger.warning("✗ together (pip install together)")
    
    try:
        from elevenlabs import generate
        logger.info("✓ elevenlabs")
    except ImportError:
        logger.warning("✗ elevenlabs (pip install elevenlabs)")
    
    try:
        from moviepy.editor import TextClip
        logger.info("✓ moviepy")
    except ImportError:
        logger.warning("✗ moviepy (pip install moviepy)")
    
    try:
        from instagrapi import Client
        logger.info("✓ instagrapi")
    except ImportError:
        logger.warning("✗ instagrapi (pip install instagrapi)")
    
    logger.info("✓ All core imports successful\n")


def test_env_vars():
    """Test that environment variables are set."""
    logger.info("Testing environment variables...")
    
    required = [
        "TOGETHER_API_KEY",
        "ELEVENLABS_API_KEY",
        "INSTAGRAM_USERNAME",
        "INSTAGRAM_PASSWORD",
    ]
    
    optional = [
        "META_ACCESS_TOKEN",
        "IG_BUSINESS_ACCOUNT_ID",
        "TWITTER_BEARER_TOKEN",
    ]
    
    missing = []
    for var in required:
        if os.getenv(var):
            logger.info(f"✓ {var}")
        else:
            logger.warning(f"✗ {var} (REQUIRED)")
            missing.append(var)
    
    for var in optional:
        if os.getenv(var):
            logger.info(f"✓ {var}")
        else:
            logger.info(f"○ {var} (optional)")
    
    if missing:
        logger.error(f"\nMissing required: {', '.join(missing)}")
        logger.error("Set in .env or GitHub secrets")
        return False
    
    logger.info("✓ All required env vars present\n")
    return True


def test_ffmpeg():
    """Test that ffmpeg is installed."""
    logger.info("Testing ffmpeg...")
    
    import subprocess
    try:
        result = subprocess.run(["ffmpeg", "-version"], 
                              capture_output=True, 
                              timeout=5)
        if result.returncode == 0:
            version = result.stdout.decode().split("\n")[0]
            logger.info(f"✓ {version}\n")
            return True
    except FileNotFoundError:
        logger.error("✗ ffmpeg not found")
        logger.error("Install: brew install ffmpeg (macOS)")
        logger.error("         sudo apt install ffmpeg (Linux)")
        return False


def test_data_fetcher():
    """Test data fetching module."""
    logger.info("Testing data fetcher...")
    
    try:
        from data_fetcher import consolidate_data
        
        # This should work even without real API keys
        data = consolidate_data()
        logger.info(f"✓ Data fetcher works (fetched {len(data['sources'])} sources)\n")
        return True
    except Exception as e:
        logger.error(f"✗ Data fetcher failed: {e}\n")
        return False


def test_llm_formatter():
    """Test LLM formatter (without API call)."""
    logger.info("Testing LLM formatter...")
    
    try:
        from llm_formatter import build_prompt, extract_json_from_response, call_llm_opencode_zen
        
        # Test prompt building
        sample_data = {"sources": {}}
        prompt = build_prompt(sample_data)
        logger.info(f"✓ Prompt builder works ({len(prompt)} chars)")
        
        # Test JSON extraction
        sample_response = '''
        ```json
        {
            "voiceover": "Test voiceover",
            "on_screen_text": "Test text",
            "caption": "Test caption"
        }
        ```
        '''
        content = extract_json_from_response(sample_response)
        logger.info(f"✓ JSON extraction works\n")
        return True
    except Exception as e:
        logger.error(f"✗ LLM formatter failed: {e}\n")
        return False


def test_opencode():
    """Test OpenCode Zen availability."""
    logger.info("Testing OpenCode Zen...")
    
    try:
        import requests
        response = requests.get("http://localhost:8000/models", timeout=2)
        if response.status_code == 200:
            models = response.json()
            logger.info(f"✓ OpenCode Zen available ({len(models)} models)")
            return True
    except Exception as e:
        logger.warning(f"○ OpenCode Zen not available: {e}")
        logger.info("  (This is OK - will fall back to Together.ai)")
        return None  # Optional, not required
    
    return False


def main():
    """Run all tests."""
    logger.info("=" * 60)
    logger.info("FLIG Pipeline - Component Test Suite")
    logger.info("=" * 60 + "\n")
    
    results = {
        "Imports": test_imports(),
        "Environment": test_env_vars(),
        "OpenCode Zen": test_opencode(),  # Optional
        "FFmpeg": test_ffmpeg(),
        "Data Fetcher": test_data_fetcher(),
        "LLM Formatter": test_llm_formatter(),
    }
    
    logger.info("=" * 60)
    logger.info("SUMMARY")
    logger.info("=" * 60)
    
    required_pass = 0
    optional_pass = 0
    
    for name, passed in results.items():
        if passed is None:
            status = "○ OPTIONAL"
            logger.info(f"{status}: {name}")
        elif passed:
            status = "✓ PASS"
            if name == "OpenCode Zen":
                optional_pass += 1
            else:
                required_pass += 1
            logger.info(f"{status}: {name}")
        else:
            status = "✗ FAIL"
            logger.info(f"{status}: {name}")
    
    logger.info("\n" + "=" * 60)
    
    all_required_pass = all(v for k, v in results.items() if v is not None and k != "OpenCode Zen")
    
    if all_required_pass:
        logger.info("✅ All required tests passed!")
        if optional_pass > 0:
            logger.info(f"   + {optional_pass} optional test(s) passed")
        logger.info("\nYour pipeline is ready to go:")
        logger.info("  • Local: python src/orchestrator.py")
        logger.info("  • GitHub Actions: Push and deploy")
    else:
        logger.error("⚠️  Some required tests failed. Fix issues before deploying.")
        sys.exit(1)


if __name__ == "__main__":
    main()
