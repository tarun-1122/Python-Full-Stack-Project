# frontend/app.py
import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000"  # change if backend deployed

st.set_page_config(page_title="Simple Polling System", layout="wide")
st.title("🗳 Simple Polling System")

# username input
# Ask for username only if not stored yet
if "user_id" not in st.session_state:
    st.session_state.user_id = ""

# input box for username
username_input = st.text_input("Enter your username :", value=st.session_state.user_id)
if username_input:
    st.session_state.user_id = username_input  # save typed username

tab1, tab2, tab3, tab4 = st.tabs(["Create Question", "Respond", "View Results", "Fetch by ID"])

# Helper to safely GET and return JSON (or empty list)
def safe_get(path):
    try:
        r = requests.get(f"{API_URL}{path}", timeout=5)
    except Exception as e:
        return {"error": f"Connection error: {e}"}
    if r.status_code != 200:
        return {"error": f"API error: {r.status_code} - {r.text}"}
    try:
        return r.json()
    except Exception as e:
        return {"error": f"Invalid JSON from API: {e}. Raw: {r.text}"}

# Create Question
with tab1:
    st.header("Create a Question")
    q = st.text_input("Question Text:")
    opts = st.text_area("Choices (comma-separated):")
    if st.button("Create Question"):
        if not st.session_state.user_id:
            st.error("Enter username first.")
        else:
            choices = [o.strip() for o in opts.split(",") if o.strip()]
            payload = {"question_text": q, "created_by": st.session_state.user_id, "choices": choices}
            try:
                r = requests.post(f"{API_URL}/create_question", json=payload, timeout=5)
                if r.status_code == 200:
                    st.success(f"Question created: {r.json()}")
                else:
                    st.error(f"Error: {r.status_code} - {r.text}")
            except Exception as e:
                st.error(f"Request failed: {e}")

# Respond (vote)
with tab2:
    st.header("Respond to a Question")
    q_res = safe_get("/questions")
    if isinstance(q_res, dict) and q_res.get("error"):
        st.error(q_res["error"])
    else:
        questions = q_res or []
        q_map = {q["question_text"]: q["id"] for q in questions}
        if not q_map:
            st.info("No questions available.")
        else:
            selected = st.selectbox("Choose Question:", list(q_map.keys()))
            question_id = q_map[selected]
            q_detail = safe_get(f"/questions/{question_id}")
            if isinstance(q_detail, dict) and q_detail.get("error"):
                st.error(q_detail["error"])
            elif q_detail:
                choices = {c["choice_text"]: c["id"] for c in q_detail.get("choices", [])}
                choice = st.radio("Choices:", list(choices.keys()))
                if st.button("Submit Response"):
                    if not st.session_state.user_id:
                        st.error("Enter username first.")
                    else:
                        payload = {"question_id": question_id, "choice_id": choices[choice], "user_id": st.session_state.user_id}
                        try:
                            r = requests.post(f"{API_URL}/respond", json=payload, timeout=5)
                            if r.status_code == 200:
                                st.success(r.json())
                            else:
                                st.error(f"Error: {r.status_code} - {r.text}")
                        except Exception as e:
                            st.error(f"Request failed: {e}")

# View Results
with tab3:
    st.header("Question Results")
    q_res = safe_get("/questions")
    if isinstance(q_res, dict) and q_res.get("error"):
        st.error(q_res["error"])
    else:
        questions = q_res or []
        q_map = {q["question_text"]: q["id"] for q in questions}
        if not q_map:
            st.info("No questions available.")
        else:
            selected = st.selectbox("Choose Question:", list(q_map.keys()), key="results_box")
            question_id = q_map[selected]
            r = safe_get(f"/results/{question_id}")
            if isinstance(r, dict) and r.get("error"):
                st.error(r["error"])
            else:
                results = r or []
                if results:
                    chart_data = {item["choice_text"]: item["votes"] for item in results}
                    st.bar_chart(chart_data)
                else:
                    st.info("No results yet.")

# Fetch by ID
# Fetch by ID and allow voting
# Tab 4: Fetch Question by ID / Vote (works for numeric or string IDs)
# Tab 4: Fetch Question by ID / Vote with proper state handling
with tab4:
    st.header("Fetch Question by ID / Vote")

    qid_input = st.text_input("Enter Question ID:", value=st.session_state.get("last_question_id", ""))
    
    # Store fetched question in session_state to persist across reruns
    if "fetched_question" not in st.session_state:
        st.session_state.fetched_question = None

    if st.button("Fetch Question", key="fetch_question_btn"):
        if not qid_input.strip():
            st.error("Enter a Question ID.")
        else:
            question_id = qid_input.strip()
            r = requests.get(f"{API_URL}/questions/{question_id}", timeout=5)
            if r.status_code != 200:
                st.error(f"API Error {r.status_code}: {r.text}")
            else:
                st.session_state.fetched_question = r.json()
                st.session_state.last_question_id = question_id  # optional: remember last

    # Display question and voting only if fetched
    q_data = st.session_state.fetched_question
    if q_data:
        st.subheader(q_data["question_text"])
        choices = {c["choice_text"]: c["id"] for c in q_data.get("choices", [])}

        if choices:
            # store selected choice in session_state to persist across reruns
            if "selected_choice" not in st.session_state:
                st.session_state.selected_choice = None

            st.session_state.selected_choice = st.radio(
                "Choices:",
                list(choices.keys()),
                index=0 if st.session_state.selected_choice is None else
                      list(choices.keys()).index(st.session_state.selected_choice),
                key=f"radio_tab4_{q_data['id']}"
            )

            # Submit vote button
            if st.button("Submit Vote", key=f"submit_vote_tab4_{q_data['id']}"):
                if not st.session_state.user_id:
                    st.error("Enter username first.")
                else:
                    payload = {
                        "question_id": q_data["id"],
                        "choice_id": choices[st.session_state.selected_choice],
                        "user_id": st.session_state.user_id
                    }
                    resp = requests.post(f"{API_URL}/respond", json=payload, timeout=5)
                    if resp.status_code == 200:
                        st.success("Vote submitted successfully!")
                        # Clear fetched question to prevent re-submission
                        st.session_state.fetched_question = None
                        st.session_state.selected_choice = None
                    else:
                        st.error(f"Vote failed {resp.status_code}: {resp.text}")
