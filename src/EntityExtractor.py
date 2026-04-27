# EntityExtractor.py
# this file handles Skill Matching
# comparing resume skills vs job description skills using sets

from src.GlobalSettings import TechSkills



def MatchSkills(ResumeTokens, JdTokens):
    """
    takes two lists of tokens and finds which skills matched and which are missing
    uses Pythons set operations (.intersection and .difference)
    
    also cross-references against our hardcoded TechSkills list from config
    to catch skills that might have been missed
    
    returns a dictionary with:
    - Matched: skills found in BOTH resume and JD
    - Missing: skills in JD but NOT in resume (what the candidate lacks)
    - Extra: skills in resume but NOT in JD (bonus skills the candidate has)
    """

    # step 1: convert token lists to sets
    # sets automatically remove duplicates and allow fast comparison
    ResumeSet = set(ResumeTokens)
    JdSet = set(JdTokens)

    # step 2: find skills that are in BOTH the resume and job description
    # .intersection() gives us the overlap between two sets
    MatchedSkills = ResumeSet.intersection(JdSet)

    # step 3: find skills in the JD that are NOT in the resume
    # these are what the candidate is MISSING
    # .difference() gives us whats in JD but not in resume
    MissingSkills = JdSet.difference(ResumeSet)

    # step 4: find skills in the resume that are NOT in the JD
    # these are EXTRA/BONUS skills the candidate brings
    ExtraSkills = ResumeSet.difference(JdSet)

    # step 5: filter to only keep actual tech skills
    # without this filter we'd show random words like "team" or "work"
    # which arent really skills
    MatchedTech = set()
    MissingTech = set()
    ExtraTech = set()

    # check each matched skill against our tech skills database
    for Skill in MatchedSkills:
        if Skill.lower() in TechSkills:
            MatchedTech.add(Skill)

    for Skill in MissingSkills:
        if Skill.lower() in TechSkills:
            MissingTech.add(Skill)

    for Skill in ExtraSkills:
        if Skill.lower() in TechSkills:
            ExtraTech.add(Skill)

    print(f"skill matching done:")
    print(f"  matched: {len(MatchedTech)} tech skills")
    print(f"  missing from resume: {len(MissingTech)} tech skills")
    print(f"  extra in resume: {len(ExtraTech)} tech skills")

    # pack everything into a dictionary
    SkillResults = {
        "Matched": sorted(list(MatchedTech)),      # sorted for clean display
        "Missing": sorted(list(MissingTech)),
        "Extra": sorted(list(ExtraTech)),
        "MatchedCount": len(MatchedTech),
        "MissingCount": len(MissingTech),
        "ExtraCount": len(ExtraTech),
        # also include the raw (unfiltered) results in case user wants them
        "AllMatched": sorted(list(MatchedSkills)),
        "AllMissing": sorted(list(MissingSkills)),
        "AllExtra": sorted(list(ExtraSkills)),
    }

    return SkillResults
