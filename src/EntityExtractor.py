# this file handles Skill Matching
# comparing resume skills vs job description skills

from src.GlobalSettings import TechSkills



def MatchSkills(ResumeTokens, JdTokens):
    """    
    returns a dictionary with:
    - Matched: skills found in BOTH resume and job description
    - Missing: skills in JD but NOT in resume
    - Extra: skills in resume but NOT in JD 
    """

    # 1: convert token lists to sets
    ResumeSet = set(ResumeTokens)
    JdSet = set(JdTokens)

    # 2: find skills that are in both the resume and job description
    MatchedSkills = ResumeSet.intersection(JdSet)

    # 3: find skills in the JD that are not in the resume
    MissingSkills = JdSet.difference(ResumeSet)

    # 4: Extra skills
    ExtraSkills = ResumeSet.difference(JdSet)

    MatchedTech = set()
    MissingTech = set()
    ExtraTech = set()

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

    
    SkillResults = {
        "Matched": sorted(list(MatchedTech)),      
        "Missing": sorted(list(MissingTech)),
        "Extra": sorted(list(ExtraTech)),
        "MatchedCount": len(MatchedTech),
        "MissingCount": len(MissingTech),
        "ExtraCount": len(ExtraTech),
        "AllMatched": sorted(list(MatchedSkills)),
        "AllMissing": sorted(list(MissingSkills)),
        "AllExtra": sorted(list(ExtraSkills)),
    }

    return SkillResults
