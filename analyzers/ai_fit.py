def compute_ai_fit_score(skills, experience, education, format_check, ats):
    score = 0
    popular = ['python','sql','aws','docker','react','tensorflow']
    found_pop = sum(1 for p in popular if p in skills['technical'])
    skills_score = (found_pop / len(popular)) * 100
    exp_score = 50
    if experience['positions']:
        exp_score += min(50, len(experience['positions'])*10)
    exp_score = min(100, exp_score)
    edu_score = 100 if education['degrees'] else 30
    fmt_score = 100 if not format_check.get('warnings') else 60
    final = round((skills_score*0.4 + exp_score*0.3 + edu_score*0.15 + fmt_score*0.15),2)
    breakdown = {
        "skills_score": round(skills_score,2),
        "experience_score": round(exp_score,2),
        "education_score": edu_score,
        "format_score": fmt_score
    }
    return {"final_score": final, "breakdown": breakdown}