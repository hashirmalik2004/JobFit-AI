# 📄 Resume AI — Smart Resume Analyzer

A Python-based AI tool that analyzes resumes against job descriptions using **TF-IDF Vectorization** and **Cosine Similarity**. Upload a PDF resume, paste a job description, and instantly get a match score, skill breakdown, and extracted entities.

---

## 🚀 Features

- **PDF Parsing** — Extracts text from PDF resumes, handles multi-column layouts
- **Text Sanitization** — Removes URLs, emails, emojis, and noise using regex
- **NLP Pipeline** — Tokenizes, removes stopwords, and lemmatizes using spaCy
- **TF-IDF + Cosine Similarity** — Computes a mathematical match score between resume and JD
- **Named Entity Recognition (NER)** — Extracts company names and dates from the resume
- **Skill Matching** — Shows exactly which skills matched, which are missing, and which are extra
- **Streamlit Dashboard** — Beautiful dark-themed web UI for recruiters

---

## 🔬 How it Works

### TF-IDF (Term Frequency — Inverse Document Frequency)
TF-IDF converts text into numerical vectors by assigning weights to words. Words that are **frequent in one document but rare across all documents** get higher weights. For example, "Python" is more meaningful than "Responsibilities" because "Responsibilities" appears in nearly every JD.

### Cosine Similarity
Once both the resume and JD are represented as vectors, Cosine Similarity measures the **angle** between them:
- **Score ≈ 1.0** → Vectors point the same direction → Strong match
- **Score ≈ 0.0** → Vectors are perpendicular → Weak match

### Named Entity Recognition (NER)
spaCy's pre-trained model identifies entities like **Organizations** (companies) and **Dates** directly from the resume text, giving recruiters structured data beyond just a score.

---

## 🛠️ Tech Stack

| Component | Library | Why |
|-----------|---------|-----|
| Parsing | PyMuPDF (`fitz`) | Best at preserving text order in PDF layouts |
| NLP | spaCy | Industrial-strength; handles "meaning" better than NLTK |
| Math | Scikit-Learn | The gold standard for classic ML algorithms |
| Interface | Streamlit | Fastest way to turn a script into a web app |

---

## 📦 Installation

```bash
# 1. clone the repo
git clone https://github.com/yourusername/resume-ai.git
cd resume-ai

# 2. install dependencies
pip install -r requirements.txt

# 3. download the spaCy english model
python -m spacy download en_core_web_sm

# 4. run the app
streamlit run app.py
```

---

## 📁 Project Structure

```
resume-ai/
├── data/                    # sample PDFs for testing
├── src/
│   ├── __init__.py
│   ├── config.py            # domain keep-list, regex patterns, tech skills
│   ├── pdf_parser.py        # PDF text extraction (PyMuPDF)
│   ├── text_cleaner.py      # text sanitization (regex)
│   ├── nlp_processor.py     # spaCy pipeline (tokenize, lemmatize)
│   ├── vectorizer.py        # TF-IDF + Cosine Similarity
│   └── entity_extractor.py  # NER + skill matching
├── app.py                   # Streamlit dashboard (entry point)
├── requirements.txt
├── README.md
└── .gitignore
```

---

## 📸 Usage

1. Open the app in your browser (runs on `localhost:8501`)
2. Upload a resume PDF using the file uploader
3. Paste the job description in the text area
4. Click **Analyze Resume**
5. View your match score, skill breakdown, and extracted entities

---

## 🧠 Key Design Decisions

- **Multi-column PDF handling**: PyMuPDF's `sort=True` flag re-sorts text blocks in natural reading order
- **Case-sensitive stopword removal**: "IT" (the domain) is kept while "it" (the pronoun) is removed
- **Dual skill matching**: Cross-references against a hardcoded tech skills database AND TF-IDF overlap
- **Raw text for NER**: Entity extraction runs on unsanitized text to preserve formatting needed for detection

---

## 📄 License

MIT License — feel free to use and modify.
