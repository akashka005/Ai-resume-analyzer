import re
from dateutil import parser

ACTION_VERBS = ["developed","designed","implemented","improved","led","managed","built","optimized","reduced","increased","created","launched","architected","automated","streamlined","collaborated","mentored"]

DATE_RE = re.compile(r'((?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z]*\.?\s+\d{4})|(\d{4})', re.IGNORECASE)

def parse_experience(text):
    ex = {"positions": [], "gaps": [], "weak_phrases": [], "action_verb_score": 0}
    lines = [l.strip() for l in text.splitlines() if l.strip()]
    exp_lines = []
    start = False
    for l in lines:
        if any(k in l.lower() for k in ['experience','work experience','professional experience','employment']):
            start = True
            continue
        if start:
            exp_lines.append(l)
    if not exp_lines:
        for l in lines:
            if re.search(r'\d{4}.*[-–].*\d{4}|\d{4}\s*-\s*Present', l):
                exp_lines.append(l)
    for l in exp_lines[:60]:
        dates = DATE_RE.findall(l)
        years = [m[0] or m[1] for m in dates if m]
        parts = re.split(r'\s+\|\s+|\s+at\s+| - ', l)
        title = parts[0] if parts else l
        company = parts[1] if len(parts)>1 else None
        ex['positions'].append({
            "raw": l,
            "title": title,
            "company": company,
            "years": years
        })
    total_actions = 0
    words = text.lower().split()
    for v in ACTION_VERBS:
        total_actions += words.count(v)
    ex['action_verb_score'] = total_actions
    if total_actions < 3:
        ex['weak_phrases'].append("Few action verbs found — consider stronger action verbs and quantifying results.")
    years_flat = []
    for p in ex['positions']:
        for y in p['years']:
            try:
                years_flat.append(int(re.sub(r'[^\d]','',y)))
            except:
                pass
    years_flat = sorted(set([y for y in years_flat if y>1900 and y<2100]))
    if years_flat:
        for i in range(len(years_flat)-1):
            if years_flat[i+1] - years_flat[i] > 4:
                ex['gaps'].append(f"Gap detected between {years_flat[i]} and {years_flat[i+1]}")
    return ex