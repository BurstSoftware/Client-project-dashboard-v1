import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import json
import os
from datetime import datetime

# Mock project data (replace with database)
PROJECTS_FILE = "data/projects.json"
UPLOADS_DIR = "uploads"

def load_projects():
    if os.path.exists(PROJECTS_FILE):
        with open(PROJECTS_FILE, "r") as f:
            return json.load(f)
    return {
        "client1@example.com": [
            {
                "id": 1,
                "name": "Home Renovation",
                "start_date": "2025-01-01",
                "end_date": "2025-06-30",
                "budget": 50000,
                "actual_cost": 35000,
                "milestones": [
                    {"name": "Foundation", "date": "2025-02-01", "status": "Completed", "media": []},
                    {"name": "Framing", "date": "2025-03-15", "status": "In Progress", "media": []}
                ],
                "invoices": [{"id": "INV001", "amount": 10000, "status": "Paid"}]
            }
        ],
        "client2@example.com": [
            {
                "id": 2,
                "name": "Office Build",
                "start_date": "2025-03-01",
                "end_date": "2025-12-31",
                "budget": 100000,
                "actual_cost": 40000,
                "milestones": [
                    {"name": "Site Prep", "date": "2025-04-01", "status": "Completed", "media": []}
                ],
                "invoices": [{"id": "INV002", "amount": 20000, "status": "Pending"}]
            }
        ]
    }

def save_projects(projects):
    with open(PROJECTS_FILE, "w") as f:
        json.dump(projects, f)

def render_dashboard(user):
    st.title(f"Welcome to Your Project Dashboard, {user['name']}")
    
    # Load client-specific projects
    projects = load_projects().get(user["email"], [])
    
    if not projects:
        st.warning("No projects assigned to you.")
        return

    # Project selection
    project_names = [p["name"] for p in projects]
    selected_project = st.selectbox("Select Project", project_names)
    project = next(p for p in projects if p["name"] == selected_project)

    # Layout: Two columns
    col1, col2 = st.columns([2, 1])

    with col1:
        # Timeline Visualization
        st.subheader("Project Timeline")
        fig = go.Figure()
        milestones = project["milestones"]
        for m in milestones:
            color = "green" if m["status"] == "Completed" else "orange"
            fig.add_trace(go.Bar(
                x=[m["date"]],
                y=[m["name"]],
                orientation="h",
                marker=dict(color=color)
            ))
        fig.update_layout(title="Milestone Progress", xaxis_title="Date", yaxis_title="Milestone")
        st.plotly_chart(fig)

        # Cost Tracking
        st.subheader("Cost Tracking")
        budget = project["budget"]
        actual = project["actual_cost"]
        progress = (actual / budget) * 100 if budget > 0 else 0
        st.write(f"**Budget**: ${budget:,.2f}")
        st.write(f"**Actual Cost**: ${actual:,.2f}")
        st.progress(min(progress / 100, 1.0))

    with col2:
        # Milestone Updates
        st.subheader("Milestone Updates")
        with st.form("milestone_update"):
            milestone = st.selectbox("Select Milestone", [m["name"] for m in milestones])
            status = st.selectbox("Update Status", ["In Progress", "Completed"])
            media = st.file_uploader("Upload Photo/Video", accept_multiple_files=True)
            submit = st.form_submit_button("Update")
            if submit:
                for m in milestones:
                    if m["name"] == milestone:
                        m["status"] = status
                        if media:
                            for file in media:
                                file_path = os.path.join(UPLOADS_DIR, file.name)
                                with open(file_path, "wb") as f:
                                    f.write(file.getbuffer())
                                m["media"].append(file_path)
                save_projects(load_projects())
                st.success("Milestone updated!")

        # Invoice Integration
        st.subheader("Invoices")
        for inv in project["invoices"]:
            st.write(f"Invoice {inv['id']}: ${inv['amount']:,.2f} - {inv['status']}")
        if st.button("View Invoices"):
            st.write("Redirecting to Invoice Generator...")  # Integrate with your Invoice Generator
        if st.button("View Receipts"):
            st.write("Redirecting to Receipts Input Tool...")  # Integrate with your Receipts Input Tool

    # Display Media
    st.subheader("Milestone Media")
    for m in milestones:
        if m["media"]:
            st.write(f"**{m['name']}**")
            for media in m["media"]:
                if media.endswith((".jpg", ".png")):
                    st.image(media)
                elif media.endswith((".mp4", ".mov")):
                    st.video(media)
