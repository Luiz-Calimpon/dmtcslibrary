from app import db
from datetime import datetime

class Case(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    type = db.Column(db.String(50))
    case_no = db.Column(db.String(50))
    location = db.Column(db.String(100))
    content = db.Column(db.Text)
    file_type = db.Column(db.String(10))
    file_path = db.Column(db.String(200))
    embedding = db.Column(db.PickleType)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'type': self.type,
            'caseNo': self.case_no,
            'location': self.location
        }