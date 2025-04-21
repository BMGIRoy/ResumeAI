import streamlit as st
import json
import uuid
import os
from datetime import datetime
from utils import save_job, save_candidate, analyze_resume, analyze_video, load_jobs, load_candidates

# Ensure database folders exist
if not os.path.exists('database'):
    os.makedirs('database')

st.set_page_config(page_title="Recruiter AI App", layout="wide")

# Recruiter Dashboard
def recruiter_dashboard():
    st.header("Recruiter Dashboard")

    st.subheader("Post a Job")
    job_title = st.text_input("Job Title")
    jd_file = st.file_uploader("Upload Job Description (PDF/DOCX)", type=["pdf", "docx"])
    interview_questions = st.text_area("Set Interview Questions (one per line)")

    if st.button("Create Job Posting"):
        if job_title and jd_file:
            job_id = str(uuid.uuid4())[:8]
            save_job(job_id, job_title, jd_file, interview_questions)
            st.success(f"Job Created! Share this link with candidates:")
            st.code(f"?page=candidate&job_id={job_id}")
        else:
            st.error("Please provide all the information.")

    st.subheader("Manage Jobs")
    jobs = load_jobs()
    if jobs:
        for job in jobs:
            st.write(f"**{job['job_title']}** - ID: {job['job_id']}")

# Candidate Interface
def candidate_interface(job_id):
    st.header("Candidate Application")

    jobs = load_jobs()
    job = next((j for j in jobs if j['job_id'] == job_id), None)

    if job:
        st.subheader(f"Applying for: {job['job_title']}")

        name = st.text_input("Full Name")
        email = st.text_input("Email")
        phone = st.text_input("Phone Number")

        resume_file = st.file_uploader("Upload Your Resume", type=["pdf", "docx"])

        st.subheader("Interview Questions")
        questions = job['questions'].splitlines()
        answers = []
        for q in questions:
            answer = st.text_area(q)
            answers.append((q, answer))

        st.subheader("Record your Interview Video")
        video_file = st.camera_input("Record Video")

        if st.button("Submit Application"):
            if name and email and resume_file:
                save_candidate(job_id, name, email, phone, resume_file, answers, video_file)
                st.success("Application Submitted Successfully!")
            else:
                st.error("Please fill in all required fields.")
    else:
        st.error("Invalid Job Link")

# Dashboard
def recruiter_dashboard_status():
    st.header("Recruiter Status Dashboard")

    jobs = load_jobs()
    candidates = load_candidates()

    for job in jobs:
        st.subheader(f"Job: {job['job_title']}")
        job_candidates = [c for c in candidates if c['job_id'] == job['job_id']]
        st.write(f"Total Candidates: {len(job_candidates)}")
        for candidate in job_candidates:
            st.write(f"- {candidate['name']} ({candidate['email']})")
            st.write(f"  Applied On: {candidate['timestamp']}")
            st.write(f"  Resume Score: {candidate.get('resume_score', 'N/A')}")
            st.write(f"  Video Score: {candidate.get('video_score', 'N/A')}")

        if st.button(f"Download Candidates for {job['job_title']}"):
            job_data = [c for c in candidates if c['job_id'] == job['job_id']]
            st.download_button(
                label="Download JSON",
                data=json.dumps(job_data),
                file_name=f"{job['job_title']}_candidates.json",
                mime="application/json"
            )

# Router
def main():
    query_params = st.query_params
    page = query_params.get("page", "home")

    with st.sidebar:
        st.title("Navigation")
        selected_page = st.selectbox("Go to:", ["Home", "Post Jobs (Recruiter)", "Dashboard"])

        if selected_page == "Post Jobs (Recruiter)":
            st.query_params.update({"page": "recruiter"})
        elif selected_page == "Dashboard":
            st.query_params.update({"page": "dashboard"})
        else:
            st.query_params.update({"page": "home"})

    if page == "recruiter":
        recruiter_dashboard()
    elif page == "candidate":
        job_id = query_params.get("job_id", None)
        if job_id:
            candidate_interface(job_id)
        else:
            st.error("Job ID missing.")
    elif page == "dashboard":
        recruiter_dashboard_status()
    else:
        st.title("Welcome to Recruiter AI Platform")
        st.write("Please choose a role from the sidebar.")

if __name__ == "__main__":
    main()
