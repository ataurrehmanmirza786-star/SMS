from PyQt5.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
                            QStackedWidget, QLabel, QFrame)
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QIcon, QFont

class MainWindow(QMainWindow):
    def __init__(self, user):
        super().__init__()
        self.user = user
        self.initUI()
        
    def initUI(self):
        self.setWindowTitle("Property Management System")
        self.setGeometry(100, 100, 1200, 800)
        
        # Create central widget and main layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QHBoxLayout(central_widget)
        
        # Create sidebar
        self.sidebar = self.createSidebar()
        main_layout.addWidget(self.sidebar)
        
        # Create content area with stacked widget
        self.content_stack = QStackedWidget()
        main_layout.addWidget(self.content_stack, 1)
        
        # Add modules to stack based on user permissions
        self.loadModules()
        
        # Set default module to dashboard
        self.content_stack.setCurrentIndex(0)
        
    def createSidebar(self):
        sidebar = QFrame()
        sidebar.setFrameShape(QFrame.StyledPanel)
        sidebar.setFixedWidth(250)
        sidebar.setStyleSheet("""
            QFrame {
                background-color: #2c3e50;
                color: white;
            }
            QPushButton {
                background-color: #34495e;
                color: white;
                border: none;
                padding: 10px;
                text-align: left;
                border-radius: 3px;
            }
            QPushButton:hover {
                background-color: #4a5f7a;
            }
            QPushButton:pressed {
                background-color: #1a252f;
            }
        """)
        
        layout = QVBoxLayout(sidebar)
        
        # App title
        title = QLabel("Property Management")
        title.setAlignment(Qt.AlignCenter)
        title.setFont(QFont("Arial", 14, QFont.Bold))
        title.setStyleSheet("padding: 15px;")
        layout.addWidget(title)
        
        # User info
        user_label = QLabel(f"User: {self.user.full_name}")
        user_label.setStyleSheet("padding: 5px 15px;")
        layout.addWidget(user_label)
        
        # Sidebar buttons will be added dynamically based on permissions
        self.sidebar_buttons = []
        
        layout.addStretch()
        
        # Logout button
        logout_btn = QPushButton("Logout")
        logout_btn.clicked.connect(self.logout)
        layout.addWidget(logout_btn)
        
        return sidebar
    
    def loadModules(self):
        # This would load modules based on user permissions
        # For now, we'll add placeholder modules
        
        # Dashboard
        from .dashboard import DashboardWidget
        dashboard = DashboardWidget()
        self.content_stack.addWidget(dashboard)
        self.addSidebarButton("Dashboard", 0)
        
        # Address Management
        from .address_management import AddressManagementWidget
        address_mgmt = AddressManagementWidget()
        self.content_stack.addWidget(address_mgmt)
        self.addSidebarButton("Address Management", 1)
        
        # Resident Management
        from .resident_management import ResidentManagementWidget
        resident_mgmt = ResidentManagementWidget()
        self.content_stack.addWidget(resident_mgmt)
        self.addSidebarButton("Resident Management", 2)
        
        # Financial Management
        from .financial_management import FinancialManagementWidget
        financial_mgmt = FinancialManagementWidget()
        self.content_stack.addWidget(financial_mgmt)
        self.addSidebarButton("Financial Management", 3)
        
        # Complaint Management
        from .complaint_management import ComplaintManagementWidget
        complaint_mgmt = ComplaintManagementWidget()
        self.content_stack.addWidget(complaint_mgmt)
        self.addSidebarButton("Complaint Management", 4)
        
        # User Management (only for admins)
        if self.user.has_permission("user_management", "can_view"):
            from .user_management import UserManagementWidget
            user_mgmt = UserManagementWidget()
            self.content_stack.addWidget(user_mgmt)
            self.addSidebarButton("User Management", 5)
    
    def addSidebarButton(self, text, index):
        btn = QPushButton(text)
        btn.clicked.connect(lambda: self.content_stack.setCurrentIndex(index))
        self.sidebar.layout().insertWidget(len(self.sidebar_buttons) + 2, btn)  # +2 for title and user label
        self.sidebar_buttons.append(btn)
    
    def logout(self):
        # Close current window and show login dialog
        from auth.login import LoginDialog
        self.close()
        login_dialog = LoginDialog()
        if login_dialog.exec_():
            main_window = MainWindow(login_dialog.current_user)
            main_window.show()
