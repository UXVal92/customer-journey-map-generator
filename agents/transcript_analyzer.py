"""
Agent 1: Transcript Analyzer
Reads customer call transcripts and extracts structured journey data.
"""

import json
import anthropic


SYSTEM_PROMPT = """You are a customer experience analyst. You analyse customer call transcripts
and extract structured journey mapping data.

For each transcript, identify:
1. Which journey stage(s) it covers (Awareness, Consideration, Purchase, Onboarding, Retention, Advocacy)
2. Customer touchpoints (channels and interaction points)
3. Customer actions (what they did)
4. Customer thinking (direct quotes that reveal mindset)
5. Emotions (how they felt)
6. Pain points (friction, frustration, failures)
7. Opportunities (improvements and fixes)

Return your analysis as a JSON object with this exact structure:
{
    "business_name": "string",
    "business_type": "string",
    "customers_analysed": [{"name": "string", "pet": "string", "call_type": "string"}],
    "stages": {
        "Awareness": {
            "touchpoints": ["string"],
            "actions": ["string"],
            "thinking": ["string (direct quotes with attribution)"],
            "emotions": ["string"],
            "pain_points": ["string"],
            "opportunities": ["string"]
        },
        "Consideration": { ... },
        "Purchase": { ... },
        "Onboarding": { ... },
        "Retention": { ... },
        "Advocacy": { ... }
    },
    "critical_insights": [
        {"title": "string", "description": "string", "impact": "high|medium|low", "stage": "string"}
    ],
    "emotion_curve": [
        {"stage": "string", "emotion": "string", "score": "number (-5 to +5)"}
    ]
}

Only return valid JSON. No markdown, no explanation, just the JSON object.
"""


def analyse_transcripts(transcripts_text: str) -> dict:
    """Analyse customer call transcripts and return structured journey data."""
    client = anthropic.Anthropic()

    message = client.messages.create(
        model="claude-sonnet-4-5-20250929",
        max_tokens=8192,
        system=SYSTEM_PROMPT,
        messages=[
            {
                "role": "user",
                "content": f"Analyse these customer call transcripts and extract journey mapping data:\n\n{transcripts_text}",
            }
        ],
    )

    response_text = message.content[0].text

    # Parse JSON from response
    try:
        return json.loads(response_text)
    except json.JSONDecodeError:
        # Try to extract JSON if wrapped in markdown
        if "```json" in response_text:
            json_str = response_text.split("```json")[1].split("```")[0].strip()
            return json.loads(json_str)
        elif "```" in response_text:
            json_str = response_text.split("```")[1].split("```")[0].strip()
            return json.loads(json_str)
        raise


if __name__ == "__main__":
    import sys
    from pathlib import Path

    if len(sys.argv) > 1:
        transcript_path = Path(sys.argv[1])
    else:
        transcript_path = Path(__file__).parent.parent / "transcripts" / "pawbox_transcripts.md"

    transcripts = transcript_path.read_text(encoding="utf-8")
    result = analyse_transcripts(transcripts)

    output_path = Path(__file__).parent.parent / "output" / "journey_data.json"
    output_path.write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(f"Analysis complete. Output saved to {output_path}")
