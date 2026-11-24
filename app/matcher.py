import re
from collections import Counter

ALIASES = {'ml':'machine learning','sklearn':'scikit-learn','sklearn':'scikit-learn','nlp':'natural language processing','js':'javascript'}

def normalize_skills(skills):
    return sorted({ALIASES.get(s.strip().lower(), s.strip().lower()) for s in skills if s.strip()})

def extract_skills(text, taxonomy):
    text = text.lower()
    found=[]
    for skill in taxonomy:
        s=ALIASES.get(skill.lower(),skill.lower())
        if re.search(r'(?<![\w])'+re.escape(s)+r'(?![\w])',text): found.append(skill)
    return sorted(set(found))

def score_match(candidate_skills, required_skills, preferred_skills=None):
    required=normalize_skills(required_skills)
    candidate=normalize_skills(candidate_skills)
    preferred=normalize_skills(preferred_skills or [])
    if not required and not preferred:
        return {'score':0,'matched_required':[],'missing_required':[],'matched_preferred':[],'explanation':'No skills specified in job requirements.'}
    c=set(candidate); r=set(required); p=set(preferred)
    matched=sorted(c&r); missing=sorted(r-c); matched_pref=sorted(c&p)
    # Required skills carry 80% and preferred skills 20% when both groups exist.
    req_score=(len(matched)/len(r)*80) if r else 80
    pref_score=(len(matched_pref)/len(p)*20) if p else 20
    score=round(req_score+pref_score)
    expl=f'Matched {len(matched)} of {len(r)} required skills and {len(matched_pref)} of {len(p)} preferred skills.'
    return {'score':score,'matched_required':matched,'missing_required':missing,'matched_preferred':matched_pref,'explanation':expl}
