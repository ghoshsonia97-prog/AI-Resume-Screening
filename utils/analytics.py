import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st


# ==============================
# Convert Results to DataFrame
# ==============================

def create_dataframe(results):

    if not results:
        return pd.DataFrame()

    return pd.DataFrame(results)


# ==============================
# KPI Cards
# ==============================

def show_kpis(df):

    if df.empty:
        return

    col1, col2, col3, col4 = st.columns(4)

    col1.metric(
        "👥 Candidates",
        len(df)
    )

    col2.metric(
        "⭐ Average Match",
        f"{df['match_score'].mean():.1f}%"
    )

    col3.metric(
        "🎯 Average ATS",
        f"{df['ats_score'].mean():.1f}%"
    )

    col4.metric(
        "🏆 Highest Score",
        f"{df['match_score'].max()}%"
    )


# ==============================
# Match Score Bar Chart
# ==============================

def match_score_chart(df):

    if df.empty:
        return

    fig = px.bar(
        df,
        x="candidate_name",
        y="match_score",
        color="recommendation",
        title="Candidate Match Scores",
        text="match_score"
    )

    st.plotly_chart(fig, use_container_width=True)


# ==============================
# ATS Score Chart
# ==============================

def ats_chart(df):

    if df.empty:
        return

    fig = px.bar(
        df,
        x="candidate_name",
        y="ats_score",
        color="ats_score",
        title="ATS Score"
    )

    st.plotly_chart(fig, use_container_width=True)


# ==============================
# Recommendation Pie Chart
# ==============================

def recommendation_chart(df):

    if df.empty:
        return

    fig = px.pie(
        df,
        names="recommendation",
        title="Hiring Recommendation"
    )

    st.plotly_chart(fig, use_container_width=True)


# ==============================
# Experience Distribution
# ==============================

def experience_chart(df):

    if df.empty:
        return

    fig = px.histogram(
        df,
        x="experience_level",
        title="Experience Distribution"
    )

    st.plotly_chart(fig, use_container_width=True)


# ==============================
# Skill Frequency Chart
# ==============================

def skills_chart(df):

    if df.empty:
        return

    skills = []

    for row in df["matched_skills"]:

        if isinstance(row, list):
            skills.extend(row)

    if len(skills) == 0:
        return

    skill_df = pd.DataFrame(
        pd.Series(skills).value_counts()
    ).reset_index()

    skill_df.columns = ["Skill", "Count"]

    fig = px.bar(
        skill_df,
        x="Skill",
        y="Count",
        title="Top Skills"
    )

    st.plotly_chart(fig, use_container_width=True)


# ==============================
# Radar Chart
# ==============================

def radar_chart(candidate):

    categories = [
        "Match",
        "ATS",
        "Technical",
        "Projects",
        "Communication"
    ]

    values = [
        candidate.get("match_score", 0),
        candidate.get("ats_score", 0),
        85,
        80,
        75
    ]

    fig = go.Figure()

    fig.add_trace(
        go.Scatterpolar(
            r=values,
            theta=categories,
            fill="toself",
            name=candidate["candidate_name"]
        )
    )

    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 100]
            )
        ),
        title="Candidate Profile"
    )

    st.plotly_chart(fig, use_container_width=True)