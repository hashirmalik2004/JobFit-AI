# the streamlit dashboard
import streamlit as st
import pandas as pd
import time

from src.PdfParser import ExtractTextFromBytes
from src.TextCleaner import Sanitize
from src.NlpProcessor import Process
from src.Vectorizer import ComputeSimilarity, ComputeBatchSimilarity
from src.EntityExtractor import MatchSkills
from src.DatasetLoader import LoadDataset, GetCategories, PreprocessDataset

st.set_page_config(
    page_title="JobFit AI",
    page_icon="📄",
    layout="wide",
    initial_sidebar_state="expanded"
)

#sidebar design
with st.sidebar:
    st.markdown("## How it works")
    st.markdown("---")
    
    st.markdown("""
     Single Job Match:
    1. Upload your resume in PDF format
    2. Paste a job description in the text box
    3. Click Analyze and it will give you a score based on how much your skills match
    """)
    
    st.markdown("---")

    st.markdown("""
    Dataset Job Search:
    1. Upload your resume in PDF format
    2. Pick a category filter (optional)
    3. Click Search and your resume gets ranked
       against 1,167 real job posts against a exisiting dataset
    """)


#main header
st.markdown("""
<div class="main-header">
    <h1>JobFit AI</h1>
    <p> Discover how well your resume matches real job descriptions in seconds</p>
</div>
""", unsafe_allow_html=True)


#custom css
st.markdown("""
<style>
    /* main background */
    
    .stApp {
        background-color: #222831;
        color: #DFD0B8;
    }
    
    /* sidebar styling */
    [data-testid="stSidebar"] {
        background-color: #393E46;
        border-right: 1px solid #948979;
    }
    
    /* header styling */
    .main-header {
        text-align: center;
        padding: 2rem 0;
        background-color: #393E46;
        border-radius: 20px;
        border: 2px solid #948979;
        margin-bottom: 2.5rem;
        box-shadow: 0 10px 30px rgba(0,0,0,0.3);
    }
    
    .main-header h1 {
        color: #DFD0B8;
        font-size: 3.5rem;
        font-weight: 900;
        margin-bottom: 0.5rem;
        letter-spacing: -1px;
    }
    
    .main-header p {
        color: #948979;
        font-size: 1.2rem;
        font-weight: 500;
    }
    
    /* score card styling */

    .score-card {
        text-align: center;
        padding: 2.5rem;
        background-color: #393E46;
        border-radius: 20px;
        border: 2px solid #948979;
        margin: 1rem 0;
        transition: transform 0.3s ease;
    }
    
    .score-card:hover {
        transform: translateY(-5px);
    }
    
    .score-number {
        font-size: 4.5rem;
        font-weight: 900;
        color: #948979;
        line-height: 1;
    }
    
    .score-label {
        color: #DFD0B8;
        font-size: 1.2rem;
        margin-top: 1rem;
        font-weight: 600;
    }
    
    /* skill tags styling */

    .skill-tag-matched {
        display: inline-block;
        padding: 6px 14px;
        margin: 4px;
        border-radius: 8px;
        background: rgba(148, 137, 121, 0.15);
        border: 1px solid #948979;
        color: #948979;
        font-size: 0.9rem;
        font-weight: 600;
    }
    
    .skill-tag-missing {
        display: inline-block;
        padding: 6px 14px;
        margin: 4px;
        border-radius: 8px;
        background: rgba(255, 69, 58, 0.1);
        border: 1px solid rgba(255, 69, 58, 0.5);
        color: #ff6b6b;
        font-size: 0.9rem;
    }
    
    .skill-tag-extra {
        display: inline-block;
        padding: 6px 14px;
        margin: 4px;
        border-radius: 8px;
        background: rgba(223, 208, 184, 0.1);
        border: 1px solid rgba(223, 208, 184, 0.4);
        color: #DFD0B8;
        font-size: 0.9rem;
    }
    
    /* override streamlit components */

    .stButton>button {
        background-color: #948979 !important;
        color: #222831 !important;
        font-weight: 700 !important;
        border-radius: 10px !important;
        border: none !important;
        padding: 0.5rem 2rem !important;
    }
    
    .stTextInput>div>div>input, .stTextArea>div>div>textarea {
        background-color: #393E46 !important;
        color: #DFD0B8 !important;
        border: 1px solid #948979 !important;
    }
    
    [data-testid="stMetric"] {
        background-color: #393E46;
        border: 1px solid #948979;
        border-radius: 15px;
        padding: 1.5rem;
    }

    [data-testid="stMetricValue"] {
        color: #948979 !important;
    }

    [data-testid="stMetricLabel"] {
        color: #DFD0B8 !important;
    }
    
    h1, h2, h3, h4, h5, h6, p, span, label {
        color: #DFD0B8 !important;
    }

    hr {
        border-color: #393E46 !important;
    }
</style>
""", unsafe_allow_html=True)




