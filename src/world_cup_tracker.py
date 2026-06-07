"""
World Cup & International Tracker

Integrates international play data into the UnfranchisedFC pipeline:
- Live USMNT/MXMNT World Cup matches
- Cross-reference with USL players
- Global transfer market tracking
- Player development narrative
"""

import os
import json
import requests
from datetime import datetime
from pathlib import Path
from typing import Dict, Any, List, Optional
from loguru import logger


def fetch_world_cup_matches(team_ids: List[int] = None) -> List[Dict[str, Any]]:
    """
    Fetch live World Cup matches for specific teams (USMNT, MXMNT, etc).
    
    Uses API-Football or Sportmonks international endpoints.
    
    Args:
        team_ids: List of team IDs (e.g., [1, 84] for USA, Mexico)
    
    Returns:
        List of match data with scores, goalscorers, possession stats
    """
    if team_ids is None:
        # Default: USMNT (1) and Mexico (84) - adjust based on API
        team_ids = [1, 84]
    
    try:
        logger.info("🌍 Fetching World Cup matches...")
        
        api_key = os.getenv("API_FOOTBALL_KEY")
        if not api_key:
            logger.warning("⚠ API_FOOTBALL_KEY not set. Skipping World Cup matches.")
            return []
        
        # World Cup 2026 league ID (varies by API - check documentation)
        # Example: Sportmonks uses 25 for World Cup
        url = "https://api-football-v1.p.rapidapi.com/v3/fixtures"
        
        all_matches = []
        
        for team_id in team_ids:
            params = {
                "league": 25,  # World Cup 2026
                "team": team_id,
                "last": 10  # Last 10 matches for this team
            }
            headers = {
                "X-RapidAPI-Key": api_key,
                "X-RapidAPI-Host": "api-football-v1.p.rapidapi.com"
            }
            
            response = requests.get(url, headers=headers, params=params, timeout=10)
            response.raise_for_status()
            
            matches = response.json().get("response", [])
            all_matches.extend(matches)
            logger.info(f"✓ Fetched {len(matches)} matches")
        
        return all_matches
        
    except Exception as e:
        logger.error(f"World Cup match fetch failed: {e}")
        return []


def load_usl_world_cup_players() -> Dict[str, Any]:
    """
    Load USL players competing in World Cup 2026.
    
    This enables cross-referencing: when a match happens, check if any
    participating players are on this list. If yes, generate a content hook.
    """
    try:
        logger.info("🌟 Loading USL-to-World Cup player list...")
        
        players_path = Path(__file__).parent.parent / "data" / "usl_world_cup_players.json"
        
        if not players_path.exists():
            logger.warning(f"usl_world_cup_players.json not found")
            return {}
        
        with open(players_path) as f:
            data = json.load(f)
        
        player_count = len(data.get("usl_players_world_cup_2026", {}).get("players", []))
        logger.info(f"✓ Loaded {player_count} USL players in World Cup")
        return data
        
    except Exception as e:
        logger.error(f"Failed to load USL World Cup players: {e}")
        return {}


def cross_reference_usl_players(match_data: Dict[str, Any], usl_players: Dict[str, Any]) -> Optional[Dict[str, Any]]:
    """
    Check if a match involves any USL-connected players.
    
    Args:
        match_data: Match data from API (includes lineups)
        usl_players: Loaded USL player data
    
    Returns:
        Content hook if USL player found, None otherwise
    """
    try:
        match_teams = match_data.get("teams", {})
        home_team = match_teams.get("home", {}).get("id")
        away_team = match_teams.get("away", {}).get("id")
        
        # Get player list from JSON
        players = usl_players.get("usl_players_world_cup_2026", {}).get("players", [])
        
        # Check each player's national team
        for player in players:
            if player.get("world_cup_squad"):
                # This would need actual team ID from API
                # Simplified for demo
                player_info = {
                    "player_name": player.get("name"),
                    "national_team": player.get("national_team"),
                    "usl_club": player.get("usl_club"),
                    "position": player.get("position"),
                    "narrative": player.get("narrative"),
                    "usl_stats": player.get("usl_stats")
                }
                
                # Return on first match (in real implementation, check actual lineups)
                return player_info
        
        return None
        
    except Exception as e:
        logger.error(f"Cross-reference failed: {e}")
        return None


def load_transfer_data() -> Dict[str, Any]:
    """
    Load global transfer market data.
    
    Tracks player movements between USL, MLS, and European clubs.
    Generates narrative hooks around:
    - Youth-to-Europe transfers (bypassing MLS)
    - International veterans joining USL
    - Academy graduates signing pro contracts
    """
    try:
        logger.info("🔄 Loading transfer data...")
        
        transfers_path = Path(__file__).parent.parent / "data" / "transfers.json"
        
        if not transfers_path.exists():
            logger.warning("transfers.json not found")
            return {}
        
        with open(transfers_path) as f:
            data = json.load(f)
        
        transfer_count = len(data.get("recent_transfers", {}).get("2025-2026_season", []))
        logger.info(f"✓ Loaded {transfer_count} transfers")
        return data
        
    except Exception as e:
        logger.error(f"Failed to load transfer data: {e}")
        return {}


