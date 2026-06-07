"""
LLM formatting module: Call open-weight LLM to generate structured content.

Supports multiple backends:
1. OpenCode Zen (FREE, cloud-based, no API key needed) - PRIMARY
2. Together.ai (free tier available, ~$0.0008/1K tokens)
3. OpenRouter (various model pricing)

Returns strict JSON with voiceover, on-screen text, and caption.

⚠️  PRIVACY NOTE: Free cloud models may use your data for training.
   For sensitive code, use local Ollama or paid tier.
"""

import os
import json
import re
from typing import Dict, Any, Optional
from loguru import logger
from pathlib import Path

try:
    import together
except ImportError:
    together = None

try:
    import requests
except ImportError:
    requests = None


def build_prompt(data: Dict[str, Any]) -> str:
    """
    Build a detailed, deterministic prompt for the LLM.
    
    Instructs the model to return strict JSON format.
    """
    
    # Extract key data points (you'll customize this based on your sources)
    api_sports = data.get("sources", {}).get("api_sports", {})
    twitter = data.get("sources", {}).get("twitter", [])
    news = data.get("sources", {}).get("news", [])
    
    # Build the prompt
    prompt = f"""You are a sports content creator for an Instagram Reel about USL Championship.
Your job is to generate engaging, factual content for a SHORT video (15-30 seconds).

INPUT DATA:
{json.dumps(data, indent=2)[:1000]}  # Truncate for context

INSTRUCTIONS:
1. Generate a SHORT voiceover script (2-3 sentences max, ~15 seconds when read aloud)
2. Generate on-screen text that complements the voiceover (max 2 lines, large font)
3. Generate an Instagram caption (max 150 characters, include relevant hashtags)

CONSTRAINTS:
- Be factual. Use only data from the input.
- Make it engaging but professional (for sports fans).
- Avoid hype-speak. Focus on facts, updates, and interesting angles.
- Format EXACTLY as valid JSON (no markdown, no extra text).

REQUIRED JSON OUTPUT FORMAT (and ONLY this):
{{
  "voiceover": "Your voiceover script here",
  "on_screen_text": "Text line 1\\nText line 2",
  "caption": "Instagram caption with #hashtags"
}}

Generate the JSON now:"""
    
    return prompt


def call_llm_opencode_zen(prompt: str, model: str = "big-pickle") -> str:
    """
    Call LLM via OpenCode Zen (FREE cloud models, no API key needed).
    
    Available models (all free, cloud-based):
    - big-pickle: General coding tasks
    - minimax-m2.5-free: Long context, strong reasoning
    - mimo-v2-pro-free: Xiaomi's coding model
    - nemotron-3-super-free: NVIDIA's fast model
    
    ⚠️  NOTE: Free models may log data for training purposes.
    See .env.example for OpenCode configuration.
    """
    logger.info(f"🤖 Calling LLM via OpenCode Zen ({model})...")
    
    # OpenCode Zen runs via a local server or direct integration
    # The VS Code extension handles authentication automatically
    
    opencode_api_url = os.getenv("OPENCODE_API_URL", "http://localhost:8000")
    opencode_token = os.getenv("OPENCODE_TOKEN", "")
    
    headers = {}
    if opencode_token:
        headers["Authorization"] = f"Bearer {opencode_token}"
    
    payload = {
        "model": model,
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "max_tokens": 512,
        "temperature": 0.7,
    }
    
    try:
        response = requests.post(
            f"{opencode_api_url}/chat/completions",
            json=payload,
            headers=headers,
            timeout=30
        )
        response.raise_for_status()
        result = response.json()
        return result["choices"][0]["message"]["content"]
    except Exception as e:
        logger.error(f"OpenCode Zen call failed: {e}. Falling back to Together.ai.")
        if together:
            return call_llm_together(prompt)
        raise


def call_llm_together(prompt: str) -> str:
    """
    Fallback: Call Llama 3 or Mistral via Together.ai API.
    
    Costs ~$0.0008 per 1K tokens (very cheap).
    Requires TOGETHER_API_KEY environment variable.
    """
    api_key = os.getenv("TOGETHER_API_KEY")
    if not api_key:
        raise ValueError("TOGETHER_API_KEY not set in environment variables")
    
    logger.info("🤖 Calling LLM via Together.ai (Llama 3)...")
    
    client = together.Together(api_key=api_key)
    
    response = client.complete(
        model="meta-llama/Llama-3-70b-chat-hf",
        prompt=prompt,
        max_tokens=512,
        temperature=0.7,
        top_p=0.95,
        top_k=50,
        repetition_penalty=1.1,
        stop=["</response>"]
    )
    
    return response.output.text


