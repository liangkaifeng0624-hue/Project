# Evaluation Results

## Evaluation Setup

I tested the AI Resume Screening Assistant on 8 realistic synthetic resume cases. Each case was manually labeled as Strong Match, Moderate Match, or Weak Match.

The GenAI evaluator was compared against a simpler keyword-matching baseline.

## What Counted as Good Output

A good output should:

- Match the human label reasonably well
- Explain the recommendation using evidence from the resume
- Identify missing skills or weak evidence
- Avoid making a final hiring decision
- Include a human review note

## Baseline

The baseline uses simple keyword matching. It extracts common keywords from the job description and checks whether they appear in the resume.

## Findings

The GenAI evaluator performed better than the keyword baseline when the resume used different wording from the job description. It also provided more useful explanations about strengths, weaknesses, and missing skills.

The keyword baseline worked when the resume and job description shared exact terms. However, it over-scored keyword-heavy resumes that did not show strong actual experience.

In the sample output, the GenAI evaluator gave a match score of 85 and recommended "Shortlist," while the keyword baseline only scored 30. This showed that the GenAI system could recognize relevant finance, Excel, reporting, and teamwork experience even when the resume did not repeat every JD keyword exactly.

## Failure Cases

The GenAI system sometimes gave overly positive evaluations when resume language was vague. It also depended on the quality of PDF text extraction. If the PDF was poorly formatted, the evaluation became less reliable.

## Human Review

This tool should only support initial resume screening. A human recruiter should verify the candidate's actual experience, context, and job fit before making any hiring decision.