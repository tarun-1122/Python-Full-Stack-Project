# logic.py
import supabase
from db import add_user, create_poll, cast_vote
from supabase import create_client
from dotenv import load_dotenv
import os
API_URL="http://localhost:8000"

# Load environment variables for Supabase
load_dotenv()
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# -----------------------------
# Function to register a new user
def register_user(username, email, password):
    if not username or not email or not password:
        return "All fields are required"
    
    # Call db.py function to insert user
    result = add_user(username, email, password)
    return result

# -----------------------------
# Login a user
def login_user(email, password):
    if not email or not password:
        return "Email and password are required"

    # Query Supabase to find the user by email
    resp = supabase.table("Users").select("*").eq("email", email).execute()

    if resp.data and len(resp.data) > 0:
        stored_password = resp.data[0]["password"]

        # Compare plain passwords
        if password == stored_password:
            return f"Login successful for {resp.data[0]['username']}"
        else:
            return "Invalid password"
    else:
        return "User not found"

# -----------------------------
# Function to create a new poll
def add_new_poll(question, option1, option2, option3=None, option4=None, created_by=None):
    if not question or not option1 or not option2:
        return "Question and at least 2 options are required"

    payload = {
        "question1": question,
        "option1": option1,
        "option2": option2,
        "option3": option3,
        "option4": option4
    }

    # Optional: include created_by if you want to track creator
    if created_by:
        payload["created_by"] = created_by

    # Call db.py function
    resp = create_poll(question, option1, option2, option3, option4)
    if resp.data:
        return "Poll created successfully"
    return "Poll creation failed"

# -----------------------------
# Function to cast vote
def vote(poll_id, user_id, chosen_option):
    # Basic validation
    if not poll_id or not user_id or not chosen_option:
        return "All fields are required to vote"
    
    # Optional: Check if user has already voted for this poll
    existing_votes = supabase.table("Votes").select("*").eq("poll_id", poll_id).eq("user_id", user_id).execute()
    if existing_votes.data and len(existing_votes.data) > 0:
        return "You have already voted in this poll"

    # Call db.py function to insert vote
    result = cast_vote(poll_id, user_id, chosen_option)
    return result

# -----------------------------
# Example usage
if __name__ == "__main__":
    # Register user
    print(register_user("Alice", "alice@example.com", "pass123"))

    # Create poll
    print(add_new_poll("Favorite programming language?", "Python", "Java", "C++", "JavaScript", created_by=1))

    # Cast vote
    print(vote(1, 2, 1))  # user_id=2 votes option1 in poll_id=1
