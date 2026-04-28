# JobFit AI - Resume Analyzer & Job Matcher

JobFit AI is a Python-based tool designed to help job seekers and recruiters analyze how well a resume matches specific job descriptions. By utilizing Natural Language Processing (NLP) and Machine Learning techniques, the application provides an objective similarity score, detailed skill gap analysis, and the ability to search for relevant roles within a dataset of over 1,000 job descriptions.

## core features

*   **resume parsing**: automatically extracts text from PDF resumes using `PyMuPDF`.
*   **single job match**: provides a keyword similarity score (TF-IDF) and a skill match ratio between a resume and a pasted job description.
*   **dataset search & ranking**: compares a resume against a dataset of 1,167 job postings and ranks them based on tech skill alignment.
*   **skill gap analysis**: identifies matched tech skills, missing skills and extra skills.
*   **custom dashboard**: a polished Streamlit interface designed for a professional user experience.

##  tech stack

*   **frontend**: [Streamlit](https://streamlit.io/) (with custom CSS for premium styling)
*   **nlp processing**: [spaCy](https://spacy.io/) (tokenization, lemmatization, and stopword removal)
*   **machine learning**: [Scikit-Learn](https://scikit-learn.org/) (TF-IDF Vectorization & Cosine Similarity)
*   **data management**: [Pandas](https://pandas.pydata.org/)
*   **pdf extraction**: [PyMuPDF](https://pymupdf.readthedocs.io/)

##  project structure

```
├── app.py                # main streamlit dashboard
├── src/
│   ├── PdfParser.py      # handles PDF text extraction
│   ├── TextCleaner.py    # sanitizes and cleans raw text
│   ├── NlpProcessor.py   # spaCy pipeline for tokenization/lemmatization
│   ├── Vectorizer.py     # TF-IDF and Cosine Similarity logic
│   ├── EntityExtractor.py # skill matching and extraction
│   ├── DatasetLoader.py  # handles job dataset loading and caching
│   └── GlobalSettings.py # skill taxonomy and configuration
├── data/
│   └── all_job_post.csv  # dataset of job descriptions
└── requirements.txt      # project dependencies
```

## how it works

1.  **text extraction**: the tool reads the uploaded PDF and extracts raw text while maintaining readability.
2.  **sanitization**: special characters, URLs, and irrelevant noise are removed to ensure high-quality data input.
3.  **nlp pipeline**: text is processed using `spaCy` to remove stopwords, punctuation, and numbers, followed by lemmatization to reduce words to their base form.
4.  **vectorization**: the processed text is converted into numerical vectors using `TfidfVectorizer`.
5.  **similarity calculation**: `Cosine Similarity` is used to calculate the mathematical overlap between the resume and the job description.
6.  **skill matching**: the system cross-references tokens against a predefined tech skill taxonomy to identify specific technical matches.

## ⚙️ installation

1.  **clone the repository**:
    ```bash
    git clone https://github.com/hashirmalik2004/JobFit-ai.git
    ```
2.  **install dependencies**:
    ```bash
    pip install -r requirements.txt
    ```
3.  **download the spaCy model**:
    ```bash
    python -m spacy download en_core_web_sm
    ```
4.  **run the application**:
    ```bash
    streamlit run app.py
    ```


## here are some images of the working UI

<img width="1920" height="931" alt="image" src="https://github.com/user-attachments/assets/f7a8adb3-7dcf-4964-82c1-76e6b8ac9294" />

<img width="1493" height="891" alt="image" src="https://github.com/user-attachments/assets/95f794ac-775f-4516-be25-888eb3d0cb71" />

<img width="1919" height="929" alt="image" src="https://github.com/user-attachments/assets/90ecc1f5-3406-40d3-81eb-defb5865cdf6" />

<img width="1526" height="912" alt="image" src="https://github.com/user-attachments/assets/f34756ed-bcdf-4866-99a0-efa779b2fe1b" />

<img width="1531" height="908" alt="image" src="https://github.com/user-attachments/assets/a60000cc-0cfe-453d-9f38-b4da1decf796" />




