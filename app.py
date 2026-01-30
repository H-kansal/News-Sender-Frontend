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

if "subscribed" not in st.session_state:
    st.session_state.subscribed = False


# ---------------- SIGNUP ----------------
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
                st.session_state.email = email
                st.session_state.subscribed = True

                st.success(
                    "Signup successful! Check your email to verify your subscription."
                )
            else:
                st.error("Signup failed")

# ---------------- SUBSCRIPTION STATE ----------------
else:
    st.subheader("📬 Subscription Status")

    if st.session_state.subscribed:
        st.success("We are sending you daily AI updates.")

        if st.button("Unsubscribe"):
            resp = requests.post(
                f"{BASE_URL}/unsubscribe",
                json={"email": st.session_state.email}
            )

            if resp.status_code == 200:
                st.session_state.subscribed = resp.get("is_active",False)
                st.warning("You have unsubscribed from daily updates.")

            else:
                st.error("Failed to unsubscribe")

    else:
        st.info("You are currently unsubscribed from daily AI updates.")

        if st.button("Subscribe"):
            resp = requests.post(
                f"{BASE_URL}/signup",
                json={"email": st.session_state.email}
            )

            if resp.status_code == 200:
                st.session_state.subscribed = resp.get("is_active",False)
                st.success(
                    "Subscription request sent! Please verify via email."
                )
            else:
                st.error("Failed to subscribe")
