# Resume AI — Implementation Plan

A Python application that parses resumes (PDF), compares them to job descriptions using **TF-IDF + Cosine Similarity**, extracts entities and skills, and presents results via a polished **Streamlit** dashboard.

---

## Project Structure

```
c:\Users\user\Desktop\AI\New folder\
├── data/                       # Sample PDFs for testing
│   └── sample_resume.pdf       # (user-provided or generated test PDF)
├── src/
│   ├── __init__.py
│   ├── pdf_parser.py           # Phase 1 — PDF extraction
│   ├── text_cleaner.py         # Phase 1 — Sanitization & regex cleaning
│   ├── nlp_processor.py        # Phase 2 — spaCy pipeline (tokenize, lemmatize, stopword removal)
│   ├── vectorizer.py           # Phase 3 — TF-IDF + Cosine Similarity
│   ├── entity_extractor.py     # Phase 4 — NER + Skill matching
│   └── config.py               # Domain-specific keep-lists, constants
├── app.py                      # Phase 5 — Streamlit dashboard (entry point)
├── requirements.txt
├── README.md                   # Phase 5 — Polished README with technical vocabulary
└── .gitignore
```

---

## Dependencies (`requirements.txt`)

| Package | Version | Purpose |
|---|---|---|
| `PyMuPDF` | ≥1.24 | PDF parsing (imported as `fitz`) |
| `spacy` | ≥3.7 | NLP pipeline — tokenization, lemmatization, NER |
| `scikit-learn` | ≥1.4 | TF-IDF vectorizer + cosine similarity |
| `streamlit` | ≥1.35 | Web dashboard UI |

> [!NOTE]
> After `pip install`, we also need to download the spaCy model:
> ```
> python -m spacy download en_core_web_sm
> ```

---

## Proposed Changes

### Phase 1 — Input & Extraction Layer

#### [NEW] [config.py](file:///c:/Users/user/Desktop/AI/New%20folder/src/config.py)
- **Domain keep-list**: Words like `"Go"`, `"C"`, `"R"`, `"IT"`, `"AI"`, `"UI"`, `"UX"` that must survive stop-word removal.
- **Regex patterns** for URL, email, emoji, and bullet stripping.
- Centralises all tuneable constants in one place.

#### [NEW] [pdf_parser.py](file:///c:/Users/user/Desktop/AI/New%20folder/src/pdf_parser.py)
- `extract_text(pdf_path: str) -> str`
  - Opens the PDF with `fitz.open()`.
  - Iterates pages; uses `page.get_text("text")` (preserves reading order better than `"blocks"`).
  - Returns concatenated text.
- **Multi-column handling**: PyMuPDF's default `get_text("text")` already reads in natural reading order for most layouts. We'll add a `sort=True` flag to `get_text()` (available since PyMuPDF 1.22) which re-sorts text blocks top-to-bottom, left-to-right — the safest approach for 2-column resumes.

#### [NEW] [text_cleaner.py](file:///c:/Users/user/Desktop/AI/New%20folder/src/text_cleaner.py)
- `sanitize(text: str) -> str`
  - Strip URLs (`https?://\S+`), emails (`\S+@\S+`), emojis (Unicode ranges), bullets/special chars.
  - Collapse excessive whitespace.

---

### Phase 2 — NLP Processing Layer

#### [NEW] [nlp_processor.py](file:///c:/Users/user/Desktop/AI/New%20folder/src/nlp_processor.py)
- Loads `en_core_web_sm` once (module-level singleton).
- `process(text: str) -> list[str]`
  - Runs spaCy pipeline → tokenizes → filters stop words (respecting the keep-list) → lemmatizes.
  - Returns a list of cleaned lemmas.
- **Case-sensitivity logic**: Before checking if a token is a stop word, we compare the **original** casing against the keep-list. `"IT"` (uppercase) → kept; `"it"` (lowercase) → removed.

---

### Phase 3 — Vectorization & Math

