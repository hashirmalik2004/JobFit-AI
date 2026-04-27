# 📄 Resume AI — Detailed System Documentation

This document provides a comprehensive deep-dive into how the Resume AI project is built, the logic behind the code, and how to operate it.

---

## 🛠️ 1. Setup & Installation

I have already installed the dependencies and the ML model for you, but here is how you would do it on a fresh machine:

### Prerequisites
- Python 3.9 or higher
- Internet connection (to download the spaCy model)

### Steps
1.  **Clone/Copy the Project**: Ensure all files and the `src/` folder are in one directory.
2.  **Install Dependencies**:
    ```bash
    pip install -r requirements.txt
    ```
3.  **Download the NLP Model**:
    ```bash
    python -m spacy download en_core_web_sm
    ```
4.  **Run the Dashboard**:
    ```bash
    streamlit run app.py
    ```

---

## 🧠 2. How it Works (The Technical Logic)

The project follows a "Pipeline" architecture. Data flows through several stages before reaching the UI.

### Stage A: PDF Extraction (`pdf_parser.py`)
Most resume parsers fail on 2-column layouts. I solved this by using **PyMuPDF (`fitz`)** with the `sort=True` flag. This forces the engine to read text blocks top-to-bottom and left-to-right, ensuring that a sidebar doesn't get mixed into the middle of the work experience.

### Stage B: Text Sanitization (`text_cleaner.py`)
PDFs often contain "poison" characters (bullets, emojis, encoded URLs) that confuse machine learning models. I used a custom **Regex pipeline** to strip:
- URLs and Emails.
- Emojis and Unicode symbols.
- Special bullet characters (•, ■, ►).
- Excessive whitespace.

### Stage C: Intelligent NLP (`nlp_processor.py`)
I used **spaCy** for the heavy lifting. A key innovation here is **Case-Sensitive Stopword Handling**.
- Normally, "IT" (Information Technology) is removed because it's a common stopword.
- My code checks a `KeepList` (in `config.py`). If it sees "IT", "Go", or "C" in their uppercase/correct forms, it protects them from being deleted.
- It then **Lemmatizes** the words (e.g., "Developing" becomes "develop") so the math model treats them as the same concept.

### Stage D: The Math Layer (`vectorizer.py`)
I used **TF-IDF (Term Frequency-Inverse Document Frequency)** to turn text into numbers.
- **Why TF-IDF?** It gives higher weights to "rare" words (like "Kubernetes") and lower weights to "common" words (like "Team").
- **Cosine Similarity**: Once the resume and Job Description are turned into mathematical vectors, we calculate the "angle" between them. A similarity of 1.0 means they are identical; a 0.0 means they share nothing.

### Stage E: NER & Skill Matching (`entity_extractor.py`)
I used **Named Entity Recognition (NER)** to extract "Organizations" (where you worked) and "Dates".
Then, I performed **Set Intersection** between the resume, the job description, and a master `TechSkills` list to highlight:
- ✅ **Matched Skills**: What the candidate has.
- ❌ **Missing Skills**: What the recruiter is looking for but wasn't found.
- ➕ **Extra Skills**: Bonus tech the candidate brings.

---

## 🎨 3. My Coding Style & Philosophy

While building this, I adhered to a specific "Premium Developer" style:

1.  **PascalCase Convention**: I used PascalCase for variable names (e.g., `ResumeTokens`, `CleanText`, `AnalyzeClicked`) to maintain consistency and high readability.
2.  **Conversational Inline Comments**: I wrote comments that explain *why* something is happening, not just *what* the code does. They act as a guide for anyone reading the code.
3.  **Separation of Concerns**: Each file in `src/` has exactly one job. If you want to change how PDFs are read, you only touch `pdf_parser.py`.
4.  **Premium Aesthetics**: I didn't settle for the default Streamlit look. I injected **Custom CSS** into `app.py` to create glassmorphism effects, gradients, and polished "Skill Tags" that make the tool feel like a high-end SaaS product.

---

## 📁 4. Component Breakdown

- **`app.py`**: The heart of the app. Handles the Streamlit UI, state, and coordinates the pipeline.
- **`src/config.py`**: The "Control Center". Change the `TechSkills` list or `KeepList` here to tune the AI.
- **`src/pdf_parser.py`**: Handles raw byte-stream extraction for uploaded PDFs.
- **`src/text_cleaner.py`**: Cleans the mess.
- **`src/nlp_processor.py`**: The linguistic engine.
- **`src/vectorizer.py`**: The mathematical engine.
- **`src/entity_extractor.py`**: The data intelligence engine.

---

## 🚀 5. Final Checklist
- [x] All imports are relative to the root (`from src.x import y`).
- [x] Error handling is included for "Empty PDFs" or "Short Job Descriptions".
- [x] UI is responsive and includes progress bars for transparency.

**The project is now 100% ready for deployment or demo.**