# mode selector
st.markdown("") 
SelectedMode = st.radio(
    "choose analysis mode",
    ["Single Job Match", "Dataset Job Search"],
    horizontal=True,
)

st.markdown("---")

# mode 1: single job match
if SelectedMode == "Single Job Match":
    # input section
    InputCol1, InputCol2 = st.columns(2)

    with InputCol1:
        st.markdown("###  Upload Resume")
        UploadedFile = st.file_uploader(
            "Drop your resume PDF here",
            type=["pdf"],
            key="single_upload"
        )
        if UploadedFile:
            st.success(f"✅ Uploaded: {UploadedFile.name}")

    with InputCol2:
        st.markdown("###  Job Description")
        JobDescription = st.text_area(
            "Paste the job description here",
            height=200,
            placeholder="Paste the full job description text against which u want to match ur resume here..."
        )
        if JobDescription:
            st.caption(f"{len(JobDescription)} characters")

    # analyze button
    st.markdown("")
    ButtonCol1, ButtonCol2, ButtonCol3 = st.columns([1, 1, 1])
    with ButtonCol2:
        AnalyzeClicked = st.button(
            "analyze resume",
            use_container_width=True,
            type="primary"
        )

    # analysis pipeline
    if AnalyzeClicked:

        if not UploadedFile:
            st.error(" Please upload a resume PDF first")
            st.stop()

        if not JobDescription or len(JobDescription.strip()) < 20:
            st.error(" Please paste a job description (at least 20 characters)")
            st.stop()

        ProgressBar = st.progress(0, text="Starting analysis...")

        ProgressBar.progress(10, text=" Extracting text from PDF...")
        time.sleep(0.3)
        PdfBytes = UploadedFile.read()
        ResumeRawText = ExtractTextFromBytes(PdfBytes)

        if not ResumeRawText or len(ResumeRawText.strip()) < 10:
            st.error(" Couldnt extract text from the PDF. Make sure its not a scanned image.")
            st.stop()

        ProgressBar.progress(25, text=" Cleaning and sanitizing text...")
        time.sleep(0.3)
        ResumeClean = Sanitize(ResumeRawText)
        JdClean = Sanitize(JobDescription)

        ProgressBar.progress(40, text=" Running NLP pipeline...")
        time.sleep(0.3)
        ResumeTokens = Process(ResumeClean)
        JdTokens = Process(JdClean)

        ProgressBar.progress(60, text=" Computing TF-IDF vectors and similarity...")
        time.sleep(0.3)
        SimilarityResults = ComputeSimilarity(ResumeTokens, JdTokens)

        ProgressBar.progress(80, text="Matching skills...")
        time.sleep(0.3)
        SkillResults = MatchSkills(ResumeTokens, JdTokens)

        ProgressBar.progress(100, text=" Analysis complete!")
        time.sleep(0.5)
        ProgressBar.empty()

        # results display
        st.markdown("---")
        st.markdown("## analysis results")

        ScoreCol, StatsCol = st.columns([1, 1])

        with ScoreCol:
            MatchScore = SimilarityResults["PercentageNum"]
            if MatchScore >= 70:
                StatusEmoji = "🟢"
                StatusText = "Keyword Similarity Score"
            elif MatchScore >= 40:
                StatusEmoji = "🟡"
                StatusText = "Keyword Similarity Score"
            else:
                StatusEmoji = "🔴"
                StatusText = "Keyword Similarity Score"

            st.markdown(f"""
            <div class="score-card">
                <div class="score-number">{SimilarityResults["Percentage"]}</div>
                <div class="score-label">{StatusEmoji} {StatusText}</div>
            </div>
            """, unsafe_allow_html=True)

            # context note
            st.info("these results are calculated based on keyword similarity (tf-idf). "
                    "a higher score means more keyword overlap with your resume, "
                    "not necessarily a better or worse fit. use this as a starting "
                    "point to find relevant job postings or improve your resume.")
                    

        TotalSkills = SkillResults["MatchedCount"] + SkillResults["MissingCount"]
        if TotalSkills > 0:
            SkillRatio = SkillResults["MatchedCount"] / TotalSkills
        else:
            SkillRatio = 0
        
        SkillPercent = round(SkillRatio * 100, 1)

        # skill status
        if SkillRatio >= 0.7:
            StatusEmoji = "🟢"
            StatusText = "strong match"
        elif SkillRatio >= 0.4:
            StatusEmoji = "🟡"
            StatusText = "partial match"
        else:
            StatusEmoji = "🔴"
            StatusText = "low match"

        with StatsCol:
            st.markdown("###  skill analysis")

            # main metric
            st.metric(
                label=f"{StatusEmoji} skill match",
                value=f"{SkillPercent}%",
                delta=f"{StatusText}"
            )

            # context message
            if SkillRatio >= 0.7:
                st.success("your resume aligns well with the required skills.")
            elif SkillRatio >= 0.4:
                st.warning("you meet some requirements but could improve key areas.")
            else:
                st.error("significant skill gaps detected for this role.")

            st.markdown("---")

            # secondary metrics
            MetricCol1, MetricCol2 = st.columns(2)

            with MetricCol1:
                st.metric("✅ matched skills", SkillResults["MatchedCount"])
                st.metric("❌ missing skills", SkillResults["MissingCount"])

            with MetricCol2:
                st.metric("➕ extra skills", SkillResults["ExtraCount"])

        # skill breakdown
        st.markdown("### skill breakdown")
        SkillCol1, SkillCol2, SkillCol3 = st.columns(3)

        with SkillCol1:
            st.markdown("#### matched skills")
            if SkillResults["Matched"]:
                MatchedHtml = ""
                for Skill in SkillResults["Matched"]:
                    MatchedHtml = MatchedHtml + f'<span class="skill-tag-matched">{Skill}</span>'
                st.markdown(MatchedHtml, unsafe_allow_html=True)
            else:
                st.info("no matching tech skills found")

        with SkillCol2:
            st.markdown("#### missing from resume")
            if SkillResults["Missing"]:
                MissingHtml = ""
                for Skill in SkillResults["Missing"]:
                    MissingHtml = MissingHtml + f'<span class="skill-tag-missing">{Skill}</span>'
                st.markdown(MissingHtml, unsafe_allow_html=True)
            else:
                st.success("no missing skills")

        with SkillCol3:
            st.markdown("#### extra skills")
            if SkillResults["Extra"]:
                ExtraHtml = ""
                for Skill in SkillResults["Extra"]:
                    ExtraHtml = ExtraHtml + f'<span class="skill-tag-extra">{Skill}</span>'
                st.markdown(ExtraHtml, unsafe_allow_html=True)
            else:
                st.info("no extra tech skills found")

        st.markdown("---")

        with st.expander("📄 view extracted resume text (raw)"):
            st.text(ResumeRawText[:3000])
            if len(ResumeRawText) > 3000:
                st.caption(f"... showing first 3000 of {len(ResumeRawText)} characters")

