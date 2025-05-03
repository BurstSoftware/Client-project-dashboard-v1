import streamlit as st
import json
import os

# Mock client data (replace with database)
CLIENTS_FILE = "data/clients.json"

def load_clients():
    if os.path.exists(CLIENTS_FILE):
        with open(CLIENTS_FILE, "r") as f:
            return json.load(f)
    return {
        "client1@example.com": {"password": "pass123", "role": "client", "name": "Client 1"},
        "client2@example.com": {"password": "pass456", "role": "client", "name": "Client 2"}
    }

def authenticate_user():
    st.title("Client Login")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    
    if st.button("Login"):
        clients = load_clients()
        if email in clients and clients[email]["password"] == password:
            st.session_state.authenticated = True
            st.session_state.user = {"email": email, "name": clients[email]["name"]}
            st.success(f"Welcome, {clients[email]['name']}!")
            st.experimental_rerun()
        else:
            st.error("Invalid credentials")

    # Optional: Register new client (admin-managed)
    with st.expander("Register (Admin Only)"):
        new_email = st.text_input("New Client Email")
        new_password = st.text_input("New Client Password", type="password")
        new_name = st.text_input("Client Name")
        if st.button("Register"):
            clients = load_clients()
            clients[new_email] = {"password": new_password, "role": "client", "name": new_name}
            with open(CLIENTS_FILE, "w") as f:
                json.dump(clients, f)
            st.success("Client registered!")
