import json
import os
import uuid
from datetime import datetime
from pdfminer.high_level import extract_text
import random
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Load database safely
def load_jobs():
    try:
        with open("database/jobs.json", "r") as f:
            return json.load(f)
    except:
        return []


def load_candidates():
    try:
        with open("database/candidates.json", "r") as f:
            return json.load(f)
    except:
        return []

# Save job posting
def save_job(job_id, job_title, jd_file, questions):
    jd_path = f"database/{job_id}_jd.pdf"
    with open(jd_path, "wb") as f:
        f.write(jd_file.getbuffer())

    jobs = load_jobs()
    jobs.append({
        "job_id": job_id,
        "job_title": job_title,
        "jd_file": jd_path,
        "questions": questions,
        "timestamp": str(datetime.now())
    })
    with open("database/jobs.json", "w") as f:
        json.dump(jobs, f)

# Save candidate application or manual upload
def save_candidate(job_id, name, email, phone, resume_file, answers, video_file):
    candidate_id = str(uuid.uuid4())[:8]
    resume_path = f"database/{candidate_id}_resume.pdf"
    with open(resume_path, "wb") as f:
        f.write(resume_file.getbuffer())

    video_path = None
    if video_file:
        video_path = f"database/{candidate_id}_video.mp4"
        with open(video_path, "wb") as f:
            f.write(video_file.getbuffer())

    candidate = {
        "candidate_id": candidate_id,
        "job_id": job_id,
        "name": name,
        "email": email,
        "phone": phone,
        "resume_path": resume_path,
        "video_path": video_path,
        "answers": answers,
        "timestamp": str(datetime.now()),
        "resume_score": analyze_resume(resume_path),
        "video_score": analyze_video(video_path) if video_path else None
    }

    candidates = load_candidates()
    candidates.append(candidate)

    with open("database/candidates.json", "w") as f:
        json.dump(candidates, f)

# Simple Resume Analysis
def analyze_resume(resume_path):
    try:
        text = extract_text(resume_path)
        keywords = ["python", "data", "machine learning", "ai", "project management", "communication", "leadership"]
        match_count = sum(1 for word in keywords if word.lower() in text.lower())
        score = min(match_count * 15, 100)
        return score
    except:
        return 50

# Simulated Video Analysis
def analyze_video(video_path):
    confidence_score = random.randint(70, 95)
    return confidence_score

# Email Sending Function
def send_email(recipient_email, subject, body):
    sender_email = "your_email@example.com"  # <-- replace with your sender email
    sender_password = "your_password"        # <-- replace with your email password or app password

    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = recipient_email
    msg['Subject'] = subject

    msg.attach(MIMEText(body, 'plain'))

    try:
        with smtplib.SMTP('smtp.gmail.com', 587) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.sendmail(sender_email, recipient_email, msg.as_string())
    except Exception as e:
        print("Email sending failed:", e)
