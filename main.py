from flask import Flask, render_template, request, send_file
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib.units import inch
import os

app = Flask(__name__)


# ---------------- HOME ----------------
@app.route('/')
def home():
    return render_template("index.html")


# ---------------- ANALYZE ----------------
@app.route('/analyze', methods=['POST'])
def analyze():

    name = request.form['name']
    skills = request.form['skills']
    education = request.form['education']
    experience = request.form['experience']

    skill_list = skills.lower()

    # Career Suggestion Logic
    if "python" in skill_list:
        career = "Software Developer / AI Engineer"
        required_skills = ["DSA", "Flask", "APIs", "Git"]
    elif "cybersecurity" in skill_list:
        career = "Cybersecurity Analyst"
        required_skills = ["Networking", "Linux", "Penetration Testing", "SIEM"]
    elif "data" in skill_list:
        career = "Data Scientist"
        required_skills = ["Machine Learning", "Statistics", "SQL", "Visualization"]
    else:
        career = "Software Engineer"
        required_skills = ["Problem Solving", "System Design", "Git"]

    # ATS Score Calculation
    score = 50

    if "python" in skill_list:
        score += 15
    if "data" in skill_list:
        score += 10
    if "cybersecurity" in skill_list:
        score += 15
    if experience:
        score += 10
    if len(skills.split(",")) >= 3:
        score += 10

    if score > 95:
        score = 95

    # Skill Gap Analysis
    user_skills = [s.strip().lower() for s in skills.split(",")]
    missing_skills = []

    for rs in required_skills:
        if rs.lower() not in user_skills:
            missing_skills.append(rs)

    return render_template(
        "dashboard.html",
        name=name,
        education=education,
        skills=skills,
        ats_score=score,
        career_suggestions=[career],
        missing_skills=missing_skills
    )


# ---------------- DOWNLOAD REPORT ----------------
@app.route('/download-report')
def download_report():

    file_name = "Resume_Report.pdf"
    doc = SimpleDocTemplate(file_name)
    elements = []
    styles = getSampleStyleSheet()

    elements.append(Paragraph("VidhyaAI Resume Report", styles['Title']))
    elements.append(Spacer(1, 0.5 * inch))

    doc.build(elements)

    return send_file(file_name, as_attachment=True)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
