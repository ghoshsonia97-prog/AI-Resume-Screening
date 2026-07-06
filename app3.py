"""
Combined app.py (starter)
NOTE: This is the merged version of Parts 1–5 with an enterprise-grade professional UI.
"""
import streamlit as st
import pandas as pd
import os

from utils.gemini_analysis import analyze_resume
from utils.pdf_parser import extract_candidate_information
from utils.analytics import (
    create_dataframe,
    show_kpis,
    match_score_chart,
    recommendation_chart,
    skills_chart,
    radar_chart
)
from utils.generator import (
    excel_download_button,
    pdf_download_button
)
from utils.ats import calculate_ats_score

# 1. Page Global Setup
st.set_page_config(
    page_title="Next-Gen AI Resume Screener", 
    page_icon="💼",
    layout="wide"
)

# 2. Premium Professional Custom CSS Styling Injection
st.markdown("""
    <style>
        /* Main Workspace Optimization */
        .main .block-container { padding-top: 1.5rem; padding-bottom: 2rem; }
        h1, h2, h3 { font-family: 'Inter', system-ui, -apple-system, sans-serif; font-weight: 700; color: #1E293B; }
        
        /* Premium Card UI for Dashboard and Lists */
        .recruiter-card {
            background-color: #FFFFFF;
            padding: 1.5rem;
            border-radius: 10px;
            border: 1px solid #E2E8F0;
            box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.05);
            margin-bottom: 1.25rem;
        }
        
        /* Form container wrapper */
        div[data-testid="stForm"] {
            border: 1px solid #E2E8F0;
            border-radius: 12px;
            padding: 2rem;
            background-color: #FFFFFF;
            box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.05);
        }
        
        /* Subtle Typography enhancements */
        .section-header {
            color: #475569;
            font-size: 0.95rem;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            margin-bottom: 0.5rem;
            font-weight: 600;
        }
    </style>
""", unsafe_allow_html=True)

# 3. Session State Core Setup
if "analysis_results" not in st.session_state:
    st.session_state.analysis_results = []
if "recruiter_notes" not in st.session_state:
    st.session_state.recruiter_notes = {}
if "trigger_balloons" not in st.session_state:
    st.session_state.trigger_balloons = False

# Safe Balloon Animation Trigger check
if st.session_state.trigger_balloons:
    st.balloons()
    st.session_state.trigger_balloons = False

# 4. Clean Sidebar Configuration
with st.sidebar:
    st.markdown("<h2 style='margin-bottom:0;'>💼 ATS Core AI</h2>", unsafe_allow_html=True)
    st.markdown("<p style='color:#64748B; font-size:0.85rem;'>Talent Assessment Platform</p>", unsafe_allow_html=True)
    st.markdown("---")
    page = st.radio("Navigation Workspace", ["Dashboard", "Resume Screening", "Recruiter"])
    st.markdown("---")
    
    # --- Inconspicuous Kaggle Dataset Loader Utility Integration ---
    st.markdown("### 📊 Kaggle Dataset Loader")
    csv_path = st.text_input("CSV File Path", value="ai_resume_screening.csv", key="kaggle_csv_path")
    
    if st.button("📥 Load Kaggle Dataset", use_container_width=True):
        if os.path.exists(csv_path):
            try:
                raw_df = pd.read_csv(csv_path)
                mapped_results = []
                for idx, row in raw_df.iterrows():
                    name = row.get("candidate_name") or row.get("Name") or f"Candidate {idx+1}"
                    resume_text = row.get("resume_text") or row.get("Resume") or ""
                    
                    score_val = row.get("ats_score") or row.get("Score") or row.get("match_score") or 70
                    ats_score = int(score_val)
                    rec_tier = str(row.get("recommendation") or row.get("Category") or "Good Fit")
                    
                    record = {
                        "candidate_name": name,
                        "email": row.get("email", "N/A"),
                        "phone": row.get("phone", "N/A"),
                        "education": row.get("education", "N/A"),
                        "detected_skills": str(row.get("skills", "")).split(",") if "skills" in row else [],
                        "summary": row.get("summary", "Historical dataset entry - automated extraction snapshot."),
                        "ats_score": ats_score,
                        "match_score": ats_score,
                        "recommendation": rec_tier,
                        "matched_skills": str(row.get("matched_skills", "Python,Data Analysis")).split(","),
                        "missing_skills": str(row.get("missing_skills", "Cloud Architecture")).split(","),
                        "matched_keywords": str(row.get("matched_keywords", "Agile,SQL")).split(","),
                        "missing_keywords": str(row.get("missing_keywords", "Docker")).split(",")
                    }
                    mapped_results.append(record)
                
                st.session_state.analysis_results = mapped_results
                st.session_state.trigger_balloons = True
                st.rerun()
            except Exception as e:
                st.error(f"Data mapping mismatch: {e}")
        else:
            st.error(f"Target file path variant not found at: {csv_path}")
            
    st.markdown("---")
    st.caption("v2.5.0 • Powered by Groq Llama Architecture")

