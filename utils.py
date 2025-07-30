import os
import re
from datetime import datetime
from werkzeug.utils import secure_filename
from app import app, db
from models import Report, Match

def normalize_plate(s: str) -> str:
    """Normalize license plate string for consistent matching"""
    if not s: 
        return ""
    s = s.upper()
    s = re.sub(r"[\s\-_/\.]", "", s)
    return s

def normalize_chassis(s: str) -> str:
    """Normalize chassis number string for consistent matching"""
    if not s: 
        return ""
    s = s.upper()
    s = re.sub(r"[\s\-_/\.]", "", s)
    return s

def allowed_file(filename: str) -> bool:
    """Check if uploaded file has allowed extension"""
    ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "webp"}
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

def save_image(file_storage):
    """Save uploaded image and return relative path"""
    if not file_storage or file_storage.filename == "":
        return None
    if not allowed_file(file_storage.filename):
        return None
    
    filename = secure_filename(file_storage.filename)
    base, ext = os.path.splitext(filename)
    unique_name = f"{base}_{int(datetime.utcnow().timestamp())}{ext}"
    path = os.path.join(app.config["UPLOAD_FOLDER"], unique_name)
    file_storage.save(path)
    return f"uploads/{unique_name}"

def find_matches_for(report: Report):
    """Find and record matches for a given report"""
    matches = []
    
    if report.report_type == "lost":
        # Look for sightings that match this lost report
        q = Report.query.filter_by(report_type="sighting", is_active=True)
        if report.plate:
            matches += [("plate", r) for r in q.filter(Report.plate == report.plate).all()]
        if report.chassis:
            matches += [("chassis", r) for r in q.filter(Report.chassis == report.chassis).all()]
    else:
        # Look for lost reports that match this sighting
        q = Report.query.filter_by(report_type="lost", is_active=True)
        if report.plate:
            matches += [("plate", r) for r in q.filter(Report.plate == report.plate).all()]
        if report.chassis:
            matches += [("chassis", r) for r in q.filter(Report.chassis == report.chassis).all()]

    # Record new matches only
    for rule, other in matches:
        if report.report_type == "lost":
            lost_id, sighting_id = report.id, other.id
        else:
            lost_id, sighting_id = other.id, report.id
            
        # Check if match already exists
        exists = Match.query.filter_by(
            lost_id=lost_id, 
            sighting_id=sighting_id, 
            rule=rule
        ).first()
        
        if not exists:
            new_match = Match()
            new_match.lost_id = lost_id
            new_match.sighting_id = sighting_id
            new_match.rule = rule
            db.session.add(new_match)
    
    if matches:
        db.session.commit()
    
    return matches
