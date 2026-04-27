# NlpProcessor.py
# uses spaCy to tokenize text, remove stopwords, and lemmatize
import spacy
from src.GlobalSettings import KeepList

# we load it here so it doesnt reload every time we call the function
print("loading spaCy model... (this might take a sec the first time)")
NLP = spacy.load("en_core_web_sm")
print("spaCy model loaded successfully")


def Process(Text):
    """
    takes a cleaned text string and runs it through the NLP pipeline
    tokenizes -> removes stopwords -> lemmatizes
    returns a list of clean lemmas (base form of words)
    
    IMPORTANT: we handle case sensitivity carefully here
    before checking if something is a stopword we compare 
    the ORIGINAL casing against our KeepList
    so "IT" (the domain) stays but "it" (the pronoun) gets removed
    """

    # run the text through spaCys pipeline
    # this tokenizes it (breaks into individual words/tokens)
    Doc = NLP(Text)

    # this list will hold our final cleaned tokens
    ProcessedTokens = []

    # go through each token one by one
    for Token in Doc:

        # get the original word as it appeared in the text
        OriginalWord = Token.text

        # skip punctuation - we dont need commas, periods etc
        if Token.is_punct:
            continue

        # skip whitespace tokens (spaces, tabs, newlines)
        if Token.is_space:
            continue

        # skip single character tokens that arent in our keep list
        # random single letters are usually noise
        if len(OriginalWord) <= 1 and OriginalWord not in KeepList:
            continue

        # skip tokens that are just numbers
        # things like page numbers, dates as standalone numbers etc
        if Token.like_num:
            continue

        # NOW the important part - stopword handling with case sensitivity
        # check if the ORIGINAL word (with its casing) is in our keep list
        WordIsInKeepList = OriginalWord in KeepList

        # if it IS in the keep list, we keep it no matter what
        # even if spaCy thinks its a stopword
        if WordIsInKeepList:
            # keep the original casing for domain terms
            ProcessedTokens.append(OriginalWord.lower())
            continue

        # if its NOT in the keep list, check if its a stopword
        # spaCy has a built-in list of english stopwords (the, is, at, etc)
        if Token.is_stop:
            # its a stopword and NOT a protected term, so skip it
            continue

        # if we got here, the token is legit
        # lemmatize it (get the base form) and make it lowercase
        # "running" -> "run", "better" -> "good", etc
        Lemma = Token.lemma_.lower()

        # one more check - skip if the lemma is empty or just a dash
        if len(Lemma) <= 1 and Lemma not in {"c", "r"}:
            continue

        ProcessedTokens.append(Lemma)

    print(f"NLP processing done , extracted {len(ProcessedTokens)} tokens from the text")

    return ProcessedTokens
