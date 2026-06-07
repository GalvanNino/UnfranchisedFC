"""
Audio Strategy Module: UnfranchisedFC Sound Design

Two options, both drawn from authentic working-class/protest culture:

1. RAW MATCHDAY CHANTS (Recommended)
   - Live crowd recordings from grassroots/pro/rel clubs
   - St. Pauli ultras, Rayo Vallecano, Detroit City FC supporters
   - Pure authenticity, zero corporate polish
   - Layered under fast-cut video montages

2. PROTEST SOUNDTRACK / BARRIO Y REBELDÍA
   - Curated playlist of anti-establishment music
   - Latin hip-hop, punk, indie with political messaging
   - Artists: Residente, Violeta, Los Chiquibum, etc.
   - Sonic DNA: Neighborhood rebellion, not stadium spectacle

Playlist reference: Barrio y Rebeldía
- Title = the ethos perfectly: "Neighborhood and Rebellion"
- Genre blend: Latin trap, reggaeton, indie, punk
- Vibe: Street-level politics, community power, anti-corporate
"""

from dataclasses import dataclass
from typing import Dict, List


@dataclass
class AudioStrategy:
    """UnfranchisedFC audio aesthetic"""
    
    name: str
    description: str
    authenticity_score: int  # 1-10, 10 = most authentic
    cost: str
    production_complexity: str
    mood: str


AUDIO_OPTIONS = {
    "raw_matchday_chants": AudioStrategy(
        name="Raw Matchday Chants",
        description="Live crowd recordings from grassroots/pro/rel clubs. St. Pauli ultras, Rayo Vallecano, Detroit City FC, Oakland Roots supporters.",
        authenticity_score=10,
        cost="Free (source from YouTube/supporter archives)",
        production_complexity="Low (just layer under video)",
        mood="Pure, unpolished, working-class power"
    ),
    "protest_soundtrack": AudioStrategy(
        name="Protest Soundtrack / Barrio y Rebeldía",
        description="Curated playlist of anti-establishment music. Latin hip-hop, reggaeton, indie, punk with political messaging.",
        authenticity_score=9,
        cost="Spotify/Apple Music licensing (~$0.005 per stream)",
        production_complexity="Medium (mix/edit/transition)",
        mood="Street-level rebellion, community power"
    ),
    "documentary_narrator": AudioStrategy(
        name="Gritty Documentary Narrator",
        description="ElevenLabs TTS with harsh voice settings. Fast delivery, clipped phrases, no softness.",
        authenticity_score=5,
        cost="Included in ElevenLabs API",
        production_complexity="Low (just TTS)",
        mood="Synthetic but intentional. Can work for data visualization moments."
    )
}


AUDIO_STYLE_GUIDE = {
    "primary": "raw_matchday_chants",
    "secondary": "protest_soundtrack",
    "fallback": "documentary_narrator",
    
    "mixing_guidelines": {
        "chants": {
            "volume": "0-3dB",
            "compression": "hard (make it punch)",
            "reverb": "minimal (preserve rawness)",
            "layering": "Cut under voiceover by -12dB, keep at full on transitions"
        },
        "protest_music": {
            "volume": "-6dB (let lyrics breathe)",
            "compression": "medium",
            "reverb": "subtle",
            "layering": "Dynamic: loud on hooks, drop for voiceover"
        }
    },
    
    "ffmpeg_audio_examples": {
        "chants_only": "ffmpeg -i video.mp4 -i chants.mp3 -filter_complex '[1]volume=0.3[a];[0][a]amix=inputs=2' output.mp4",
        "music_with_voiceover": "ffmpeg -i video.mp4 -i voiceover.mp3 -i music.mp3 -filter_complex '[1][2]amix=inputs=2:duration=first[audio]' -map 0:v -map '[audio]' output.mp4"
    }
}


