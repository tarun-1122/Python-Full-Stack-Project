import os
from supabase import create_client
from dotenv import load_dotenv

#load environment variables
load_dotenv()
url=os.getenv("SUPABASE_URL")
key=os.getenv("SUPABASE_KEY")

supabase=create_client(url,key)

def add_user(name,email,password):
    payload={"username":name, "email":email, "password":password}
    resp=supabase.table("users").insert(payload).execute()
    if(resp.data):
        return "user added successfully"
    else:
        return "user not added"
    
def login_user(email, password):
    resp = supabase.table("Users").select("*").eq("email", email).eq("password", password).execute()
    if resp.data and len(resp.data) > 0:
        return f"Login successful for {resp.data[0]['username']}"
    else:
        return "Invalid email or password"


def create_poll(poll,op1,op2,op3,op4):
    payload={"question1":poll,"option1":op1,"option2":op2,"option3":op3,"option4":op4} 
    resp=supabase.table("Polls").insert(payload).execute()
    return resp

def cast_vote(poll_id, user_id, chosen_option):
    payload = {
        "poll_id": poll_id,
        "user_id": user_id,
        "chosen_option": chosen_option
    }
    resp = supabase.table("Votes").insert(payload).execute()
    if resp.data:
        return "Vote cast successfully"
    return "Vote not added"