from fpdf import FPDF
from io import BytesIO
import pandas as pd
import streamlit as st


# ======================================
# PDF REPORT GENERATOR
# ======================================

class ResumePDF(FPDF):

    def header(self):
        self.set_font("Arial", "B", 16)
        self.cell(0, 10, "AI Resume Screening Report", ln=True, align="C")
        self.ln(5)

    def section_title(self, title):
        self.set_font("Arial", "B", 12)
        self.cell(0, 8, title, ln=True)

    def section_body(self, text):
        self.set_font("Arial", "", 11)
        self.multi_cell(0, 6, str(text))
        self.ln(2)


def generate_candidate_pdf(candidate):

    pdf = ResumePDF()

    pdf.add_page()

    pdf.section_title("Candidate Information")

    pdf.section_body(f"Name : {candidate.get('candidate_name','')}")

    pdf.section_body(f"Match Score : {candidate.get('match_score',0)}%")

    pdf.section_body(f"ATS Score : {candidate.get('ats_score',0)}%")

    pdf.section_body(f"Recommendation : {candidate.get('recommendation','')}")

    pdf.section_body(f"Experience : {candidate.get('experience_level','')}")

    pdf.section_body(f"Education : {candidate.get('education','')}")

    pdf.section_title("Summary")

    pdf.section_body(candidate.get("summary",""))

    pdf.section_title("Matched Skills")

    pdf.section_body(", ".join(candidate.get("matched_skills",[])))

    pdf.section_title("Missing Skills")

    pdf.section_body(", ".join(candidate.get("missing_skills",[])))

    pdf.section_title("Resume Improvements")

    improvements = "\n".join(candidate.get("resume_improvements",[]))

    pdf.section_body(improvements)

    pdf.section_title("Projects")

    pdf.section_body(", ".join(candidate.get("projects",[])))

    pdf.section_title("Certifications")

    pdf.section_body(", ".join(candidate.get("certifications",[])))

    pdf.section_title("Interview Questions")

    questions = "\n".join(candidate.get("interview_questions",[]))

    pdf.section_body(questions)

    pdf.section_title("Salary Prediction")

    pdf.section_body(candidate.get("salary_prediction",""))

    pdf_bytes = pdf.output(dest="S")

    if isinstance(pdf_bytes, str):
        pdf_bytes = pdf_bytes.encode("latin-1")

    return pdf_bytes


# ======================================
# DOWNLOAD PDF BUTTON
# ======================================

def pdf_download_button(candidate):

    pdf = generate_candidate_pdf(candidate)

    st.download_button(
        label="📄 Download PDF Report",
        data=pdf,
        file_name=f"{candidate['candidate_name']}_Report.pdf",
        mime="application/pdf"
    )


# ======================================
# EXCEL REPORT
# ======================================

def generate_excel(df):

    output = BytesIO()

    with pd.ExcelWriter(output, engine="openpyxl") as writer:

        df.to_excel(writer, index=False)

    return output.getvalue()


# ======================================
# DOWNLOAD EXCEL BUTTON
# ======================================

def excel_download_button(df):

    excel = generate_excel(df)

    st.download_button(
        label="📊 Download Excel Report",
        data=excel,
        file_name="Resume_Analysis.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )