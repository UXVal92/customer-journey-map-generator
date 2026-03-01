# Customer Journey Map Generator

Transform customer call transcripts into a visual Customer Journey Map on Miro, using AI agents and the Miro MCP.

![Sample Miro board output](Screenshot%202026-03-01%20011540.png)

> Read the full write-up: [I Built an AI Workflow That Turns Call Transcripts Into a Customer Journey Map on Miro](https://medium.com/@milanavalerio) *(link to be updated)*

## How it works

```
Call Transcripts (input)
         │
         ▼
┌─────────────────────────┐
│ Agent 1: Transcript      │
│ Analyzer                 │
│ Reads transcripts,       │
│ extracts structured      │
│ journey data             │
└────────────┬────────────┘
             │
             ▼
┌─────────────────────────┐
│ Agent 2: Insights        │
│ Summarizer               │
│ Generates prioritised    │
│ insights and actions     │
└────────────┬────────────┘
             │
             ▼
     JSON output files
             │
             ▼
┌─────────────────────────┐
│ Claude Code + Miro MCP   │
│ Creates visual journey   │
│ map with tables, docs,   │
│ and formatted content    │
└────────────┬────────────┘
             │
             ▼
   Miro Board (output)
```

## What you get

A Customer Journey Map on Miro with:

- **Journey map table**: 6 stages (Awareness → Consideration → Purchase → Onboarding → Retention → Advocacy) × 6 dimensions (Touchpoints, Actions, Thinking, Emotions, Pain Points, Opportunities)
- **Insights document**: The Good / The Bad / The Ugly findings, critical insights with impact analysis, and priority actions ranked by impact and effort

## Setup

### 1. Clone the repo

```bash
git clone https://github.com/UXVal92/customer-journey-map-generator.git
cd customer-journey-map-generator
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure environment

```bash
cp .env.example .env
```

Edit `.env` and add your `ANTHROPIC_API_KEY` from [console.anthropic.com](https://console.anthropic.com/).

### 4. Add your transcripts

Place your call transcripts in `transcripts/` as a markdown file. See `transcripts/pawbox_transcripts.md` for the expected format.

### 5. Run the analysis

```bash
python run.py                           # Uses sample transcripts
python run.py transcripts/my_calls.md   # Uses your own
```

This generates two JSON files in `output/`:
- `journey_data.json` — structured journey map data
- `insights_summary.json` — prioritised insights and actions

### 6. Build the Miro board

Install the Miro MCP in Claude Code:

```bash
claude mcp add --transport http miro https://mcp.miro.com
```

Then in Claude Code, say:

> Build a customer journey map on my Miro board using the data in output/

Claude will use the Miro MCP to create a formatted table and insights document on your board.

## Sample output

The included sample uses **PawBox**, a fictitious pet food subscription, with 6 customer call transcripts covering the full journey from discovery to advocacy.

## Tech stack

- **Claude API** (Anthropic) — powers the transcript analysis and insight generation
- **Miro MCP** — creates the visual board elements (tables, documents)
- **Python** — orchestrates the agent pipeline

## Project structure

```
├── run.py                  # Main orchestrator (Agents 1 & 2)
├── agents/
│   ├── transcript_analyzer.py   # Agent 1: Extracts journey data
│   ├── insights_summarizer.py   # Agent 2: Generates insights
├── transcripts/
│   └── pawbox_transcripts.md    # Sample call transcripts
├── output/                      # Generated JSON (gitignored)
├── requirements.txt
├── .env.example
└── README.md
```

## Get the ready-to-run template

Want to skip the setup? [Get the template on Gumroad](https://milanavalerio.gumroad.com) *(link to be updated)* for £5. Includes everything pre-configured with sample transcripts and output.

## Licence

MIT — use it however you like.
