# i used spaCy to tokenize text, remove stopwords, and lemmatize
import spacy
from src.GlobalSettings import KeepList

print("loading spaCy model(this might take a sec the first time)")
NLP = spacy.load("en_core_web_sm")
print("spaCy model loaded successfully")


def Process(Text):
    """
     takes a cleaned text string and runs it through the NLP pipeline
    tokenizes -> removes stopwords -> lemmatizes
    returns a list of clean lemmas (base form of words)
    """

    Doc = NLP(Text)
    ProcessedTokens = []

    for Token in Doc:

        OriginalWord = Token.text

        if Token.is_punct:
            continue
        if Token.is_space:
            continue
        if len(OriginalWord) <= 1 and OriginalWord not in KeepList:
            continue
        if Token.like_num:
            continue

        WordIsInKeepList = OriginalWord in KeepList

        if WordIsInKeepList:
            ProcessedTokens.append(OriginalWord.lower())
            continue

        # if its not in the keep list check if its a stopword
        if Token.is_stop:
            continue
        #lematize
        Lemma = Token.lemma_.lower()

        #bcz c and r can be only one word token that can mean its a tech skill
        if len(Lemma) <= 1 and Lemma not in {"c", "r"}:
            continue

        ProcessedTokens.append(Lemma)

    print(f"NLP processing done , extracted {len(ProcessedTokens)} tokens from the text")

    return ProcessedTokens
