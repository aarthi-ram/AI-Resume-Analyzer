from flask import Flask, render_template, request, jsonify
from pypdf import PdfReader
from docx import Document
import os

app = Flask(__name__)

SKILLS = [
    "python",
    "java",
    "javascript",
    "html",
    "css",
    "sql",
    "react",
    "node.js",
    "flask",
    "django",
    "machine learning",
    "deep learning",
    "artificial intelligence",
    "data science",
    "tensorflow",
    "pytorch",
    "git",
    "mongodb",
    "mysql",
    "power bi",
    "aws",
    "docker"
]


def extract_pdf(file):
    reader = PdfReader(file)

    text = ""

    for page in reader.pages:
        page_text = page.extract_text()

        if page_text:
            text += page_text + "\n"

    return text


def extract_docx(file):
    document = Document(file)

    text = ""

    for paragraph in document.paragraphs:
        text += paragraph.text + "\n"

    return text


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/analyze", methods=["POST"])
def analyze():

    if "resume" not in request.files:
        return jsonify({
            "error": "Please upload your resume."
        }), 400

    file = request.files["resume"]

    if file.filename == "":
        return jsonify({
            "error": "Please select a resume file."
        }), 400

    filename = file.filename.lower()

    try:

        if filename.endswith(".pdf"):
            resume_text = extract_pdf(file)

        elif filename.endswith(".docx"):
            resume_text = extract_docx(file)

        elif filename.endswith(".txt"):
            resume_text = file.read().decode("utf-8")

        else:
            return jsonify({
                "error": "Only PDF, DOCX and TXT files are supported."
            }), 400

        resume_text_lower = resume_text.lower()

        found_skills = []

        for skill in SKILLS:
            if skill in resume_text_lower:
                found_skills.append(skill.title())

        score = int(
            (len(found_skills) / len(SKILLS)) * 100
        )

        if score >= 70:

            recommendation = (
                "Excellent! Your resume has strong technical "
                "skill coverage."
            )

        elif score >= 40:

            recommendation = (
                "Good foundation. Add more relevant technical "
                "skills and projects."
            )

        else:

            recommendation = (
                "Improve your technical skills and add more "
                "relevant projects."
            )

        return jsonify({
            "filename": file.filename,
            "score": score,
            "skills": found_skills,
            "recommendation": recommendation
        })

    except Exception as e:

        return jsonify({
            "error": "Could not read the uploaded resume: " + str(e)
        }), 500


if __name__ == "__main__":
    app.run(debug=True)