def get_recommended_artists_for_barrio_y_rebeldia() -> Dict[str, List[str]]:
    """
    Artists that embody the 'Barrio y Rebeldía' ethos:
    
    Working-class, Latinx, anti-corporate, street-level
    """
    return {
        "latin_hip_hop_protest": [
            "Residente",  # Puerto Rico's political conscience
            "Bad Bunny",  # Uses platform for justice
            "Ivy Queen",  # Reggaeton pioneer, LGBTQ+ icon
            "Don Omar",  # OG reggaeton rebel
            "J Balvin",  # (selectively - political moments)
        ],
        "indie_punk_latin": [
            "Violeta",  # Chilean indie/protest
            "Los Chiquibum",  # Argentine punk energy
            "Café Tacvba",  # Mexican political rock
            "Molotov",  # Mexican rap-rock rebels
            "Cultura Profética",  # Puerto Rican reggae activism",
        ],
        "street_soccer_culture": [
            "Fulanito",  # Dominican hip-hop/reggaeton
            "Wisin y Yandel",  # Perreo energy
            "Tego Calderón",  # Street poet
            "Vico C",  # Puerto Rican hip-hop legend
        ]
    }


def get_matchday_chant_sources() -> Dict[str, Dict]:
    """
    Where to find authentic matchday chants from culture clubs
    """
    return {
        "st_pauli": {
            "name": "FC St. Pauli",
            "source": "YouTube/Ultras87 channels",
            "vibe": "Punk, anti-fascist, football terrace energy",
            "keywords": ["Millerntor", "FCSP", "ultras"]
        },
        "rayo_vallecano": {
            "name": "Rayo Vallecano",
            "source": "YouTube/Red Rayo channels",
            "vibe": "Working-class Madrid, communist, fierce",
            "keywords": ["Rayo", "Vallecano", "ultras"]
        },
        "detroit_city_fc": {
            "name": "Detroit City FC",
            "source": "YouTube/TikTok supporter videos",
            "vibe": "American street soccer energy, rust belt pride",
            "keywords": ["DCFC", "Detroit", "supporter"]
        },
        "oakland_roots": {
            "name": "Oakland Roots",
            "source": "YouTube/TikTok supporter videos",
            "vibe": "Bay Area culture, hip-hop influence, BIPOC-centered",
            "keywords": ["Oakland", "Roots", "supporter"]
        },
        "forward_madison": {
            "name": "Forward Madison",
            "source": "YouTube/TikTok supporter videos",
            "vibe": "Midwest solidarity, environmental consciousness",
            "keywords": ["Madison", "Forward"]
        }
    }


def get_audio_integration_instructions() -> str:
    """
    How to integrate audio into UnfranchisedFC Reels
    """
    return """
AUDIO INTEGRATION STRATEGY FOR INSTAGRAM REELS

STRUCTURE A:
- 0-2s: Raw chant intro (high energy)
- 2-10s: Voiceover + music layered (chants drop to -12dB)
- 10-15s: Music surge into final hook
- 15-30s: Chant outro (full volume, fade out)

STRUCTURE B (Data Viz):
- 0-5s: Documentary narrator TTS (hard, clipped)
- 5-30s: Protest music underneath (builds tension)
- Narrator ends, music swells for final frame

STRUCTURE C (Street Soccer):
- 0-30s: Barrio y Rebeldía playlist (keep full volume)
- Voiceover ONLY on key frames (reduced mix)
- Let the music tell the story
- Text overlay carries narrative weight

AUDIO MIXING PHILOSOPHY:
- Never polish away the grittiness
- Chants = authenticity, keep them raw
- Music = emotional fuel, use it to amplify anger/hope
- Voiceover = sparingly, only when needed
- The sound should feel ALIVE, not produced

TESTING:
1. Record on phone speaker (listener's first experience)
2. Ask: "Does this sound like corporate ESPN?"
3. If yes: Add more chants, remove polish
4. If no: Ship it
"""


if __name__ == "__main__":
    import json
    
    print("=== UnfranchisedFC Audio Strategy ===\n")
    
    print("AUDIO OPTIONS:")
    for option_id, strategy in AUDIO_OPTIONS.items():
        print(f"\n{option_id.upper()}:")
        print(f"  Name: {strategy.name}")
        print(f"  Authenticity: {strategy.authenticity_score}/10")
        print(f"  Cost: {strategy.cost}")
        print(f"  Mood: {strategy.mood}")
    
    print("\n\n=== Recommended Artists ===")
    artists = get_recommended_artists_for_barrio_y_rebeldia()
    print(json.dumps(artists, indent=2))
    
    print("\n\n=== Matchday Chant Sources ===")
    sources = get_matchday_chant_sources()
    print(json.dumps({k: v for k, v in sources.items()}, indent=2, default=str))
