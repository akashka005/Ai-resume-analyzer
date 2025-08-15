import re
import spacy
nlp = spacy.load("en_core_web_sm")

DEGREE_KEYWORDS = ['bachelor','b.sc','b.s','bs','btech','b.e','master','m.sc','m.s','mba','phd','associate','diploma']

def analyze_education(text):
    ed = {"degrees": [], "flags": [], "raw": []}
    lines = [l.strip() for l in text.splitlines() if l.strip()]
    for line in lines:
        low = line.lower()
        if any(k in low for k in DEGREE_KEYWORDS) or 'university' in low or 'college' in low:
            ed['raw'].append(line)
            year = re.search(r'(20\d{2}|19\d{2})', line)
            deg = None
            for k in DEGREE_KEYWORDS:
                if k in low:
                    deg = k
                    break
            ed['degrees'].append({
                "line": line,
                "degree_hint": deg,
                "year": int(year.group(0)) if year else None
            })
    if not ed['degrees']:
        ed['flags'].append("No clear education section found")
    else:
        for d in ed['degrees']:
            if not d['year']:
                ed['flags'].append(f"Missing graduation year in '{d['line'][:40]}...'")
    return ed