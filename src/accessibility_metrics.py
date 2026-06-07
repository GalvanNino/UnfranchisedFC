"""
Accessibility & Inequality Metrics Module

Generates data visualizations that highlight the cost-of-entry 
difference between MLS (billionaire franchises) and USL (community-owned).

This is ammunition for the manifesto.
"""

import json
from typing import Dict, Any, List
from dataclasses import dataclass
from loguru import logger


@dataclass
class AccessibilityMetric:
    """A single accessibility metric comparing MLS vs USL"""
    category: str  # e.g., "ticket_price", "youth_academy_cost"
    mls_average: str
    usl_average: str
    narrative: str  # Why this matters
    inequality_factor: float  # How much worse MLS is (e.g., 5.7x more expensive)


def get_ticket_price_comparison() -> AccessibilityMetric:
    """
    Average ticket prices: MLS vs USL
    
    MLS: $100-150 (luxury event)
    USL: $15-35 (accessible to working class)
    """
    return AccessibilityMetric(
        category="Average Ticket Price",
        mls_average="$125",
        usl_average="$22",
        narrative="Billionaires priced out the working class. USL brought them back.",
        inequality_factor=5.7
    )


def get_youth_academy_comparison() -> AccessibilityMetric:
    """
    Youth academy cost: MLS academy vs independent USL clubs
    
    MLS academy: $8,000/year (pay-to-play)
    USL community clubs: Free (merit-based)
    """
    return AccessibilityMetric(
        category="Youth Academy Annual Cost",
        mls_average="$8,000/year",
        usl_average="Free",
        narrative="Talent shouldn't require wealth. Pro/rel clubs invest in local youth.",
        inequality_factor=float('inf')  # No cost vs. thousands
    )


def get_beer_price_comparison() -> AccessibilityMetric:
    """
    Beer at the stadium (indicator of working-class accessibility)
    
    MLS: $12-15
    USL: $5-7
    """
    return AccessibilityMetric(
        category="Stadium Beer Price",
        mls_average="$13",
        usl_average="$6",
        narrative="Even a beer is a luxury in the billionaire league.",
        inequality_factor=2.2
    )


def get_merchandise_comparison() -> AccessibilityMetric:
    """
    Jersey/merchandise prices
    
    MLS: $120-150 (luxury goods)
    USL: $45-65 (accessible)
    """
    return AccessibilityMetric(
        category="Official Team Jersey",
        mls_average="$130",
        usl_average="$55",
        narrative="Your culture shouldn't cost a week's groceries.",
        inequality_factor=2.4
    )


def get_ownership_comparison() -> Dict[str, Dict[str, str]]:
    """
    Ownership structure comparison: Who controls the club?
    """
    return {
        "mls_franchise": {
            "owner": "Single billionaire or private equity firm",
            "fan_input": "None. Owner makes all decisions.",
            "profits": "Flow to owner/shareholders",
            "narrative": "Autocracy. You have no say."
        },
        "usl_member_owned": {
            "owner": "Club members/supporters",
            "fan_input": "Democratic voting on major decisions",
            "profits": "Reinvested in club and community",
            "narrative": "Democracy. You own it."
        }
    }


def get_all_metrics() -> List[AccessibilityMetric]:
    """Return all accessibility metrics as a list"""
    return [
        get_ticket_price_comparison(),
        get_youth_academy_comparison(),
        get_beer_price_comparison(),
        get_merchandise_comparison(),
    ]


def generate_inequality_narrative(metric: AccessibilityMetric) -> str:
    """
    Generate a short, punchy narrative for a specific metric.
    
    This becomes LLM prompt data.
    """
    if metric.inequality_factor == float('inf'):
        factor_text = "infinitely more expensive"
    else:
        factor_text = f"{metric.inequality_factor:.1f}x more expensive"
    
    return f"""
DATA: {metric.category}
- MLS: {metric.mls_average}
- USL: {metric.usl_average}
- Inequality: MLS is {factor_text}

MANIFESTO: {metric.narrative}

This is class warfare dressed up as sports.
The franchise model doesn't just charge more.
It charges out the working class entirely.
"""


def generate_accessibility_heat_map_data() -> Dict[str, Any]:
    """
    Generate data structure for a visual heat map showing
    MLS (red = expensive/inaccessible) vs USL (green = affordable/accessible)
    """
    metrics = get_all_metrics()
    
    return {
        "title": "The Cost of Football: MLS vs USL",
        "subtitle": "Who owns your sport? Your wallet knows the answer.",
        "data": [
            {
                "category": m.category,
                "mls": m.mls_average,
                "usl": m.usl_average,
                "accessibility_score": 100 / m.inequality_factor if m.inequality_factor != float('inf') else 0
                # Higher = more accessible
            }
            for m in metrics
        ],
        "narrative": "Red = billionaire pricing. Green = working-class accessibility."
    }


def get_pro_rel_accessibility_case() -> str:
    """
    Summary argument: Why pro/rel solves the accessibility crisis
    """
    return """
THE CASE FOR ACCESSIBILITY:

Promotion & Relegation creates accountability.
If you price out your fans, you lose your stadium.
You lose your revenue. You get demoted.

The franchise system has no accountability.
Billionaires can charge whatever they want.
Fans have nowhere else to go.

Until they build something new.
Until they own it themselves.

USL is that something.
Pro/rel is the mechanism.

Accessibility is justice.
Justice is pro/rel.
"""


def consolidate_accessibility_data() -> Dict[str, Any]:
    """
    Consolidate all accessibility metrics into one object
    for use in LLM prompts
    """
    logger.info("📊 Generating accessibility metrics...")
    
    return {
        "timestamp": "2026-06-07",
        "metrics": [m.__dict__ for m in get_all_metrics()],
        "ownership_comparison": get_ownership_comparison(),
        "heat_map_data": generate_accessibility_heat_map_data(),
        "pro_rel_case": get_pro_rel_accessibility_case(),
        "narratives": [generate_inequality_narrative(m) for m in get_all_metrics()]
    }


if __name__ == "__main__":
    data = consolidate_accessibility_data()
    print(json.dumps(data, indent=2, default=str))
