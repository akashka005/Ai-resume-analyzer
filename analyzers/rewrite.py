import re

WEAK_TO_STRONG = {
    "responsible for": "led",
    "worked on": "built",
    "involved in": "contributed to",
    "helped": "improved",
    "did": "implemented"
}

def rewrite_line(line):
    l = line
    for weak, strong in WEAK_TO_STRONG.items():
        l = re.sub(re.escape(weak), strong, l, flags=re.IGNORECASE)
    if any(w in l.lower() for w in ['improved','increased','reduced','decreased']) and not re.search(r'\d+%', l):
        l = l + " (e.g., improved by X% — quantify if possible)"
    return l

def rewrite_resume_sections(raw_text, experience_obj):
    rewrites = {"experience_rewrites": []}
    for pos in experience_obj['positions']:
        raw = pos.get('raw','')
        new = rewrite_line(raw)
        if new != raw:
            rewrites['experience_rewrites'].append({"original": raw, "suggested": new})
    lines = [l for l in raw_text.splitlines() if l.strip()]
    summary = " ".join(lines[:3]) if lines else ""
    rewrites['summary_suggestion'] = f"Rewrite suggestion: {summary[:200]} — make it concise, start with role + years + top skills."
    return rewrites