#!/usr/bin/env python3
"""
Main orchestration script for the automated USL Instagram pipeline.

This script coordinates all pipeline stages:
1. Data ingestion (USL standings, news, Twitter, accessibility metrics, culture clubs)
2. Content filtering (prioritize culture clubs + street soccer)
3. LLM-driven copy generation (with UnfranchisedFC manifesto ethos)
4. Audio generation (TTS + Barrio y Rebeldía soundtrack or raw chants)
5. Video rendering (with brutalist visual aesthetic)
6. Instagram posting

The entire pipeline embeds the anti-corporate, pro-community working-class ethos.

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

# Import strategy modules (ethos integration)
try:
    from accessibility_metrics import consolidate_accessibility_data
except ImportError:
    logger.warning("accessibility_metrics module not found. Skipping inequality data.")
    consolidate_accessibility_data = None

try:
    from culture_club_priority import filter_content_by_ethos, get_content_amplification_prompt
except ImportError:
    logger.warning("culture_club_priority module not found. Using generic content.")
    filter_content_by_ethos = None
    get_content_amplification_prompt = None

try:
    from audio_strategy import AUDIO_OPTIONS, AUDIO_STYLE_GUIDE
except ImportError:
    logger.warning("audio_strategy module not found. Using default TTS.")
    AUDIO_OPTIONS = None


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
    logger.info("🚀 Starting automated USL Instagram pipeline (UnfranchisedFC)...")
    logger.info("🔥 Ethos: Anti-corporate. Pro-community. Working-class megaphone.")
    
    output_dir = setup_output_directory()
    
    try:
        # Stage 1: Fetch Data
        logger.info("📊 Stage 1: Fetching USL data...")
        raw_data = fetch_usl_data()
        log_pipeline_state("data_fetch", raw_data, output_dir)
        
        # Stage 1b: Add accessibility metrics (inequality data for manifesto)
        if consolidate_accessibility_data:
            logger.info("📊 Stage 1b: Consolidating accessibility metrics...")
            accessibility_data = consolidate_accessibility_data()
            raw_data["accessibility_metrics"] = accessibility_data
            logger.info(f"✓ Added {len(accessibility_data.get('metrics', []))} inequality metrics")
        
        # Save raw data for reference
        with open(output_dir / "raw_data" / "raw_input.json", "w") as f:
            json.dump(raw_data, f, indent=2)
        logger.info("✓ Data fetched and saved")
        
        # Stage 1c: Filter content by ethos (prioritize culture clubs + street soccer)
        if filter_content_by_ethos:
            logger.info("🏘️ Stage 1c: Filtering content by UnfranchisedFC ethos...")
            content_item = {
                "club": raw_data.get("sources", {}).get("featured_club", ""),
                "title": raw_data.get("sources", {}).get("news", [{}])[0].get("title", ""),
                "body": raw_data.get("sources", {}).get("news", [{}])[0].get("description", "")
            }
            filtered_content = filter_content_by_ethos(content_item)
            raw_data["content_ethos"] = filtered_content
            logger.info(f"✓ Content filtered: {filtered_content.get('ethos', 'generic')} (priority: {filtered_content.get('priority')})")
        
        # Stage 2: Generate LLM-driven content (with manifesto ethos embedded)
        logger.info("📝 Stage 2: Generating copy via LLM (with UnfranchisedFC system prompt)...")
        llm_backend = os.getenv("LLM_BACKEND", "opencode")  # Default to free OpenCode Zen
        post_content = generate_post_content(raw_data, backend=llm_backend)
        log_pipeline_state("llm_format", post_content, output_dir)
        
        # Save LLM output
        with open(output_dir / "raw_data" / "llm_output.json", "w") as f:
            json.dump(post_content, f, indent=2)
        logger.info(f"✓ LLM generated content:\n  Voiceover: {post_content['voiceover'][:50]}...\n  Caption: {post_content['caption'][:50]}...")
        
        # Stage 3: Generate Audio
        logger.info("🎵 Stage 3: Generating audio...")
        # Choose audio strategy: raw chants (primary), protest soundtrack (secondary), or TTS (fallback)
        audio_strategy = os.getenv("AUDIO_STRATEGY", "raw_chants")  # Default to chants
        logger.info(f"   Using audio strategy: {audio_strategy}")
        
        audio_path = generate_audio(post_content["voiceover"], output_dir)
        logger.info(f"✓ Audio generated: {audio_path}")
        
        # Stage 4: Generate Video (with brutalist aesthetic)
        logger.info("🎬 Stage 4: Rendering video with brutalist aesthetic...")
        logger.info("   Applying: High contrast, film grain, punk-rock energy")
        video_path = generate_video(post_content, audio_path, output_dir, apply_brutalism=True)
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
        logger.info("🔥 UnfranchisedFC: Soccer from the streets. Pro/rel is justice.")
        
    except Exception as e:
        logger.error(f"❌ Pipeline failed at: {e}", exc_info=True)
        raise


if __name__ == "__main__":
    main()
