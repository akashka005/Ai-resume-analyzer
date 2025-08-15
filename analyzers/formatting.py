from textstat import flesch_reading_ease

def formatting_checks(text):
    # naive checks: presence of bullets, section headers, tables (tabs), images (not in plain text)
    checks = {"sections_present": [], "warnings": []}
    lower = text.lower()
    for sec in ['experience','education','skills','projects','certifications','summary','professional summary','contact']:
        if sec in lower:
            checks['sections_present'].append(sec)
    if 'skills' not in lower:
        checks['warnings'].append("Skills section missing")
    # bullet consistency
    bullets = any(ch in text for ch in ['•','-','*'])
    if not bullets:
        checks['warnings'].append("No bullets detected — use bullets for achievements")
    # font uniformity can't be checked in plain text; flag if many short lines that look like headings
    return checks

def readability_score(text):
    try:
        score = flesch_reading_ease(text)
    except:
        score = None
    return {"flesch_reading_ease": score}