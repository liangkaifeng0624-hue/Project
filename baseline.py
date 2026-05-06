import re
from collections import Counter


STOPWORDS = {
    "and", "or", "the", "a", "an", "to", "of", "in", "for", "with", "on",
    "as", "is", "are", "be", "by", "from", "this", "that", "will", "can",
    "you", "your", "we", "our", "at", "it", "role", "candidate", "job",
    "responsibilities", "required", "preferred", "qualification", "qualifications"
}


def clean_tokens(text: str):
    text = text.lower()
    tokens = re.findall(r"[a-zA-Z][a-zA-Z+#.]*", text)
    return [t for t in tokens if t not in STOPWORDS and len(t) > 2]


def keyword_baseline_score(resume_text: str, job_description: str) -> dict:
    jd_tokens = clean_tokens(job_description)
    resume_tokens = set(clean_tokens(resume_text))

    if not jd_tokens:
        return {
            "baseline_score": 0,
            "matched_keywords": [],
            "missing_keywords": [],
            "explanation": "No meaningful keywords found in the job description."
        }

    keyword_counts = Counter(jd_tokens)
    top_keywords = [word for word, count in keyword_counts.most_common(20)]

    matched = [kw for kw in top_keywords if kw in resume_tokens]
    missing = [kw for kw in top_keywords if kw not in resume_tokens]

    score = round((len(matched) / len(top_keywords)) * 100)

    return {
        "baseline_score": score,
        "matched_keywords": matched,
        "missing_keywords": missing,
        "explanation": (
            f"The keyword baseline found {len(matched)} matching keywords "
            f"out of {len(top_keywords)} important JD keywords."
        )
    }