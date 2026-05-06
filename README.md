# AI Resume Screening Assistant for Entry-Level Hiring

## 1. Context, User, and Problem

The target user is an HR professional or recruiter responsible for screening entry-level job applicants.

The workflow is resume pre-screening. The user uploads a candidate resume and enters a job description. The system compares the resume against the job description and produces a structured evaluation.

This problem matters because early-stage hiring can involve many resumes. Manual screening is time-consuming and can be inconsistent across reviewers. This tool aims to make the first review faster and more structured, while still keeping a human recruiter involved.

## 2. Solution and Design

I built a Streamlit web app that evaluates resume-job description fit.

The app supports the following workflow:

1. Upload a PDF resume
2. Paste a job description
3. Extract text from the resume
4. Run a keyword-matching baseline
5. Run a GenAI rubric-based evaluation
6. Display a comparison between the baseline and the GenAI result

The GenAI evaluator produces:

- Match score from 0 to 100
- Candidate level: Strong Match, Moderate Match, or Weak Match
- Key strengths
- Key weaknesses
- Missing skills
- Risk factors
- Recommendation: Shortlist, Maybe, or Reject
- Human review note

The main GenAI design choice is to use a fixed HR screening rubric instead of a vague open-ended prompt. This makes the output more structured and easier to evaluate.

I did not use RAG or agents because the workflow only compares one resume with one job description. A simpler design is enough for this narrow business use case.

## 3. Evaluation and Results

I tested the tool on 8 realistic synthetic resume cases. Each case was manually labeled as Strong Match, Moderate Match, or Weak Match.

The GenAI evaluator was compared against a simpler keyword-matching baseline.

Good output was defined as output that:

- Agreed with the human label
- Used evidence from the resume
- Identified missing or weak areas
- Gave a useful recommendation
- Included a reminder for human review

The keyword baseline performed well when the resume used the same words as the job description. However, it struggled with resumes that used different wording. It also over-scored keyword-heavy resumes that did not show strong actual experience.

The GenAI evaluator gave more useful reasoning and better identified strengths and weaknesses. However, it sometimes became too positive when resume language was vague. For this reason, the system should be used as an advisory tool only.

## 4. Artifact Snapshot

The app includes:

- PDF resume upload
- Job description input box
- GenAI match score
- Keyword baseline score
- Structured screening report
- Human review warning

A sample screenshot is included in the `screenshots/` folder.

