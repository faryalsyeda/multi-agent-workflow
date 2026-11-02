"""Multi-Agent Research and Outreach Workflow (demo).

Three small agents work in sequence on one task:

1. Researcher: finds facts about a topic in local sample notes.
2. Writer: turns those facts into a short outreach draft.
3. Reviewer: checks the draft for problems before it is shown.

This demo uses rule-based agents from the Python standard library
only. It does not use an LLM, so the Writer does not invent facts:
every fact in the draft comes from a research note, with its source,
and the Reviewer rejects a draft that contains a price, a guessed
contact, or a fact with no source.

Run:
    python3 workflow.py --topic "lead generation" --audience "small cafes"
    python3 workflow.py --topic "follow-up automation" --audience "real estate teams"

Sample notes live in data/. Replace that folder with a client's own
research notes to use it on real content. Sample notes are fictional
examples, not real market research.
"""

import argparse
import os
import re


def load_notes(data_dir):
    notes = []
    for filename in sorted(os.listdir(data_dir)):
        if not filename.endswith(".txt"):
            continue
        with open(os.path.join(data_dir, filename), encoding="utf-8") as f:
            text = f.read()
        for line in text.splitlines():
            line = line.strip()
            if line and not line.startswith("#"):
                notes.append({"source": filename, "text": line})
    return notes


def tokenize(text):
    stopwords = {"a", "an", "the", "is", "are", "for", "and", "or", "of",
                 "to", "in", "on", "with", "small", "what", "how"}
    words = re.findall(r"[a-z0-9]+", text.lower())
    return [w for w in words if w not in stopwords]


def researcher(topic, notes, top_n=3):
    """Agent 1: return the notes that best match the topic."""
    topic_tokens = set(tokenize(topic))
    scored = []
    for note in notes:
        note_tokens = set(tokenize(note["text"]))
        overlap = len(topic_tokens & note_tokens)
        if overlap:
            scored.append((overlap, note))
    scored.sort(key=lambda item: item[0], reverse=True)
    return [note for _, note in scored[:top_n]]


def writer(topic, audience, facts):
    """Agent 2: draft a short outreach message from the facts only."""
    lines = [f"Hi, I help {audience} with {topic}.", ""]
    if facts:
        lines.append("From recent notes on this topic:")
        for fact in facts:
            lines.append(f"- {fact['text']} (source: {fact['source']})")
        lines.append("")
    lines.append(
        "Would a short demo help? Reply with your main problem and I "
        "will show a small example for your business, with no obligation."
    )
    return "\n".join(lines)


def reviewer(draft, facts):
    """Agent 3: check the draft. Returns (passed, issues)."""
    issues = []
    if "$" in draft or "price" in draft.lower() and "no price" not in draft.lower():
        # A price in the draft is only allowed if it is quoted from a fact.
        if not any("$" in f["text"] for f in facts):
            issues.append("Draft contains a price that is not in the research facts.")
    if "@" in draft:
        issues.append("Draft contains an email address that was not supplied.")
    if "guaranteed" in draft.lower():
        issues.append("Draft claims a guaranteed result.")
    for fact in facts:
        if fact["text"] not in draft:
            issues.append(f"Research fact missing from draft: {fact['text'][:40]}...")
    if len(draft.split()) > 200:
        issues.append("Draft is over 200 words; shorten it.")
    return (not issues), issues


def run_workflow(topic, audience, data_dir):
    notes = load_notes(data_dir)
    facts = researcher(topic, notes)
    draft = writer(topic, audience, facts)
    passed, issues = reviewer(draft, facts)
    return {"topic": topic, "audience": audience, "facts": facts,
            "draft": draft, "review_passed": passed, "review_issues": issues}


def main():
    parser = argparse.ArgumentParser(description="Run the multi-agent workflow.")
    parser.add_argument("--topic", required=True)
    parser.add_argument("--audience", required=True)
    parser.add_argument("--data", default="sample_data")
    args = parser.parse_args()

    data_dir = args.data
    if not os.path.isdir(data_dir):
        data_dir = os.path.join(os.path.dirname(__file__), "sample_data")
    result = run_workflow(args.topic, args.audience, data_dir)

    print(f"Topic: {result['topic']}  |  Audience: {result['audience']}\n")
    print("Researcher found:")
    for fact in result["facts"]:
        print(f"- [{fact['source']}] {fact['text']}")
    print("\nWriter draft:\n")
    print(result["draft"])
    print("\nReviewer verdict:", "PASS" if result["review_passed"] else "FAIL")
    for issue in result["review_issues"]:
        print(f"- {issue}")


if __name__ == "__main__":
    main()
