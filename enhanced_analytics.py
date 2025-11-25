"""
Enhanced Analytics Module - Advanced visualizations and analytics for student results
Author: Aditya Kumar
"""

import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from data_processor import add_grade_category, get_statistics_summary


def show_key_metrics(df: pd.DataFrame):
    """Displays key statistics in metric cards."""
    stats = get_statistics_summary(df)
    
    st.subheader("📌 Key Metrics")
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Students", stats["Total Students"])
    with col2:
        st.metric("Pass Rate", stats["Pass Rate"])
    with col3:
        st.metric("Avg SGPA", stats["Average SGPA"])
    with col4:
        st.metric("Avg CGPA", stats["Average CGPA"])


def show_sgpa_distribution(df: pd.DataFrame):
    """Displays SGPA distribution histogram."""
    st.subheader("📈 SGPA Distribution")
    
    fig = px.histogram(
        df,
        x="Current SGPA",
        nbins=15,
        title="Student Distribution by SGPA",
        labels={"Current SGPA": "SGPA", "count": "Number of Students"},
        color_discrete_sequence=["#1f77b4"]
    )
    fig.update_layout(
        bargap=0.1,
        hovermode="x unified",
        height=400,
        showlegend=False
    )
    st.plotly_chart(fig, use_container_width=True)


def show_grade_distribution(df: pd.DataFrame):
    """Displays performance category pie chart."""
    st.subheader("🎯 Performance Category Distribution")
    
    df_with_category = add_grade_category(df)
    category_counts = df_with_category["Grade Category"].value_counts()
    
    fig = px.pie(
        names=category_counts.index,
        values=category_counts.values,
        title="Students by Performance Category",
        color_discrete_sequence=px.colors.qualitative.Set3
    )
    fig.update_traces(textposition='inside', textinfo='percent+label')
    fig.update_layout(height=400)
    st.plotly_chart(fig, use_container_width=True)


def show_top_performers(df: pd.DataFrame, top_n: int = 10):
    """Displays top performers."""
    st.subheader(f"🏅 Top {top_n} Performers")
    
    top_students = df.nlargest(top_n, "Current SGPA")[
        ["Registration No.", "Student Name", "Current SGPA", "CGPA", "College Name"]
    ].reset_index(drop=True)
    top_students.index = top_students.index + 1
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        fig = px.bar(
            df.nlargest(top_n, "Current SGPA"),
            x="Student Name",
            y="Current SGPA",
            title=f"Top {top_n} Students by SGPA",
            color="Current SGPA",
            color_continuous_scale="Viridis",
            labels={"Current SGPA": "SGPA", "Student Name": "Student"}
        )
        fig.update_layout(height=400, showlegend=False)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.dataframe(top_students, use_container_width=True)


def show_college_wise_analysis(df: pd.DataFrame):
    """Displays college-wise performance analysis."""
    st.subheader("🏫 College-wise Analysis")
    
    college_stats = df.groupby("College Name").agg({
        "Registration No.": "count",
        "Current SGPA": ["mean", "max"],
        "Status": lambda x: (x == "PASS").sum()
    }).reset_index()
    
    college_stats.columns = ["College Name", "Total Students", "Avg SGPA", "Max SGPA", "Passed"]
    college_stats = college_stats.sort_values("Avg SGPA", ascending=False)
    
    col1, col2 = st.columns([1, 1])
    
    with col1:
        fig1 = px.bar(
            college_stats,
            x="College Name",
            y="Avg SGPA",
            title="Average SGPA by College",
            color="Avg SGPA",
            color_continuous_scale="Blues",
            labels={"Avg SGPA": "Average SGPA"}
        )
        fig1.update_layout(height=400, xaxis_tickangle=-45)
        st.plotly_chart(fig1, use_container_width=True)
    
    with col2:
        fig2 = px.bar(
            college_stats,
            x="College Name",
            y="Total Students",
            title="Student Count by College",
            color="Total Students",
            color_continuous_scale="Greens",
            labels={"Total Students": "Number of Students"}
        )
        fig2.update_layout(height=400, xaxis_tickangle=-45)
        st.plotly_chart(fig2, use_container_width=True)
    
    st.dataframe(college_stats.sort_values("Avg SGPA", ascending=False), use_container_width=True)


