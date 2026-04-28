# this file holds all the constants and settings used across the project

import re

# these are words that look like stopwords in normal english so we dont wna get rid of them
KeepList = {
    "Go", "C", "R", "D", "F", "V",
    "IT", "AI", "ML", "DL", "NLP", "CV",
    "UI", "UX", "QA", "DB", "OS", "CI", "CD",
    "API", "AWS", "GCP", "SQL", "CSS", "HTML",
    "REST", "SOAP", "SaaS", "PaaS", "IaaS",
    "Vue", "Dart", "Rust", "Swift", "Scala",
    "Node", "React", "Flask", "Ruby", "Perl",
    "Bash", "Vim", "Git", "Jira", "Figma",
}


# regex patterns for cleaning
UrlPattern = re.compile(r'https?://\S+')

EmailPattern = re.compile(r'\S+@\S+\.\S+')

EmojiPattern = re.compile(
    "["
    "\U0001F600-\U0001F64F" 
    "\U0001F300-\U0001F5FF"  
    "\U0001F680-\U0001F6FF"  
    "\U0001F1E0-\U0001F1FF"  
    "\U00002702-\U000027B0"  
    "\U000024C2-\U0001F251"  
    "]+",
    flags=re.UNICODE
)

# matches bullet points and special characters
BulletPattern = re.compile(r'[•■►▸▹▪▫★☆○●◆◇→←↑↓↔▶◀]{1,}')

# matches phone numbers in various formats
PhonePattern = re.compile(r'[\+]?[\d\s\-\(\)]{7,15}')

# common tech skills
TechSkills = {
    "python", "java", "javascript", "typescript", "c++", "c#", "c",
    "go", "rust", "ruby", "php", "swift", "kotlin", "scala",
    "r", "matlab", "perl", "bash", "shell", "dart", "lua",
    "html", "css", "react", "angular", "vue", "nextjs", "nodejs",
    "express", "django", "flask", "fastapi", "spring", "springboot",
    "pandas", "numpy", "scipy", "matplotlib", "seaborn", "plotly",
    "scikit-learn", "tensorflow", "pytorch", "keras", "opencv",
    "spacy", "nltk", "huggingface", "transformers",
    "sql", "mysql", "postgresql", "mongodb", "redis", "elasticsearch",
    "firebase", "dynamodb", "cassandra", "sqlite", "oracle",
    "aws", "azure", "gcp", "docker", "kubernetes", "jenkins",
    "terraform", "ansible", "ci/cd", "github actions", "gitlab",
    "git", "linux", "jira", "confluence", "figma", "postman",
    "rest api", "graphql", "microservices", "agile", "scrum",
    "machine learning", "deep learning", "nlp", "computer vision",
    "data analysis", "data engineering", "data science",
    "power bi", "tableau", "excel", "sap",
}
