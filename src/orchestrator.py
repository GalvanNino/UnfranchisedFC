#!/usr/bin/env python3
"""
Main orchestration script for the automated USL Instagram pipeline.

This script coordinates all pipeline stages:
1. Data ingestion (USL standings, news, Twitter)
2. LLM-driven copy generation
3. Audio generation (TTS)
4. Video rendering
5. Instagram posting

Author: Your Team
"""

import os
import json
from pathlib import Path
from datetime import datetime
from loguru import logger

# Import pipeline modules
from data_fetcher import fetch_usl_data
from llm_formatter import generate_post_content
from media_generator import generate_audio, generate_video
from instagram_poster import post_to_instagram


def setup_output_directory():
    """Create output directory for generated media."""
    output_dir = Path(os.getenv("OUTPUT_DIR", "./output"))
    output_dir.mkdir(parents=True, exist_ok=True)
    
    # Create subdirectories
    (output_dir / "raw_data").mkdir(exist_ok=True)
    (output_dir / "audio").mkdir(exist_ok=True)
    (output_dir / "video").mkdir(exist_ok=True)
    (output_dir / "final").mkdir(exist_ok=True)
    
    return output_dir


def log_pipeline_state(stage: str, data: dict, output_dir: Path):
    """Log pipeline state to JSON for debugging."""
    log_file = output_dir / f"pipeline_log_{datetime.now().isoformat()}.json"
    with open(log_file, "w") as f:
        json.dump({"stage": stage, "timestamp": datetime.now().isoformat(), "data": data}, f, indent=2)
    logger.info(f"✓ {stage} | Logged to {log_file}")


def main():
    """Execute the full pipeline."""
    logger.add("logs/pipeline_{time}.log", rotation="500 MB")
    logger.info("🚀 Starting automated USL Instagram pipeline...")
    
    output_dir = setup_output_directory()
    
    try:
        # Stage 1: Fetch Data
        logger.info("📊 Stage 1: Fetching USL data...")
        raw_data = fetch_usl_data()
        log_pipeline_state("data_fetch", raw_data, output_dir)
        
        # Save raw data for reference
        with open(output_dir / "raw_data" / "raw_input.json", "w") as f:
            json.dump(raw_data, f, indent=2)
        logger.info("✓ Data fetched and saved")
        
        # Stage 2: Generate LLM-driven content (structured JSON response)
        logger.info("📝 Stage 2: Generating copy via LLM...")
        llm_backend = os.getenv("LLM_BACKEND", "opencode")  # Default to free OpenCode Zen
        post_content = generate_post_content(raw_data, backend=llm_backend)
        log_pipeline_state("llm_format", post_content, output_dir)
        
        # Save LLM output
        with open(output_dir / "raw_data" / "llm_output.json", "w") as f:
            json.dump(post_content, f, indent=2)
        logger.info(f"✓ LLM generated content:\n  Voiceover: {post_content['voiceover'][:50]}...\n  Caption: {post_content['caption'][:50]}...")
        
        # Stage 3: Generate Audio
        logger.info("🎵 Stage 3: Generating audio...")
        audio_path = generate_audio(post_content["voiceover"], output_dir)
        logger.info(f"✓ Audio generated: {audio_path}")
        
        # Stage 4: Generate Video
        logger.info("🎬 Stage 4: Rendering video...")
        video_path = generate_video(post_content, audio_path, output_dir)
        logger.info(f"✓ Video generated: {video_path}")
        
        # Stage 5: Post to Instagram
        logger.info("📱 Stage 5: Posting to Instagram...")
        result = post_to_instagram(video_path, post_content["caption"])
        if result:
            logger.info(f"✓ Successfully posted to Instagram!")
            log_pipeline_state("instagram_post", {"status": "success", "media_id": result}, output_dir)
        else:
            logger.warning("⚠ Post to Instagram failed. Check credentials.")
            log_pipeline_state("instagram_post", {"status": "failed"}, output_dir)
        
        logger.info("✅ Pipeline complete!")
        
    except Exception as e:
        logger.error(f"❌ Pipeline failed at: {e}", exc_info=True)
        raise


if __name__ == "__main__":
    main()
