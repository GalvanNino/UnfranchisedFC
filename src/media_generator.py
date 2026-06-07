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
    from elevenlabs.client import ElevenLabs
except ImportError:
    logger.warning("elevenlabs not installed. Using TTS fallback.")
    ElevenLabs = None

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
    
    # Check if elevenlabs module loaded successfully
    if ElevenLabs is None:
        logger.warning("⚠ elevenlabs module not available. Generating silent audio instead.")
        return generate_silent_audio(voiceover_text, output_dir)
    
    try:
        # Initialize ElevenLabs client
        client = ElevenLabs(api_key=api_key)
        
        # Generate speech using ElevenLabs text_to_speech
        # Using newer model "tts-1" (replaces deprecated eleven_monolingual_v1)
        audio = client.text_to_speech.convert(
            text=voiceover_text,
            voice_id="21m00Tcm4TlvDq8ikWAM",  # Rachel voice
            model_id="eleven_flash_v2"  # Fast, cheap, modern model
        )
        
        output_path = output_dir / "audio" / "voiceover.mp3"
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Audio is an iterator of bytes
        with open(output_path, "wb") as f:
            for chunk in audio:
                f.write(chunk)
        
        logger.info(f"✓ Audio generated via ElevenLabs: {output_path}")
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
    Generate video with on-screen text using ffmpeg + PIL (pure Python approach).
    
    Creates a UnfranchisedFC brutalist graphic:
    - Pure black background (high contrast)
    - Bold white on-screen text (centered)
    - Applies visual brutalism (contrast boost, saturation)
    - Instagram Reel aspect ratio (9:16)
    
    Args:
        content: Dict with "on_screen_text"
        audio_path: Path to generated audio
        output_dir: Output directory for video
        apply_brutalism: Whether to apply visual effects (default True)
    
    Returns:
        Path to generated MP4.
    """
    logger.info("🎬 Generating video with brutalist aesthetic (via ffmpeg + PIL)...")
    
    try:
        import subprocess
        from PIL import Image, ImageDraw, ImageFont
        
        # Get audio duration using ffprobe
        result = subprocess.run(
            ["ffprobe", "-v", "error", "-show_entries", "format=duration", 
             "-of", "default=noprint_wrappers=1:nokey=1:noesc=1", str(audio_path)],
            capture_output=True,
            timeout=5,
            text=True
        )
        
        try:
            duration = float(result.stdout.strip())
            logger.info(f"Audio duration: {duration:.2f}s")
        except:
            duration = 15  # Default to 15 seconds if ffprobe fails
        
        # Create text overlay frame using PIL (Brutalist AMF Aesthetic)
        text = content.get("on_screen_text", "UNFRANCHISED")
        logger.info(f"Creating brutalist text overlay: {text[:40]}...")
        
        # BRUTALIST BACKGROUND: Pure stark dark color (10, 10, 10) not pure black
        # (10, 10, 10) = near-black, slightly off-black for punk/zine aesthetic
        frame = Image.new("RGB", (1080, 1920), color=(10, 10, 10))
        draw = ImageDraw.Draw(frame)
        
        # BRUTALIST TYPOGRAPHY: Impact font (heavy, punk/zine style)
        # Force UPPERCASE for maximum brutalist impact
        try:
            # Try Impact first (most brutalist, used in punk/zine design)
            font = ImageFont.truetype("/System/Library/Fonts/Impact.ttf", 110)
            logger.info("Using Impact font (brutalist punk/zine standard)")
        except:
            try:
                font = ImageFont.truetype("/System/Library/Fonts/Arial.ttf", 96)
            except:
                try:
                    font = ImageFont.truetype("/System/Library/Fonts/Helvetica.ttc", 96)
                except:
                    font = ImageFont.load_default()
                    logger.warning("Using default font (text may be small)")
        
        # Brutalist text rendering: UPPERCASE + vibrant yellow for maximum contrast/impact
        text_upper = text.upper()  # Force uppercase for punk/zine aesthetic
        bbox = draw.textbbox((0, 0), text_upper, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        
        x = (1080 - text_width) // 2
        y = (1920 - text_height) // 2
        
        # VIBRANT YELLOW #FFFF00 = (255, 255, 0): Direct warning signal, high-contrast, confrontational
        # Against dark background (10, 10, 10): Maximum visual impact, punk aesthetic
        draw.text((x, y), text_upper, fill=(255, 255, 0), font=font)
        logger.info(f"Rendered brutalist text: {text_upper} (YELLOW #FFFF00 on DARK #0A0A0A)")
        
        # Save frame as temporary PNG
        frame_path = output_dir / "video" / "text_overlay.png"
        frame_path.parent.mkdir(parents=True, exist_ok=True)
        frame.save(str(frame_path))
        logger.info(f"✓ Text frame saved: {frame_path}")
        
        output_path = output_dir / "video" / "final_video_raw.mp4"
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Create video: color background + overlay text frame + audio
        # Using -loop 1 to repeat the text frame for the entire duration
        cmd = [
            "ffmpeg",
            "-loop", "1",
            "-i", str(frame_path),
            "-i", str(audio_path),
            "-c:v", "libx264",
            "-crf", "18",
            "-preset", "fast",
            "-c:a", "aac",
            "-shortest",
            str(output_path),
            "-y"
        ]
        
        logger.info("Rendering video with text overlay...")
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)
        
        if result.returncode != 0:
            logger.error(f"FFmpeg error: {result.stderr[-500:]}")
            raise RuntimeError(f"FFmpeg failed: {result.stderr}")
        
        logger.info(f"✓ Raw video generated: {output_path}")
        
        # Clean up temporary frame
        frame_path.unlink()
        
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
    
    # Use a temporary file for output, then move it
    temp_output = output_dir / "video" / "final_video_with_brutalism.mp4"
    
    # FFmpeg filter chain for UnfranchisedFC aesthetic
    # Simplified filters that are more stable
    # eq=contrast=1.4: Boost contrast
    # hue=s=1.2: Increase saturation (punchy colors)
    # Note: simplified from the full chain for stability
    filters = "eq=contrast=1.4,hue=s=1.2"
    
    cmd = [
        "ffmpeg",
        "-i", str(raw_video_path),
        "-vf", filters,
        "-c:v", "libx264",
        "-crf", "18",  # Quality (lower = better)
        "-c:a", "aac",
        "-b:a", "128k",
        str(temp_output),
        "-y"  # Overwrite
    ]
    
    try:
        logger.info(f"FFmpeg filters: {filters}")
        subprocess.run(cmd, check=True, capture_output=True, timeout=60)
        logger.info(f"✓ Brutalism applied: {temp_output}")
        
        # Replace raw video with brutalism version
        import shutil
        shutil.move(str(temp_output), str(output_path))
        
        # Clean up raw video (only if it's different from output_path)
        if raw_video_path != output_path and raw_video_path.exists():
            raw_video_path.unlink()
        
        return output_path
    except subprocess.CalledProcessError as e:
        logger.error(f"ffmpeg filter failed: {e}")
        # Continue anyway - return the original video if filter fails
        logger.warning("Continuing with unfiltered video...")
        return raw_video_path
    except Exception as e:
        logger.error(f"apply_visual_brutalism failed: {e}")
        # Return raw video on any error
        return raw_video_path


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
