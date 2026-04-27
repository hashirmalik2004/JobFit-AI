# Vectorizer.py
# this is where the math happens
# we use TF-IDF to turn text into numbers (vectors)
# then use Cosine Similarity to measure how close the resume is to the job description
# 
# TF-IDF stands for Term Frequency - Inverse Document Frequency
# basically it figures out which words are IMPORTANT and UNIQUE
# "Python" in a resume is more meaningful than "Responsibilities"
# because "Responsibilities" appears in EVERY job description
#
# Cosine Similarity measures the angle between two vectors
# if they point in the same direction = similar (score close to 1)
# if they point in opposite directions = different (score close to 0)

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def ComputeSimilarity(ResumeTokens, JdTokens):
    """
    takes two lists of tokens (one from resume, one from job description)
    converts them into TF-IDF vectors and calculates cosine similarity
    
    returns a dictionary with:
    - Score: the raw similarity score (like 0.85)
    - Percentage: human readable percentage (like "85%")
    - ResumeVector: the TF-IDF vector for the resume (for debugging)
    - JdVector: the TF-IDF vector for the job description (for debugging)
    """

    # step 1: join the token lists back into strings
    # TfidfVectorizer expects strings not lists
    ResumeString = " ".join(ResumeTokens)
    JdString = " ".join(JdTokens)

    # step 2: create the TF-IDF vectorizer
    # this will learn the vocabulary from BOTH documents
    # and assign weights to each word based on importance
    Vectorizer = TfidfVectorizer()

    # step 3: fit and transform both documents at once
    # we put them in a list so the vectorizer sees both
    # index 0 = resume, index 1 = job description
    BothDocuments = [ResumeString, JdString]
    TfidfMatrix = Vectorizer.fit_transform(BothDocuments)

    # step 4: extract the individual vectors
    ResumeVector = TfidfMatrix[0]  # first row = resume
    JdVector = TfidfMatrix[1]      # second row = job description

    # step 5: calculate cosine similarity between the two vectors
    # this returns a 2D array but we only need the [0][1] value
    # which is the similarity between document 0 and document 1
    SimilarityMatrix = cosine_similarity(ResumeVector, JdVector)
    RawScore = SimilarityMatrix[0][0]  # extract the single similarity value

    # step 6: convert to percentage for humans to read
    Percentage = round(RawScore * 100, 2)
    PercentageStr = f"{Percentage}%"

    # step 7: get the feature names (words) for reference
    FeatureNames = Vectorizer.get_feature_names_out().tolist()

    print(f"similarity calculated: {PercentageStr}")

    # pack everything into a dictionary and return
    Results = {
        "Score": RawScore,
        "Percentage": PercentageStr,
        "PercentageNum": Percentage,
        "ResumeVector": ResumeVector,
        "JdVector": JdVector,
        "FeatureNames": FeatureNames,
    }

    return Results


def ComputeBatchSimilarity(ResumeTokens, ListOfJdTokens):
    """
    takes one resume token list and a LIST of JD token lists
    compares the resume against ALL job descriptions at once
    
    we build ONE big TF-IDF matrix across all documents
    so the IDF weights are calculated properly against the full corpus
    this is more accurate than comparing one-by-one
    
    returns a list of dictionaries with:
    - Index: the original index of the JD in the list
    - Score: raw cosine similarity (0 to 1)
    - Percentage: human readable percentage string
    - PercentageNum: numeric percentage for sorting
    """

    # step 1: join all token lists into strings
    ResumeString = " ".join(ResumeTokens)
    JdStrings = [" ".join(Tokens) for Tokens in ListOfJdTokens]

    # step 2: build the full document list
    # index 0 = resume, index 1 to N = job descriptions
    AllDocuments = [ResumeString] + JdStrings

    # step 3: create TF-IDF matrix across ALL documents at once
    # this gives us proper IDF weights since the vectorizer sees everything
    Vectorizer = TfidfVectorizer()
    TfidfMatrix = Vectorizer.fit_transform(AllDocuments)

    # step 4: the resume is row 0, all JDs are rows 1 onwards
    ResumeVector = TfidfMatrix[0]
    JdVectors = TfidfMatrix[1:]

    # step 5: compute cosine similarity between resume and ALL JDs at once
    # this returns a 1xN matrix where N = number of job descriptions
    SimilarityScores = cosine_similarity(ResumeVector, JdVectors)
    ScoresFlat = SimilarityScores[0]  # flatten to 1D array

    # step 6: build the results list
    Results = []
    for Idx, RawScore in enumerate(ScoresFlat):
        Percentage = round(RawScore * 100, 2)
        Results.append({
            "Index": Idx,
            "Score": RawScore,
            "Percentage": f"{Percentage}%",
            "PercentageNum": Percentage,
        })

    # step 7: sort by score descending (best matches first)
    Results.sort(key=lambda x: x["PercentageNum"], reverse=True)

    print(f"batch similarity done: compared resume against {len(ListOfJdTokens)} job descriptions")

    return Results
