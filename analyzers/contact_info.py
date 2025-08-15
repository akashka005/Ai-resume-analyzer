import re
import spacy

nlp = spacy.load("en_core_web_sm")

EMAIL_RE = re.compile(r'[\w\.-]+@[\w\.-]+\.\w+')
PHONE_RE = re.compile(r'(\+?\d{1,3}[\s-]?)?(\(?\d{3,4}\)?[\s-]?)?[\d\s-]{6,12}')

def extract_contact_info(text):
    contact = {
        "name": None,
        "email": None,
        "phone": None,
        "linkedin": None,
        "github": None,
        "location": None,
        "missing": []
    }
    lines = [l.strip() for l in text.splitlines() if l.strip()]
    if lines:
        candidate_name = lines[0]
        if EMAIL_RE.search(candidate_name) or PHONE_RE.search(candidate_name):
            candidate_name = lines[1] if len(lines)>1 else candidate_name
        if len(candidate_name.split()) <= 5:
            contact['name'] = candidate_name

    em = EMAIL_RE.search(text)
    if em: contact['email'] = em.group(0)
    ph = PHONE_RE.search(text)
    if ph:
        contact['phone'] = ph.group(0)
    if 'linkedin.com' in text.lower():
        m = re.search(r'(https?://)?(www\.)?linkedin\.com/[^\s,;]+', text, re.IGNORECASE)
        if m: contact['linkedin'] = m.group(0)
    if 'github.com' in text.lower():
        m = re.search(r'(https?://)?(www\.)?github\.com/[^\s,;]+', text, re.IGNORECASE)
        if m: contact['github'] = m.group(0)
    doc = nlp(text[:400])
    for ent in doc.ents:
        if ent.label_ in ('GPE','LOC'):
            contact['location'] = ent.text
            break
    for k in ['name','email','phone','linkedin']:
        if not contact.get(k):
            contact['missing'].append(k)

    return contact