def call_llm_via_requests(prompt: str) -> str:
    """
    Fallback: call LLM via raw HTTP request to Together.ai.
    
    Useful if the together package isn't available.
    """
    import requests
    
    api_key = os.getenv("TOGETHER_API_KEY")
    if not api_key:
        raise ValueError("TOGETHER_API_KEY not set")
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": "meta-llama/Llama-3-70b-chat-hf",
        "prompt": prompt,
        "max_tokens": 512,
        "temperature": 0.7,
        "top_p": 0.95,
    }
    
    response = requests.post(
        "https://api.together.ai/inference",
        headers=headers,
        json=payload,
        timeout=30
    )
    
    response.raise_for_status()
    return response.json()["output"]["text"]


def extract_json_from_response(response_text: str) -> Dict[str, str]:
    """
    Extract JSON from LLM response (handles markdown code blocks, etc.).
    """
    # Try to find JSON block (handles markdown ```json ... ``` format)
    json_match = re.search(r"```json\s*(.*?)\s*```", response_text, re.DOTALL)
    if json_match:
        json_str = json_match.group(1)
    else:
        # Try to find plain JSON object
        json_match = re.search(r"\{.*\}", response_text, re.DOTALL)
        if json_match:
            json_str = json_match.group(0)
        else:
            raise ValueError(f"Could not extract JSON from response: {response_text[:200]}")
    
    return json.loads(json_str)


def validate_content(content: Dict[str, str]) -> bool:
    """
    Validate that LLM output has required fields.
    """
    required_keys = ["voiceover", "on_screen_text", "caption"]
    
    for key in required_keys:
        if key not in content:
            logger.error(f"Missing required field: {key}")
            return False
        if not isinstance(content[key], str) or len(content[key]) == 0:
            logger.error(f"Empty or invalid value for: {key}")
            return False
    
    # Length checks
    if len(content["voiceover"]) > 500:
        logger.warning("Voiceover is very long (>500 chars). This may exceed 30 seconds.")
    if len(content["caption"]) > 200:
        logger.warning("Caption exceeds typical Instagram limit.")
    
    return True


def generate_post_content(data: Dict[str, Any], backend: str = "opencode") -> Dict[str, str]:
    """
    Main entry point: generate LLM-formatted post content.
    
    Args:
        data: Aggregated data from data fetcher
        backend: 'opencode' (default, free), 'together', or 'auto' (tries opencode first)
    
    Returns:
        Validated JSON with voiceover, on_screen_text, and caption.
    
    ⚠️  PRIVACY: OpenCode Zen (free) may log data. Use 'together' for sensitive work.
    """
    logger.info(f"📝 Generating post content via {backend}...")
    
    # Build the prompt
    prompt = build_prompt(data)
    
    # Determine which backend to use
    if backend == "auto":
        # Try OpenCode first (free), fall back to Together.ai
        try:
            logger.info("Trying OpenCode Zen (free, no API key)...")
            response = call_llm_opencode_zen(prompt)
        except Exception as e:
            logger.warning(f"OpenCode failed: {e}. Falling back to Together.ai.")
            if together:
                response = call_llm_together(prompt)
            else:
                raise
    elif backend == "opencode":
        response = call_llm_opencode_zen(prompt)
    elif backend == "together":
        response = call_llm_together(prompt)
    else:
        raise ValueError(f"Unknown backend: {backend}")
    
    logger.info(f"LLM Response (first 200 chars): {response[:200]}")
    
    logger.info(f"LLM Response (first 200 chars): {response[:200]}")
    
    # Extract and validate JSON
    try:
        content = extract_json_from_response(response)
    except Exception as e:
        logger.error(f"Failed to parse LLM response as JSON: {e}")
        raise
    
    # Validate
    if not validate_content(content):
        raise ValueError("Generated content failed validation")
    
    logger.info("✓ Content generated and validated")
    return content
