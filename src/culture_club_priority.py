"""
Culture Club Prioritization Module

Ensures coverage of "the clubs that matter"—clubs with actual political
and cultural mission, not just billionaire vanity projects.

These clubs embody the ethos:
- Detroit City FC (American St. Pauli)
- Oakland Roots (Racial justice, grassroots)
- Forward Madison (Environmental, community)
- Vermont Green FC (Community-owned)
- Chattanooga FC (Rapidly growing, accessible)
- Louisville City FC (Community investment)

Content from these clubs gets amplified. Corporate franchise content gets critiqued.
"""

from typing import Dict, Any, List
from loguru import logger


CULTURE_CLUBS = {
    "detroit_city_fc": {
        "name": "Detroit City FC",
        "league": "USL Championship",
        "ethos": "American St. Pauli. Community-owned, anti-corporate",
        "keywords": ["Detroit", "DCFC", "independent", "community-owned"],
        "significance": 10,  # Highest priority
        "narrative": "The blueprint for American working-class soccer",
        "alignment": ["anti-racism", "LGBTQ+", "community ownership", "local investment"]
    },
    "atletico_dallas": {
        "name": "Atlético Dallas",
        "league": "USL Championship",
        "ethos": "Latinx representation, street soccer roots, community-embedded",
        "keywords": ["Atlético Dallas", "ATX", "Dallas", "street soccer", "Latinx"],
        "significance": 10,  # HIGHEST - street soccer connection
        "narrative": "Soccer from the streets. Built by immigrants, for immigrants.",
        "alignment": ["immigrant inclusion", "street soccer", "grassroots", "Latinx representation"]
    },
    "oakland_roots": {
        "name": "Oakland Roots",
        "league": "USL Championship",
        "ethos": "Racial justice, grassroots development, democratic ownership",
        "keywords": ["Oakland", "Roots", "racial justice", "BIPOC"],
        "significance": 9,
        "narrative": "Rooted in Oakland. Owned by Oakland. For Oakland.",
        "alignment": ["anti-racism", "grassroots", "community ownership", "immigrant inclusion"]
    },
    "forward_madison": {
        "name": "Forward Madison",
        "league": "USL Championship",
        "ethos": "Environmental sustainability, community-driven",
        "keywords": ["Madison", "Forward", "environmental", "sustainability"],
        "significance": 8,
        "narrative": "Soccer for the future. Literally.",
        "alignment": ["environmentalism", "community ownership", "grassroots"]
    },
    "chattanooga_fc": {
        "name": "Chattanooga FC",
        "league": "USL Championship",
        "ethos": "Rapid growth, community investment, anti-corporate",
        "keywords": ["Chattanooga", "CFC", "Tennessee"],
        "significance": 8,
        "narrative": "Building culture from the ground up",
        "alignment": ["community investment", "grassroots", "growth"]
    },
    "louisville_city_fc": {
        "name": "Louisville City FC",
        "league": "USL Championship",
        "ethos": "Working-class roots, growing rapidly, community-embedded",
        "keywords": ["Louisville", "City", "Kentucky"],
        "significance": 7,
        "narrative": "Working-class power in the South",
        "alignment": ["working-class", "community investment"]
    },
    "vermont_green_fc": {
        "name": "Vermont Green FC",
        "league": "USL Championship",
        "ethos": "Community-owned, environmentally conscious",
        "keywords": ["Vermont", "Green"],
        "significance": 7,
        "narrative": "Local ownership in rural America",
        "alignment": ["community ownership", "environmentalism", "regional"]
    }
}

# Clubs to CRITIQUE (billionaire franchises, corporate models)
CRITIQUE_TARGETS = {
    "lafc": {
        "name": "Los Angeles FC",
        "league": "MLS",
        "critique": "Billionaire-owned franchise masquerading as 'independent'",
        "keywords": ["LAFC", "Banc of California"],
        "narrative": "Corporate soccer dressed as culture"
    },
    "inter_miami": {
        "name": "Inter Miami CF",
        "league": "MLS",
        "critique": "Beckham's vanity project. Billionaire ownership.",
        "keywords": ["Inter Miami", "Beckham"],
        "narrative": "Celebrity franchise, not community club"
    }
}


def prioritize_reddit_scraping() -> Dict[str, List[str]]:
    """
    Keywords to prioritize when scraping Reddit (r/USLPRO, r/MLS)
    """
    return {
        "high_priority": [
            "Detroit City FC",
            "DCFC",
            "Atlético Dallas",
            "street soccer",
            "Oakland Roots",
            "community-owned",
            "pro/rel",
            "franchise system",
            "accessibility",
            "working class",
            "independent",
            "Latinx soccer",
            "grassroots development",
            "immigrant soccer",
            "MLS expansion",
            "promotion and relegation"
        ],
        "medium_priority": [
            "USL Championship",
            "Louisville City",
            "Chattanooga FC",
            "Sacramento Republic",
            "futsal",
            "youth development"
        ],
        "low_priority": [
            "MLS news",
            "billionaire owners",
            "expansion franchise",
            "$500 million expansion fee"
        ],
        "critique_targets": [
            "LAFC",
            "Inter Miami",
            "venture capital",
            "investor-backed",
            "franchise fee"
        ]
    }


