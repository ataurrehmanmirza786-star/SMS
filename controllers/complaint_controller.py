from database.models import Complaint, session
from sqlalchemy import and_

class ComplaintController:
    def __init__(self):
        self.session = session
    
    def get_pending_complaints_count(self):
        return self.session.query(Complaint).filter(
            Complaint.status.in_(['PENDING', 'IN_PROGRESS'])
        ).count()
    
    def get_recent_complaints(self, limit=5):
        return self.session.query(Complaint).order_by(
            Complaint.created_at.desc()
        ).limit(limit).all()
