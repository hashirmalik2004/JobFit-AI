# i use TF-IDF to turn text into numbers
# then use Cosine Similarity to measure how close the resume is to the job description
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


def ComputeSimilarity(ResumeTokens, JdTokens):
    """
    takes two lists of tokens one from resume and one from job description
    converts them into TF-IDF vectors and calculates cosine similarity
    """
                     
    ResumeString = " ".join(ResumeTokens)
    JdString = " ".join(JdTokens)

    Vectorizer = TfidfVectorizer()

    # fit and transform both documents at once
    BothDocuments = [ResumeString, JdString]
    TfidfMatrix = Vectorizer.fit_transform(BothDocuments)

    #extract the individual vectors
    ResumeVector = TfidfMatrix[0]  
    JdVector = TfidfMatrix[1] 

    #calculate cosine similarity between the two vectors
    SimilarityMatrix = cosine_similarity(ResumeVector, JdVector)
    RawScore = SimilarityMatrix[0][0]

    #convert to percentage
    Percentage = round(RawScore * 100, 2)
    PercentageStr = f"{Percentage}%"

    FeatureNames = Vectorizer.get_feature_names_out().tolist()

    print(f"similarity calculated: {PercentageStr}")

    Results = {
        "Score": RawScore,
        "Percentage": PercentageStr,
        "PercentageNum": Percentage,
        "ResumeVector": ResumeVector,
        "JdVector": JdVector,
        "FeatureNames": FeatureNames,
    }

    return Results

#mode 2 in the ui for comparing resume against dataset
def ComputeBatchSimilarity(ResumeTokens, ListOfJdTokens):


    ResumeString = " ".join(ResumeTokens)
    JdStrings = [" ".join(Tokens) for Tokens in ListOfJdTokens]

    AllDocuments = [ResumeString] + JdStrings

    Vectorizer = TfidfVectorizer()
    TfidfMatrix = Vectorizer.fit_transform(AllDocuments)

    ResumeVector = TfidfMatrix[0]
    JdVectors = TfidfMatrix[1:]

    SimilarityScores = cosine_similarity(ResumeVector, JdVectors)
    ScoresFlat = SimilarityScores[0]  # flatten to 1D array

    Results = []
    for Idx, RawScore in enumerate(ScoresFlat):
        Percentage = round(RawScore * 100, 2)
        Results.append({
            "Index": Idx,
            "Score": RawScore,
            "Percentage": f"{Percentage}%",
            "PercentageNum": Percentage,
        })

    #sort by score descending (best matches first)
    Results.sort(key=lambda x: x["PercentageNum"], reverse=True)

    print(f"batch similarity done: compared resume against {len(ListOfJdTokens)} job descriptions")

    return Results
