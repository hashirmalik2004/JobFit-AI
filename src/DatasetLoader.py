# DatasetLoader.py
# handles loading and preprocessing the job description CSV dataset
# uses streamlit caching so we dont re-read and re-process the CSV every time
# the CSV has 1167 job posts with columns:
# job_id, category, job_title, job_description, job_skill_set

import os
import pandas as pd
import streamlit as st

from src.TextCleaner import Sanitize
from src.NlpProcessor import Process

DatasetPath = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "all_job_post.csv")


@st.cache_data(show_spinner=False)
def LoadDataset():

    print(f"loading dataset from: {DatasetPath}")
    Df = pd.read_csv(DatasetPath)

    # clean up any NaN values 
    Df["job_description"] = Df["job_description"].fillna("")
    Df["job_title"] = Df["job_title"].fillna("Untitled")
    Df["category"] = Df["category"].fillna("Unknown")
    Df["job_skill_set"] = Df["job_skill_set"].fillna("[]")

    print(f"dataset loaded: {len(Df)} jobs across {Df['category'].nunique()} categories")

    return Df


def GetCategories(Df):
    # returns a sorted list of unique category names from the dataset
    Categories = sorted(Df["category"].unique().tolist())
    return Categories


@st.cache_data(show_spinner=False)
def PreprocessDataset(_Df, ProgressCallback=None):
    """
    runs the full cleaning + NLP pipeline on every job description in the dataset
    returns a list of token list
    """

    TotalJobs = len(_Df)
    AllTokenLists = []

    print(f"starting preprocessing of {TotalJobs} job descriptions...")

    for Idx in range(TotalJobs):
        RawJd = _Df.iloc[Idx]["job_description"]

        if not RawJd or len(str(RawJd).strip()) < 5:
            AllTokenLists.append([])
            continue

        # 1: clean the text 
        CleanJd = Sanitize(str(RawJd))

        # 2: NLP processing (tokenize, remove stopwords, lemmatize)
        Tokens = Process(CleanJd)

        AllTokenLists.append(Tokens)

        if ProgressCallback and Idx % 50 == 0:
            ProgressCallback(Idx + 1, TotalJobs)

    print(f"preprocessing complete: processed {TotalJobs} job descriptions")

    return AllTokenLists
