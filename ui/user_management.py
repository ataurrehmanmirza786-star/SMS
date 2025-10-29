from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel

class UserManagementWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        
    def initUI(self):
        layout = QVBoxLayout(self)
        
        title = QLabel("User Management")
        title.setStyleSheet("font-size: 18px; font-weight: bold; margin: 10px;")
        layout.addWidget(title)
        
        content = QLabel("User Management module will be implemented here.")
        layout.addWidget(content)
