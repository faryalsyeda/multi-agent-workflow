# Multi-Agent Research and Outreach Workflow

A small, working demo of three agents working in sequence on one task:
research, write, then review.

## The agents

1. **Researcher** — finds the sample notes that match the topic, using
   keyword overlap. It only returns notes that exist in `sample_data/`.
2. **Writer** — turns those facts into a short outreach draft. It does
   not invent facts: every fact in the draft comes from a research
   note, with its source.
3. **Reviewer** — checks the draft before it is shown. It fails a draft
   that contains a price not in the facts, an email address that was
   not supplied, a guaranteed-result claim, a missing research fact,
   or more than 200 words.

## Honest limits

- These agents are rule-based functions, not LLM agents. The Writer
  does not generate new ideas; it assembles the facts it was given.
- Sample notes are fictional examples, not real market research. For
  a real client, replace `sample_data/` with that client's notes.
- A real LLM writer and reviewer can be added later, keeping the same
  checks in place.

## Run it

```bash
python3 workflow.py --topic "lead generation" --audience "small cafes"
python3 workflow.py --topic "follow-up automation" --audience "real estate teams"
```

## Optional API demo

```bash
pip install -r requirements.txt
uvicorn app:app --reload
```

Then send:

```json
POST /run
{"topic": "lead generation", "audience": "small cafes"}
```

## Files

- `workflow.py` — the three agents and the command-line tool
- `app.py` — optional FastAPI demo
- `sample_data/notes.txt` — fictional sample research notes
- `requirements.txt` — FastAPI and Uvicorn, only needed for the API demo
