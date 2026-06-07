"""
AMF (Against Modern Football) Launch Strategy
==============================================

9-post inaugural campaign structure for UnfranchisedFC.

This strategy hardcodes the worldview directly into the pipeline,
ensuring that open-weight LLM models generate anti-corporate,
community-first, pro-pyramid soccer scripts.

Each post targets a specific structural critique of modern football.
"""

# Post type definitions with their ideological focus
AMF_LAUNCH_POSTS = [
    {
        "post_number": 1,
        "type": "franchise_vs_pyramid",
        "title": "The Structural Trap",
        "context": (
            "USL structural blueprint and the 2028 USL Premier Division 1 target "
            "versus MLS single-entity structure. USL: open pyramid, merit-based. "
            "MLS: closed franchise cartel, financial gatekeeping."
        ),
        "focus": "Analyze the structural trap of the franchise loop versus the freedom of a 3-tier pyramid with true pro/rel.",
        "ethos_keywords": ["meritocracy", "open pyramid", "monopoly", "franchise cartel", "pro/rel justice"]
    },
    {
        "post_number": 2,
        "type": "ticket_index",
        "title": "Working Class Gatekeeping",
        "context": (
            "Average ticket pricing comparison: MLS $125+ vs USL $22. Youth academy pricing: "
            "MLS $8,000/year vs USL free. Beer at stadium: MLS $13 vs USL $6. "
            "Financial gatekeeping prices out inner-city families from supporting their local clubs."
        ),
        "focus": "Expose the financial gatekeeping of soccer. Contrast working-class terrace culture with billionaire luxury pricing.",
        "ethos_keywords": ["accessibility is justice", "working class", "financial gatekeeping", "terraces", "affordability"]
    },
    {
        "post_number": 3,
        "type": "death_of_draft",
        "title": "The Draft Trap",
        "context": (
            "American collegiate soccer draft system limits player mobility and development. "
            "Direct comparison: USL players transfer directly to European clubs (Bundesliga, Championship). "
            "MLS players stuck in single-entity system. Case: Birmingham Legion's Ramiz Hamouda transferred directly to Werder Bremen."
        ),
        "focus": "Break down how the American collegiate draft limits player mobility and praise direct European transfers.",
        "ethos_keywords": ["player freedom", "global market", "direct transfers", "merit-based movement", "European pathway"]
    },
    {
        "post_number": 4,
        "type": "culture_clubs",
        "title": "Community Ownership Model",
        "context": (
            "Detroit City FC (supporter-owned, 95/5 fan ownership split), Oakland Roots (democratic governance), "
            "Forward Madison (community-first), Atlético Dallas (Latinx grassroots). These clubs embody radical inclusion, "
            "supporter democracy, and anti-billionaire infrastructure."
        ),
        "focus": "Highlight clubs like Detroit City FC or Oakland Roots who embody supporter-ownership and radical community inclusion.",
        "ethos_keywords": ["supporter ownership", "democracy", "community first", "grassroots", "radical inclusion"]
    },
    {
        "post_number": 5,
        "type": "global_stage",
        "title": "World Cup Base Camps",
        "context": (
            "2026 World Cup base camps: 12 countries announced. USL players in World Cup squads: Balogun, Reyna, Scally, Dest, Giménez, Robinson, McKennie, Huerta. "
            "Connect international competition infrastructure directly to local, independent American soccer club development. "
            "Global stage = local club pathway."
        ),
        "focus": "Connect the 2026 World Cup base camps to local, independent American soccer club infrastructure.",
        "ethos_keywords": ["global stage", "local club development", "international pipeline", "World Cup justice", "player development"]
    },
    {
        "post_number": 6,
        "type": "franchise_vs_pyramid",
        "title": "Promotion/Relegation = Democracy",
        "context": (
            "England Championship model: teams fight for promotion, direct stakes, sporting merit determines investment. "
            "MLS: billionaires guarantee franchise survival regardless of performance. "
            "Pro/rel = performance accountability. Single-entity = billionaire security blanket."
        ),
        "focus": "Explain why pro/rel creates sporting meritocracy while franchise systems protect billionaire incompetence.",
        "ethos_keywords": ["meritocracy", "accountability", "sporting justice", "billionaire security", "true competition"]
    },
    {
        "post_number": 7,
        "type": "ticket_index",
        "title": "Billionaire Erasure",
        "context": (
            "MLS teams owned by tech billionaires, hedge fund managers, Saudi money. "
            "Detroit City FC: owned by 95% fans. Oakland Roots: democratic governance. "
            "Ownership structure = who controls culture. Billionaires = corporate erasure of local identity."
        ),
        "focus": "Expose billionaire ownership structures and celebrate community-owned models.",
        "ethos_keywords": ["ownership structure", "billionaire control", "community power", "corporate erasure", "fan democracy"]
    },
    {
        "post_number": 8,
        "type": "death_of_draft",
        "title": "Free Players From Draft Prison",
        "context": (
            "NCAA to MLS pipeline: players forced to 4-year college commitment before professional career. "
            "USL direct entry: sign at 16, play professionally, develop in real competition. "
            "Draft = artificial delay. Free entry = player power."
        ),
        "focus": "Critique the college-to-MLS pipeline as a prison delaying professional development.",
        "ethos_keywords": ["player freedom", "professional development", "artificial delay", "real competition", "direct entry"]
    },
    {
        "post_number": 9,
        "type": "culture_clubs",
        "title": "The Underground Movement",
        "context": (
            "St. Pauli, Rayo Vallecano, DCFC, Oakland Roots: underground supporter movements resisting billionaire soccer. "
            "2026 World Cup: American players will showcase global talent. American soccer reckoning: choose billionaire cartel or underground community movement."
        ),
        "focus": "Position American soccer at a crossroads: billionaire franchises or underground community revolution.",
        "ethos_keywords": ["underground movement", "supporter power", "reckoning", "community revolution", "against modern football"]
    }
]


def get_amf_post(post_number: int) -> dict:
    """Retrieve a specific AMF launch post by number (1-9)."""
    for post in AMF_LAUNCH_POSTS:
        if post["post_number"] == post_number:
            return post
    return None


def list_amf_posts() -> list:
    """Return all 9 AMF launch posts."""
    return AMF_LAUNCH_POSTS
