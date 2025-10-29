from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QTableWidget, 
                            QTableWidgetItem, QPushButton, QLineEdit, QLabel, 
                            QComboBox, QGroupBox, QFormLayout, QDialog, QDateEdit,
                            QMessageBox, QHeaderView, QTabWidget, QFrame)
from PyQt5.QtCore import Qt, QDate
from controllers.resident_controller import ResidentController
from controllers.address_controller import AddressController

class ResidentManagementWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.controller = ResidentController()
        self.address_controller = AddressController()
        self.initUI()
        self.loadResidents()
        
    def initUI(self):
        layout = QVBoxLayout(self)
        
        # Title
        title = QLabel("Resident Management")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 18px; font-weight: bold; margin: 10px;")
        layout.addWidget(title)
        
        # Create tab widget
        self.tab_widget = QTabWidget()
        
        # Residents tab
        self.residents_tab = QWidget()
        residents_layout = QVBoxLayout(self.residents_tab)
        
        # Filter section
        filter_group = QGroupBox("Filters")
        filter_layout = QHBoxLayout()
        
        # Name filter
        self.name_filter = QLineEdit()
        self.name_filter.setPlaceholderText("Name...")
        filter_layout.addWidget(QLabel("Name:"))
        filter_layout.addWidget(self.name_filter)
        
        # Contact filter
        self.contact_filter = QLineEdit()
        self.contact_filter.setPlaceholderText("Contact Number...")
        filter_layout.addWidget(QLabel("Contact:"))
        filter_layout.addWidget(self.contact_filter)
        
        # Address filter
        self.address_filter = QLineEdit()
        self.address_filter.setPlaceholderText("Address...")
        filter_layout.addWidget(QLabel("Address:"))
        filter_layout.addWidget(self.address_filter)
        
        # Apply filter button
        apply_filter_btn = QPushButton("Apply Filter")
        apply_filter_btn.clicked.connect(self.applyFilter)
        filter_layout.addWidget(apply_filter_btn)
        
        # Reset filter button
        reset_filter_btn = QPushButton("Reset")
        reset_filter_btn.clicked.connect(self.resetFilter)
        filter_layout.addWidget(reset_filter_btn)
        
        filter_group.setLayout(filter_layout)
        residents_layout.addWidget(filter_group)
        
        # Buttons section
        buttons_layout = QHBoxLayout()
        
        add_btn = QPushButton("Add Resident")
        add_btn.clicked.connect(self.showAddDialog)
        buttons_layout.addWidget(add_btn)
        
        edit_btn = QPushButton("Edit Resident")
        edit_btn.clicked.connect(self.showEditDialog)
        buttons_layout.addWidget(edit_btn)
        
        delete_btn = QPushButton("Delete Resident")
        delete_btn.clicked.connect(self.deleteResident)
        buttons_layout.addWidget(delete_btn)
        
        allot_btn = QPushButton("Allot Address")
        allot_btn.clicked.connect(self.showAllotDialog)
        buttons_layout.addWidget(allot_btn)
        
        buttons_layout.addStretch()
        residents_layout.addLayout(buttons_layout)
        
        # Table for residents
        self.resident_table = QTableWidget()
        self.resident_table.setColumnCount(7)
        self.resident_table.setHorizontalHeaderLabels(["ID", "Name", "Contact", "Email", "Emergency Contact", "ID Proof", "Move-in Date"])
        self.resident_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.resident_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.resident_table.setEditTriggers(QTableWidget.NoEditTriggers)
        residents_layout.addWidget(self.resident_table)
        
        # Allotment tab
        self.allotment_tab = QWidget()
        allotment_layout = QVBoxLayout(self.allotment_tab)
        
        # Allotment filter section
        allotment_filter_group = QGroupBox("Filters")
        allotment_filter_layout = QHBoxLayout()
        
        # Address filter
        self.allotment_address_filter = QComboBox()
        self.allotment_address_filter.addItem("All Addresses")
        self.populateAddressFilter()
        allotment_filter_layout.addWidget(QLabel("Address:"))
        allotment_filter_layout.addWidget(self.allotment_address_filter)
        
        # Block filter
        self.allotment_block_filter = QComboBox()
        self.allotment_block_filter.addItem("All Blocks")
        self.allotment_block_filter.addItems(["A", "B", "C", "D", "E"])
        allotment_filter_layout.addWidget(QLabel("Block:"))
        allotment_filter_layout.addWidget(self.allotment_block_filter)
        
        # Apply allotment filter button
        apply_allotment_filter_btn = QPushButton("Apply Filter")
        apply_allotment_filter_btn.clicked.connect(self.applyAllotmentFilter)
        allotment_filter_layout.addWidget(apply_allotment_filter_btn)
        
        # Reset allotment filter button
        reset_allotment_filter_btn = QPushButton("Reset")
        reset_allotment_filter_btn.clicked.connect(self.resetAllotmentFilter)
        allotment_filter_layout.addWidget(reset_allotment_filter_btn)
        
        allotment_filter_group.setLayout(allotment_filter_layout)
        allotment_layout.addWidget(allotment_filter_group)
        
        # Allotment table
        self.allotment_table = QTableWidget()
        self.allotment_table.setColumnCount(5)
        self.allotment_table.setHorizontalHeaderLabels(["Address", "Block", "Floor", "Resident", "Actions"])
        self.allotment_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.allotment_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.allotment_table.setEditTriggers(QTableWidget.NoEditTriggers)
        allotment_layout.addWidget(self.allotment_table)
        
        # Add tabs to tab widget
        self.tab_widget.addTab(self.residents_tab, "Residents")
        self.tab_widget.addTab(self.allotment_tab, "Allotment")
        
        layout.addWidget(self.tab_widget)
        
        # Connect tab change event
        self.tab_widget.currentChanged.connect(self.onTabChanged)
    
    def populateAddressFilter(self):
        addresses = self.address_controller.get_all_addresses()
        for address in addresses:
            self.allotment_address_filter.addItem(f"{address.number}, {address.block.value} Block", address.id)
    
    def loadResidents(self):
        residents = self.controller.get_all_residents()
        self.populateResidentTable(residents)
    
    def populateResidentTable(self, residents):
        self.resident_table.setRowCount(0)
        for row, resident in enumerate(residents):
            self.resident_table.insertRow(row)
            self.resident_table.setItem(row, 0, QTableWidgetItem(str(resident.id)))
            self.resident_table.setItem(row, 1, QTableWidgetItem(resident.name))
            self.resident_table.setItem(row, 2, QTableWidgetItem(resident.contact_number))
            self.resident_table.setItem(row, 3, QTableWidgetItem(resident.email))
            self.resident_table.setItem(row, 4, QTableWidgetItem(resident.emergency_contact))
            self.resident_table.setItem(row, 5, QTableWidgetItem(resident.id_proof_number))
            
            move_in_date = resident.move_in_date.strftime("%Y-%m-%d") if resident.move_in_date else ""
            self.resident_table.setItem(row, 6, QTableWidgetItem(move_in_date))
    
    def loadAllotments(self):
        # This would load all address-floor-resident relationships
        # For simplicity, we'll just load floors with residents
        from database.models import Floor, Address, Resident
        
        floors_with_residents = self.controller.session.query(
            Floor, Address, Resident
        ).join(
            Address, Floor.address_id == Address.id
        ).join(
            Resident, Floor.id == Resident.floor_id
        ).filter(
            Resident.is_active == True
        ).all()
        
        self.allotment_table.setRowCount(0)
        for row, (floor, address, resident) in enumerate(floors_with_residents):
            self.allotment_table.insertRow(row)
            self.allotment_table.setItem(row, 0, QTableWidgetItem(f"{address.number}"))
            self.allotment_table.setItem(row, 1, QTableWidgetItem(address.block.value))
            self.allotment_table.setItem(row, 2, QTableWidgetItem(str(floor.floor_number)))
            self.allotment_table.setItem(row, 3, QTableWidgetItem(resident.name))
            
            # Add remove button
            remove_btn = QPushButton("Remove")
            remove_btn.setProperty("floor_id", floor.id)
            remove_btn.setProperty("resident_id", resident.id)
            remove_btn.clicked.connect(self.removeAllotment)
            
            self.allotment_table.setCellWidget(row, 4, remove_btn)
    
    def applyFilter(self):
        filters = {}
        if self.name_filter.text():
            filters['name'] = self.name_filter.text()
        if self.contact_filter.text():
            filters['contact_number'] = self.contact_filter.text()
        if self.address_filter.text():
            filters['address'] = self.address_filter.text()
        
        filtered_residents = self.controller.filter_residents(filters)
        self.populateResidentTable(filtered_residents)
    
    def resetFilter(self):
        self.name_filter.clear()
        self.contact_filter.clear()
        self.address_filter.clear()
        self.loadResidents()
    
    def applyAllotmentFilter(self):
        # This would implement filtering for the allotment table
        # For simplicity, we'll just reload all allotments
        self.loadAllotments()
    
    def resetAllotmentFilter(self):
        self.allotment_address_filter.setCurrentIndex(0)
        self.allotment_block_filter.setCurrentIndex(0)
        self.loadAllotments()
    
    def onTabChanged(self, index):
        if index == 1:  # Allotment tab
            self.loadAllotments()
    
    def showAddDialog(self):
        dialog = ResidentDialog(self)
        if dialog.exec_():
            self.controller.add_resident(dialog.get_resident_data())
            self.loadResidents()
    
    def showEditDialog(self):
        selected_row = self.resident_table.currentRow()
        if selected_row >= 0:
            resident_id = int(self.resident_table.item(selected_row, 0).text())
            resident = self.controller.get_resident_by_id(resident_id)
            
            dialog = ResidentDialog(self, resident)
            if dialog.exec_():
                self.controller.update_resident(resident_id, dialog.get_resident_data())
                self.loadResidents()
        else:
            QMessageBox.warning(self, "No Selection", "Please select a resident to edit.")
    
    def deleteResident(self):
        selected_row = self.resident_table.currentRow()
        if selected_row >= 0:
            resident_id = int(self.resident_table.item(selected_row, 0).text())
            
            reply = QMessageBox.question(self, "Confirm Delete", 
                                        "Are you sure you want to delete this resident?",
                                        QMessageBox.Yes | QMessageBox.No)
            if reply == QMessageBox.Yes:
                self.controller.delete_resident(resident_id)
                self.loadResidents()
        else:
            QMessageBox.warning(self, "No Selection", "Please select a resident to delete.")
    
    def showAllotDialog(self):
        selected_row = self.resident_table.currentRow()
        if selected_row >= 0:
            resident_id = int(self.resident_table.item(selected_row, 0).text())
            resident = self.controller.get_resident_by_id(resident_id)
            
            dialog = AllotmentDialog(self, resident, self.address_controller)
            if dialog.exec_():
                address_id = dialog.get_selected_address_id()
                floor_id = dialog.get_selected_floor_id()
                
                if address_id:
                    self.controller.allot_address_to_resident(resident_id, address_id, floor_id)
                    QMessageBox.information(self, "Success", "Address allotted successfully.")
        else:
            QMessageBox.warning(self, "No Selection", "Please select a resident to allot an address.")
    
    def removeAllotment(self):
        button = self.sender()
        if button:
            floor_id = button.property("floor_id")
            resident_id = button.property("resident_id")
            
            if floor_id and resident_id:
                reply = QMessageBox.question(self, "Confirm Remove", 
                                            "Are you sure you want to remove this allotment?",
                                            QMessageBox.Yes | QMessageBox.No)
                if reply == QMessageBox.Yes:
                    # Get the address associated with the floor
                    from database.models import Floor
                    floor = self.controller.session.query(Floor).filter(Floor.id == floor_id).first()
                    if floor:
                        self.controller.remove_address_from_resident(resident_id, floor.address_id)
                        self.loadAllotments()

