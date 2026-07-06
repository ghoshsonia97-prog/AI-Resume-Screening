import re


# ======================================
# Clean Text
# ======================================

def clean_text(text):

    text = text.lower()

    text = re.sub(r'[^a-z0-9 ]', ' ', text)

    return text


# ======================================
# Extract Keywords from Job Description
# ======================================

def extract_keywords(job_description):

    keywords = [

        "python",
        "java",
        "c",
        "c++",
        "sql",
        "mysql",
        "mongodb",
        "excel",
        "power bi",
        "tableau",
        "machine learning",
        "deep learning",
        "tensorflow",
        "pytorch",
        "docker",
        "kubernetes",
        "aws",
        "azure",
        "gcp",
        "streamlit",
        "flask",
        "django",
        "react",
        "node.js",
        "html",
        "css",
        "javascript",
        "git",
        "github",
        "linux",
        "numpy",
        "pandas",
        "scikit-learn"
    ]

    text = clean_text(job_description)

    found = []

    for keyword in keywords:

        if keyword.lower() in text:

            found.append(keyword)

    return sorted(list(set(found)))


# ======================================
# Calculate ATS Score
# ======================================

def calculate_ats_score(resume_text, job_description):

    resume = clean_text(resume_text)

    required_keywords = extract_keywords(job_description)

    matched = []

    missing = []

    if len(required_keywords) == 0:

        return {
            "ats_score": 100,
            "matched_keywords": [],
            "missing_keywords": []
        }

    for keyword in required_keywords:

        if keyword.lower() in resume:

            matched.append(keyword)

        else:

            missing.append(keyword)

    score = round((len(matched) / len(required_keywords)) * 100)

    return {

        "ats_score": score,

        "matched_keywords": matched,

        "missing_keywords": missing

    }


# ======================================
# Recommendation
# ======================================

def ats_recommendation(score):

    if score >= 90:

        return "Excellent ATS Match"

    elif score >= 75:

        return "Strong ATS Match"

    elif score >= 60:

        return "Average ATS Match"

    else:

        return "Needs Improvement"