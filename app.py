# app.py
# this is the main entry point - the Streamlit dashboard
# run it with: streamlit run app.py
# it creates a web interface where recruiters can upload resumes
# and paste job descriptions to see how well they match

import streamlit as st
import pandas as pd
import time

# import all our custom modules
from src.PdfParser import ExtractTextFromBytes
from src.TextCleaner import Sanitize
from src.NlpProcessor import Process
from src.Vectorizer import ComputeSimilarity, ComputeBatchSimilarity
from src.EntityExtractor import MatchSkills
from src.DatasetLoader import LoadDataset, GetCategories, PreprocessDataset


# ============================================================
# PAGE CONFIG - set up the streamlit page settings
# this has to be the very first streamlit command
# ============================================================

st.set_page_config(
    page_title="JobFit AI - Discover how well your resume matches real job descriptions in seconds.",
    page_icon="📄",
    layout="wide",  # use the full width of the page
    initial_sidebar_state="expanded"
)

# ============================================================
# SIDEBAR - instructions 
# ============================================================

with st.sidebar:
    st.markdown("## 📄JobFit AI")
    st.markdown("---")
    
    st.markdown("""
     Single Job Match:
    1. Upload your resume in PDF format
    2. Paste a job description in the text box
    3. Click Analyze
    """)
    
    st.markdown("---")

    st.markdown("""
    Dataset Job Search:
    1. Upload your resume in PDF format
    2. Pick a category filter (optional)
    3. Click Search and your resume gets ranked
       against 1,167 real job posts against a exisiting dataset
    """)


# ============================================================
# MAIN HEADER
# ============================================================

st.markdown("""
<div class="main-header">
    <h1>JobFit AI</h1>
    <p> Discover how well your resume matches real job descriptions in seconds</p>
</div>
""", unsafe_allow_html=True)

# ============================================================
# CUSTOM CSS - make it look dark and premium
# streamlit has a theming system but custom css gives more control
# ============================================================

st.markdown("""
<style>
    /* main background and text */
    .stApp {
        background: linear-gradient(135deg, #0f0f1a 0%, #1a1a2e 50%, #16213e 100%);
    }
    
    /* header styling */
    .main-header {
        text-align: center;
        padding: 1.5rem 0;
        background: linear-gradient(135deg, rgba(0, 150, 255, 0.1), rgba(138, 43, 226, 0.1));
        border-radius: 16px;
        border: 1px solid rgba(0, 150, 255, 0.2);
        margin-bottom: 2rem;
    }
    
    .main-header h1 {
        background: linear-gradient(135deg, #00bfff, #8a2be2);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 2.8rem;
        font-weight: 800;
        margin-bottom: 0.3rem;
    }
    
    .main-header p {
        color: #a0a0c0;
        font-size: 1.1rem;
    }
    
    /* score display card */
    .score-card {
        text-align: center;
        padding: 2rem;
        background: linear-gradient(135deg, rgba(0, 150, 255, 0.15), rgba(138, 43, 226, 0.15));
        border-radius: 16px;
        border: 1px solid rgba(0, 150, 255, 0.3);
        margin: 1rem 0;
    }
    
    .score-number {
        font-size: 4rem;
        font-weight: 900;
        background: linear-gradient(135deg, #00bfff, #8a2be2);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    .score-label {
        color: #a0a0c0;
        font-size: 1.1rem;
        margin-top: 0.5rem;
    }
    
    /* skill tags */
    .skill-tag-matched {
        display: inline-block;
        padding: 4px 12px;
        margin: 3px;
        border-radius: 20px;
        background: rgba(50, 205, 50, 0.2);
        border: 1px solid rgba(50, 205, 50, 0.4);
        color: #50cd32;
        font-size: 0.85rem;
    }
    
    .skill-tag-missing {
        display: inline-block;
        padding: 4px 12px;
        margin: 3px;
        border-radius: 20px;
        background: rgba(255, 69, 58, 0.2);
        border: 1px solid rgba(255, 69, 58, 0.4);
        color: #ff453a;
        font-size: 0.85rem;
    }
    
    .skill-tag-extra {
        display: inline-block;
        padding: 4px 12px;
        margin: 3px;
        border-radius: 20px;
        background: rgba(0, 150, 255, 0.2);
        border: 1px solid rgba(0, 150, 255, 0.4);
        color: #0096ff;
        font-size: 0.85rem;
    }
    
    /* info cards */
    .info-card {
        padding: 1.2rem;
        background: rgba(255, 255, 255, 0.05);
        border-radius: 12px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        margin: 0.5rem 0;
    }
    
    .info-card h4 {
        color: #00bfff;
        margin-bottom: 0.5rem;
    }
    
    /* sidebar styling */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #0f0f1a 0%, #1a1a2e 100%);
    }
    
    /* status indicator dots */
    .status-good { color: #32cd32; }
    .status-ok { color: #ffa500; }
    .status-bad { color: #ff453a; }
    
    /* metric cards override */
    [data-testid="stMetric"] {
        background: rgba(255, 255, 255, 0.05);
        border-radius: 12px;
        padding: 1rem;
        border: 1px solid rgba(255, 255, 255, 0.1);
    }
</style>
""", unsafe_allow_html=True)




