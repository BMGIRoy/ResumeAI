import json
import os
import uuid
from datetime import datetime

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

def analyze_resume(resume_path):
    # Placeholder: simple scoring logic
    return 80

def analyze_video(video_path):
    # Placeholder: simulate emotional analysis
    return 75

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