class ResidentDialog(QDialog):
    def __init__(self, parent=None, resident=None):
        super().__init__(parent)
        self.resident = resident
        self.initUI()
        
        if resident:
            self.setWindowTitle("Edit Resident")
            self.populateFields()
        else:
            self.setWindowTitle("Add Resident")
    
    def initUI(self):
        layout = QFormLayout(self)
        
        # Name
        self.name_input = QLineEdit()
        layout.addRow("Name:", self.name_input)
        
        # Contact Number
        self.contact_input = QLineEdit()
        layout.addRow("Contact Number:", self.contact_input)
        
        # Email
        self.email_input = QLineEdit()
        layout.addRow("Email:", self.email_input)
        
        # Emergency Contact
        self.emergency_input = QLineEdit()
        layout.addRow("Emergency Contact:", self.emergency_input)
        
        # ID Proof Number
        self.id_proof_input = QLineEdit()
        layout.addRow("ID Proof Number:", self.id_proof_input)
        
        # Move-in Date
        self.move_in_date = QDateEdit()
        self.move_in_date.setCalendarPopup(True)
        self.move_in_date.setDate(QDate.currentDate())
        layout.addRow("Move-in Date:", self.move_in_date)
        
        # Buttons
        buttons_layout = QHBoxLayout()
        save_btn = QPushButton("Save")
        save_btn.clicked.connect(self.accept)
        cancel_btn = QPushButton("Cancel")
        cancel_btn.clicked.connect(self.reject)
        
        buttons_layout.addWidget(save_btn)
        buttons_layout.addWidget(cancel_btn)
        layout.addRow("", buttons_layout)
    
    def populateFields(self):
        if self.resident:
            self.name_input.setText(self.resident.name)
            self.contact_input.setText(self.resident.contact_number)
            self.email_input.setText(self.resident.email)
            self.emergency_input.setText(self.resident.emergency_contact)
            self.id_proof_input.setText(self.resident.id_proof_number)
            
            if self.resident.move_in_date:
                self.move_in_date.setDate(self.resident.move_in_date)
    
    def get_resident_data(self):
        return {
            'name': self.name_input.text(),
            'contact_number': self.contact_input.text(),
            'email': self.email_input.text(),
            'emergency_contact': self.emergency_input.text(),
            'id_proof_number': self.id_proof_input.text(),
            'move_in_date': self.move_in_date.date().toPyDate()
        }