def show_course_wise_analysis(df: pd.DataFrame):
    """Displays course-wise performance analysis."""
    st.subheader("📚 Course-wise Analysis")
    
    if "Course" in df.columns:
        course_stats = df.groupby("Course").agg({
            "Registration No.": "count",
            "Current SGPA": ["mean", "max", "min"],
            "Status": lambda x: (x == "PASS").sum()
        }).reset_index()
        
        course_stats.columns = ["Course", "Total Students", "Avg SGPA", "Max SGPA", "Min SGPA", "Passed"]
        course_stats = course_stats.sort_values("Avg SGPA", ascending=False)
        
        fig = px.bar(
            course_stats,
            x="Course",
            y=["Avg SGPA", "Max SGPA", "Min SGPA"],
            title="SGPA Statistics by Course",
            barmode="group",
            labels={"value": "SGPA"}
        )
        fig.update_layout(height=400, xaxis_tickangle=-45)
        st.plotly_chart(fig, use_container_width=True)
        
        st.dataframe(course_stats, use_container_width=True)


def show_subject_analysis(df: pd.DataFrame):
    """Displays subject-wise grade distribution."""
    st.subheader("📖 Subject-wise Grade Distribution")
    
    # Extract theory subjects
    theory_subjects = {}
    theory_cols = [col for col in df.columns if col.startswith("Theory_") and col.endswith("_Grade")]
    
    for col in theory_cols:
        subject_name_col = col.replace("_Grade", "_Name")
        if subject_name_col in df.columns and len(df) > 0:
            subject_name = df[subject_name_col].iloc[0]
            grades = df[col].value_counts()
            theory_subjects[subject_name] = grades
    
    # Display theory subject analysis
    if theory_subjects:
        st.markdown("#### Theory Subjects")
        
        col1, col2 = st.columns([1, 1])
        
        with col1:
            selected_subject = st.selectbox(
                "Select Theory Subject",
                options=list(theory_subjects.keys()),
                key="theory_subject"
            )
            
            if selected_subject in theory_subjects:
                fig = px.pie(
                    names=theory_subjects[selected_subject].index,
                    values=theory_subjects[selected_subject].values,
                    title=f"Grade Distribution: {selected_subject}",
                    color_discrete_sequence=px.colors.qualitative.Set2
                )
                fig.update_traces(textposition='inside', textinfo='percent+label')
                st.plotly_chart(fig, use_container_width=True)
    
    # Extract practical subjects
    practical_subjects = {}
    practical_cols = [col for col in df.columns if col.startswith("Practical_") and col.endswith("_Grade")]
    
    for col in practical_cols:
        subject_name_col = col.replace("_Grade", "_Name")
        if subject_name_col in df.columns and len(df) > 0:
            subject_name = df[subject_name_col].iloc[0]
            grades = df[col].value_counts()
            practical_subjects[subject_name] = grades
    
    # Display practical subject analysis
    if practical_subjects:
        st.markdown("#### Practical Subjects")
        
        col1, col2 = st.columns([1, 1])
        
        with col1:
            selected_subject = st.selectbox(
                "Select Practical Subject",
                options=list(practical_subjects.keys()),
                key="practical_subject"
            )
            
            if selected_subject in practical_subjects:
                fig = px.pie(
                    names=practical_subjects[selected_subject].index,
                    values=practical_subjects[selected_subject].values,
                    title=f"Grade Distribution: {selected_subject}",
                    color_discrete_sequence=px.colors.qualitative.Set3
                )
                fig.update_traces(textposition='inside', textinfo='percent+label')
                st.plotly_chart(fig, use_container_width=True)


