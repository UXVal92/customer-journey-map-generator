"""
Agent 2: Insights Summarizer
Takes structured journey data and generates a prioritised insights summary.
"""

import json
import anthropic


SYSTEM_PROMPT = """You are a senior product strategist. You take structured customer journey data
and produce a clear, actionable insights summary.

Given the journey data, produce:
1. A top-line summary (3 sentences: the good, the bad, the ugly)
2. 5 critical insights ranked by business impact, each with:
   - Title
   - Description (2-3 sentences)
   - Impact level
   - Recommended fix
3. A prioritised action list (ordered by impact vs effort)

Return your analysis as a JSON object with this exact structure:
{
    "top_line": {
        "the_good": "string",
        "the_bad": "string",
        "the_ugly": "string"
    },
    "critical_insights": [
        {
            "rank": 1,
            "title": "string",
            "description": "string",
            "impact": "high|medium|low",
            "fix": "string",
            "stage": "string"
        }
    ],
    "priority_actions": [
        {
            "rank": 1,
            "action": "string",
            "impact": "high|medium|low",
            "effort": "high|medium|low",
            "stage": "string"
        }
    ],
    "emotion_summary": "string (2-3 sentence narrative of the emotional journey)"
}

Only return valid JSON. No markdown, no explanation, just the JSON object.
"""


def summarise_insights(journey_data: dict) -> dict:
    """Generate prioritised insights from structured journey data."""
    client = anthropic.Anthropic()

    message = client.messages.create(
        model="claude-sonnet-4-5-20250929",
        max_tokens=4096,
        system=SYSTEM_PROMPT,
        messages=[
            {
                "role": "user",
                "content": f"Analyse this customer journey data and produce a prioritised insights summary:\n\n{json.dumps(journey_data, indent=2)}",
            }
        ],
    )

    response_text = message.content[0].text

    try:
        return json.loads(response_text)
    except json.JSONDecodeError:
        if "```json" in response_text:
            json_str = response_text.split("```json")[1].split("```")[0].strip()
            return json.loads(json_str)
        elif "```" in response_text:
            json_str = response_text.split("```")[1].split("```")[0].strip()
            return json.loads(json_str)
        raise


if __name__ == "__main__":
    from pathlib import Path

    journey_path = Path(__file__).parent.parent / "output" / "journey_data.json"
    journey_data = json.loads(journey_path.read_text(encoding="utf-8"))

    result = summarise_insights(journey_data)

    output_path = Path(__file__).parent.parent / "output" / "insights_summary.json"
    output_path.write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(f"Insights summary complete. Output saved to {output_path}")
