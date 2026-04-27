# GlobalSettings.py
# this file holds all the constants and settings used across the project
# keeps everything in one place so we dont have to hunt for stuff later

import re


# ============================================================
# DOMAIN KEEP LIST
# these are words that look like stopwords in normal english
# but in tech they are actual programming languages or domains
# so we DONT want spaCy to delete them during stopword removal
# ============================================================

KeepList = {
    # programming languages that look like normal english words
    "Go", "C", "R", "D", "F", "V",
    
    # tech acronyms that could get confused
    "IT", "AI", "ML", "DL", "NLP", "CV",
    "UI", "UX", "QA", "DB", "OS", "CI", "CD",
    "API", "AWS", "GCP", "SQL", "CSS", "HTML",
    "REST", "SOAP", "SaaS", "PaaS", "IaaS",
    
    # frameworks and tools that are short words
    "Vue", "Dart", "Rust", "Swift", "Scala",
    "Node", "React", "Flask", "Ruby", "Perl",
    "Bash", "Vim", "Git", "Jira", "Figma",
}


# ============================================================
# REGEX PATTERNS FOR CLEANING
# we use these to strip out stuff that confuses the ML model
# things like URLs, emails, emojis, and random special chars
# ============================================================

# matches any URL starting with http or https
UrlPattern = re.compile(r'https?://\S+')

# matches email addresses like someone@example.com
EmailPattern = re.compile(r'\S+@\S+\.\S+')

# matches emojis and other weird unicode symbols
# covers most emoji ranges in unicode
EmojiPattern = re.compile(
    "["
    "\U0001F600-\U0001F64F"  # emoticons (smiley faces etc)
    "\U0001F300-\U0001F5FF"  # misc symbols and pictographs
    "\U0001F680-\U0001F6FF"  # transport and map symbols
    "\U0001F1E0-\U0001F1FF"  # country flags
    "\U00002702-\U000027B0"  # dingbats
    "\U000024C2-\U0001F251"  # enclosed characters
    "]+",
    flags=re.UNICODE
)

# matches bullet points and special characters that pdfs love to throw in
# things like •, ■, ►, ★, ○, etc
BulletPattern = re.compile(r'[•■►▸▹▪▫★☆○●◆◇→←↑↓↔▶◀]{1,}')

# matches phone numbers in various formats
# like (123) 456-7890 or +1-234-567-8901 or just 1234567890
PhonePattern = re.compile(r'[\+]?[\d\s\-\(\)]{7,15}')


# ============================================================
# COMMON TECH SKILLS LIST
# a hardcoded list of skills that we know are legit tech skills
# this helps with matching since TF-IDF might miss some
# ============================================================

TechSkills = {
    # programming languages
    "python", "java", "javascript", "typescript", "c++", "c#", "c",
    "go", "rust", "ruby", "php", "swift", "kotlin", "scala",
    "r", "matlab", "perl", "bash", "shell", "dart", "lua",
    
    # web stuff
    "html", "css", "react", "angular", "vue", "nextjs", "nodejs",
    "express", "django", "flask", "fastapi", "spring", "springboot",
    
    # data and ML
    "pandas", "numpy", "scipy", "matplotlib", "seaborn", "plotly",
    "scikit-learn", "tensorflow", "pytorch", "keras", "opencv",
    "spacy", "nltk", "huggingface", "transformers",
    
    # databases
    "sql", "mysql", "postgresql", "mongodb", "redis", "elasticsearch",
    "firebase", "dynamodb", "cassandra", "sqlite", "oracle",
    
    # cloud and devops
    "aws", "azure", "gcp", "docker", "kubernetes", "jenkins",
    "terraform", "ansible", "ci/cd", "github actions", "gitlab",
    
    # tools and misc
    "git", "linux", "jira", "confluence", "figma", "postman",
    "rest api", "graphql", "microservices", "agile", "scrum",
    "machine learning", "deep learning", "nlp", "computer vision",
    "data analysis", "data engineering", "data science",
    "power bi", "tableau", "excel", "sap",
}
