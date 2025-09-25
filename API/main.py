# frontend --> api --> logic --> db --> response


# api/main.py

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from logic import register_user, login_user, add_new_poll, vote
from typing import Optional

app = FastAPI(title="Simple Poll API")

# -----------------------------
# Request Models
class RegisterUser(BaseModel):
    username: str
    email: str
    password: str

class LoginUser(BaseModel):
    email: str
    password: str

class CreatePoll(BaseModel):
    question: str
    option1: str
    option2: str
    option3: Optional[str] = None
    option4: Optional[str] = None
    created_by: int

class CastVote(BaseModel):
    poll_id: int
    user_id: int
    chosen_option: int

# -----------------------------
# Endpoints

@app.post("/register")
def api_register(user: RegisterUser):
    result = register_user(user.username, user.email, user.password)
    return {"message": result}

@app.post("/login")

def api_login(user: LoginUser):
    result = login_user(user.email, user.password)
    if "successful" in result:
        return {"message": result}
    else:
        raise HTTPException(status_code=400, detail=result)

@app.post("/create_poll")
def api_create_poll(poll: CreatePoll):
    result = add_new_poll(
        poll.question, poll.option1, poll.option2, poll.option3, poll.option4, poll.created_by
    )
    return {"message": result}

@app.post("/vote")
def api_cast_vote(vote_data: CastVote):
    result = vote(vote_data.poll_id, vote_data.user_id, vote_data.chosen_option)
    if "successfully" in result:
        return {"message": result}
    else:
        raise HTTPException(status_code=400, detail=result)

# -----------------------------
# Optional: Fetch all polls
@app.get("/polls")
def get_polls():
    from supabase import create_client
    import os
    from dotenv import load_dotenv

    load_dotenv()
    SUPABASE_URL = os.getenv("SUPABASE_URL")
    SUPABASE_KEY = os.getenv("SUPABASE_KEY")
    supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

    resp = supabase.table("Polls").select("*").execute()
    return {"polls": resp.data}

# -----------------------------
# Optional: Fetch poll results
@app.get("/poll_results/{poll_id}")
def get_poll_results(poll_id: int):
    from supabase import create_client
    import os
    from dotenv import load_dotenv

    load_dotenv()
    SUPABASE_URL = os.getenv("SUPABASE_URL")
    SUPABASE_KEY = os.getenv("SUPABASE_KEY")
    supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

    votes = supabase.table("Votes").select("*").eq("poll_id", poll_id).execute()
    results = {}
    for vote_record in votes.data:
        opt = vote_record["chosen_option"]
        results[opt] = results.get(opt, 0) + 1

    return {"poll_id": poll_id, "results": results}
