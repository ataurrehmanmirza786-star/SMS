from database.models import Base, User, Permission, session
from utils.security import hash_password

def init_db():
    # Create tables
    Base.metadata.create_all()
    
    # Create admin user if not exists
    admin_user = session.query(User).filter(User.username == 'admin').first()
    if not admin_user:
        admin_user = User(
            username='admin',
            password_hash=hash_password('admin123'),
            full_name='System Administrator',
            email='admin@example.com'
        )
        session.add(admin_user)
        
        # Create permissions
        permissions = [
            Permission(name='view_dashboard', module='dashboard', can_view=True),
            Permission(name='manage_addresses', module='address_management', can_view=True, can_add=True, can_edit=True, can_delete=True),
            Permission(name='manage_residents', module='resident_management', can_view=True, can_add=True, can_edit=True, can_delete=True),
            Permission(name='manage_financial', module='financial_management', can_view=True, can_add=True, can_edit=True, can_delete=True),
            Permission(name='manage_complaints', module='complaint_management', can_view=True, can_add=True, can_edit=True, can_delete=True),
            Permission(name='manage_users', module='user_management', can_view=True, can_add=True, can_edit=True, can_delete=True)
        ]
        
        for permission in permissions:
            session.add(permission)
            admin_user.permissions.append(permission)
        
        session.commit()
        print("Database initialized successfully!")
        print("Admin user created with username: admin and password: admin123")
    else:
        print("Database already initialized.")

if __name__ == "__main__":
    init_db()
