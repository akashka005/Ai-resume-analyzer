import os
from flask import Flask, render_template, request, send_file, redirect, url_for
from utils.file_parser import extract_text_from_file
from analyzers.contact_info import extract_contact_info
from analyzers.education import analyze_education
from analyzers.experience import parse_experience
from analyzers.skills import extract_and_categorize_skills
from analyzers.ats_scoring import score_keywords
from analyzers.formatting import formatting_checks, readability_score
from analyzers.ai_fit import compute_ai_fit_score
from analyzers.rewrite import rewrite_resume_sections
from analyzers.final_resume import generate_final_docx
from analyzers.cover_letter import generate_cover_letter
from utils.resources import learning_resources

UPLOAD_FOLDER = 'static/uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
ALLOWED_EXT = {'pdf','docx','txt'}

def allowed_file(fn):
    return '.' in fn and fn.rsplit('.',1)[1].lower() in ALLOWED_EXT

@app.route('/', methods=['GET','POST'])
def index():
    return render_template('index.html')

@app.route('/analyze', methods=['POST'])
def analyze():
    resume_file = request.files.get('resume')
    jd_text = request.form.get('jobdesc','').strip()
    if not resume_file or resume_file.filename == '' or not allowed_file(resume_file.filename):
        return redirect(url_for('index'))

    save_path = os.path.join(app.config['UPLOAD_FOLDER'], resume_file.filename)
    resume_file.save(save_path)
    raw_text = extract_text_from_file(save_path)
    contact = extract_contact_info(raw_text)
    education = analyze_education(raw_text)
    experience = parse_experience(raw_text)
    skills = extract_and_categorize_skills(raw_text)
    ats = score_keywords(raw_text, jd_text)
    format_check = formatting_checks(raw_text)
    readability = readability_score(raw_text)
    ai_fit = compute_ai_fit_score(skills, experience, education, format_check, ats)
    rewrites = rewrite_resume_sections(raw_text, experience)
    final_docx_path = generate_final_docx(contact, education, experience, skills, rewrites, filename='optimized_resume.docx')
    cover_letter = generate_cover_letter(contact, jd_text, skills)
    resources = learning_resources(skills['missing_skills_short'])
    results = {
        "contact": contact,
        "education": education,
        "experience": experience,
        "skills": skills,
        "ats": ats,
        "format_check": format_check,
        "readability": readability,
        "ai_fit": ai_fit,
        "rewrites": rewrites,
        "final_docx": final_docx_path,
        "cover_letter": cover_letter,
        "resources": resources
    }

    return render_template('results.html', results=results)

@app.route('/download/<path:filename>')
def download_file(filename):
    return send_file(filename, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)