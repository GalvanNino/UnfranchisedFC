"""
Data fetching module: Comprehensive data architecture for UnfranchisedFC.

Sources:
1. LIVE MATCH DATA
   - API-Football (Sportmonks) - Live standings, results
   - Wikipedia API - Stadium capacity, club info

2. NARRATIVE & CULTURE
   - Reddit API (PRAW) - r/USLPRO, r/MLS sentiment
   
3. STATIC CONTEXT DATA
   - base_camps.json - World Cup 2026 base camps
   
4. NEWS & UPDATES
   - RSS feeds - USL official, team news
   - Twitter/X feeds - Breaking updates
"""

import os
import requests
import json
from datetime import datetime
from loguru import logger
from typing import Dict, Any, List, Optional
from pathlib import Path

try:
    import feedparser
except ImportError:
    feedparser = None
    logger.warning("feedparser not installed. RSS feeds will be skipped.")

try:
    import praw
except ImportError:
    praw = None
    logger.warning("praw not installed. Reddit sentiment will be skipped.")


def fetch_from_api_sports() -> Dict[str, Any]:
    """
    Fetch USL standings from API-Football or Sportmonks.
    
    Supports:
    - API-Football (rapid-api): https://rapidapi.com/api-sports/api/api-football
    - Sportmonks: https://www.sportmonks.com/
    
    Both provide live standings, recent results, and team statistics.
    """
    try:
        logger.info("📡 Fetching from API-Football...")
        
        api_key = os.getenv("API_FOOTBALL_KEY")
        if not api_key:
            logger.warning("⚠ API_FOOTBALL_KEY not set. Skipping live standings.")
            return {}
        
        # Example: USL Championship 2026
        # League ID varies by API - check your API docs for USL Championship ID
        url = "https://api-football-v1.p.rapidapi.com/v3/standings"
        params = {
            "league": 248,  # USL Championship (verify ID with your API)
            "season": 2026
        }
        headers = {
            "X-RapidAPI-Key": api_key,
            "X-RapidAPI-Host": "api-football-v1.p.rapidapi.com"
        }
        
        response = requests.get(url, headers=headers, params=params, timeout=10)
        response.raise_for_status()
        
        standings = response.json()
        logger.info(f"✓ Fetched standings for {len(standings.get('response', []))} groups")
        return standings
        
    except Exception as e:
        logger.error(f"API-Football failed: {e}")
        return {}


def fetch_wikipedia_club_data(club_name: str) -> Dict[str, Any]:
    """
    Fetch club data from Wikipedia API for stadium capacity and eligibility checks.
    
    For Pro/Rel content: Verify if clubs meet USL Premier requirements:
    - 15,000+ seat stadium
    - $70M+ ownership net worth
    
    Args:
        club_name: e.g., "Sacramento Republic FC"
    
    Returns:
        Club data including stadium capacity, location, ownership info
    """
    try:
        logger.info(f"🏟️  Fetching Wikipedia data for {club_name}...")
        
        url = "https://en.wikipedia.org/w/api.php"
        params = {
            "action": "query",
            "titles": club_name,
            "prop": "extracts",
            "explaintext": True,
            "format": "json"
        }
        
        response = requests.get(url, params=params, timeout=10)
        response.raise_for_status()
        
        data = response.json()
        pages = data.get("query", {}).get("pages", {})
        
        # Extract text
        for page_id, page_data in pages.items():
            extract = page_data.get("extract", "")
            
            # Parse for key metrics (basic extraction)
            club_info = {
                "club_name": club_name,
                "wikipedia_summary": extract[:300],  # First 300 chars
                "timestamp": datetime.now().isoformat()
            }
            
            # Look for stadium capacity in text (basic pattern matching)
            if "stadium" in extract.lower():
                logger.info(f"  Found stadium info for {club_name}")
            
            return club_info
        
        return {}
        
    except Exception as e:
        logger.error(f"Wikipedia fetch failed for {club_name}: {e}")
        return {}


