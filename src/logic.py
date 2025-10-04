# src/logic.py
from src import db

def create_question_logic(question_text: str, created_by: str, choices: list):
    if not question_text or not isinstance(choices, list) or len(choices) < 2:
        return {"error": "Question must have text and at least 2 choices"}
    return db.create_question(question_text, created_by, choices)

def fetch_all_questions():
    return db.get_questions()

def fetch_question_by_id(question_id: str):
    return db.get_question(question_id)

def response_logic(question_id: str, choice_id: str, user_id: str):
    if not question_id or not choice_id or not user_id:
        return {"error": "question_id, choice_id and user_id are required"}
    return db.add_response(question_id, choice_id, user_id)

def results_logic(question_id: str):
    return db.get_results(question_id)
