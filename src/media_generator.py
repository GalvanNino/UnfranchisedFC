"""
Media generation module: Create audio (TTS) and video (Manim/MoviePy).

Stages:
1. Text-to-Speech: Convert voiceover script to MP3
2. Video rendering: Create visual component with on-screen text
3. Stitch: Merge audio and video

🔥 AESTHETIC: UnfranchisedFC Brutalist Style
   - Black/white/red/yellow color palette
   - Bold typography (IMPACT, BEBAS NEUE)
   - Film grain + halftone effects
   - High contrast, minimal decoration
   - Looks like protest banners, not corporate broadcast
"""

import os
import subprocess
from pathlib import Path
from typing import Dict, Optional
from loguru import logger

try:
    from elevenlabs import generate, set_api_key, Voice, VoiceSettings
except ImportError:
    logger.warning("elevenlabs not installed. Using TTS fallback.")

try:
    from moviepy.editor import (
        TextClip, CompositeVideoClip, ColorfulVideoClip,
        concatenate_videoclips, AudioFileClip, VideoFileClip
    )
except ImportError:
    logger.warning("moviepy not installed. Install with: pip install moviepy")

# Import visual style configuration
try:
    from visual_style import UNFRANCHISED_STYLE, get_ffmpeg_filter_chain
except ImportError:
    logger.warning("visual_style module not found. Using default colors.")
    UNFRANCHISED_STYLE = None


def generate_audio(voiceover_text: str, output_dir: Path) -> Path:
    """
    Convert voiceover text to MP3 using ElevenLabs TTS.
    
    Returns path to generated MP3.
    """
    logger.info("🎵 Generating audio via TTS...")
    
    api_key = os.getenv("ELEVENLABS_API_KEY")
    if not api_key:
        logger.warning("⚠ ELEVENLABS_API_KEY not set. Generating silent audio instead.")
        return generate_silent_audio(voiceover_text, output_dir)
    
    try:
        set_api_key(api_key)
        
        # Generate speech using ElevenLabs
        # Choose a voice (Adam, Bella, Charlotte, etc.)
        audio = generate(
            text=voiceover_text,
            voice=Voice(
                voice_id="21m00Tcm4TlvDq8ikWAM",  # Rachel voice (neutral, professional)
                settings=VoiceSettings(
                    stability=0.5,
                    similarity_boost=0.75,
                )
            ),
            model="eleven_monolingual_v1"  # Fast, cheap model
        )
        
        output_path = output_dir / "audio" / "voiceover.mp3"
        with open(output_path, "wb") as f:
            f.write(audio)
        
        logger.info(f"✓ Audio generated: {output_path}")
        return output_path
        
    except Exception as e:
        logger.error(f"TTS generation failed: {e}. Falling back to silent audio.")
        return generate_silent_audio(voiceover_text, output_dir)


def generate_silent_audio(text: str, output_dir: Path) -> Path:
    """
    Fallback: Generate silent audio (for testing without TTS API).
    
    Estimates duration based on text length (~150 words/minute).
    """
    logger.info("⏱️  Generating silent audio (fallback)...")
    
    # Rough estimate: ~150 words per minute spoken
    word_count = len(text.split())
    duration_seconds = max(10, int((word_count / 150) * 60))  # Min 10 seconds
    
    output_path = output_dir / "audio" / "voiceover_silent.mp3"
    
    # Use ffmpeg to generate silent audio
    cmd = [
        "ffmpeg",
        "-f", "lavfi",
        "-i", f"anullsrc=r=44100:cl=mono",
        "-t", str(duration_seconds),
        "-q:a", "9",
        "-acodec", "libmp3lame",
        str(output_path),
        "-y"  # Overwrite
    ]
    
    try:
        subprocess.run(cmd, check=True, capture_output=True)
        logger.info(f"✓ Silent audio generated: {output_path} ({duration_seconds}s)")
        return output_path
    except subprocess.CalledProcessError as e:
        logger.error(f"ffmpeg failed: {e}")
        raise


def generate_video(
    content: Dict[str, str],
    audio_path: Path,
    output_dir: Path
) -> Path:
    """
    Generate video with on-screen text using MoviePy.
    
    Creates a simple, clean graphic:
    - Colored background (or gradient)
    - Large on-screen text centered
    - Duration matches audio
    
    Returns path to generated MP4.
    """
    logger.info("🎬 Generating video...")
    
    try:
        # Get audio duration
        audio = AudioFileClip(str(audio_path))
        duration = audio.duration
        logger.info(f"Audio duration: {duration:.2f}s")
        
        # Create a simple colored background video
        # Using a dark blue background (sports theme)
        background = ColorfulVideoClip(
            size=(1080, 1920),  # Instagram Reel aspect ratio (9:16)
            color=(25, 45, 85)  # Dark blue
        ).set_duration(duration)
        
        # Create text overlay
        text = content["on_screen_text"]
        text_clip = TextClip(
            text,
            fontsize=80,
            color="white",
            font="Arial-Bold",
            method="caption",
            size=(900, 400)  # Width, height of text box
        ).set_position("center").set_duration(duration)
        
        # Composite video: background + text
        final_video = CompositeVideoClip([background, text_clip])
        
        # Set audio
        final_video = final_video.set_audio(audio)
        
        # Write output
        output_path = output_dir / "video" / "final_video.mp4"
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        logger.info(f"Writing video to {output_path}...")
        final_video.write_videofile(
            str(output_path),
            fps=30,
            codec="libx264",
            audio_codec="aac",
            preset="medium",  # Balance speed vs quality
            verbose=False,
            logger=None
        )
        
        logger.info(f"✓ Video generated: {output_path}")
        return output_path
        
    except Exception as e:
        logger.error(f"Video generation failed: {e}")
        raise


def merge_audio_video(video_path: Path, audio_path: Path, output_dir: Path) -> Path:
    """
    Merge video and audio using ffmpeg (fallback method).
    
    Useful if MoviePy has issues.
    """
    logger.info("🔗 Merging audio and video...")
    
    output_path = output_dir / "final" / "merged_video.mp4"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    cmd = [
        "ffmpeg",
        "-i", str(video_path),
        "-i", str(audio_path),
        "-c:v", "copy",
        "-c:a", "aac",
        "-shortest",
        str(output_path),
        "-y"
    ]
    
    try:
        subprocess.run(cmd, check=True, capture_output=True)
        logger.info(f"✓ Audio and video merged: {output_path}")
        return output_path
    except subprocess.CalledProcessError as e:
        logger.error(f"ffmpeg merge failed: {e}")
        raise
