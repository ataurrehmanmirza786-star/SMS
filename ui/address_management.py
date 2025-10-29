from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QTableWidget, 
                            QTableWidgetItem, QPushButton, QComboBox, QLineEdit, 
                            QLabel, QCheckBox, QSpinBox, QGroupBox, QFormLayout,
                            QHeaderView, QDialog, QFileDialog, QMessageBox)
from PyQt5.QtCore import Qt
from controllers.address_controller import AddressController
from utils.data_import import import_addresses_from_csv

class AddressManagementWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.controller = AddressController()
        self.initUI()
        self.loadAddresses()
        
    def initUI(self):
        layout = QVBoxLayout(self)
        
        # Title
        title = QLabel("Address Management")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 18px; font-weight: bold; margin: 10px;")
        layout.addWidget(title)
        
        # Filter section
        filter_group = QGroupBox("Filters")
        filter_layout = QHBoxLayout()
        
        # Category filter
        self.category_filter = QComboBox()
        self.category_filter.addItem("All Categories")
        self.category_filter.addItems(["R", "A", "AS", "PB"])
        filter_layout.addWidget(QLabel("Category:"))
        filter_layout.addWidget(self.category_filter)
        
        # Block filter
        self.block_filter = QComboBox()
        self.block_filter.addItem("All Blocks")
        self.block_filter.addItems(["A", "B", "C", "D", "E"])
        filter_layout.addWidget(QLabel("Block:"))
        filter_layout.addWidget(self.block_filter)
        
        # Number filter
        self.number_filter = QLineEdit()
        self.number_filter.setPlaceholderText("Number...")
        filter_layout.addWidget(QLabel("Number:"))
        filter_layout.addWidget(self.number_filter)
        
        # Apply filter button
        apply_filter_btn = QPushButton("Apply Filter")
        apply_filter_btn.clicked.connect(self.applyFilter)
        filter_layout.addWidget(apply_filter_btn)
        
        # Reset filter button
        reset_filter_btn = QPushButton("Reset")
        reset_filter_btn.clicked.connect(self.resetFilter)
        filter_layout.addWidget(reset_filter_btn)
        
        filter_group.setLayout(filter_layout)
        layout.addWidget(filter_group)
        
        # Buttons section
        buttons_layout = QHBoxLayout()
        
        add_btn = QPushButton("Add Address")
        add_btn.clicked.connect(self.showAddDialog)
        buttons_layout.addWidget(add_btn)
        
        edit_btn = QPushButton("Edit Address")
        edit_btn.clicked.connect(self.showEditDialog)
        buttons_layout.addWidget(edit_btn)
        
        delete_btn = QPushButton("Delete Address")
        delete_btn.clicked.connect(self.deleteAddress)
        buttons_layout.addWidget(delete_btn)
        
        import_btn = QPushButton("Import CSV")
        import_btn.clicked.connect(self.importCSV)
        buttons_layout.addWidget(import_btn)
        
        buttons_layout.addStretch()
        layout.addLayout(buttons_layout)
        
        # Table for addresses
        self.address_table = QTableWidget()
        self.address_table.setColumnCount(6)
        self.address_table.setHorizontalHeaderLabels(["ID", "Category", "Number", "Row", "Block", "Floors"])
        self.address_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.address_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.address_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.address_table.doubleClicked.connect(self.showFloorsDialog)
        layout.addWidget(self.address_table)
        
    def loadAddresses(self):
        addresses = self.controller.get_all_addresses()
        self.populateTable(addresses)
        
    def populateTable(self, addresses):
        self.address_table.setRowCount(0)
        for row, address in enumerate(addresses):
            self.address_table.insertRow(row)
            self.address_table.setItem(row, 0, QTableWidgetItem(str(address.id)))
            self.address_table.setItem(row, 1, QTableWidgetItem(address.category.value))
            self.address_table.setItem(row, 2, QTableWidgetItem(address.number))
            self.address_table.setItem(row, 3, QTableWidgetItem(address.row))
            self.address_table.setItem(row, 4, QTableWidgetItem(address.block.value))
            self.address_table.setItem(row, 5, QTableWidgetItem(str(address.total_floors)))
    
    def applyFilter(self):
        filters = {}
        if self.category_filter.currentText() != "All Categories":
            filters['category'] = self.category_filter.currentText()
        if self.block_filter.currentText() != "All Blocks":
            filters['block'] = self.block_filter.currentText()
        if self.number_filter.text():
            filters['number'] = self.number_filter.text()
        
        filtered_addresses = self.controller.filter_addresses(filters)
        self.populateTable(filtered_addresses)
    
    def resetFilter(self):
        self.category_filter.setCurrentIndex(0)
        self.block_filter.setCurrentIndex(0)
        self.number_filter.clear()
        self.loadAddresses()
    
    def showAddDialog(self):
        dialog = AddressDialog(self)
        if dialog.exec_():
            self.controller.add_address(dialog.get_address_data())
            self.loadAddresses()
    
    def showEditDialog(self):
        selected_row = self.address_table.currentRow()
        if selected_row >= 0:
            address_id = int(self.address_table.item(selected_row, 0).text())
            address = self.controller.get_address_by_id(address_id)
            
            dialog = AddressDialog(self, address)
            if dialog.exec_():
                self.controller.update_address(address_id, dialog.get_address_data())
                self.loadAddresses()
        else:
            QMessageBox.warning(self, "No Selection", "Please select an address to edit.")
    
    def deleteAddress(self):
        selected_row = self.address_table.currentRow()
        if selected_row >= 0:
            address_id = int(self.address_table.item(selected_row, 0).text())
            
            reply = QMessageBox.question(self, "Confirm Delete", 
                                        "Are you sure you want to delete this address?",
                                        QMessageBox.Yes | QMessageBox.No)
            if reply == QMessageBox.Yes:
                self.controller.delete_address(address_id)
                self.loadAddresses()
        else:
            QMessageBox.warning(self, "No Selection", "Please select an address to delete.")
    
    def showFloorsDialog(self):
        selected_row = self.address_table.currentRow()
        if selected_row >= 0:
            address_id = int(self.address_table.item(selected_row, 0).text())
            address = self.controller.get_address_by_id(address_id)
            
            dialog = FloorsDialog(self, address)
            dialog.exec_()
    
    def importCSV(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Import Addresses", "", "CSV Files (*.csv)")
        if file_path:
            try:
                import_addresses_from_csv(file_path, self.controller)
                self.loadAddresses()
                QMessageBox.information(self, "Success", "Addresses imported successfully.")
            except Exception as e:
                QMessageBox.critical(self, "Error", f"Failed to import addresses: {str(e)}")

class AddressDialog(QDialog):
    def __init__(self, parent=None, address=None):
        super().__init__(parent)
        self.address = address
        self.initUI()
        
        if address:
            self.setWindowTitle("Edit Address")
            self.populateFields()
        else:
            self.setWindowTitle("Add Address")
    
    def initUI(self):
        layout = QFormLayout(self)
        
        # Category
        self.category_combo = QComboBox()
        self.category_combo.addItems(["R", "A", "AS", "PB"])
        layout.addRow("Category:", self.category_combo)
        
        # Number
        self.number_input = QLineEdit()
        layout.addRow("Number:", self.number_input)
        
        # Row
        self.row_input = QLineEdit()
        layout.addRow("Row:", self.row_input)
        
        # Block
        self.block_combo = QComboBox()
        self.block_combo.addItems(["A", "B", "C", "D", "E"])
        layout.addRow("Block:", self.block_combo)
        
        # Total Floors
        self.floors_input = QSpinBox()
        self.floors_input.setMinimum(1)
        self.floors_input.setMaximum(100)
        layout.addRow("Total Floors:", self.floors_input)
        
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
        if self.address:
            self.category_combo.setCurrentText(self.address.category.value)
            self.number_input.setText(self.address.number)
            self.row_input.setText(self.address.row)
            self.block_combo.setCurrentText(self.address.block.value)
            self.floors_input.setValue(self.address.total_floors)
    
    def get_address_data(self):
        return {
            'category': self.category_combo.currentText(),
            'number': self.number_input.text(),
            'row': self.row_input.text(),
            'block': self.block_combo.currentText(),
            'total_floors': self.floors_input.value()
        }

class FloorsDialog(QDialog):
    def __init__(self, parent=None, address=None):
        super().__init__(parent)
        self.address = address
        self.controller = AddressController()
        self.initUI()
        self.loadFloors()
    
    def initUI(self):
        layout = QVBoxLayout(self)
        
        # Title
        title = QLabel(f"Floors for Address: {self.address.number}, {self.address.block.value} Block")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 16px; font-weight: bold; margin: 10px;")
        layout.addWidget(title)
        
        # Buttons
        buttons_layout = QHBoxLayout()
        add_floor_btn = QPushButton("Add Floor")
        add_floor_btn.clicked.connect(self.showAddFloorDialog)
        buttons_layout.addWidget(add_floor_btn)
        
        edit_floor_btn = QPushButton("Edit Floor")
        edit_floor_btn.clicked.connect(self.showEditFloorDialog)
        buttons_layout.addWidget(edit_floor_btn)
        
        delete_floor_btn = QPushButton("Delete Floor")
        delete_floor_btn.clicked.connect(self.deleteFloor)
        buttons_layout.addWidget(delete_floor_btn)
        
        buttons_layout.addStretch()
        layout.addLayout(buttons_layout)
        
        # Table for floors
        self.floors_table = QTableWidget()
        self.floors_table.setColumnCount(7)
        self.floors_table.setHorizontalHeaderLabels(["ID", "Floor Number", "Owner", "Tenant", "Commercial", "Shop", "Vacant"])
        self.floors_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.floors_table.setSelectionBehavior(QTableWidget.SelectRows)
        self.floors_table.setEditTriggers(QTableWidget.NoEditTriggers)
        layout.addWidget(self.floors_table)
        
        # Shop count (only visible when a floor with shop is selected)
        self.shop_group = QGroupBox("Shop Details")
        shop_layout = QFormLayout()
        
        self.shop_count_spin = QSpinBox()
        self.shop_count_spin.setMinimum(0)
        self.shop_count_spin.setMaximum(100)
        shop_layout.addRow("Number of Shops:", self.shop_count_spin)
        
        update_shop_btn = QPushButton("Update Shop Count")
        update_shop_btn.clicked.connect(self.updateShopCount)
        shop_layout.addRow("", update_shop_btn)
        
        self.shop_group.setLayout(shop_layout)
        self.shop_group.setVisible(False)
        layout.addWidget(self.shop_group)
        
        self.floors_table.itemSelectionChanged.connect(self.onFloorSelectionChanged)
    
    def loadFloors(self):
        floors = self.controller.get_floors_by_address(self.address.id)
        self.populateTable(floors)
    
    def populateTable(self, floors):
        self.floors_table.setRowCount(0)
        for row, floor in enumerate(floors):
            self.floors_table.insertRow(row)
            self.floors_table.setItem(row, 0, QTableWidgetItem(str(floor.id)))
            self.floors_table.setItem(row, 1, QTableWidgetItem(str(floor.floor_number)))
            
            # Add checkboxes for floor types
            owner_check = QTableWidgetItem()
            owner_check.setCheckState(Qt.Checked if floor.is_owner else Qt.Unchecked)
            owner_check.setFlags(owner_check.flags() & ~Qt.ItemIsEditable)
            self.floors_table.setItem(row, 2, owner_check)
            
            tenant_check = QTableWidgetItem()
            tenant_check.setCheckState(Qt.Checked if floor.is_tenant else Qt.Unchecked)
            tenant_check.setFlags(tenant_check.flags() & ~Qt.ItemIsEditable)
            self.floors_table.setItem(row, 3, tenant_check)
            
            commercial_check = QTableWidgetItem()
            commercial_check.setCheckState(Qt.Checked if floor.is_commercial else Qt.Unchecked)
            commercial_check.setFlags(commercial_check.flags() & ~Qt.ItemIsEditable)
            self.floors_table.setItem(row, 4, commercial_check)
            
            shop_check = QTableWidgetItem()
            shop_check.setCheckState(Qt.Checked if floor.is_shop else Qt.Unchecked)
            shop_check.setFlags(shop_check.flags() & ~Qt.ItemIsEditable)
            self.floors_table.setItem(row, 5, shop_check)
            
            vacant_check = QTableWidgetItem()
            vacant_check.setCheckState(Qt.Checked if floor.is_vacant else Qt.Unchecked)
            vacant_check.setFlags(vacant_check.flags() & ~Qt.ItemIsEditable)
            self.floors_table.setItem(row, 6, vacant_check)
    
    def onFloorSelectionChanged(self):
        selected_rows = self.floors_table.selectedItems()
        if selected_rows:
            selected_row = self.floors_table.currentRow()
            floor_id = int(self.floors_table.item(selected_row, 0).text())
            floor = self.controller.get_floor_by_id(floor_id)
            
            if floor.is_shop:
                self.shop_group.setVisible(True)
                self.shop_count_spin.setValue(floor.shop_count)
            else:
                self.shop_group.setVisible(False)
        else:
            self.shop_group.setVisible(False)
    
    def showAddFloorDialog(self):
        dialog = FloorDialog(self, self.address)
        if dialog.exec_():
            self.controller.add_floor(self.address.id, dialog.get_floor_data())
            self.loadFloors()
    
    def showEditFloorDialog(self):
        selected_row = self.floors_table.currentRow()
        if selected_row >= 0:
            floor_id = int(self.floors_table.item(selected_row, 0).text())
            floor = self.controller.get_floor_by_id(floor_id)
            
            dialog = FloorDialog(self, self.address, floor)
            if dialog.exec_():
                self.controller.update_floor(floor_id, dialog.get_floor_data())
                self.loadFloors()
        else:
            QMessageBox.warning(self, "No Selection", "Please select a floor to edit.")
    
    def deleteFloor(self):
        selected_row = self.floors_table.currentRow()
        if selected_row >= 0:
            floor_id = int(self.floors_table.item(selected_row, 0).text())
            
            reply = QMessageBox.question(self, "Confirm Delete", 
                                        "Are you sure you want to delete this floor?",
                                        QMessageBox.Yes | QMessageBox.No)
            if reply == QMessageBox.Yes:
                self.controller.delete_floor(floor_id)
                self.loadFloors()
        else:
            QMessageBox.warning(self, "No Selection", "Please select a floor to delete.")
    
    def updateShopCount(self):
        selected_row = self.floors_table.currentRow()
        if selected_row >= 0:
            floor_id = int(self.floors_table.item(selected_row, 0).text())
            shop_count = self.shop_count_spin.value()
            
            self.controller.update_shop_count(floor_id, shop_count)
            QMessageBox.information(self, "Success", "Shop count updated successfully.")
        else:
            QMessageBox.warning(self, "No Selection", "Please select a floor to update.")

class FloorDialog(QDialog):
    def __init__(self, parent=None, address=None, floor=None):
        super().__init__(parent)
        self.address = address
        self.floor = floor
        self.initUI()
        
        if floor:
            self.setWindowTitle("Edit Floor")
            self.populateFields()
        else:
            self.setWindowTitle("Add Floor")
    
    def initUI(self):
        layout = QFormLayout(self)
        
        # Floor Number
        self.floor_number_spin = QSpinBox()
        self.floor_number_spin.setMinimum(1)
        self.floor_number_spin.setMaximum(self.address.total_floors if self.address else 100)
        layout.addRow("Floor Number:", self.floor_number_spin)
        
        # Floor Type Checkboxes
        self.owner_check = QCheckBox("Owner")
        layout.addRow("", self.owner_check)
        
        self.tenant_check = QCheckBox("Tenant")
        layout.addRow("", self.tenant_check)
        
        self.commercial_check = QCheckBox("Commercial")
        layout.addRow("", self.commercial_check)
        
        self.shop_check = QCheckBox("Shop")
        self.shop_check.stateChanged.connect(self.onShopCheckChanged)
        layout.addRow("", self.shop_check)
        
        self.vacant_check = QCheckBox("Vacant")
        layout.addRow("", self.vacant_check)
        
        # Shop Count (only visible when shop is checked)
        self.shop_count_group = QGroupBox("Shop Details")
        shop_layout = QFormLayout()
        
        self.shop_count_spin = QSpinBox()
        self.shop_count_spin.setMinimum(1)
        self.shop_count_spin.setMaximum(100)
        shop_layout.addRow("Number of Shops:", self.shop_count_spin)
        
        self.shop_count_group.setLayout(shop_layout)
        self.shop_count_group.setVisible(False)
        layout.addRow("", self.shop_count_group)
        
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
        if self.floor:
            self.floor_number_spin.setValue(self.floor.floor_number)
            self.owner_check.setChecked(self.floor.is_owner)
            self.tenant_check.setChecked(self.floor.is_tenant)
            self.commercial_check.setChecked(self.floor.is_commercial)
            self.shop_check.setChecked(self.floor.is_shop)
            self.vacant_check.setChecked(self.floor.is_vacant)
            
            if self.floor.is_shop:
                self.shop_count_group.setVisible(True)
                self.shop_count_spin.setValue(self.floor.shop_count)
    
    def onShopCheckChanged(self, state):
        self.shop_count_group.setVisible(state == Qt.Checked)
    
    def get_floor_data(self):
        return {
            'floor_number': self.floor_number_spin.value(),
            'is_owner': self.owner_check.isChecked(),
            'is_tenant': self.tenant_check.isChecked(),
            'is_commercial': self.commercial_check.isChecked(),
            'is_shop': self.shop_check.isChecked(),
            'is_vacant': self.vacant_check.isChecked(),
            'shop_count': self.shop_count_spin.value() if self.shop_check.isChecked() else 0
        }
