"""
Configuration management for the FLIG pipeline.

Load settings from environment, YAML config files, or defaults.
"""

import os
from pathlib import Path
from typing import Dict, Any
import yaml
from loguru import logger

# Default configuration
DEFAULTS = {
    # Schedule
    "schedule_cron": "0 10 * * 2,4",  # Tuesday, Thursday at 10 AM UTC
    
    # LLM Settings
    "llm_model": "meta-llama/Llama-3-70b-chat-hf",
    "llm_temperature": 0.7,
    "llm_max_tokens": 512,
    
    # TTS Settings
    "tts_provider": "elevenlabs",
    "tts_voice_id": "21m00Tcm4TlvDq8ikWAM",  # Rachel
    
    # Video Settings
    "video_width": 1080,
    "video_height": 1920,  # 9:16 for Instagram Reels
    "video_fps": 30,
    "video_codec": "libx264",
    
    # Background color (RGB)
    "background_color": (25, 45, 85),  # Dark blue
    "text_color": "white",
    "text_fontsize": 80,
    "text_font": "Arial-Bold",
    
    # Output
    "output_dir": "./output",
    "keep_intermediate_files": False,  # Delete audio/video after merge
}


class Config:
    """Configuration manager for the pipeline."""
    
    def __init__(self, config_path: Path = None):
        """
        Initialize configuration from multiple sources.
        
        Priority order:
        1. Environment variables
        2. YAML config file
        3. Defaults
        """
        self.config = DEFAULTS.copy()
        
        # Load from YAML if provided
        if config_path and config_path.exists():
            self._load_from_yaml(config_path)
        
        # Override with environment variables
        self._load_from_env()
    
    def _load_from_yaml(self, path: Path):
        """Load configuration from YAML file."""
        try:
            with open(path) as f:
                yaml_config = yaml.safe_load(f) or {}
                self.config.update(yaml_config)
                logger.info(f"Loaded config from {path}")
        except Exception as e:
            logger.warning(f"Failed to load YAML config: {e}")
    
    def _load_from_env(self):
        """Load configuration from environment variables."""
        env_mappings = {
            "LLM_MODEL": "llm_model",
            "LLM_TEMPERATURE": ("llm_temperature", float),
            "TTS_PROVIDER": "tts_provider",
            "OUTPUT_DIR": "output_dir",
            "VIDEO_WIDTH": ("video_width", int),
            "VIDEO_HEIGHT": ("video_height", int),
            "VIDEO_FPS": ("video_fps", int),
        }
        
        for env_var, config_key in env_mappings.items():
            if isinstance(config_key, tuple):
                key, typ = config_key
                value = os.getenv(env_var)
                if value:
                    try:
                        self.config[key] = typ(value)
                    except ValueError:
                        logger.warning(f"Invalid {env_var}: {value}")
            else:
                value = os.getenv(env_var)
                if value:
                    self.config[config_key] = value
    
    def get(self, key: str, default=None) -> Any:
        """Get configuration value."""
        return self.config.get(key, default)
    
    def __getitem__(self, key: str) -> Any:
        """Dict-like access."""
        return self.config[key]
    
    def __repr__(self) -> str:
        """String representation (hide secrets)."""
        safe_config = {k: v for k, v in self.config.items() 
                      if "key" not in k.lower() and "password" not in k.lower()}
        return f"Config({safe_config})"


# Load default config on import
config = Config()


def reload_config(config_path: Path = None):
    """Reload configuration."""
    global config
    config = Config(config_path)
    logger.info("Configuration reloaded")
