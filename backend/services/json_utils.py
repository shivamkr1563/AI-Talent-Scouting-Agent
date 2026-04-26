"""
Utility functions for parsing Gemini AI responses
"""
import json
import re


def extract_json(text: str) -> dict | list:
    """
    Extract JSON from Gemini response, handling markdown code blocks.
    Gemini often returns: ```json\n{...}\n```
    """
    # Try direct JSON parsing first
    text = text.strip()
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        pass
    
    # Try removing markdown code blocks
    # Pattern: ```json\n{...}\n``` or ```\n{...}\n```
    json_pattern = r'```(?:json)?\s*([\s\S]*?)\s*```'
    match = re.search(json_pattern, text)
    if match:
        json_str = match.group(1).strip()
        try:
            return json.loads(json_str)
        except json.JSONDecodeError:
            pass
    
    # If all else fails, try to find JSON object/array in text
    # Look for first { or [ and last } or ]
    for start_char, end_char in [('{', '}'), ('[', ']')]:
        start_idx = text.find(start_char)
        end_idx = text.rfind(end_char)
        if start_idx != -1 and end_idx != -1 and end_idx > start_idx:
            try:
                return json.loads(text[start_idx:end_idx+1])
            except json.JSONDecodeError:
                continue
    
    raise ValueError(f"Could not extract valid JSON from: {text[:100]}")