# ============================================================
# MODE SELECTOR - choose between single JD or dataset search
# ============================================================

st.markdown("")  # spacing
SelectedMode = st.radio(
    "Choose Analysis Mode",
    ["Single Job Match", "Dataset Job Search"],
    horizontal=True,
    
)

st.markdown("---")


# ============================================================
# MODE 1: SINGLE JOB MATCH (existing feature - untouched logic)
# ============================================================

if SelectedMode == "Single Job Match":

    # ---- INPUT SECTION ----
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

    # ---- ANALYZE BUTTON ----
    st.markdown("")
    ButtonCol1, ButtonCol2, ButtonCol3 = st.columns([1, 1, 1])
    with ButtonCol2:
        AnalyzeClicked = st.button(
            " Analyze Resume",
            use_container_width=True,
            type="primary"
        )

    # ---- ANALYSIS PIPELINE ----
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

        # ---- RESULTS DISPLAY ----
        st.markdown("---")
        st.markdown("## Analysis Results")

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

            # ---- context note ----
            st.info("These results are calculated based on keyword similarity (TF-IDF). "
                    "A higher score means more keyword overlap with your resume, "
                    "not necessarily a better or worse fit. Use this as a starting "
                    "point to find relevant job postings or improve your resume.")
                    

        TotalSkills = SkillResults["MatchedCount"] + SkillResults["MissingCount"]
        if TotalSkills > 0:
            SkillRatio = SkillResults["MatchedCount"] / TotalSkills
        else:
            SkillRatio = 0
        
        SkillPercent = round(SkillRatio * 100, 1)

        # ---- Skill Status ----
        if SkillRatio >= 0.7:
            StatusEmoji = "🟢"
            StatusText = "Strong Match"
        elif SkillRatio >= 0.4:
            StatusEmoji = "🟡"
            StatusText = "Partial Match"
        else:
            StatusEmoji = "🔴"
            StatusText = "Low Match"

        with StatsCol:
            st.markdown("### 🎯 Skill Analysis")

            # --- MAIN METRIC (dominant) ---
            st.metric(
                label=f"{StatusEmoji} Skill Match",
                value=f"{SkillPercent}%",
                delta=f"{StatusText}"
            )

            # --- CONTEXT MESSAGE ---
            if SkillRatio >= 0.7:
                st.success("Your resume aligns well with the required skills.")
            elif SkillRatio >= 0.4:
                st.warning("You meet some requirements but could improve key areas.")
            else:
                st.error("Significant skill gaps detected for this role.")

            st.markdown("---")

            # --- SECONDARY METRICS ---
            MetricCol1, MetricCol2 = st.columns(2)

            with MetricCol1:
                st.metric("✅ Matched Skills", SkillResults["MatchedCount"])
                st.metric("❌ Missing Skills", SkillResults["MissingCount"])

            with MetricCol2:
                st.metric("➕ Extra Skills", SkillResults["ExtraCount"])

        # ---- Skill Breakdown ----
        st.markdown("### Skill Breakdown")
        SkillCol1, SkillCol2, SkillCol3 = st.columns(3)

        with SkillCol1:
            st.markdown("####  Matched Skills")
            if SkillResults["Matched"]:
                MatchedHtml = ""
                for Skill in SkillResults["Matched"]:
                    MatchedHtml = MatchedHtml + f'<span class="skill-tag-matched">{Skill}</span>'
                st.markdown(MatchedHtml, unsafe_allow_html=True)
            else:
                st.info("No matching tech skills found")

        with SkillCol2:
            st.markdown("####  Missing from Resume")
            if SkillResults["Missing"]:
                MissingHtml = ""
                for Skill in SkillResults["Missing"]:
                    MissingHtml = MissingHtml + f'<span class="skill-tag-missing">{Skill}</span>'
                st.markdown(MissingHtml, unsafe_allow_html=True)
            else:
                st.success("No missing skills")

        with SkillCol3:
            st.markdown("#### Extra Skills ")
            if SkillResults["Extra"]:
                ExtraHtml = ""
                for Skill in SkillResults["Extra"]:
                    ExtraHtml = ExtraHtml + f'<span class="skill-tag-extra">{Skill}</span>'
                st.markdown(ExtraHtml, unsafe_allow_html=True)
            else:
                st.info("No extra tech skills found")

        st.markdown("---")

        with st.expander("📄 View Extracted Resume Text (raw)"):
            st.text(ResumeRawText[:3000])
            if len(ResumeRawText) > 3000:
                st.caption(f"... showing first 3000 of {len(ResumeRawText)} characters")


