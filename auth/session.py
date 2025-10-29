from datetime import datetime, timedelta
from database.models import User, session

class SessionManager:
    def __init__(self):
        self.current_user = None
        self.session_expiry = None
    
    def login(self, user):
        self.current_user = user
        # Set session expiry to 1 hour from now
        self.session_expiry = datetime.now() + timedelta(hours=1)
    
    def is_active(self):
        if not self.current_user or not self.session_expiry:
            return False
        return datetime.now() < self.session_expiry
    
    def logout(self):
        self.current_user = None
        self.session_expiry = None

# Global session manager
session_manager = SessionManager()