# mode 2: dataset job search
elif SelectedMode == "Dataset Job Search":
    # input section
    InputCol1, InputCol2 = st.columns([1, 1])

    with InputCol1:
        st.markdown("###  Upload Resume")
        DatasetUploadedFile = st.file_uploader(
            "Drop your resume PDF here",
            type=["pdf"],
            help="Upload a PDF resume to search against the job dataset",
            key="dataset_upload"
        )
        if DatasetUploadedFile:
            st.success(f"✅ Uploaded: {DatasetUploadedFile.name}")

    with InputCol2:
        st.markdown("###  Search Filters")

        # load the dataset to get category options
        DatasetDf = LoadDataset()
        CategoryList = GetCategories(DatasetDf)

        # category multiselect filter
        SelectedCategories = st.multiselect(
            "Filter by Category (leave empty for all)",
            options=CategoryList,
            default=[],
            help="Select one or more categories to narrow your search"
        )

        # how many results to show
        TopN = st.slider(
            "Number of top results to show",
            min_value=5, max_value=50, value=15, step=5
        )

    # search button
    st.markdown("")
    BtnCol1, BtnCol2, BtnCol3 = st.columns([1, 1, 1])
    with BtnCol2:
        SearchClicked = st.button(
            "search job dataset",
            use_container_width=True,
            type="primary"
        )

    # search pipeline
    if SearchClicked:

        if not DatasetUploadedFile:
            st.error(" Please upload a resume PDF first")
            st.stop()

        ProgressBar = st.progress(0, text="Starting dataset search...")

        # step 1: extract resume text
        ProgressBar.progress(5, text=" Extracting text from PDF...")
        time.sleep(0.3)
        PdfBytes = DatasetUploadedFile.read()
        ResumeRawText = ExtractTextFromBytes(PdfBytes)

        if not ResumeRawText or len(ResumeRawText.strip()) < 10:
            st.error(" Couldnt extract text from the PDF.")
            st.stop()

        # step 2: clean resume
        ProgressBar.progress(10, text=" Cleaning resume text...")
        time.sleep(0.3)
        ResumeClean = Sanitize(ResumeRawText)

        # step 3: NLP on resum
        ProgressBar.progress(15, text=" Processing resume with NLP...")
        time.sleep(0.3)
        ResumeTokens = Process(ResumeClean)

        # step 4: load and filter dataset
        ProgressBar.progress(20, text=" Loading job dataset...")
        time.sleep(0.3)
        FullDf = LoadDataset()

        # apply category filter if selected
        if SelectedCategories:
            FilteredDf = FullDf[FullDf["category"].isin(SelectedCategories)].reset_index(drop=True)
        else:
            FilteredDf = FullDf.reset_index(drop=True)

        TotalJobs = len(FilteredDf)

        if TotalJobs == 0:
            st.error("No jobs found for the selected categories")
            st.stop()

        # step 5: preprocess all job descriptions (cached after first run)
        ProgressBar.progress(30, text=f" Preprocessing {TotalJobs} job descriptions (first run only)...")

        # we pass the filtered dataframe's job descriptions through the pipeline
        # use cache key based on categories to avoid reprocessing
        CacheKey = str(sorted(SelectedCategories)) if SelectedCategories else "all"

        @st.cache_data(show_spinner=False)
        def ProcessFilteredJobs(CatKey, _JobDescriptions):
            """process all job descriptions - cached per category filter"""
            TokenLists = []
            for Jd in _JobDescriptions:
                if not Jd or len(str(Jd).strip()) < 5:
                    TokenLists.append([])
                    continue
                CleanJd = Sanitize(str(Jd))
                Tokens = Process(CleanJd)
                TokenLists.append(Tokens)
            return TokenLists

        JdTokenLists = ProcessFilteredJobs(CacheKey, FilteredDf["job_description"].tolist())

        # step 6: compute batch similarity
        ProgressBar.progress(70, text=" Computing TF-IDF similarity against all jobs...")
        time.sleep(0.3)
        BatchResults = ComputeBatchSimilarity(ResumeTokens, JdTokenLists)

        # step 7: compute skill match for all jobs and re-rank
        ProgressBar.progress(85, text=" Calculating skill matches...")
        for Result in BatchResults:
            Idx = Result["Index"]
            JobTokens = JdTokenLists[Idx]
            SkillRes = MatchSkills(ResumeTokens, JobTokens)
            
            TotalSkills = SkillRes["MatchedCount"] + SkillRes["MissingCount"]
            if TotalSkills > 0:
                SkillRatio = SkillRes["MatchedCount"] / TotalSkills
            else:
                SkillRatio = 0
                
            Result["SkillRatio"] = SkillRatio
            Result["SkillPercent"] = round(SkillRatio * 100, 1)
            Result["SkillResults"] = SkillRes

        # re-sort by SkillRatio descending, use TF-IDF as tiebreaker
        BatchResults.sort(key=lambda x: (x["SkillRatio"], x["PercentageNum"]), reverse=True)

        ProgressBar.progress(100, text=" Search complete!")
        time.sleep(0.5)
        ProgressBar.empty()

        # results display
        st.markdown("---")
        st.markdown("## dataset search results")

        # summary card
        st.markdown(f"""
        <div class="score-card">
            <div class="score-number">{TotalJobs}</div>
            <div class="score-label">jobs analyzed</div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("")

        # build results table
        TopResults = BatchResults[:TopN]
        TableRows = []
        for Rank, Result in enumerate(TopResults, 1):
            Idx = Result["Index"]
            Row = FilteredDf.iloc[Idx]
            TableRows.append({
                "Rank": Rank,
                "Job Title": Row["job_title"],
                "Category": Row["category"],
                "Skill Match %": f"{Result['SkillPercent']}%",
                "Keyword Similarity %": Result["Percentage"],
            })

        ResultsDf = pd.DataFrame(TableRows)

        # context note
        st.info("these results are ranked by skill match ratio. "
                "keyword similarity (tf-idf) is also shown for reference.")


        # ranked table
        st.markdown("### ranked job matches")
        st.caption("ranked by keyword overlap — not a quality judgment on your resume.")
        st.dataframe(
            ResultsDf,
            use_container_width=True,
            hide_index=True,
            height=min(400, 40 + len(TableRows) * 35)
        )

        st.markdown("---")

        # expandable job details
        st.markdown("### job details (click to expand)")
        for Rank, Result in enumerate(TopResults[:10], 1):
            Idx = Result["Index"]
            Row = FilteredDf.iloc[Idx]
            
            # use precomputed skill match
            SkillResults = Result["SkillResults"]
            SkillRatio = Result["SkillRatio"]
            SkillPercent = Result["SkillPercent"]

            # skill status
            if SkillRatio >= 0.7:
                StatusEmoji = "🟢"
                StatusText = "strong match"
            elif SkillRatio >= 0.4:
                StatusEmoji = "🟡"
                StatusText = "partial match"
            else:
                StatusEmoji = "🔴"
                StatusText = "low match"

            with st.expander(f"{StatusEmoji} #{Rank} — {Row['job_title']} (Skill Match: {SkillPercent}%)"):
                st.markdown(f"**category:** {Row['category']} | **job id:** {Row['job_id']}")
                st.markdown(f"**keyword similarity (tf-idf):** {Result['Percentage']}")
                st.caption("this score reflects keyword overlap, not how qualified you are.")

                st.markdown("---")
                st.markdown("####  skill analysis")
                
                # main metric
                st.metric(
                    label=f"{StatusEmoji} skill match",
                    value=f"{SkillPercent}%",
                    delta=f"{StatusText}"
                )

                # context message
                if SkillRatio >= 0.7:
                    st.success("your resume aligns well with the required skills.")
                elif SkillRatio >= 0.4:
                    st.warning("you meet some requirements but could improve key areas.")
                else:
                    st.error("significant skill gaps detected for this role.")

                # secondary metrics
                MetricCol1, MetricCol2 = st.columns(2)

                with MetricCol1:
                    st.metric("✅ matched skills", SkillResults["MatchedCount"])
                    st.metric("❌ missing skills", SkillResults["MissingCount"])

                with MetricCol2:
                    st.metric("➕ extra skills", SkillResults["ExtraCount"])

                st.markdown("---")
                st.markdown("**skills required:**")
                st.markdown(f"```\n{Row['job_skill_set']}\n```")

                st.markdown("**job description (first 1500 chars):**")
                JdPreview = str(Row["job_description"])[:1500]
                st.text(JdPreview)
                if len(str(Row["job_description"])) > 1500:
                    st.caption("... truncated")