def detect_transfer_alerts(transfers: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    Scan transfers for content-worthy alerts.
    
    Examples:
    - Player under 22 moving to Europe
    - Transfer fee over $500k
    - International player joining USL
    
    Returns:
        List of transfer alerts suitable for LLM prompts
    """
    try:
        logger.info("🚨 Detecting transfer alerts...")
        
        alerts = []
        recent = transfers.get("recent_transfers", {}).get("2025-2026_season", [])
        
        for transfer in recent:
            alert = None
            
            # Youth to Europe
            if transfer.get("age_at_transfer", 0) < 22 and "European" in transfer.get("to_league", ""):
                alert = {
                    "type": "youth_to_europe",
                    "player": transfer.get("player_name"),
                    "age": transfer.get("age_at_transfer"),
                    "from": transfer.get("from_club"),
                    "to": transfer.get("to_club"),
                    "narrative": transfer.get("pro_rel_narrative")
                }
            
            # High-value transfer
            elif transfer.get("transfer_fee") and "$" in transfer.get("transfer_fee", ""):
                alert = {
                    "type": "high_value",
                    "player": transfer.get("player_name"),
                    "fee": transfer.get("transfer_fee"),
                    "narrative": transfer.get("pro_rel_narrative")
                }
            
            # International to USL
            elif "USL" in transfer.get("to_league", ""):
                alert = {
                    "type": "international_to_usl",
                    "player": transfer.get("player_name"),
                    "from": transfer.get("from_club"),
                    "to": transfer.get("to_club"),
                    "narrative": transfer.get("pro_rel_narrative")
                }
            
            if alert:
                alerts.append(alert)
        
        logger.info(f"✓ Detected {len(alerts)} transfer alerts")
        return alerts
        
    except Exception as e:
        logger.error(f"Transfer alert detection failed: {e}")
        return []


def generate_world_cup_context(match_data: Dict[str, Any], usl_player: Optional[Dict[str, Any]]) -> str:
    """
    Generate LLM context for World Cup match with USL connection.
    
    Args:
        match_data: Match result data
        usl_player: USL player involved (if any)
    
    Returns:
        Formatted prompt context for LLM
    """
    if not usl_player:
        return ""
    
    context = f"""
WORLD CUP MATCH CONTEXT:

A player with USL roots just played in the World Cup:

Player: {usl_player.get('player_name')}
National Team: {usl_player.get('national_team')}
USL Club: {usl_player.get('usl_club')}
Position: {usl_player.get('position')}

USL Stats:
- Goals: {usl_player.get('usl_stats', {}).get('goals', 'N/A')}
- Assists: {usl_player.get('usl_stats', {}).get('assists', 'N/A')}
- Appearances: {usl_player.get('usl_stats', {}).get('appearances', 'N/A')}

Narrative: {usl_player.get('narrative')}

Connect this player's journey from {usl_player.get('usl_club')} to the World Cup stage.
Emphasize how independent USL clubs develop global talent outside the MLS franchise system.
"""
    
    return context


def consolidate_international_data() -> Dict[str, Any]:
    """
    Consolidate all international data sources.
    
    Returns a single object with:
    - World Cup matches
    - USL player cross-references
    - Transfer alerts
    - Context for LLM
    """
    try:
        logger.info("🌐 Consolidating international data...")
        
        # Load data sources
        usl_players = load_usl_world_cup_players()
        transfers = load_transfer_data()
        matches = fetch_world_cup_matches()
        
        # Process transfers
        alerts = detect_transfer_alerts(transfers)
        
        # Check matches for USL connections
        usl_connections = []
        for match in matches:
            usl_player = cross_reference_usl_players(match, usl_players)
            if usl_player:
                context = generate_world_cup_context(match, usl_player)
                usl_connections.append({
                    "match": match,
                    "usl_player": usl_player,
                    "context": context
                })
        
        consolidated = {
            "timestamp": datetime.now().isoformat(),
            "tournament": "FIFA World Cup 2026",
            "sources": {
                "world_cup_matches": matches,
                "usl_world_cup_players": usl_players,
                "transfer_data": transfers,
                "transfer_alerts": alerts,
                "usl_player_matches": usl_connections
            }
        }
        
        logger.info(f"✓ Consolidated international data: {len(alerts)} alerts, {len(usl_connections)} USL matches")
        return consolidated
        
    except Exception as e:
        logger.error(f"International data consolidation failed: {e}")
        return {}


def fetch_international_data() -> Dict[str, Any]:
    """
    Main entry point: Fetch all international/World Cup data.
    
    Integrates with main pipeline in data_fetcher.py
    """
    logger.info("🌍 Starting international data aggregation...")
    
    data = consolidate_international_data()
    
    logger.info("✓ International data aggregation complete")
    
    return data
