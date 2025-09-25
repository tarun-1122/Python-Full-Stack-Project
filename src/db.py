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

def create_poll(poll,op1,op2,op3,op4):
    payload={"question1":poll,"option1":op1,"option2":op2,"option3":op3,"option4":op4} 
    resp=supabase.table("Polls").insert(payload).execute()
    return resp