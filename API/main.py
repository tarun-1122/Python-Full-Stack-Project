# api/main.py
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from src import logic

app = FastAPI(title="Simple Poll API")

# allow Streamlit local origin and others during dev
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8501", "http://127.0.0.1:8501", "*"],  # '*' is permissive for dev; lock down in prod
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class QuestionRequest(BaseModel):
    question_text: str
    created_by: str
    choices: list

class ResponseRequest(BaseModel):
    question_id: str
    choice_id: str
    user_id: str

@app.get("/questions")
def list_questions():
    res = logic.fetch_all_questions()
    if isinstance(res, dict) and res.get("error"):
        raise HTTPException(status_code=500, detail=res["error"])
    return res

@app.get("/questions/{question_id}")
def get_question(question_id: str):
    res = logic.fetch_question_by_id(question_id)
    if res is None:
        raise HTTPException(status_code=404, detail="Question not found")
    if isinstance(res, dict) and res.get("error"):
        raise HTTPException(status_code=500, detail=res["error"])
    return res

@app.post("/create_question")
def create_question(req: QuestionRequest):
    res = logic.create_question_logic(req.question_text, req.created_by, req.choices)
    if isinstance(res, dict) and res.get("error"):
        raise HTTPException(status_code=400, detail=res["error"])
    return res

@app.post("/respond")
def respond(req: ResponseRequest):
    res = logic.response_logic(req.question_id, req.choice_id, req.user_id)
    if isinstance(res, dict) and res.get("error"):
        raise HTTPException(status_code=400, detail=res["error"])
    return res

@app.get("/results/{question_id}")
def results(question_id: str):
    res = logic.results_logic(question_id)
    if isinstance(res, dict) and res.get("error"):
        raise HTTPException(status_code=500, detail=res["error"])
    return res
