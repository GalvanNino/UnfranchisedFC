#!/usr/bin/env python3
"""
Closed-Loop Test: Generate complete .mp4 output without API keys.

This test simulates the full pipeline with mock data, generating:
1. LLM-formatted content (with UnfranchisedFC manifesto system prompt)
2. Audio (silent fallback, no TTS needed)
3. Video (with brutalist aesthetic)
4. Saves output to /output folder

Run: python3 closed_loop_test.py
"""

import os
import sys
import json
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from loguru import logger
from data_fetcher import consolidate_data
from llm_formatter import generate_post_content, build_prompt, extract_json_from_response, UNFRANCHISED_SYSTEM_PROMPT
from media_generator import generate_audio, generate_video


def setup_test_env():
    """Set up test environment variables."""
    logger.info("🔧 Setting up test environment...")
    
    # Create output directory
    output_dir = Path("output")
    output_dir.mkdir(exist_ok=True)
    (output_dir / "audio").mkdir(exist_ok=True)
    (output_dir / "video").mkdir(exist_ok=True)
    (output_dir / "final").mkdir(exist_ok=True)
    
    logger.info(f"✓ Output directory: {output_dir.absolute()}\n")
    return output_dir


def test_system_prompt():
    """Test that system prompt is properly embedded."""
    logger.info("🔥 Testing UnfranchisedFC System Prompt...")
    
    if "anti-corporate" in UNFRANCHISED_SYSTEM_PROMPT.lower():
        logger.info("✓ System prompt contains 'anti-corporate'")
    if "working-class" in UNFRANCHISED_SYSTEM_PROMPT.lower():
        logger.info("✓ System prompt contains 'working-class'")
    if "manifesto" in UNFRANCHISED_SYSTEM_PROMPT.lower():
        logger.info("✓ System prompt contains 'manifesto'")
    
    logger.info(f"✓ System prompt loaded ({len(UNFRANCHISED_SYSTEM_PROMPT)} chars)\n")


def test_llm_formatter_mock():
    """Test LLM formatter with mock LLM response."""
    logger.info("📝 Testing LLM Formatter (with mock response)...")
    
    # Create mock data
    mock_data = {
        "sources": {
            "api_sports": {"featured_match": "Detroit City FC vs Charlotte FC"},
            "news": [{"title": "Community Ownership Works"}],
            "rss": [{"title": "Detroit City FC wins again", "description": "Grassroots power"}]
        }
    }
    
    # Build prompt
    prompt = build_prompt(mock_data)
    logger.info(f"✓ Prompt built ({len(prompt)} chars, includes system prompt)")
    
    # Simulate LLM response (mock JSON)
    mock_response = '''
    ```json
    {
        "voiceover": "Detroit City FC proved it: working-class ownership beats billionaire franchises. Community power. Pro/rel justice.",
        "on_screen_text": "COMMUNITY OWNS\\nTHE GAME",
        "caption": "Detroit City FC: grassroots, community-owned, pro/rel ready. Soccer belongs to the people, not billionaires. #DCFC #ProRel"
    }
    ```
    '''
    
    # Extract JSON
    content = extract_json_from_response(mock_response)
    
    logger.info(f"✓ LLM response parsed:")
    logger.info(f"  - Voiceover: {content['voiceover'][:60]}...")
    logger.info(f"  - On-screen: {content['on_screen_text']}")
    logger.info(f"  - Caption: {content['caption'][:50]}...\n")
    
    return content


def test_media_generation(post_content, output_dir):
    """Test audio and video generation."""
    logger.info("🎬 Testing Media Generation...")
    
    # Generate audio (will use silent fallback if TTS not available)
    logger.info("  Generating audio...")
    audio_path = generate_audio(post_content["voiceover"], output_dir)
    logger.info(f"  ✓ Audio generated: {audio_path}")
    
    # Generate video with brutalist aesthetic
    logger.info("  Generating video with brutalist aesthetic...")
    video_path = generate_video(post_content, audio_path, output_dir, apply_brutalism=True)
    logger.info(f"  ✓ Video generated: {video_path}\n")
    
    return video_path


def verify_output(video_path):
    """Verify that the output file was created and has size."""
    logger.info("✅ Verifying output...")
    
    if video_path.exists():
        size_mb = video_path.stat().st_size / (1024 * 1024)
        logger.info(f"✓ Video file exists: {video_path}")
        logger.info(f"✓ File size: {size_mb:.2f} MB\n")
        return True
    else:
        logger.error(f"✗ Video file not found: {video_path}\n")
        return False


def main():
    """Run closed-loop test."""
    logger.info("=" * 70)
    logger.info("FLIG PIPELINE - CLOSED-LOOP TEST")
    logger.info("(No API keys required - uses mock data & local processing)")
    logger.info("=" * 70 + "\n")
    
    try:
        # Setup
        output_dir = setup_test_env()
        
        # Test system prompt
        test_system_prompt()
        
        # Test LLM formatter
        post_content = test_llm_formatter_mock()
        
        # Generate media
        video_path = test_media_generation(post_content, output_dir)
        
        # Verify output
        success = verify_output(video_path)
        
        # Final report
        logger.info("=" * 70)
        if success:
            logger.info("✅ CLOSED-LOOP TEST PASSED!")
            logger.info("\nNext steps:")
            logger.info("1. Play video: open output/video/final_video.mp4")
            logger.info("2. Verify gritty visual style (high contrast, film grain)")
            logger.info("3. Check caption for anti-corporate tone")
            logger.info("4. Set API keys and run full pipeline: python3 src/orchestrator.py")
            logger.info("5. Deploy to GitHub Actions")
        else:
            logger.error("❌ CLOSED-LOOP TEST FAILED")
            sys.exit(1)
        
        logger.info("=" * 70 + "\n")
        
    except Exception as e:
        logger.error(f"❌ Test failed: {e}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
