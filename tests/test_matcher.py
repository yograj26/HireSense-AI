from app.matcher import score_match, extract_skills
T=['Python','SQL','Machine Learning','Scikit-learn','Pandas']
def test_full_required_match():
 r=score_match(['Python','SQL'],['Python','SQL'],[]); assert r['score']==100

def test_partial_required():
 r=score_match(['Python'],['Python','SQL'],[]); assert r['score']==60

def test_preferred_score():
 r=score_match(['Python','Pandas'],['Python'],['Pandas']); assert r['score']==100

def test_skill_alias():
 r=score_match(['ML','sklearn'],['Machine Learning','Scikit-learn'],[]); assert r['score']==100

def test_extract():
 assert 'Python' in extract_skills('I use Python and SQL',T)
