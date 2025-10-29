from database.models import FinancialRecord, session
from sqlalchemy import func, and_

class FinancialController:
    def __init__(self):
        self.session = session
    
    def get_total_pending_dues(self):
        result = self.session.query(
            func.sum(FinancialRecord.amount)
        ).filter(
            and_(FinancialRecord.is_paid == False, FinancialRecord.due_date >= func.now())
        ).scalar()
        
        return result if result else 0.0
    
    def get_recent_financial_records(self, limit=5):
        return self.session.query(FinancialRecord).order_by(
            FinancialRecord.due_date.desc()
        ).limit(limit).all()