class AllotmentDialog(QDialog):
    def __init__(self, parent=None, resident=None, address_controller=None):
        super().__init__(parent)
        self.resident = resident
        self.address_controller = address_controller
        self.selected_address_id = None
        self.selected_floor_id = None
        self.initUI()
    
    def initUI(self):
        layout = QVBoxLayout(self)
        
        # Title
        title = QLabel(f"Allot Address to {self.resident.name}")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 16px; font-weight: bold; margin: 10px;")
        layout.addWidget(title)
        
        # Address selection
        address_group = QGroupBox("Select Address")
        address_layout = QVBoxLayout()
        
        self.address_combo = QComboBox()
        self.populateAddresses()
        self.address_combo.currentIndexChanged.connect(self.onAddressChanged)
        address_layout.addWidget(self.address_combo)
        
        address_group.setLayout(address_layout)
        layout.addWidget(address_group)
        
        # Floor selection
        floor_group = QGroupBox("Select Floor")
        floor_layout = QVBoxLayout()
        
        self.floor_combo = QComboBox()
        floor_layout.addWidget(self.floor_combo)
        
        floor_group.setLayout(floor_layout)
        layout.addWidget(floor_group)
        
        # Buttons
        buttons_layout = QHBoxLayout()
        allot_btn = QPushButton("Allot")
        allot_btn.clicked.connect(self.accept)
        cancel_btn = QPushButton("Cancel")
        cancel_btn.clicked.connect(self.reject)
        
        buttons_layout.addWidget(allot_btn)
        buttons_layout.addWidget(cancel_btn)
        layout.addLayout(buttons_layout)
    
    def populateAddresses(self):
        addresses = self.address_controller.get_all_addresses()
        for address in addresses:
            self.address_combo.addItem(f"{address.number}, {address.block.value} Block", address.id)
    
    def onAddressChanged(self, index):
        if index >= 0:
            address_id = self.address_combo.currentData()
            self.selected_address_id = address_id
            
            # Populate floors for this address
            self.floor_combo.clear()
            floors = self.address_controller.get_floors_by_address(address_id)
            
            for floor in floors:
                self.floor_combo.addItem(f"Floor {floor.floor_number}", floor.id)
        else:
            self.selected_address_id = None
            self.floor_combo.clear()
    
    def get_selected_address_id(self):
        return self.selected_address_id
    
    def get_selected_floor_id(self):
        if self.floor_combo.currentIndex() >= 0:
            return self.floor_combo.currentData()
        return None
