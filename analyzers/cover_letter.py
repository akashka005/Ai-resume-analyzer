def generate_cover_letter(contact, jd_text, skills):
    name = contact.get('name') or "Candidate"
    intro = f"Dear Hiring Manager,\n\nI am {name}, and I am excited to apply for this role. I bring relevant experience in {', '.join(skills.get('technical', [])[:5])} and a track record of delivering measurable impact."
    body = "\n\nBased on the job description, I match the following key requirements:\n"
    jd_matches = skills.get('technical', [])[:8]
    body += "\n".join(f"- {m}" for m in jd_matches)
    closing = "\n\nI would love to discuss how I can contribute. Thank you for considering my application.\n\nSincerely,\n" + name
    return intro + body + closing