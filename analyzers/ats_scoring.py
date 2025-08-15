import re
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def tokenize(text):
    return re.findall(r'\w+', text.lower())

def score_keywords(resume_text, job_description):
    if not job_description or job_description.strip()=="":
        return {"match_percent": None, "matched_terms": [], "missing_terms": []}
    resume_text = resume_text.lower()
    jd = job_description.lower()
    r_tokens = set(tokenize(resume_text))
    jd_tokens = set(tokenize(jd))
    matched = sorted([t for t in jd_tokens if t in r_tokens])
    missing = sorted([t for t in jd_tokens if t not in r_tokens])
    match_percent = round((len(matched)/max(1,len(jd_tokens)))*100,2)
    vec = CountVectorizer().fit_transform([resume_text, jd])
    sim = cosine_similarity(vec)[0,1]
    return {"match_percent": match_percent, "matched_terms": matched[:80], "missing_terms": missing[:80], "similarity": float(sim)}