def fetch_reddit_sentiment() -> List[Dict[str, Any]]:
    """
    Fetch top weekly posts from r/USLPRO and r/MLS for cultural sentiment.
    
    Uses PRAW (Python Reddit API Wrapper).
    Requires Reddit OAuth credentials.
    
    This data helps the LLM adopt authentic fan voice and tone.
    """
    if not praw:
        logger.warning("⚠ praw not installed. Skipping Reddit sentiment.")
        return []
    
    try:
        logger.info("🔴 Fetching Reddit sentiment from r/USLPRO...")
        
        reddit = praw.Reddit(
            client_id=os.getenv("REDDIT_CLIENT_ID"),
            client_secret=os.getenv("REDDIT_CLIENT_SECRET"),
            user_agent=os.getenv("REDDIT_USER_AGENT", "UnfranchisedFC/1.0"),
        )
        
        posts = []
        
        for subreddit_name in ["USLPRO", "MLS"]:
            subreddit = reddit.subreddit(subreddit_name)
            
            # Get top posts from the week
            for post in subreddit.top(time_filter="week", limit=5):
                posts.append({
                    "subreddit": subreddit_name,
                    "title": post.title,
                    "score": post.score,
                    "url": post.url,
                    "comments_sample": [
                        {"text": c.body, "score": c.score}
                        for c in post.comments[:3]  # Top 3 comments
                    ],
                    "timestamp": datetime.fromtimestamp(post.created_utc).isoformat()
                })
        
        logger.info(f"✓ Fetched {len(posts)} posts from Reddit")
        return posts
        
    except Exception as e:
        logger.error(f"Reddit fetch failed: {e}")
        logger.info("  (Ensure REDDIT_CLIENT_ID, REDDIT_CLIENT_SECRET are set)")
        return []


def fetch_rss_feeds() -> List[Dict[str, Any]]:
    """
    Fetch latest news from USL and team RSS feeds.
    
    Feeds include:
    - USL Official news
    - Individual club RSS feeds
    - Soccer journalism sites
    """
    if not feedparser:
        logger.warning("⚠ feedparser not installed. Skipping RSS feeds.")
        return []
    
    try:
        logger.info("📰 Fetching RSS feeds...")
        
        rss_urls = [
            {"name": "USL Official", "url": "https://www.uslchampionship.com/feed"},
            {"name": "Pittsburgh Riverhounds", "url": "https://www.riverhoundssoccer.com/feed"},
            {"name": "Detroit City FC", "url": "https://www.detcityfc.com/feed"},
            {"name": "Sacramento Republic", "url": "https://www.sacrepublicfc.com/feed"},
            {"name": "Soccer.com News", "url": "https://www.soccer.com/feed"},
            # Add more as needed
        ]
        
        all_items = []
        
        for feed_info in rss_urls:
            try:
                feed = feedparser.parse(feed_info["url"])
                
                for entry in feed.entries[:3]:  # Top 3 items per feed
                    all_items.append({
                        "source": feed_info["name"],
                        "title": entry.get("title", ""),
                        "link": entry.get("link", ""),
                        "summary": entry.get("summary", "")[:200],
                        "published": entry.get("published", ""),
                    })
                
                logger.info(f"  ✓ {feed_info['name']}")
                
            except Exception as e:
                logger.warning(f"  ✗ {feed_info['name']}: {e}")
        
        logger.info(f"✓ Fetched {len(all_items)} RSS items")
        return all_items
        
    except Exception as e:
        logger.error(f"RSS fetch failed: {e}")
        return []


def load_base_camps() -> Dict[str, Any]:
    """
    Load static World Cup 2026 base camp data.
    
    This connects global superpowers (Argentina, Spain, Brazil, etc.)
    to local USL Championship clubs, enabling narrative bridges.
    """
    try:
        logger.info("🏕️  Loading World Cup base camps...")
        
        base_camps_path = Path(__file__).parent.parent / "data" / "base_camps.json"
        
        if not base_camps_path.exists():
            logger.warning(f"base_camps.json not found at {base_camps_path}")
            return {}
        
        with open(base_camps_path) as f:
            data = json.load(f)
        
        logger.info(f"✓ Loaded {len(data.get('2026_world_cup_base_camps', {}).get('base_camps', []))} base camps")
        return data
        
    except Exception as e:
        logger.error(f"Failed to load base camps: {e}")
        return {}


