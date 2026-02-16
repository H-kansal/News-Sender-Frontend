import streamlit as st
import requests
from dotenv import load_dotenv
import os

load_dotenv()
st.set_page_config(page_title="AI Digest Signup")

BASE_URL = os.getenv("BACKEND_URL")

st.title("🧠 Daily AI Digest")
st.write("Curated AI updates, delivered daily.")

# ---------------- SESSION STATE ----------------
if "email" not in st.session_state:
    st.session_state.email = None

if "is_active" not in st.session_state:
    st.session_state.is_active = None


# ---------------- SIGNUP SCREEN ----------------
if not st.session_state.email:

    st.subheader("📩 Sign Up")
    email = st.text_input("Email address")

    if st.button("Sign Up"):
    if not email:
        st.error("Please enter an email address")
    else:
        resp = requests.post(
            f"{BASE_URL}/signup",
            json={"email": email}
        )

        if resp.status_code == 200:
            data = resp.json()

            st.session_state.email = data.get("email")
            st.session_state.is_active = data.get("is_active")

            st.rerun()

        else:
            st.error("Signup failed")

# ---------------- DASHBOARD ----------------
else:
    st.subheader("📬 Subscription Status")
    st.write(f"Logged in as: **{st.session_state.email}**")

    # ACTIVE USER
    if st.session_state.is_active:
        st.success("You are receiving daily AI updates.")

        if st.button("Unsubscribe"):
            try:
                resp = requests.post(
                    f"{BASE_URL}/unsubscribe",
                    json={"email": st.session_state.email}
                )

                if resp.status_code == 200:
                    data = resp.json()
                    st.session_state.is_active = data.get("is_active", False)

                    st.warning("You have unsubscribed.")

                    st.rerun()

                else:
                    st.error("Failed to unsubscribe")

            except Exception as e:
                st.error(f"Error: {e}")

    # INACTIVE USER
    else:
        st.info("You are currently unsubscribed.")

        if st.button("Subscribe"):
            try:
                resp = requests.post(
                    f"{BASE_URL}/subscribe",
                    json={"email": st.session_state.email}
                )

                if resp.status_code == 200:
                    data = resp.json()
                    st.session_state.is_active = data.get("is_active", True)

                    st.success("You are subscribed again 🎉")

                    st.rerun()

                else:
                    st.error("Failed to subscribe")

            except Exception as e:
                st.error(f"Error: {e}")

    if st.button("Logout"):
        st.session_state.email = None
        st.session_state.is_active = None
        st.rerun()
