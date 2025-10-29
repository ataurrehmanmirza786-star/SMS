from database.models import User, session

class UserController:
    def __init__(self):
        self.session = session
    
    def get_all_users(self):
        return self.session.query(User).filter(User.is_active == True).all()
    
    def get_user_by_id(self, user_id):
        return self.session.query(User).filter(User.id == user_id).first()
    
    def get_user_by_username(self, username):
        return self.session.query(User).filter(User.username == username).first()
