from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel

class FinancialManagementWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()
        
    def initUI(self):
        layout = QVBoxLayout(self)
        
        title = QLabel("Financial Management")
        title.setStyleSheet("font-size: 18px; font-weight: bold; margin: 10px;")
        layout.addWidget(title)
        
        content = QLabel("Financial Management module will be implemented here.")
        layout.addWidget(content)
