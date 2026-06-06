import re
import json

with open("judgment_text.txt", "r", encoding="utf-8") as f:
    text = f.read()

markers = [
    "FACTUAL BACKGROUND",
    "SUBMISSIONS OF THE PARTIES",
    "ANALYSIS",
    "CONCLUSION"
]

positions = {}

for marker in markers:
    matches = list(re.finditer(marker, text))

    if len(matches) < 2:
        raise Exception(f"Could not find actual section for {marker}")

    # Skip index occurrence and take actual section
    positions[marker] = matches[1].start()

facts_start = positions["FACTUAL BACKGROUND"]
submissions_start = positions["SUBMISSIONS OF THE PARTIES"]
analysis_start = positions["ANALYSIS"]
conclusion_start = positions["CONCLUSION"]

facts = text[facts_start:submissions_start]

submissions = text[submissions_start:analysis_start]

analysis = text[analysis_start:conclusion_start]

conclusion = text[conclusion_start:]

print("Facts Length:", len(facts))
print("Submissions Length:", len(submissions))
print("Analysis Length:", len(analysis))
print("Conclusion Length:", len(conclusion))

data = {
    "facts": facts,
    "submissions": submissions,
    "analysis": analysis,
    "conclusion": conclusion
}

with open(
    "structured_judgment.json",
    "w",
    encoding="utf-8"
) as f:
    json.dump(data, f, indent=4)

print("\nStructured judgment saved.")