# frontend/app.py

import streamlit as st
import requests

# -----------------------------
# Backend API URL
API_URL = "http://localhost:8000"

# -----------------------------
st.title("Simple Polling System")

# -----------------------------
# Sidebar Navigation
menu = ["Home", "Register", "Login", "Create Poll", "Vote", "View Polls"]
choice = st.sidebar.selectbox("Menu", menu)

# -----------------------------
if choice == "Home":
    st.subheader("Welcome to the Simple Polling System")
    st.write("Use the sidebar to navigate through registration, login, poll creation, voting, and viewing results.")

# -----------------------------
elif choice == "Register":
    st.subheader("Register New User")
    username = st.text_input("Username")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    if st.button("Register"):
        data = {"username": username, "email": email, "password": password}
        response = requests.post(f"{API_URL}/register", json=data)
        st.success(response.json()["message"])

# -----------------------------
elif choice == "Login":
    st.subheader("User Login")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        data = {"email": email, "password": password}
        response = requests.post(f"{API_URL}/login", json=data)
        if response.status_code == 200:
            st.success(response.json()["message"])
        else:
            st.error(response.json()["detail"])

# -----------------------------
elif choice == "Create Poll":
    st.subheader("Create a New Poll")
    question = st.text_input("Poll Question")
    option1 = st.text_input("Option 1")
    option2 = st.text_input("Option 2")
    option3 = st.text_input("Option 3 (optional)")
    option4 = st.text_input("Option 4 (optional)")
    created_by = st.number_input("Your User ID", min_value=1, step=1)

    if st.button("Create Poll"):
        data = {
            "question": question,
            "option1": option1,
            "option2": option2,
            "option3": option3 if option3 else None,
            "option4": option4 if option4 else None,
            "created_by": created_by
        }
        response = requests.post(f"{API_URL}/create_poll", json=data)
        st.success(response.json()["message"])

# -----------------------------
elif choice == "Vote":
    st.subheader("Vote in a Poll")
    poll_id = st.number_input("Poll ID", min_value=1, step=1)
    user_id = st.number_input("Your User ID", min_value=1, step=1)
    chosen_option = st.number_input("Option Number", min_value=1, step=1)

    if st.button("Vote"):
        data = {"poll_id": poll_id, "user_id": user_id, "chosen_option": chosen_option}
        response = requests.post(f"{API_URL}/vote", json=data)
        if response.status_code == 200:
            st.success(response.json()["message"])
        else:
            st.error(response.json()["detail"])

# -----------------------------
elif choice == "View Polls":
    st.subheader("View Polls and Results")
    response = requests.get(f"{API_URL}/polls")
    polls = response.json()["polls"]
    for poll in polls:
        st.write(f"Poll ID: {poll['id']}")
        st.write(f"Question: {poll['question1']}")
        st.write(f"Options: 1.{poll['option1']}  2.{poll['option2']}  3.{poll.get('option3','')}  4.{poll.get('option4','')}")
        # Show poll results
        result_resp = requests.get(f"{API_URL}/poll_results/{poll['id']}")
        st.write(f"Results: {result_resp.json()['results']}")
        st.markdown("---")
