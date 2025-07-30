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

def process_bulk_data(bulk_data):
    """Process bulk import data and create reports"""
    from models import Report
    
    lines = bulk_data.strip().split('\n')
    results = {
        'success': 0,
        'errors': [],
        'matches': 0
    }
    
    for line_num, line in enumerate(lines, 1):
        if not line.strip():
            continue
        
        try:
            # Split by comma and clean up
            parts = [part.strip() for part in line.split(',')]
            
            if len(parts) < 8:
                results['errors'].append({
                    'line': line_num,
                    'message': f'بيانات ناقصة. يجب أن يكون هناك 8 حقول على الأقل، وجد {len(parts)}'
                })
                continue
            
            # Parse fields
            report_type = parts[0].strip()
            car_name = parts[1].strip()
            model = parts[2].strip() if parts[2].strip() else None
            color = parts[3].strip() if parts[3].strip() else None
            plate = parts[4].strip() if parts[4].strip() else None
            chassis = parts[5].strip() if parts[5].strip() else None
            location = parts[6].strip() if parts[6].strip() else None
            phone = parts[7].strip()
            notes = parts[8].strip() if len(parts) > 8 and parts[8].strip() else None
            
            # Validate report type
            if report_type not in ['فقدان', 'رصد', 'lost', 'sighting']:
                results['errors'].append({
                    'line': line_num,
                    'message': 'نوع البلاغ يجب أن يكون "فقدان" أو "رصد"'
                })
                continue
            
            # Normalize report type
            if report_type in ['فقدان', 'lost']:
                report_type = 'lost'
            else:
                report_type = 'sighting'
            
            # Validate required fields
            if not car_name or not phone:
                results['errors'].append({
                    'line': line_num,
                    'message': 'اسم السيارة ورقم الهاتف مطلوبان'
                })
                continue
            
            if not plate and not chassis:
                results['errors'].append({
                    'line': line_num,
                    'message': 'يجب توفر رقم اللوحة أو رقم الشاسي على الأقل'
                })
                continue
            
            # Create new report
            new_report = Report()
            new_report.report_type = report_type
            new_report.car_name = car_name
            new_report.model = model
            new_report.color = color
            new_report.chassis = chassis
            new_report.plate = plate
            new_report.location = location
            new_report.phone = phone
            new_report.notes = notes
            new_report.image_path = None  # No image in bulk import
            
            db.session.add(new_report)
            db.session.commit()
            
            # Find matches
            matches_found = find_matches_for(new_report)
            results['matches'] += len(matches_found) if matches_found else 0
            results['success'] += 1
            
        except Exception as e:
            results['errors'].append({
                'line': line_num,
                'message': f'خطأ في معالجة البيانات: {str(e)}'
            })
    
    return results