results = st.session_state.analysis_results

# ==========================================
# WORKSPACE: RESUME SCREENING
# ==========================================
if page == "Resume Screening":
    st.markdown("<h1>📄 Resume Screening & Analysis Pipeline</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color: #64748B;'>Upload candidate profiles to batch-parse metrics directly against tracking criteria.</p>", unsafe_allow_html=True)
    st.markdown("---")

    # Using an explicit form ensures the text entry and files stay intact without unpredictable re-runs
    with st.form("screening_pipeline_form"):
        col1, col2 = st.columns([1, 1], gap="large")
        
        with col1:
            st.markdown("<h3 style='color: #1E293B; margin-bottom: 0.2rem;'>📥 Ingestion Layer</h3>", unsafe_allow_html=True)
            st.markdown("<p style='color: #64748B; font-size: 0.85rem; margin-bottom: 1rem;'>Upload Target Candidate Profiles (PDF Format)</p>", unsafe_allow_html=True)
            files = st.file_uploader(
                "Upload Layer Ingestion Portal",
                type=["pdf"],
                accept_multiple_files=True,
                label_visibility="collapsed",
                help="Supports standard and parsing vector PDF structures."
            )

        with col2:
            st.markdown("<h3 style='color: #1E293B; margin-bottom: 0.2rem;'>🎯 Context Criteria</h3>", unsafe_allow_html=True)
            st.markdown("<p style='color: #64748B; font-size: 0.85rem; margin-bottom: 1rem;'>Core Job Description Context</p>", unsafe_allow_html=True)
            jd = st.text_area(
                "Core Context Ingestion Area",
                placeholder="Paste operational roles, requirements, or skills matrices here...",
                height=165,
                label_visibility="collapsed"
            )
        
        st.markdown("<br>", unsafe_allow_html=True)
        submit_btn = st.form_submit_button("🚀 Execute Analysis Pipeline", use_container_width=True, type="primary")

    # Evaluate validation conditions safely upon execution request
    if submit_btn:
        if files and jd:
            out = []
            prog = st.progress(0)
            status_message = st.empty()

            for i, file in enumerate(files):
                status_message.markdown(f"⏳ Processing profile **{file.name}** ({i+1}/{len(files)})...")
                
                candidate = extract_candidate_information(file)
                ats = calculate_ats_score(candidate["resume_text"], jd)
                analysis = analyze_resume(candidate["resume_text"], jd)

                # Map Payload Structured Variables
                analysis["candidate_name"] = candidate["name"] if candidate["name"] else file.name.split('.')[0]
                analysis["email"] = candidate["email"] if candidate["email"] else "N/A"
                analysis["phone"] = candidate["phone"] if candidate["phone"] else "N/A"
                analysis["education"] = candidate["education"] if candidate["education"] else "N/A"
                analysis["detected_skills"] = candidate["skills"] if candidate["skills"] else []

                analysis["ats_score"] = ats["ats_score"]
                analysis["match_score"] = ats["ats_score"]
                analysis["matched_keywords"] = ats["matched_keywords"]
                analysis["missing_keywords"] = ats["missing_keywords"]

                out.append(analysis)
                prog.progress((i + 1) / len(files))

            st.session_state.analysis_results = out
            status_message.empty()
            prog.empty()
            st.session_state.trigger_balloons = True
            st.rerun()
        else:
            st.error("⚠️ Validation Failed: You must provide both a target job description context AND at least one candidate profile vector.")
            
    # Persistent hint block outside of form workflow
    st.markdown("<br>", unsafe_allow_html=True)
    st.info("💡 Tip: Using a form prevents the interface from lagging or resetting while you type long-form job descriptions.")

