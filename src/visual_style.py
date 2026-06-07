"""
UnfranchisedFC Visual Style Guide

Brutalist, punk-rock aesthetic for a manifesto, not a corporate broadcast.

Color Palette: Black, white, red, yellow (like protest banners)
Typography: Bold, heavy sans-serif (impact, bebas neue)
Texture: Film grain, halftone (printed, not digital)
Layout: Asymmetrical, dense, urgent
"""

from dataclasses import dataclass
from typing import Tuple


@dataclass
class ColorPalette:
    """UnfranchisedFC color scheme"""
    
    # Primary colors (protest banner energy)
    black: Tuple[int, int, int] = (0, 0, 0)
    white: Tuple[int, int, int] = (255, 255, 255)
    red: Tuple[int, int, int] = (220, 20, 60)        # Crimson red
    yellow: Tuple[int, int, int] = (255, 200, 0)     # Bold yellow
    
    # Accent colors (high contrast)
    dark_gray: Tuple[int, int, int] = (30, 30, 30)
    light_gray: Tuple[int, int, int] = (200, 200, 200)
    
    def to_dict(self):
        return {
            "black": self.black,
            "white": self.white,
            "red": self.red,
            "yellow": self.yellow,
            "dark_gray": self.dark_gray,
            "light_gray": self.light_gray
        }


@dataclass
class Typography:
    """UnfranchisedFC fonts"""
    
    # Headline: Bold, blocky, punk energy
    headline_font: str = "Impact"  # Or BEBAS NEUE
    headline_weight: int = 900
    headline_size: int = 72
    
    # Body: Monospace, raw, manifesto feel
    body_font: str = "Courier New"  # Or INCONSOLATA
    body_weight: int = 400
    body_size: int = 24
    
    # Accent: Heavy sans-serif
    accent_font: str = "Arial Black"
    accent_weight: int = 900
    accent_size: int = 48


@dataclass
class VisualEffects:
    """Post-processing effects"""
    
    # Film grain overlay
    film_grain_enabled: bool = True
    film_grain_intensity: float = 0.15  # 0-1, subtle to harsh
    
    # Halftone effect (like punk zines)
    halftone_enabled: bool = True
    halftone_dot_size: int = 3
    halftone_angle: float = 45.0
    
    # High contrast (no soft shadows)
    contrast_boost: float = 1.4  # 1.0 = normal, >1.0 = increased
    
    # Saturation (punchy colors)
    saturation: float = 1.2  # 1.0 = normal, >1.0 = more vibrant
    
    # Vignette (edges darken)
    vignette_enabled: bool = True
    vignette_intensity: float = 0.2


@dataclass
class Layout:
    """Layout principles"""
    
    # Asymmetrical, not corporate grid
    symmetry: str = "asymmetrical"
    
    # Dense typography (crowded, urgent)
    text_density: str = "high"
    
    # Minimal decoration (data is the art)
    decoration: str = "minimal"
    
    # Left-aligned (not centered, feels raw)
    text_alignment: str = "left"
    
    # High-contrast backgrounds
    background: str = "pure_black_or_pure_white"
    
    # Line spacing: tight
    line_spacing: float = 1.1


# Global style config
UNFRANCHISED_STYLE = {
    "name": "UnfranchisedFC Brutalist",
    "inspired_by": ["FC St. Pauli", "punk zines", "protest banners", "communist posters"],
    "philosophy": "Cold data. Hot manifesto. Printed, not digital.",
    
    "colors": ColorPalette().to_dict(),
    
    "fonts": {
        "headline": {"font": "Impact", "weight": 900, "size": 72},
        "body": {"font": "Courier New", "weight": 400, "size": 24},
        "accent": {"font": "Arial Black", "weight": 900, "size": 48}
    },
    
    "effects": {
        "film_grain": {"enabled": True, "intensity": 0.15},
        "halftone": {"enabled": True, "dot_size": 3, "angle": 45},
        "contrast": 1.4,
        "saturation": 1.2,
        "vignette": {"enabled": True, "intensity": 0.2}
    },
    
    "layout": {
        "symmetry": "asymmetrical",
        "text_density": "high",
        "background": "stark (black or white)",
        "alignment": "left",
        "spacing": "tight"
    }
}


def apply_film_grain(image_array, intensity: float = 0.15):
    """
    Apply film grain overlay to image.
    
    Use in ffmpeg or PIL post-processing.
    """
    # Pseudo-code for PIL:
    # import numpy as np
    # grain = np.random.normal(0, intensity * 255, image_array.shape)
    # return image_array + grain
    
    return f"Apply Gaussian noise: sigma={intensity * 255}"


def apply_halftone(image_array, dot_size: int = 3):
    """
    Apply halftone effect (like comic book or punk zine).
    
    Use in PIL or ffmpeg with custom filter.
    """
    # PIL: ImageOps.posterize() + custom dot pattern
    return f"Apply halftone with dot size: {dot_size}px"


def get_ffmpeg_filter_chain() -> str:
    """
    Complete ffmpeg filter chain for UnfranchisedFC aesthetic.
    
    Chain: input → contrast → saturation → film_grain → vignette → output
    """
    filters = [
        # Boost contrast
        "eq=contrast=1.4",
        
        # Increase saturation
        "hue=s=1.2",
        
        # Add film grain (using noise filter)
        "noise=alls=0.04:allf=t",
        
        # Add vignette
        "vignette=angle=PI/4:ratio=2:thickness=0.15",
    ]
    
    return ",".join(filters)


def get_ffmpeg_command_example():
    """
    Example ffmpeg command for UnfranchisedFC style:
    
    Input: Raw video (16:9, 1080p)
    Output: Instagram Reel with brutalist aesthetic
    """
    return """
ffmpeg -i input.mp4 \
  -vf "eq=contrast=1.4,hue=s=1.2,noise=alls=0.04:allf=t,vignette=ratio=2:thickness=0.15" \
  -c:v libx264 -crf 18 -c:a aac -b:a 128k \
  output.mp4
"""


def get_manim_style_config():
    """
    Configuration for Manim-based animations (if using for data viz).
    
    Color palette: black background, white/red text, minimal decoration.
    """
    return {
        "background_color": "#000000",  # Pure black
        "text_color": "#FFFFFF",        # Pure white
        "accent_color": "#DC143C",      # Crimson red
        "highlight_color": "#FFC800",   # Bold yellow
        
        "font": "Impact",
        "font_size": 96,
        
        "frame_rate": 30,
        "resolution": "1080p",
        "pixel_height": 1080,
        "pixel_width": 1920,
        
        # Animation style: quick, punchy (not flowing)
        "animation_duration": 0.5,  # Shorter animations
        "stroke_width": 4,  # Bold lines
    }


def get_color_palette_hex():
    """Return color palette in hex format for web/design"""
    return {
        "black": "#000000",
        "white": "#FFFFFF",
        "red": "#DC143C",
        "yellow": "#FFC800",
        "dark_gray": "#1E1E1E",
        "light_gray": "#C8C8C8"
    }


if __name__ == "__main__":
    import json
    
    print("=== UnfranchisedFC Visual Style ===\n")
    print(json.dumps(UNFRANCHISED_STYLE, indent=2, default=str))
    
    print("\n=== FFmpeg Filter Chain ===\n")
    print(get_ffmpeg_filter_chain())
    
    print("\n=== Color Palette (Hex) ===\n")
    print(json.dumps(get_color_palette_hex(), indent=2))
