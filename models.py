from datetime import datetime
from app import db

class Report(db.Model):
    __tablename__ = "reports"
    
    id = db.Column(db.Integer, primary_key=True)
    report_type = db.Column(db.String(10), nullable=False)  # "lost" or "sighting"
    car_name = db.Column(db.String(120), nullable=False)    # اسم العربية/الشركة
    model = db.Column(db.String(120), nullable=True)
    color = db.Column(db.String(50), nullable=True)
    chassis = db.Column(db.String(120), index=True)
    plate = db.Column(db.String(120), index=True)
    location = db.Column(db.String(200), nullable=True)
    phone = db.Column(db.String(40), nullable=False)
    image_path = db.Column(db.String(300), nullable=True)   # مسار الصورة داخل static/uploads
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    is_active = db.Column(db.Boolean, default=True)
    notes = db.Column(db.String(300), nullable=True)

    def __repr__(self):
        return f'<Report {self.id}: {self.report_type} - {self.car_name}>'

class Match(db.Model):
    __tablename__ = "matches"
    
    id = db.Column(db.Integer, primary_key=True)
    lost_id = db.Column(db.Integer, db.ForeignKey("reports.id"), nullable=False)
    sighting_id = db.Column(db.Integer, db.ForeignKey("reports.id"), nullable=False)
    rule = db.Column(db.String(50), nullable=False)  # "plate" or "chassis"
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Relationships
    lost_report = db.relationship("Report", foreign_keys=[lost_id])
    sighting_report = db.relationship("Report", foreign_keys=[sighting_id])

    def __repr__(self):
        return f'<Match {self.id}: {self.rule} match between {self.lost_id} and {self.sighting_id}>'
