"""
Media generation module: Create audio (TTS) and video (Manim/MoviePy).

Stages:
1. Text-to-Speech: Convert voiceover script to MP3
2. Video rendering: Create visual component with on-screen text
3. Apply visual brutalism: Film grain, halftone, high contrast
4. Mix audio: Voiceover + Barrio y Rebeldía soundtrack or raw chants
5. Stitch: Merge audio and video

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

# Import visual style and audio strategy
try:
    from visual_style import UNFRANCHISED_STYLE, get_ffmpeg_filter_chain, get_color_palette_hex
except ImportError:
    logger.warning("visual_style module not found. Using default colors.")
    UNFRANCHISED_STYLE = None
    get_ffmpeg_filter_chain = None

try:
    from audio_strategy import AUDIO_OPTIONS, AUDIO_STYLE_GUIDE
except ImportError:
    logger.warning("audio_strategy module not found.")
    AUDIO_OPTIONS = None


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
    output_dir: Path,
    apply_brutalism: bool = True
) -> Path:
    """
    Generate video with on-screen text using MoviePy.
    
    Creates a UnfranchisedFC brutalist graphic:
    - Pure black or white background (high contrast)
    - Large, bold on-screen text
    - Applies visual brutalism (film grain, halftone, vignette)
    - Instagram Reel aspect ratio (9:16)
    
    Args:
        content: Dict with "on_screen_text" and "voiceover"
        audio_path: Path to generated audio
        output_dir: Output directory for video
        apply_brutalism: Whether to apply visual effects (default True)
    
    Returns:
        Path to generated MP4.
    """
    logger.info("🎬 Generating video with brutalist aesthetic...")
    
    try:
        # Get audio duration
        audio = AudioFileClip(str(audio_path))
        duration = audio.duration
        logger.info(f"Audio duration: {duration:.2f}s")
        
        # Get UnfranchisedFC color palette (black/white/red/yellow)
        colors_hex = get_color_palette_hex() if get_color_palette_hex else {
            "black": "#000000",
            "white": "#FFFFFF",
            "red": "#DC143C",
        }
        
        # Create background: Pure black (stark, dramatic)
        bg_color = (0, 0, 0)  # Black RGB
        background = ColorfulVideoClip(
            size=(1080, 1920),  # Instagram Reel: 9:16 vertical
            color=bg_color
        ).set_duration(duration)
        
        # Create text overlay with bold typography
        text = content["on_screen_text"]
        text_clip = TextClip(
            text,
            fontsize=90,
            color="white",
            font="Arial-Black",  # Heavy sans-serif
            method="caption",
            size=(900, 400)
        ).set_position("center").set_duration(duration)
        
        # Composite: background + text
        final_video = CompositeVideoClip([background, text_clip])
        
        # Set audio
        final_video = final_video.set_audio(audio)
        
        # Write output (without effects for now; we'll apply them with ffmpeg)
        output_path = output_dir / "video" / "final_video_raw.mp4"
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        logger.info(f"Writing raw video to {output_path}...")
        final_video.write_videofile(
            str(output_path),
            fps=30,
            codec="libx264",
            audio_codec="aac",
            preset="medium",
            verbose=False,
            logger=None
        )
        
        logger.info(f"✓ Raw video generated: {output_path}")
        
        # Apply visual brutalism using ffmpeg
        if apply_brutalism:
            final_path = apply_visual_brutalism(output_path, output_dir)
            logger.info(f"✓ Visual brutalism applied: {final_path}")
            return final_path
        
        return output_path
        
    except Exception as e:
        logger.error(f"Video generation failed: {e}")
        raise


def apply_visual_brutalism(raw_video_path: Path, output_dir: Path) -> Path:
    """
    Apply UnfranchisedFC visual brutalism to video:
    - Film grain overlay
    - Halftone effect (optional)
    - High contrast boost
    - Increased saturation
    - Vignette (darkened edges)
    
    Uses ffmpeg filter chain.
    
    Returns:
        Path to brutalism-applied video.
    """
    logger.info("🎨 Applying visual brutalism (film grain, contrast, vignette)...")
    
    output_path = output_dir / "video" / "final_video.mp4"
    output_path.parent.mkdir(parents=True, exist_ok=True)
    
    # FFmpeg filter chain for UnfranchisedFC aesthetic
    # eq=contrast=1.4: Boost contrast (make blacks blacker, whites whiter)
    # hue=s=1.2: Increase saturation (punchy colors)
    # noise=alls=0.04:allf=t: Add film grain
    # vignette=ratio=2:thickness=0.15: Darken edges
    filters = "eq=contrast=1.4,hue=s=1.2,noise=alls=0.04:allf=t,vignette=ratio=2:thickness=0.15"
    
    cmd = [
        "ffmpeg",
        "-i", str(raw_video_path),
        "-vf", filters,
        "-c:v", "libx264",
        "-crf", "18",  # Quality (lower = better)
        "-c:a", "aac",
        "-b:a", "128k",
        str(output_path),
        "-y"  # Overwrite
    ]
    
    try:
        logger.info(f"FFmpeg command: {' '.join(cmd[:5])}...")
        subprocess.run(cmd, check=True, capture_output=True)
        logger.info(f"✓ Brutalism applied: {output_path}")
        
        # Clean up raw video
        raw_video_path.unlink()
        
        return output_path
    except subprocess.CalledProcessError as e:
        logger.error(f"ffmpeg filter failed: {e}")
        raise


def get_color_palette_hex() -> Dict[str, str]:
    """Return UnfranchisedFC color palette in hex format."""
    return {
        "black": "#000000",
        "white": "#FFFFFF",
        "red": "#DC143C",
        "yellow": "#FFC800",
        "dark_gray": "#1E1E1E",
        "light_gray": "#C8C8C8"
    }


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