# ============================================================
# MODE 2: DATASET JOB SEARCH (new feature)
# ============================================================

elif SelectedMode == "Dataset Job Search":

    # ---- INPUT SECTION ----
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

    # ---- SEARCH BUTTON ----
    st.markdown("")
    BtnCol1, BtnCol2, BtnCol3 = st.columns([1, 1, 1])
    with BtnCol2:
        SearchClicked = st.button(
            " Search Job Dataset",
            use_container_width=True,
            type="primary"
        )

    # ---- SEARCH PIPELINE ----
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

        # ---- RESULTS DISPLAY ----
        st.markdown("---")
        st.markdown("## Dataset Search Results")

        # summary card
        st.markdown(f"""
        <div class="score-card">
            <div class="score-number">{TotalJobs}</div>
            <div class="score-label">Jobs Analyzed</div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("")

        # build the results dataframe from top N
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

        # ---- context note ----
        st.info("These results are ranked by Skill Match ratio. "
                "Keyword Similarity (TF-IDF) is also shown for reference.")


        # ---- RANKED TABLE ----
        st.markdown("### Ranked Job Matches")
        st.caption("Ranked by keyword overlap — not a quality judgment on your resume.")
        st.dataframe(
            ResultsDf,
            use_container_width=True,
            hide_index=True,
            height=min(400, 40 + len(TableRows) * 35)
        )

        st.markdown("---")

        # ---- EXPANDABLE JOB DETAILS ----
        st.markdown("### Job Details (click to expand)")
        for Rank, Result in enumerate(TopResults[:10], 1):
            Idx = Result["Index"]
            Row = FilteredDf.iloc[Idx]
            
            # Use precomputed Skill Match for this specific job
            SkillResults = Result["SkillResults"]
            SkillRatio = Result["SkillRatio"]
            SkillPercent = Result["SkillPercent"]

            # ---- Skill Status ----
            if SkillRatio >= 0.7:
                StatusEmoji = "🟢"
                StatusText = "Strong Match"
            elif SkillRatio >= 0.4:
                StatusEmoji = "🟡"
                StatusText = "Partial Match"
            else:
                StatusEmoji = "🔴"
                StatusText = "Low Match"

            with st.expander(f"{StatusEmoji} #{Rank} — {Row['job_title']} (Skill Match: {SkillPercent}%)"):
                st.markdown(f"**Category:** {Row['category']} | **Job ID:** {Row['job_id']}")
                st.markdown(f"**Keyword Similarity (TF-IDF):** {Result['Percentage']}")
                st.caption("This score reflects keyword overlap, not how qualified you are.")

                st.markdown("---")
                st.markdown("#### 🎯 Skill Analysis")
                
                # --- MAIN METRIC (dominant) ---
                st.metric(
                    label=f"{StatusEmoji} Skill Match",
                    value=f"{SkillPercent}%",
                    delta=f"{StatusText}"
                )

                # --- CONTEXT MESSAGE ---
                if SkillRatio >= 0.7:
                    st.success("Your resume aligns well with the required skills.")
                elif SkillRatio >= 0.4:
                    st.warning("You meet some requirements but could improve key areas.")
                else:
                    st.error("Significant skill gaps detected for this role.")

                # --- SECONDARY METRICS ---
                MetricCol1, MetricCol2 = st.columns(2)

                with MetricCol1:
                    st.metric("✅ Matched Skills", SkillResults["MatchedCount"])
                    st.metric("❌ Missing Skills", SkillResults["MissingCount"])

                with MetricCol2:
                    st.metric("➕ Extra Skills", SkillResults["ExtraCount"])

                st.markdown("---")
                st.markdown("**Skills Required:**")
                st.markdown(f"```\n{Row['job_skill_set']}\n```")

                st.markdown("**Job Description (first 1500 chars):**")
                JdPreview = str(Row["job_description"])[:1500]
                st.text(JdPreview)
                if len(str(Row["job_description"])) > 1500:
                    st.caption("... truncated")