def show_pass_fail_analysis(df: pd.DataFrame):
    """Displays pass/fail statistics."""
    st.subheader("✅ Pass/Fail Analysis")
    
    col1, col2, col3 = st.columns(3)
    
    passed = (df["Status"] == "PASS").sum()
    failed = (df["Status"] == "FAIL").sum()
    total = len(df)
    pass_rate = (passed / total * 100) if total > 0 else 0
    
    with col1:
        st.metric("Passed", passed)
    with col2:
        st.metric("Failed", failed)
    with col3:
        st.metric("Pass Rate", f"{pass_rate:.1f}%")
    
    # Visual representation
    fig = go.Figure(data=[
        go.Pie(
            labels=["Passed", "Failed"],
            values=[passed, failed],
            marker=dict(colors=["#2ecc71", "#e74c3c"]),
            textposition='inside',
            textinfo='percent+label'
        )
    ])
    fig.update_layout(title="Pass/Fail Distribution", height=400)
    st.plotly_chart(fig, use_container_width=True)
    
    # College-wise pass rate
    if "College Name" in df.columns:
        st.markdown("#### Pass Rate by College")
        
        college_pass_rate = df.groupby("College Name").apply(
            lambda x: (x["Status"] == "PASS").sum() / len(x) * 100
        ).reset_index()
        college_pass_rate.columns = ["College Name", "Pass Rate %"]
        college_pass_rate = college_pass_rate.sort_values("Pass Rate %", ascending=False)
        
        fig = px.bar(
            college_pass_rate,
            x="College Name",
            y="Pass Rate %",
            title="Pass Rate by College",
            color="Pass Rate %",
            color_continuous_scale="RdYlGn",
            labels={"Pass Rate %": "Pass Rate (%)"}
        )
        fig.update_layout(height=400, xaxis_tickangle=-45)
        st.plotly_chart(fig, use_container_width=True)


def show_sgpa_vs_cgpa_correlation(df: pd.DataFrame):
    """Displays scatter plot of SGPA vs CGPA correlation."""
    st.subheader("📊 SGPA vs CGPA Correlation")
    
    fig = px.scatter(
        df,
        x="Current SGPA",
        y="CGPA",
        hover_data=["Student Name", "Registration No.", "College Name"],
        title="SGPA vs CGPA Correlation",
        color="Current SGPA",
        color_continuous_scale="Viridis",
        labels={"Current SGPA": "Current SGPA", "CGPA": "CGPA"}
    )
    fig.add_scatter(
        x=df["Current SGPA"],
        y=df["Current SGPA"],
        mode='lines',
        name='Ideal Line',
        line=dict(dash='dash', color='red'),
        hoverinfo='skip'
    )
    fig.update_layout(height=400)
    st.plotly_chart(fig, use_container_width=True)


def show_complete_analytics(df: pd.DataFrame):
    """Displays complete analytics dashboard."""
    st.markdown("## 📊 Complete Analytics Dashboard")
    st.markdown("---")
    
    # Key metrics
    show_key_metrics(df)
    st.markdown("---")
    
    # Distribution charts
    col1, col2 = st.columns(2)
    with col1:
        show_sgpa_distribution(df)
    with col2:
        show_grade_distribution(df)
    
    st.markdown("---")
    
    # Top performers
    show_top_performers(df, top_n=10)
    st.markdown("---")
    
    # Pass/Fail analysis
    show_pass_fail_analysis(df)
    st.markdown("---")
    
    # College and course analysis
    col1, col2 = st.columns(2)
    with col1:
        show_college_wise_analysis(df)
    with col2:
        show_course_wise_analysis(df)
    
    st.markdown("---")
    
    # Subject analysis
    show_subject_analysis(df)
    st.markdown("---")
    
    # Correlation analysis
    show_sgpa_vs_cgpa_correlation(df)


def show_enhanced_analytics(df: pd.DataFrame):
    """Compatibility wrapper used by `app.py`.

    Historically `app.py` imports `show_enhanced_analytics`. Delegate
    to `show_complete_analytics` to keep older imports working.
    """
    return show_complete_analytics(df)
