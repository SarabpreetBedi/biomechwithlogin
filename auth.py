import streamlit as st
from supabase import create_client, Client
import os

# Only use st.secrets for configuration
SUPABASE_URL = st.secrets["SUPABASE_URL"]
SUPABASE_KEY = st.secrets.get("SUPABASE_SERVICE_ROLE_KEY")
if not SUPABASE_KEY:
    st.error("SUPABASE_SERVICE_ROLE_KEY is missing from your secrets! Please add it to .streamlit/secrets.toml or Streamlit Cloud secrets.")
    raise RuntimeError("SUPABASE_SERVICE_ROLE_KEY is missing from your secrets!")
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

# Add this at the top of the file
try:
    from your_main_app import is_admin
except ImportError:
    ADMIN_EMAILS = st.secrets.get("ADMIN_EMAILS", [])
    def is_admin(email):
        return email in ADMIN_EMAILS

if 'user' not in st.session_state:
    st.session_state.user = None
if 'profile' not in st.session_state:
    st.session_state.profile = {}

def login():
    st.subheader("Login")
    email = st.text_input("Email", key="login_email")
    pwd = st.text_input("Password", type="password", key="login_pwd")
    if st.button("Login"):
        try:
            res = supabase.auth.sign_in_with_password({"email": email, "password": pwd})
            if res.user and res.session:
                try:
                    profile_result = supabase.table("profiles").select("is_admin").eq("id", res.user.id).execute()
                    if profile_result.data:
                        st.session_state.profile = profile_result.data[0]
                    else:
                        profile_data = {"id": res.user.id, "is_admin": is_admin(res.user.email)}
                        user_supabase = create_client(SUPABASE_URL, res.session.access_token)
                        user_supabase.table("profiles").insert(profile_data).execute()
                        st.session_state.profile = profile_data
                except Exception as profile_error:
                    try:
                        profile_data = {"id": res.user.id, "is_admin": is_admin(res.user.email)}
                        user_supabase = create_client(SUPABASE_URL, res.session.access_token)
                        user_supabase.table("profiles").insert(profile_data).execute()
                        st.session_state.profile = profile_data
                    except Exception as create_error:
                        st.error(f"❌ Could not create profile: {create_error}")
                        st.session_state.profile = {"is_admin": False}
                        return
                st.session_state.user = res.user
                st.session_state.session = res.session
                st.session_state.user_email = res.user.email
                st.success("✅ Logged in")
                st.rerun()
            else:
                st.error("❌ Login failed. Please check your credentials.")
        except Exception as e:
            st.error(f"❌ Login error: {e}")

def signup():
    st.subheader("Create Account")
    email = st.text_input("Email", key="su_email")
    pwd = st.text_input("Password", type="password", key="su_pwd")
    if st.button("Sign Up"):
        try:
            res = supabase.auth.sign_up({"email": email, "password": pwd})
            if res.user:
                st.success("✅ Account created successfully! You can now log in.")
            else:
                st.error("❌ Sign-up error")
        except Exception as e:
            st.error(f"❌ Sign-up error: {e}")

def auth_screen():
    st.title("Login Page")
    option = st.selectbox("Choose an Action:", ["Login", "Sign Up"])
    if option == "Login":
        login()
    else:
        signup()

def sign_out():
    supabase.auth.sign_out()
    st.session_state.user = None
    st.session_state.session = None
    st.session_state.user_email = None
    st.session_state.profile = {}
    st.rerun()

def main():
    auth_screen()

if __name__ == "__main__":
    main()


