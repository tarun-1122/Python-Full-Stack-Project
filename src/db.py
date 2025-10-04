# src/db.py
import os
from dotenv import load_dotenv
from supabase import create_client

# load .env from project root
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
load_dotenv(os.path.join(ROOT, ".env"))

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

if not SUPABASE_URL or not SUPABASE_KEY:
    raise RuntimeError(
        "Missing Supabase credentials. Add SUPABASE_URL and SUPABASE_KEY to the .env in project root."
    )

supabase = create_client(SUPABASE_URL, SUPABASE_KEY)


# Create question
def create_question(question_text: str, created_by: str, choices: list):
    try:
        q = supabase.table("questions").insert({
            "question_text": question_text,
            "created_by": created_by
        }).execute()
        question_id = q.data[0]["id"]
        for c in choices:
            supabase.table("choices").insert({
                "question_id": question_id,
                "choice_text": c
            }).execute()
        return {"question_id": question_id}
    except Exception as e:
        return {"error": str(e)}


# Get all questions (list)
def get_questions():
    try:
        rows = supabase.table("questions").select("*").order("created_at", desc=True).execute().data
        return rows or []
    except Exception as e:
        return {"error": str(e)}


# Get a question by id
def get_question(question_id: str):
    try:
        question = supabase.table("questions").select("*").eq("id", question_id).execute().data
        if not question:
            return None
        choices = supabase.table("choices").select("*").eq("question_id", question_id).execute().data or []
        return {
            "id": question[0]["id"],
            "question_text": question[0]["question_text"],
            "created_by": question[0]["created_by"],
            "choices": choices
        }
    except Exception as e:
        return {"error": str(e)}


# Add response (vote)
def add_response(question_id: str, choice_id: str, user_id: str):
    try:
        existing = supabase.table("responses").select("*").eq("question_id", question_id).eq("user_id", user_id).execute().data
        if existing:
            return {"error": "User already voted"}
        supabase.table("responses").insert({
            "question_id": question_id,
            "choice_id": choice_id,
            "user_id": user_id
        }).execute()
        return {"message": "Response added"}
    except Exception as e:
        return {"error": str(e)}


# Get results for a question
def get_results(question_id: str):
    try:
        choices = supabase.table("choices").select("*").eq("question_id", question_id).execute().data or []
        results = []
        for c in choices:
            count = supabase.table("responses").select("id", count="exact").eq("choice_id", c["id"]).execute()
            # supabase select with count returns .count or .data depending; to keep simple, count occurrences:
            # We'll fetch responses rows and compute length (safe albeit slightly more queries).
            resp_rows = supabase.table("responses").select("*").eq("choice_id", c["id"]).execute().data or []
            results.append({"choice_id": c["id"], "choice_text": c["choice_text"], "votes": len(resp_rows)})
        return results
    except Exception as e:
        return {"error": str(e)}
