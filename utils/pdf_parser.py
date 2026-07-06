import pdfplumber
import re


# ======================================
# Extract Full Text from PDF
# ======================================

def extract_text_from_pdf(uploaded_file):
    """
    Extracts all text from a PDF file.

    Returns:
        str
    """

    text = ""

    try:
        with pdfplumber.open(uploaded_file) as pdf:

            for page in pdf.pages:

                page_text = page.extract_text()

                if page_text:
                    text += page_text + "\n"

    except Exception as e:

        print("PDF Error:", e)

    return text


# ======================================
# Extract Email
# ======================================

def extract_email(text):

    pattern = r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}"

    emails = re.findall(pattern, text)

    return emails[0] if emails else "Not Found"


# ======================================
# Extract Phone Number
# ======================================

def extract_phone(text):

    pattern = r"(?:\+91[\-\s]?)?[6-9]\d{9}"

    phones = re.findall(pattern, text)

    return phones[0] if phones else "Not Found"


# ======================================
# Extract Name
# ======================================

def extract_name(text):

    lines = text.split("\n")

    for line in lines:

        line = line.strip()

        if len(line.split()) >= 2 and len(line.split()) <= 4:

            if "resume" not in line.lower():

                return line

    return "Unknown"


# ======================================
# Extract Skills
# ======================================

SKILL_DATABASE = [

    "Python",
    "Java",
    "C",
    "C++",
    "SQL",
    "MySQL",
    "MongoDB",
    "Machine Learning",
    "Deep Learning",
    "TensorFlow",
    "PyTorch",
    "Docker",
    "Kubernetes",
    "AWS",
    "Azure",
    "GCP",
    "Power BI",
    "Tableau",
    "Excel",
    "Git",
    "GitHub",
    "HTML",
    "CSS",
    "JavaScript",
    "React",
    "Node.js",
    "Flask",
    "Django",
    "Streamlit",
    "Pandas",
    "NumPy",
    "Scikit-learn"
]


def extract_skills(text):

    found = []

    text = text.lower()

    for skill in SKILL_DATABASE:

        if skill.lower() in text:

            found.append(skill)

    return sorted(list(set(found)))


# ======================================
# Extract Education
# ======================================

def extract_education(text):

    education_keywords = [

        "B.Tech",
        "B.E",
        "Bachelor",
        "M.Tech",
        "M.E",
        "Master",
        "MBA",
        "BCA",
        "MCA",
        "B.Sc",
        "M.Sc",
        "Diploma",
        "PhD"

    ]

    for keyword in education_keywords:

        if keyword.lower() in text.lower():

            return keyword

    return "Not Found"


# ======================================
# Candidate Information
# ======================================

def extract_candidate_information(uploaded_file):

    text = extract_text_from_pdf(uploaded_file)

    return {

        "name": extract_name(text),

        "email": extract_email(text),

        "phone": extract_phone(text),

        "education": extract_education(text),

        "skills": extract_skills(text),

        "resume_text": text

    }