def prioritize_rss_feeds() -> Dict[str, int]:
    """
    Weighting for RSS feeds.
    Culture clubs get higher weight in the algorithm.
    Street soccer gets disproportionate coverage.
    """
    return {
        "atletico_dallas": 10,  # HIGHEST - street soccer connection
        "detroit_city_fc": 10,
        "oakland_roots": 9,
        "chattanooga_fc": 8,
        "louisville_city_fc": 7,
        "forward_madison": 8,
        "street_soccer": 9,  # Community futsal, grassroots street games
        "usl_championship_official": 6,
        "mls_news": 3,  # Low priority (critique mode)
    }


def filter_content_by_ethos(content_item: Dict[str, Any]) -> Dict[str, Any]:
    """
    Given a piece of content, determine:
    1. Is it about a culture club? (amplify)
    2. Is it about street soccer? (highest amplification)
    3. Is it about a critique target? (critique)
    4. Is it generic? (reframe through pro/rel lens)
    
    Returns enriched content with ethos instructions.
    """
    club_mentioned = content_item.get("club", "")
    title_and_body = (content_item.get("club", "") + " " + 
                      content_item.get("title", "") + " " + 
                      content_item.get("body", "")).lower()
    
    # Check for STREET SOCCER first (highest priority)
    street_soccer_keywords = ["street soccer", "futsal", "grassroots", "pickup", "community courts"]
    if any(kw in title_and_body for kw in street_soccer_keywords):
        return {
            **content_item,
            "ethos": "street_soccer",
            "priority": 10,  # HIGHEST
            "narrative": "Soccer from the streets. Where culture lives.",
            "amplification": True,
            "tone": "celebratory_grassroots"
        }
    
    # Check if it's a culture club
    for culture_club_id, club_info in CULTURE_CLUBS.items():
        if any(kw.lower() in club_mentioned.lower() for kw in club_info["keywords"]):
            return {
                **content_item,
                "ethos": "culture_club",
                "priority": club_info["significance"],
                "narrative": club_info["narrative"],
                "amplification": True,
                "tone": "celebratory_manifesto"
            }
    
    # Check if it's a critique target
    for critique_id, critique_info in CRITIQUE_TARGETS.items():
        if any(kw.lower() in club_mentioned.lower() for kw in critique_info["keywords"]):
            return {
                **content_item,
                "ethos": "critique_target",
                "priority": 8,  # High priority for critique
                "narrative": critique_info["critique"],
                "amplification": True,
                "tone": "confrontational_analysis"
            }
    
    # Generic content - reframe through pro/rel lens
    return {
        **content_item,
        "ethos": "generic",
        "priority": 4,
        "narrative": "Reframe through pro/rel lens: How does this prove open system > franchise?",
        "tone": "analytical_manifesto"
    }


def get_content_amplification_prompt(filtered_content: Dict[str, Any]) -> str:
    """
    Generate an LLM prompt that instructs how to handle this piece of content.
    
    For street soccer: CELEBRATE as ORIGINS
    For culture clubs: AMPLIFY
    For critique targets: EXPOSE
    For generic: REFRAME
    """
    ethos = filtered_content.get("ethos")
    
    if ethos == "street_soccer":
        return f"""
This is about STREET SOCCER—the origin point of all culture.

Street soccer is:
- Where working-class kids learn
- Where immigrants build community
- Where passion is pure (no billionaires)
- Where pro/rel proves itself (best rise up)

CELEBRATE this story as the foundation of real soccer.
Show how street players become professionals through merit, not money.
Show how community courts > luxury academies.

Write a script that honors the street. Make it a manifesto.
End with: "The best soccer comes from concrete, not contracts."
"""
    
    elif ethos == "culture_club":
        return f"""
This is about {filtered_content.get('club', 'a culture club')}.

This club embodies the anti-corporate, working-class ethos.
AMPLIFY this story. Make it a rallying cry.

Narrative: {filtered_content.get('narrative')}

Write a script that celebrates this club as a model for American soccer.
End with a call to action: "Support your local. Own your club."
"""
    
    elif ethos == "critique_target":
        return f"""
This is about {filtered_content.get('club', 'a billionaire franchise')}.

This club represents what's wrong with MLS: corporate ownership, billionaire control.
EXPOSE the contrast between this and what community-owned clubs are doing.

Critique: {filtered_content.get('narrative')}

Write a script that exposes the franchise model's failures.
Show how pro/rel would fix this.
"""
    
    else:  # generic
        return f"""
This USL news needs a pro/rel lens.

Ask: How does this prove that open systems > closed franchises?

Reframe: {filtered_content.get('narrative')}

Connect to the bigger picture:
- Community ownership works
- Promotion/relegation builds accountability
- Pro/rel is justice

Write from the UnfranchisedFC ethos.
"""


def get_culture_club_coverage_target() -> Dict[str, Any]:
    """
    Track what percentage of content should be about culture clubs + street soccer.
    
    Target: 65% of content is about culture clubs + street soccer
    Target: 15% is critique content
    Target: 20% is generic USL/international
    """
    return {
        "culture_club_and_street_soccer_target": 0.65,
        "critique_target": 0.15,
        "generic_target": 0.20,
        "culture_clubs_tracked": list(CULTURE_CLUBS.keys()),
        "street_soccer_priority": True,
        "rationale": "Disproportionate coverage of grassroots, working-class soccer"
    }


if __name__ == "__main__":
    import json
    
    print("=== Culture Club Prioritization ===\n")
    print(json.dumps(CULTURE_CLUBS, indent=2, default=str))
    
    print("\n=== Content Amplification Target ===\n")
    print(json.dumps(get_culture_club_coverage_target(), indent=2))
