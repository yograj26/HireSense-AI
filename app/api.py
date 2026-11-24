from fastapi import FastAPI
from pydantic import BaseModel
from .matcher import score_match
app=FastAPI(title='SmartHire AI API',version='0.1.0')
class MatchRequest(BaseModel):
 candidate_skills:list[str]
 required_skills:list[str]
 preferred_skills:list[str]=[]
@app.get('/health')
def health(): return {'status':'ok','service':'SmartHire AI'}
@app.post('/match')
def match(req:MatchRequest): return score_match(req.candidate_skills,req.required_skills,req.preferred_skills)
