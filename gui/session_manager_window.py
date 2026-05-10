from PyQt6.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QTableWidget, QTableWidgetItem, QLineEdit, QMessageBox
from PyQt6.QtCore import Qt
from database.sessions import get_all_sessions, create_session, delete_session
from datetime import datetime

class SessionManagerWindow(QDialog):
    def __init__(self, parent, on_session_selected):
        super().__init__(parent)
        self.on_session_selected = on_session_selected
        self.setWindowTitle("Session Manager - Fanland OSINT")
        self.setMinimumSize(800, 500)
        
        layout = QVBoxLayout(self)
        
        title = QLabel("OSINT Investigation Sessions")
        title.setStyleSheet("font-size: 14pt; font-weight: bold;")
        layout.addWidget(title)
        
        btn_layout = QHBoxLayout()
        self.btn_new = QPushButton("New Session")
        self.btn_continue = QPushButton("Continue")
        self.btn_delete = QPushButton("Delete")
        self.btn_refresh = QPushButton("Refresh")
        
        btn_layout.addWidget(self.btn_new)
        btn_layout.addWidget(self.btn_continue)
        btn_layout.addWidget(self.btn_delete)
        btn_layout.addWidget(self.btn_refresh)
        btn_layout.addStretch()
        layout.addLayout(btn_layout)
        
        self.table = QTableWidget()
        self.table.setColumnCount(5)
        self.table.setHorizontalHeaderLabels(["ID", "Name", "Target", "Created", "Updated"])
        self.table.setSelectionBehavior(QTableWidget.SelectionBehavior.SelectRows)
        self.table.setEditTriggers(QTableWidget.EditTrigger.NoEditTriggers)
        self.table.doubleClicked.connect(self.continue_session)
        layout.addWidget(self.table)
        
        self.btn_new.clicked.connect(self.new_session)
        self.btn_continue.clicked.connect(self.continue_session)
        self.btn_delete.clicked.connect(self.delete_session)
        self.btn_refresh.clicked.connect(self.refresh_list)
        
        self.refresh_list()
        
    def refresh_list(self):
        self.table.setRowCount(0)
        sessions = get_all_sessions()
        for session in sessions:
            sid, name, target, created, updated = session
            row = self.table.rowCount()
            self.table.insertRow(row)
            self.table.setItem(row, 0, QTableWidgetItem(str(sid)))
            self.table.setItem(row, 1, QTableWidgetItem(name))
            self.table.setItem(row, 2, QTableWidgetItem(target or "N/A"))
            self.table.setItem(row, 3, QTableWidgetItem(datetime.fromisoformat(created).strftime("%Y-%m-%d %H:%M")))
            self.table.setItem(row, 4, QTableWidgetItem(datetime.fromisoformat(updated).strftime("%Y-%m-%d %H:%M")))
    
    def new_session(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("New Session")
        dialog.setMinimumWidth(400)
        
        layout = QVBoxLayout(dialog)
        
        layout.addWidget(QLabel("Session Name:"))
        name_entry = QLineEdit()
        layout.addWidget(name_entry)
        
        layout.addWidget(QLabel("Target (optional):"))
        target_entry = QLineEdit()
        layout.addWidget(target_entry)
        
        btn_layout = QHBoxLayout()
        btn_create = QPushButton("Create")
        btn_cancel = QPushButton("Cancel")
        btn_layout.addWidget(btn_create)
        btn_layout.addWidget(btn_cancel)
        layout.addLayout(btn_layout)
        
        def create():
            name = name_entry.text().strip()
            if not name:
                QMessageBox.critical(dialog, "Error", "Session name required")
                return
            target = target_entry.text().strip()
            session_id = create_session(name, target)
            dialog.accept()
            self.on_session_selected(session_id)
            self.accept()
        
        btn_create.clicked.connect(create)
        btn_cancel.clicked.connect(dialog.reject)
        
        dialog.exec()
    
    def continue_session(self):
        row = self.table.currentRow()
        if row < 0:
            QMessageBox.warning(self, "Warning", "Select a session")
            return
        
        session_id = int(self.table.item(row, 0).text())
        self.on_session_selected(session_id)
        self.accept()
    
    def delete_session(self):
        row = self.table.currentRow()
        if row < 0:
            QMessageBox.warning(self, "Warning", "Select a session")
            return
        
        session_id = int(self.table.item(row, 0).text())
        reply = QMessageBox.question(self, "Confirm", f"Delete session #{session_id}?",
                                      QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        if reply == QMessageBox.StandardButton.Yes:
            delete_session(session_id)
            self.refresh_list()
