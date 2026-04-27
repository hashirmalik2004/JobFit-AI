# DatasetLoader.py
# handles loading and preprocessing the job description CSV dataset
# uses streamlit caching so we dont re-read and re-process the CSV every time
# the user clicks a button - that would be painfully slow
#
# the CSV has 1167 job posts with columns:
# job_id, category, job_title, job_description, job_skill_set

import os
import pandas as pd
import streamlit as st

from src.TextCleaner import Sanitize
from src.NlpProcessor import Process


# path to the CSV file (its now in the data folder)
DatasetPath = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "all_job_post.csv")


@st.cache_data(show_spinner=False)
def LoadDataset():
    """
    reads the CSV file into a pandas DataFrame
    cached by streamlit so it only runs once per session
    
    returns the full DataFrame
    """

    print(f"loading dataset from: {DatasetPath}")
    Df = pd.read_csv(DatasetPath)

    # clean up any NaN values in critical columns
    # some job descriptions might be empty which would crash our pipeline
    Df["job_description"] = Df["job_description"].fillna("")
    Df["job_title"] = Df["job_title"].fillna("Untitled")
    Df["category"] = Df["category"].fillna("Unknown")
    Df["job_skill_set"] = Df["job_skill_set"].fillna("[]")

    print(f"dataset loaded: {len(Df)} jobs across {Df['category'].nunique()} categories")

    return Df


def GetCategories(Df):
    """
    returns a sorted list of unique category names from the dataset
    used for the filter dropdown in the UI
    """
    Categories = sorted(Df["category"].unique().tolist())
    return Categories


@st.cache_data(show_spinner=False)
def PreprocessDataset(_Df, ProgressCallback=None):
    """
    runs the full cleaning + NLP pipeline on every job description in the dataset
    returns a list of token lists (one per job)
    
    this is the expensive operation - cleaning and tokenizing 1167 job descriptions
    but thanks to @st.cache_data it only runs ONCE and then the results are cached
    
    ProgressCallback is an optional function that gets called with (current, total)
    so we can show a progress bar in the UI
    
    note: the _Df parameter has an underscore prefix because streamlit cant hash
    DataFrames by default, so the underscore tells it to skip hashing this param
    """

    TotalJobs = len(_Df)
    AllTokenLists = []

    print(f"starting preprocessing of {TotalJobs} job descriptions...")

    for Idx in range(TotalJobs):
        # get the raw job description text
        RawJd = _Df.iloc[Idx]["job_description"]

        # skip empty descriptions
        if not RawJd or len(str(RawJd).strip()) < 5:
            AllTokenLists.append([])
            continue

        # step 1: clean the text (remove URLs, emojis, etc)
        CleanJd = Sanitize(str(RawJd))

        # step 2: NLP processing (tokenize, remove stopwords, lemmatize)
        Tokens = Process(CleanJd)

        AllTokenLists.append(Tokens)

        # update progress if callback is provided
        if ProgressCallback and Idx % 50 == 0:
            ProgressCallback(Idx + 1, TotalJobs)

    print(f"preprocessing complete: processed {TotalJobs} job descriptions")

    return AllTokenLists