def fetch_from_twitter_accounts(handles: List[str] = None) -> List[Dict[str, Any]]:
    """
    Fetch recent tweets from USL-related accounts.
    
    Requires Twitter API v2 credentials (Bearer token).
    
    Default handles include:
    - Official accounts: @USLChampionship, @USLLeagueOne, @USLLeagueTwo
    - Analyst accounts: @BackHeeledUSL, @USLRdio, @USLTactics
    - Commentary: @11Yanks, @TotalSoccerShow, @TheUSLShow
    - Team/player accounts and regional soccer coverage
    """
    if handles is None:
        handles = [
            # Official USL accounts
            "USLChampionship",
            "USLLeagueOne",
            "USLLeagueTwo",
            "UPSL",
            
            # Analysis & Tactical
            "BackHeeledUSL",
            "USLTactics",
            "ManagerTactical",
            "USLL1Review",
            
            # Podcasts & Shows
            "USLRdio",
            "TheUSLShow",
            "TotalSoccerShow",
            "11Yanks",
            
            # US Soccer Coverage
            "USMNT",
            "usmnonly",
            "ProtagonistUSA",
            "joeclowery",
            
            # Journalists & Analysts
            "grahamruthven",
            "jeffrueter",
            "ByDougMcIntyre",
            "BrianSciaretta",
            "WillParchman",
            
            # Team accounts
            "AkronCityFC",
            "ChattanoogaFC",
            "LexSporting",
            "mplscitysc",
            "dallastrinityfc",
            "GainbridgeSL",
            "atleticodallas",
            "ForwardMSNFC",
            
            # Regional/League Coverage
            "BigDSoccer",
            "PrepSoccerTX",
            "ESPNFC",
            "MASLarena",
            
            # Youth/Academy
            "LouCityAcademy",
        ]
    
    try:
        logger.info("🐦 Fetching from Twitter accounts...")
        
        bearer_token = os.getenv("TWITTER_BEARER_TOKEN")
        if not bearer_token:
            logger.warning("⚠ TWITTER_BEARER_TOKEN not set. Skipping Twitter data.")
            return []
        
        tweets = []
        headers = {"Authorization": f"Bearer {bearer_token}"}
        
        for handle in handles:
            url = f"https://api.twitter.com/2/tweets/search/recent?query=from:{handle}"
            params = {
                "max_results": 10,
                "tweet.fields": "created_at,public_metrics",
                "expansions": "author_id",
                "user.fields": "username"
            }
            
            response = requests.get(url, headers=headers, params=params)
            if response.status_code == 200:
                tweets.extend(response.json().get("data", []))
            else:
                logger.warning(f"Failed to fetch tweets from {handle}: {response.status_code}")
        
        return tweets
        
    except Exception as e:
        logger.error(f"Failed to fetch Twitter data: {e}")
        return []


def fetch_news_feeds() -> List[Dict[str, Any]]:
    """
    Fetch recent news about USL.
    
    Can use NewsAPI or RSS feeds.
    """
    try:
        logger.info("📰 Fetching news feeds...")
        
        # Example using NewsAPI
        api_key = os.getenv("NEWS_API_KEY")
        if not api_key:
            logger.warning("⚠ NEWS_API_KEY not set. Skipping news.")
            return []
        
        url = "https://newsapi.org/v2/everything"
        params = {
            "q": "USL Championship",
            "sortBy": "publishedAt",
            "language": "en",
            "pageSize": 10,
            "apiKey": api_key
        }
        
        response = requests.get(url, params=params)
        if response.status_code == 200:
            articles = response.json().get("articles", [])
            return articles[:5]  # Top 5 articles
        
        return []
        
    except Exception as e:
        logger.error(f"Failed to fetch news: {e}")
        return []


def consolidate_data() -> Dict[str, Any]:
    """
    Consolidate all data sources into a single structured object.
    
    This is the data foundation for the LLM and animation engine.
    """
    consolidated = {
        "timestamp": datetime.now().isoformat(),
        "sources": {
            # Live API data
            "api_sports": fetch_from_api_sports(),
            
            # Club eligibility & stadium data
            "club_data": {
                club: fetch_wikipedia_club_data(club)
                for club in [
                    "Sacramento Republic FC",
                    "San Diego Loyal",
                    "Chattanooga FC",
                    "Detroit City FC",
                    "Pittsburgh Riverhounds SC"
                ]
            },
            
            # Cultural sentiment
            "reddit_sentiment": fetch_reddit_sentiment(),
            
            # News & updates
            "rss_feeds": fetch_rss_feeds(),
            
            # Static context (World Cup base camps)
            "world_cup_base_camps": load_base_camps(),
            
            # Twitter/X feeds (from previous implementation)
            "twitter": fetch_from_twitter_accounts(),
        }
    }
    return consolidated


def fetch_usl_data() -> Dict[str, Any]:
    """
    Main entry point: fetch all USL data.
    
    Returns a consolidated dictionary with all available data.
    """
    logger.info("🔄 Starting data aggregation...")
    
    data = consolidate_data()
    
    logger.info(f"✓ Data aggregation complete. Sources processed: {len(data['sources'])}")
    
    return data