# ==========================================
# WORKSPACE: DASHBOARD
# ==========================================
elif page == "Dashboard":
    st.markdown("<h1>📈 Operational Analytics Dashboard</h1>", unsafe_allow_html=True)
    st.markdown("---")
    
    if results:
        df = create_dataframe(results)
        
        # Display Core KPIs Block
        show_kpis(df)
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Search Integration Row Filter
        search = st.text_input("🔍 Quick Directory Search", placeholder="Filter metrics table by candidate names...")
        if search:
            df = df[df["candidate_name"].str.contains(search, case=False)]
        
        st.dataframe(df, use_container_width=True)
        st.markdown("---")
        
        # Advanced Analytics Matrix Split Graphics
        st.subheader("📊 Macro Cohort Distribution Vectors")
        chart_col1, chart_col2, chart_col3 = st.columns(3)
        with chart_col1:
            match_score_chart(df)
        with chart_col2:
            recommendation_chart(df)
        with chart_col3:
            skills_chart(df)
            
        st.markdown("<br>", unsafe_allow_html=True)
        st.subheader("👥 Individual Candidate Deep Dives")
        
        # Action Bar Row
        excel_download_button(df)
        st.markdown("<br>", unsafe_allow_html=True)
        
        for _, c in df.iterrows():
            with st.expander(f"👤 {c['candidate_name']} — ATS Match Vector: {c['ats_score']}%"):
                left_col, right_col = st.columns([2, 1], gap="medium")
                
                with left_col:
                    st.markdown("<div class='section-header'>Executive Machine Summary</div>", unsafe_allow_html=True)
                    st.write(c["summary"])
                    
                    metric_col1, metric_col2 = st.columns(2)
                    metric_col1.metric("ATS Match Score", f"{c['ats_score']}%")
                    metric_col2.metric("Recommendation Tier", str(c["recommendation"]).upper())
                    
                    # Modern Tab Components for Deep Categorization
                    tab1, tab2, tab3 = st.tabs(["🎯 Core Competencies Matrix", "🎓 Academic Profiles", "🗂 Pipeline Metadata"])
                    
                    with tab1:
                        st.markdown("**Matched Stack Attributes**")
                        st.success(", ".join(c["matched_skills"]) if c["matched_skills"] else "None explicitly registered.")
                        st.markdown("**Identified Profile Gaps**")
                        st.error(", ".join(c["missing_skills"]) if c["missing_skills"] else "Zero baseline gaps identified.")
                        st.markdown("**ATS Target Keyword Hits**")
                        st.info(", ".join(c["matched_keywords"]) if c["matched_keywords"] else "No direct technical keywords hit.")
                        st.markdown("**Missing Target Keywords**")
                        st.warning(", ".join(c["missing_keywords"]) if c["missing_keywords"] else "No key gaps found.")
                        
                    with tab2:
                        st.markdown("**Parsed Academic Records**")
                        st.write(c["education"])
                        st.markdown("**System Detected Skills Block**")
                        st.write(c["detected_skills"])
                        
                    with tab3:
                        st.markdown(f"**Primary Digital Contact:** `{c['email']}`")
                        st.markdown(f"**Primary Telephony Interface:** `{c['phone']}`")
                        
                with right_col:
                    st.markdown("<p style='text-align: center; font-weight: 600; font-size: 0.9rem;'>Competency Mapping Vector</p>", unsafe_allow_html=True)
                    radar_chart(c)
                    st.markdown("---")
                    pdf_download_button(c)
    else:
        st.info("ℹ️ Pipeline directory empty. Access the 'Resume Screening' module to run baseline data loads.")

# ==========================================
# WORKSPACE: RECRUITER TOOLS
# ==========================================
elif page == "Recruiter":
    st.markdown("<h1>💼 Talent Stream Management</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color: #64748B;'>Organize candidate workflow positions, statuses, and persistent internal processing memos.</p>", unsafe_allow_html=True)
    st.markdown("---")
    
    if results:
        for c in results:
            name = c["candidate_name"]
            st.markdown(f"<div class='recruiter-card'>", unsafe_allow_html=True)
            
            card_col1, card_col2 = st.columns([1, 2])
            with card_col1:
                st.markdown(f"### {name}")
                st.caption(f"Contact Record: {c['email']}")
                
                st.selectbox(
                    "Workflow Stage Assignment",
                    ["New", "Shortlisted", "Interview", "Rejected", "Offer"],
                    key=f"s_{name}"
                )
            with card_col2:
                st.text_area(
                    "Internal Team Collaboration Notes",
                    placeholder="Log structural feedback notes, screening items, or panel commentary arrays...",
                    key=f"n_{name}",
                    height=110
                )
                
            st.markdown("</div>", unsafe_allow_html=True)
    else:
        st.info("ℹ️ Active pipeline array contains 0 loaded structures. Run ingestion processes inside 'Resume Screening' first.")