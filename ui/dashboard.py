from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                            QFrame, QSizePolicy)
from PyQt5.QtCore import Qt
from controllers.address_controller import AddressController
from controllers.resident_controller import ResidentController
from controllers.financial_controller import FinancialController
from controllers.complaint_controller import ComplaintController
import matplotlib.pyplot as plt
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

class DashboardWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.address_controller = AddressController()
        self.resident_controller = ResidentController()
        self.financial_controller = FinancialController()
        self.complaint_controller = ComplaintController()
        self.initUI()
        self.loadDashboardData()
        
    def initUI(self):
        layout = QVBoxLayout(self)
        
        # Title
        title = QLabel("Dashboard")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 24px; font-weight: bold; margin: 10px;")
        layout.addWidget(title)
        
        # Stats cards
        stats_layout = QHBoxLayout()
        
        self.address_card = self.createStatCard("Total Addresses", "0")
        stats_layout.addWidget(self.address_card)
        
        self.resident_card = self.createStatCard("Total Residents", "0")
        stats_layout.addWidget(self.resident_card)
        
        self.financial_card = self.createStatCard("Pending Dues", "₹0")
        stats_layout.addWidget(self.financial_card)
        
        self.complaint_card = self.createStatCard("Pending Complaints", "0")
        stats_layout.addWidget(self.complaint_card)
        
        layout.addLayout(stats_layout)
        
        # Charts
        charts_layout = QHBoxLayout()
        
        # Address by Category chart
        self.address_category_frame = QFrame()
        self.address_category_frame.setFrameShape(QFrame.StyledPanel)
        address_category_layout = QVBoxLayout(self.address_category_frame)
        
        address_category_title = QLabel("Addresses by Category")
        address_category_title.setAlignment(Qt.AlignCenter)
        address_category_title.setStyleSheet("font-weight: bold; margin: 5px;")
        address_category_layout.addWidget(address_category_title)
        
        self.address_category_canvas = FigureCanvas(Figure(figsize=(5, 4)))
        address_category_layout.addWidget(self.address_category_canvas)
        
        charts_layout.addWidget(self.address_category_frame)
        
        # Address by Block chart
        self.address_block_frame = QFrame()
        self.address_block_frame.setFrameShape(QFrame.StyledPanel)
        address_block_layout = QVBoxLayout(self.address_block_frame)
        
        address_block_title = QLabel("Addresses by Block")
        address_block_title.setAlignment(Qt.AlignCenter)
        address_block_title.setStyleSheet("font-weight: bold; margin: 5px;")
        address_block_layout.addWidget(address_block_title)
        
        self.address_block_canvas = FigureCanvas(Figure(figsize=(5, 4)))
        address_block_layout.addWidget(self.address_block_canvas)
        
        charts_layout.addWidget(self.address_block_frame)
        
        layout.addLayout(charts_layout)
        
        # Recent complaints and financial records
        recent_layout = QHBoxLayout()
        
        # Recent complaints
        self.recent_complaints_frame = QFrame()
        self.recent_complaints_frame.setFrameShape(QFrame.StyledPanel)
        recent_complaints_layout = QVBoxLayout(self.recent_complaints_frame)
        
        recent_complaints_title = QLabel("Recent Complaints")
        recent_complaints_title.setAlignment(Qt.AlignCenter)
        recent_complaints_title.setStyleSheet("font-weight: bold; margin: 5px;")
        recent_complaints_layout.addWidget(recent_complaints_title)
        
        self.recent_complaints_label = QLabel("No recent complaints")
        self.recent_complaints_label.setWordWrap(True)
        recent_complaints_layout.addWidget(self.recent_complaints_label)
        
        recent_layout.addWidget(self.recent_complaints_frame)
        
        # Recent financial records
        self.recent_financial_frame = QFrame()
        self.recent_financial_frame.setFrameShape(QFrame.StyledPanel)
        recent_financial_layout = QVBoxLayout(self.recent_financial_frame)
        
        recent_financial_title = QLabel("Recent Financial Records")
        recent_financial_title.setAlignment(Qt.AlignCenter)
        recent_financial_title.setStyleSheet("font-weight: bold; margin: 5px;")
        recent_financial_layout.addWidget(recent_financial_title)
        
        self.recent_financial_label = QLabel("No recent financial records")
        self.recent_financial_label.setWordWrap(True)
        recent_financial_layout.addWidget(self.recent_financial_label)
        
        recent_layout.addWidget(self.recent_financial_frame)
        
        layout.addLayout(recent_layout)
        
        layout.addStretch()
    
    def createStatCard(self, title, value):
        card = QFrame()
        card.setFrameShape(QFrame.StyledPanel)
        card.setStyleSheet("""
            QFrame {
                background-color: #f8f9fa;
                border-radius: 5px;
                padding: 10px;
            }
            QLabel {
                color: #343a40;
            }
        """)
        card.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        
        layout = QVBoxLayout(card)
        
        title_label = QLabel(title)
        title_label.setAlignment(Qt.AlignCenter)
        title_label.setStyleSheet("font-size: 14px;")
        layout.addWidget(title_label)
        
        value_label = QLabel(value)
        value_label.setAlignment(Qt.AlignCenter)
        value_label.setStyleSheet("font-size: 24px; font-weight: bold;")
        layout.addWidget(value_label)
        
        return card
    
    def loadDashboardData(self):
        # Load statistics
        total_addresses = self.address_controller.get_total_addresses()
        self.address_card.findChild(QLabel, text="0").setText(str(total_addresses))
        
        total_residents = self.resident_controller.get_total_residents()
        self.resident_card.findChild(QLabel, text="0").setText(str(total_residents))
        
        pending_dues = self.financial_controller.get_total_pending_dues()
        self.financial_card.findChild(QLabel, text="₹0").setText(f"₹{pending_dues:.2f}")
        
        pending_complaints = self.complaint_controller.get_pending_complaints_count()
        self.complaint_card.findChild(QLabel, text="0").setText(str(pending_complaints))
        
        # Load charts
        self.loadAddressCategoryChart()
        self.loadAddressBlockChart()
        
        # Load recent data
        self.loadRecentComplaints()
        self.loadRecentFinancialRecords()
    
    def loadAddressCategoryChart(self):
        categories = self.address_controller.get_addresses_by_category()
        
        figure = self.address_category_canvas.figure
        figure.clear()
        
        ax = figure.add_subplot(111)
        ax.pie(categories.values(), labels=categories.keys(), autopct='%1.1f%%')
        ax.set_title('Address Distribution by Category')
        
        self.address_category_canvas.draw()
    
    def loadAddressBlockChart(self):
        blocks = self.address_controller.get_addresses_by_block()
        
        figure = self.address_block_canvas.figure
        figure.clear()
        
        ax = figure.add_subplot(111)
        ax.bar(blocks.keys(), blocks.values())
        ax.set_title('Address Distribution by Block')
        ax.set_xlabel('Block')
        ax.set_ylabel('Count')
        
        self.address_block_canvas.draw()
    
    def loadRecentComplaints(self):
        recent_complaints = self.complaint_controller.get_recent_complaints(5)
        
        if recent_complaints:
            text = ""
            for complaint in recent_complaints:
                text += f"<b>{complaint.title}</b> - {complaint.status.value}<br>"
                text += f"{complaint.description[:50]}...<br><br>"
            
            self.recent_complaints_label.setText(text)
        else:
            self.recent_complaints_label.setText("No recent complaints")
    
    def loadRecentFinancialRecords(self):
        recent_records = self.financial_controller.get_recent_financial_records(5)
        
        if recent_records:
            text = ""
            for record in recent_records:
                resident_name = record.resident.name if record.resident else "Unknown"
                text += f"<b>{resident_name}</b> - ₹{record.amount:.2f}<br>"
                text += f"Due: {record.due_date.strftime('%Y-%m-%d')} - "
                text += f"Status: {'Paid' if record.is_paid else 'Pending'}<br><br>"
            
            self.recent_financial_label.setText(text)
        else:
            self.recent_financial_label.setText("No recent financial records")
