#!/usr/bin/env python3
"""
Test AMF Post #1: "The Structural Trap"
Franchise vs Pyramid - structural critique of closed vs open models.

This test:
1. Loads Post #1 from amf_launch_strategy
2. Builds an AMF prompt for this specific post
3. Generates mock LLM response with anti-corporate messaging
4. Creates audio + video with brutalist aesthetic
5. Validates output
"""

import sys
import json
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from loguru import logger
from llm_formatter import build_amf_prompt, extract_json_from_response, validate_content
from media_generator import generate_audio, generate_video, apply_visual_brutalism
from amf_launch_strategy import get_amf_post

# Configure logging
logger.remove()
logger.add(
    lambda msg: print(msg, end=""),
    format="<level>{time:YYYY-MM-DD HH:mm:ss.SSS}</level> | <level>{level: <8}</level> | <level>{message}</level>\n"
)

# Mock LLM response for Post #1 (Franchise vs Pyramid)
MOCK_POST_1_RESPONSE = """{
  "voiceover": "The USL Championship proves it: open pyramids destroy billionaire gatekeeping. Every club fights for promotion. No guaranteed franchise security blankets. Sporting merit determines survival, not investor bank accounts. This is what American soccer could be. Pro/rel is the only answer.",
  "on_screen_text": "OPEN PYRAMID OR BILLIONAIRE CARTEL? CHOOSE MERITOCRACY",
  "caption": "USL: meritocracy. MLS: monopoly. Open pyramids end billionaire control. This is pro/rel justice. #UnfranchisedFC #AgainstModernFootball #ProRelForUSA"
}"""


def main():
    logger.info("="*60)
    logger.info("AMF POST #1 TEST: 'The Structural Trap'")
    logger.info("="*60)
    
    # Load Post #1
    post_1 = get_amf_post(1)
    if not post_1:
        logger.error("❌ Post #1 not found")
        return
    
    logger.info(f"\n📋 Post Details:")
    logger.info(f"  Title: {post_1['title']}")
    logger.info(f"  Type: {post_1['type']}")
    logger.info(f"  Focus: {post_1['focus']}")
    logger.info(f"  Keywords: {', '.join(post_1['ethos_keywords'])}")
    
    # Build AMF prompt for this post
    logger.info(f"\n🔨 Building AMF prompt for franchise_vs_pyramid...")
    prompt = build_amf_prompt("franchise_vs_pyramid", post_1["context"])
    logger.info(f"  ✓ Prompt built ({len(prompt)} chars)")
    logger.info(f"  Preview: {prompt[:150]}...")
    
    # Parse mock LLM response
    logger.info(f"\n🤖 Mock LLM Response:")
    content = extract_json_from_response(MOCK_POST_1_RESPONSE)
    logger.info(f"  Voiceover: {content['voiceover'][:60]}...")
    logger.info(f"  On-screen: {content['on_screen_text']}")
    logger.info(f"  Caption: {content['caption'][:60]}...")
    
    # Validate content
    logger.info(f"\n✅ Validating content...")
    is_valid = validate_content(content)
    if not is_valid:
        logger.error("❌ Content validation failed")
        return
    logger.info(f"  ✓ Content valid")
    
    # Generate audio
    logger.info(f"\n🎵 Generating audio...")
    output_dir = Path(__file__).parent / "output"
    output_dir.mkdir(exist_ok=True)
    
    audio_path = generate_audio(content["voiceover"], output_dir)
    logger.info(f"  ✓ Audio: {audio_path}")
    
    # Generate video
    logger.info(f"\n🎬 Generating video...")
    video_path = generate_video(content, audio_path, output_dir)
    logger.info(f"  ✓ Raw video: {video_path}")
    
    # Apply brutalism
    logger.info(f"\n🎨 Applying brutalist aesthetic...")
    final_path = apply_visual_brutalism(video_path, output_dir)
    logger.info(f"  ✓ Final video: {final_path}")
    
    # Verify output
    if final_path.exists():
        size_mb = final_path.stat().st_size / (1024 * 1024)
        logger.info(f"\n📊 Output verification:")
        logger.info(f"  File: {final_path}")
        logger.info(f"  Size: {size_mb:.2f} MB")
        logger.info(f"\n✅ POST #1 TEST PASSED!")
        logger.info(f"\n🎯 Next steps:")
        logger.info(f"  1. Play video: open {final_path}")
        logger.info(f"  2. Check for yellow brutalist text overlay")
        logger.info(f"  3. Verify anti-corporate tone in voiceover")
        logger.info(f"  4. Post to Instagram (when ready)")
    else:
        logger.error(f"❌ Video file not created: {final_path}")


if __name__ == "__main__":
    main()
