import streamlit as st
from auth import authenticate_user
from dashboard import render_dashboard

st.set_page_config(page_title="Client Project Dashboard", layout="wide")

def main():
    # Initialize session state
    if "authenticated" not in st.session_state:
        st.session_state.authenticated = False
        st.session_state.user = None

    # Authentication
    if not st.session_state.authenticated:
        authenticate_user()
    else:
        render_dashboard(st.session_state.user)

if __name__ == "__main__":
    main()
