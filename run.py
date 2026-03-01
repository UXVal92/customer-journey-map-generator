"""
Customer Journey Map Generator
===============================
Analyses customer call transcripts and generates structured journey
data ready to be visualised on Miro.

Two modes:
  1. python run.py                    — Analyse transcripts, output JSON
  2. python run.py transcripts.md     — Analyse your own transcripts

The output JSON files can then be used by Claude Code + Miro MCP
to build a high-quality visual journey map on a Miro board.
"""

import json
import os
import sys
from pathlib import Path

from dotenv import load_dotenv

from agents.transcript_analyzer import analyse_transcripts
from agents.insights_summarizer import summarise_insights


def main():
    load_dotenv()

    # Validate environment
    api_key = os.getenv("ANTHROPIC_API_KEY")
    if not api_key:
        print("Error: ANTHROPIC_API_KEY not set. Add it to your .env file.")
        sys.exit(1)

    # Determine transcript source
    if len(sys.argv) > 1:
        transcript_path = Path(sys.argv[1])
    else:
        transcript_path = Path(__file__).parent / "transcripts" / "pawbox_transcripts.md"

    if not transcript_path.exists():
        print(f"Error: Transcript file not found: {transcript_path}")
        sys.exit(1)

    output_dir = Path(__file__).parent / "output"
    output_dir.mkdir(exist_ok=True)

    transcripts = transcript_path.read_text(encoding="utf-8")
    print(f"Loaded transcripts from: {transcript_path}")
    print(f"Transcript length: {len(transcripts):,} characters\n")

    # Agent 1: Analyse transcripts
    print("=" * 50)
    print("AGENT 1: Transcript Analyzer")
    print("=" * 50)
    print("Analysing call transcripts for journey data...")
    journey_data = analyse_transcripts(transcripts)

    journey_path = output_dir / "journey_data.json"
    journey_path.write_text(json.dumps(journey_data, indent=2), encoding="utf-8")
    print(f"Found {len(journey_data.get('stages', {}))} journey stages")
    print(f"Identified {len(journey_data.get('critical_insights', []))} critical insights")
    print(f"Saved to: {journey_path}\n")

    # Agent 2: Summarise insights
    print("=" * 50)
    print("AGENT 2: Insights Summarizer")
    print("=" * 50)
    print("Generating prioritised insights summary...")
    insights_data = summarise_insights(journey_data)

    insights_path = output_dir / "insights_summary.json"
    insights_path.write_text(json.dumps(insights_data, indent=2), encoding="utf-8")
    print(f"Generated {len(insights_data.get('priority_actions', []))} priority actions")
    print(f"Saved to: {insights_path}\n")

    # Done
    print("=" * 50)
    print("ANALYSIS COMPLETE")
    print("=" * 50)
    print(f"\nOutput files:")
    print(f"  - {journey_path}")
    print(f"  - {insights_path}")
    print(f"\nNext step: Use Claude Code + Miro MCP to build the visual journey map.")
    print(f"  Open Claude Code and say:")
    print(f'  "Build a customer journey map on Miro using the data in output/"')


if __name__ == "__main__":
    main()
