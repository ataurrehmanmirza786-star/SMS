from PyQt5.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel, 
                            QLineEdit, QPushButton, QMessageBox)
from PyQt5.QtCore import Qt
from database.models import User, session
from utils.security import check_password

class LoginDialog(QDialog):
    def __init__(self):
        super().__init__()
        self.current_user = None
        self.initUI()
        
    def initUI(self):
        self.setWindowTitle("Login")
        self.setFixedSize(400, 200)
        
        layout = QVBoxLayout()
        
        # Title
        title = QLabel("Property Management System")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 18px; font-weight: bold; margin: 10px;")
        layout.addWidget(title)
        
        # Username
        username_layout = QHBoxLayout()
        username_layout.addWidget(QLabel("Username:"))
        self.username_input = QLineEdit()
        username_layout.addWidget(self.username_input)
        layout.addLayout(username_layout)
        
        # Password
        password_layout = QHBoxLayout()
        password_layout.addWidget(QLabel("Password:"))
        self.password_input = QLineEdit()
        self.password_input.setEchoMode(QLineEdit.Password)
        password_layout.addWidget(self.password_input)
        layout.addLayout(password_layout)
        
        # Login button
        login_btn = QPushButton("Login")
        login_btn.clicked.connect(self.authenticate)
        layout.addWidget(login_btn)
        
        self.setLayout(layout)
    
    def authenticate(self):
        username = self.username_input.text()
        password = self.password_input.text()
        
        user = session.query(User).filter(User.username == username).first()
        
        if user and check_password(user.password_hash, password):
            self.current_user = user
            self.accept()
        else:
            QMessageBox.warning(self, "Login Failed", "Invalid username or password")
