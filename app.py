import streamlit as st
import pandas as pd

from pdf_utils import extract_text_from_pdf
from baseline import keyword_baseline_score
from llm_evaluator import evaluate_resume_with_llm


st.set_page_config(
    page_title="AI Resume Screening Assistant",
    page_icon="📄",
    layout="wide"
)

st.title("AI Resume Screening Assistant for Entry-Level Hiring")

st.write("""
This app helps HR professionals screen entry-level resumes against a job description.
It compares a GenAI rubric-based evaluation with a simpler keyword-matching baseline.
The tool is advisory only and should not replace human hiring judgment.
""")

st.warning(
    "Responsible use note: This tool should not make final hiring decisions. "
    "A human recruiter must review the output."
)

col1, col2 = st.columns(2)

with col1:
    st.subheader("1. Upload Candidate Resume")
    uploaded_resume = st.file_uploader("Upload a PDF resume", type=["pdf"])

with col2:
    st.subheader("2. Enter Job Description")
    job_description = st.text_area(
        "Paste the job description here",
        height=300,
        placeholder="Paste JD here..."
    )

run_button = st.button("Run Screening Evaluation")

if run_button:
    if uploaded_resume is None:
        st.error("Please upload a PDF resume.")
    elif not job_description.strip():
        st.error("Please enter a job description.")
    else:
        with st.spinner("Extracting resume text..."):
            resume_text = extract_text_from_pdf(uploaded_resume)

        if resume_text.startswith("ERROR"):
            st.error(resume_text)
        elif len(resume_text) < 100:
            st.error("The extracted resume text is too short. Please check the PDF quality.")
        else:
            st.subheader("Extracted Resume Preview")
            with st.expander("Show extracted resume text"):
                st.write(resume_text[:3000])

            with st.spinner("Running keyword baseline..."):
                baseline_result = keyword_baseline_score(resume_text, job_description)

            with st.spinner("Running GenAI evaluation..."):
                ai_result = evaluate_resume_with_llm(resume_text, job_description)

            st.header("Screening Results")

            metric_col1, metric_col2, metric_col3 = st.columns(3)

            with metric_col1:
                st.metric("GenAI Match Score", ai_result.get("match_score", "N/A"))

            with metric_col2:
                st.metric("Keyword Baseline Score", baseline_result.get("baseline_score", "N/A"))

            with metric_col3:
                st.metric("Recommendation", ai_result.get("recommendation", "N/A"))

            st.subheader("Comparison Table")

            comparison_df = pd.DataFrame([
                {
                    "Method": "Keyword Baseline",
                    "Score": baseline_result.get("baseline_score"),
                    "Output": baseline_result.get("explanation")
                },
                {
                    "Method": "GenAI Rubric Evaluator",
                    "Score": ai_result.get("match_score"),
                    "Output": ai_result.get("reasoning_summary")
                }
            ])

            st.dataframe(comparison_df, use_container_width=True)

            st.subheader("GenAI Structured Evaluation")

            st.markdown("### Candidate Level")
            st.write(ai_result.get("candidate_level", "N/A"))

            st.markdown("### Key Strengths")
            for item in ai_result.get("key_strengths", []):
                st.write(f"- {item}")

            st.markdown("### Key Weaknesses")
            for item in ai_result.get("key_weaknesses", []):
                st.write(f"- {item}")

            st.markdown("### Missing Skills")
            for item in ai_result.get("missing_skills", []):
                st.write(f"- {item}")

            st.markdown("### Risk Factors")
            for item in ai_result.get("risk_factors", []):
                st.write(f"- {item}")

            st.markdown("### Reasoning Summary")
            st.write(ai_result.get("reasoning_summary", "N/A"))

            st.markdown("### Human Review Note")
            st.info(ai_result.get("human_review_note", "A human recruiter should review the result."))

            st.subheader("Keyword Baseline Details")

            st.markdown("### Matched Keywords")
            st.write(", ".join(baseline_result.get("matched_keywords", [])))

            st.markdown("### Missing Keywords")
            st.write(", ".join(baseline_result.get("missing_keywords", [])))