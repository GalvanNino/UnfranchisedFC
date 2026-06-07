"""
Instagram posting module: Upload video + caption to Instagram.

Uses instagrapi (Unofficial Instagram API wrapper).

Security: Credentials should be stored as GitHub secrets.
Two options:
1. Business Account with Meta Graph API (official, but complex setup)
2. instagrapi with personal/test account (simple, but against TOS)

For production, use Meta Graph API.
"""

import os
from pathlib import Path
from typing import Optional
from loguru import logger

try:
    from instagrapi import Client
except ImportError:
    logger.warning("instagrapi not installed. Skipping Instagram posting.")
    Client = None


def post_to_instagram(video_path: Path, caption: str) -> Optional[str]:
    """
    Upload a video reel to Instagram.
    
    Args:
        video_path: Path to the MP4 video file
        caption: Caption text for the post
    
    Returns:
        Media ID if successful, None otherwise.
    """
    
    if not Client:
        logger.error("instagrapi not available. Cannot post to Instagram.")
        return None
    
    logger.info("📱 Posting to Instagram...")
    
    # Get credentials from environment
    username = os.getenv("INSTAGRAM_USERNAME")
    password = os.getenv("INSTAGRAM_PASSWORD")
    
    if not username or not password:
        logger.error("❌ INSTAGRAM_USERNAME or INSTAGRAM_PASSWORD not set")
        return None
    
    # Validate video exists
    if not Path(video_path).exists():
        logger.error(f"Video file not found: {video_path}")
        return None
    
    try:
        # Initialize Instagram client
        client = Client()
        logger.info(f"Logging in as {username}...")
        client.login(username, password)
        
        # Upload video as a Reel
        logger.info("Uploading video...")
        
        # For Reels (short videos), use clip_upload
        response = client.clip_upload(
            video_path=str(video_path),
            caption=caption,
            # Optional: add thumbnail, music, effects, etc.
        )
        
        media_id = response.pk if hasattr(response, 'pk') else response.id
        logger.info(f"✓ Successfully posted! Media ID: {media_id}")
        
        # Logout
        client.logout()
        
        return media_id
        
    except Exception as e:
        logger.error(f"❌ Failed to post to Instagram: {e}")
        logger.info("Troubleshooting tips:")
        logger.info("  - Check INSTAGRAM_USERNAME and INSTAGRAM_PASSWORD are correct")
        logger.info("  - Account may require 2FA (may need app password)")
        logger.info("  - Try logging in manually first to ensure account is accessible")
        logger.info("  - Consider using Meta Graph API for production (official method)")
        return None


def post_via_meta_graph_api(video_path: Path, caption: str) -> Optional[str]:
    """
    Official method: Post via Meta Graph API.
    
    Requires:
    - Instagram Business Account
    - Facebook App with Instagram Graph API access
    - Access Token
    
    This is more complex but official and reliable.
    """
    import requests
    
    logger.info("📱 Posting via Meta Graph API (official)...")
    
    access_token = os.getenv("META_ACCESS_TOKEN")
    ig_business_account_id = os.getenv("IG_BUSINESS_ACCOUNT_ID")
    
    if not access_token or not ig_business_account_id:
        logger.error("META_ACCESS_TOKEN or IG_BUSINESS_ACCOUNT_ID not set")
        return None
    
    try:
        # Step 1: Upload media container
        url = f"https://graph.instagram.com/v18.0/{ig_business_account_id}/media"
        
        with open(video_path, "rb") as f:
            files = {"video_data": f}
            data = {
                "media_type": "REELS",
                "caption": caption,
                "access_token": access_token
            }
            
            response = requests.post(url, files=files, data=data)
        
        if response.status_code != 200:
            logger.error(f"Media upload failed: {response.json()}")
            return None
        
        media_id = response.json()["id"]
        logger.info(f"✓ Media uploaded: {media_id}")
        
        # Step 2: Publish media
        publish_url = f"https://graph.instagram.com/v18.0/{ig_business_account_id}/media_publish"
        publish_data = {
            "creation_id": media_id,
            "access_token": access_token
        }
        
        publish_response = requests.post(publish_url, json=publish_data)
        
        if publish_response.status_code == 200:
            logger.info("✓ Successfully published via Meta Graph API!")
            return media_id
        else:
            logger.error(f"Publishing failed: {publish_response.json()}")
            return None
            
    except Exception as e:
        logger.error(f"Meta Graph API posting failed: {e}")
        return None


def test_instagram_connection() -> bool:
    """
    Test Instagram credentials without posting.
    """
    if not Client:
        logger.warning("instagrapi not available")
        return False
    
    username = os.getenv("INSTAGRAM_USERNAME")
    password = os.getenv("INSTAGRAM_PASSWORD")
    
    if not username or not password:
        logger.error("Credentials not set")
        return False
    
    try:
        client = Client()
        client.login(username, password)
        user = client.account_info()
        logger.info(f"✓ Successfully logged in as {user.full_name} (@{user.username})")
        client.logout()
        return True
    except Exception as e:
        logger.error(f"Connection test failed: {e}")
        return False