#### [NEW] [vectorizer.py](file:///c:/Users/user/Desktop/AI/New%20folder/src/vectorizer.py)
- `compute_similarity(resume_tokens: list[str], jd_tokens: list[str]) -> dict`
  - Joins tokens back into strings.
  - Fits a `TfidfVectorizer` on **both** documents.
  - Computes `cosine_similarity` between the two TF-IDF vectors.
  - Returns `{"score": 0.85, "percentage": "85%", "resume_vector": ..., "jd_vector": ...}`.

---

### Phase 4 — Entity Recognition & Skill Matching

#### [NEW] [entity_extractor.py](file:///c:/Users/user/Desktop/AI/New%20folder/src/entity_extractor.py)
- `extract_entities(text: str) -> dict`
  - Uses spaCy NER on **raw** (unsanitised) text to find `ORG` (companies) and `DATE` entities.
  - Returns `{"organizations": [...], "dates": [...]}`.
- `match_skills(resume_keywords: set, jd_keywords: set) -> dict`
  - `matched = resume_keywords & jd_keywords`
  - `missing = jd_keywords - resume_keywords`
  - `extra = resume_keywords - jd_keywords`
  - Returns all three sets + counts.

---

### Phase 5 — Streamlit Dashboard

#### [NEW] [app.py](file:///c:/Users/user/Desktop/AI/New%20folder/app.py)

The UI will be **polished and recruiter-friendly** with a clear layout:

| Section | Streamlit Widget | Details |
|---|---|---|
| Header | `st.title`, `st.caption` | App name + brief tagline |
| Resume Upload | `st.file_uploader` | Accepts `.pdf` |
| Job Description | `st.text_area` | Paste JD text |
| Analyze Button | `st.button` | Triggers full pipeline |
| Score | `st.metric` | Big number: "Match Score: 85%" |
| Skill Breakdown | `st.dataframe` | Matched / Missing / Extra skills tables |
| Entities | `st.expander` | Organizations & Dates extracted from resume |
| Sidebar | `st.sidebar` | Instructions + "How it Works" explanation |

- Uses `st.columns` for two-panel layout (results left, details right).
- Uses `st.progress` bar during analysis for visual feedback.

---

### Phase 5b — Packaging & README

#### [NEW] [README.md](file:///c:/Users/user/Desktop/AI/New%20folder/README.md)
- Project title, screenshot placeholder, features list.
- **"How it Works"** section explaining TF-IDF and Cosine Similarity in plain English with technical terms.
- Installation & usage instructions.
- Tech stack table.

#### [NEW] [.gitignore](file:///c:/Users/user/Desktop/AI/New%20folder/.gitignore)
- Standard Python `.gitignore` (venv, `__pycache__`, `.pyc`, etc.)

---

## User Review Required

> [!IMPORTANT]
> **spaCy model size**: I'll use `en_core_web_sm` (small, ~12 MB) as specified. If you want better NER accuracy at the cost of download size, I can switch to `en_core_web_md` or `en_core_web_lg`.

> [!IMPORTANT]
> **Sample PDF**: The `data/` folder will be created but left empty for you to drop in test resumes. I can generate a sample text-based PDF with `reportlab` if you'd like, but that adds another dependency.

---

## Open Questions

1. **Streamlit theme** — Do you want a dark-themed dashboard or light? (I'll default to a custom dark theme with accent colors.)
2. **Additional skills database** — Should I include a hard-coded list of common tech skills (Python, Java, AWS, Docker, etc.) to improve matching, or rely purely on TF-IDF overlap?

---

## Verification Plan

### Automated Tests
```powershell
# 1. Install dependencies
pip install -r requirements.txt
python -m spacy download en_core_web_sm

# 2. Run the Streamlit app
streamlit run app.py
```

### Manual Verification
- Upload a sample PDF resume and paste a job description.
- Verify: score displays correctly, skills are categorised (matched/missing/extra), entities (companies, dates) appear.
- Test with a multi-column resume PDF to confirm text order is preserved.

### Browser Verification
- I'll launch the Streamlit app and interact with it via the browser tool to confirm all widgets render and the pipeline runs end-to-end.
