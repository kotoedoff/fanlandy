from PyQt6.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QTextEdit, QLineEdit, QPushButton, QLabel, QMessageBox
from PyQt6.QtCore import Qt, QThread, pyqtSignal
from PyQt6.QtGui import QTextCursor
from ai.groq_assistant import GroqAssistant
from database.sessions import add_chat_message, get_chat_history, get_session

class AIWorker(QThread):
    chunk_received = pyqtSignal(str)
    finished = pyqtSignal(str)
    error = pyqtSignal(str)
    
    def __init__(self, assistant, session_id, session_data, message):
        super().__init__()
        self.assistant = assistant
        self.session_id = session_id
        self.session_data = session_data
        self.message = message
        
    def run(self):
        try:
            full_response = ""
            for chunk in self.assistant.chat(self.session_id, self.session_data, self.message):
                full_response += chunk
                self.chunk_received.emit(chunk)
            self.finished.emit(full_response)
        except Exception as e:
            self.error.emit(str(e))

class AIAssistantWindow(QDialog):
    def __init__(self, parent, session_id, api_key):
        super().__init__(parent)
        self.session_id = session_id
        self.assistant = GroqAssistant(api_key)
        self.session_data = get_session(session_id)
        self.worker = None
        
        self.setWindowTitle(f"AI Assistant - Session: {self.session_data[1]}")
        self.setMinimumSize(700, 600)
        
        layout = QVBoxLayout(self)
        
        title = QLabel(f"AI Assistant - Session: {self.session_data[1]}")
        title.setStyleSheet("font-size: 12pt; font-weight: bold;")
        layout.addWidget(title)
        
        self.chat_area = QTextEdit()
        self.chat_area.setReadOnly(True)
        layout.addWidget(self.chat_area)
        
        input_layout = QHBoxLayout()
        self.input_field = QLineEdit()
        self.input_field.returnPressed.connect(self.send_message)
        input_layout.addWidget(self.input_field)
        
        self.send_btn = QPushButton("Send")
        self.send_btn.clicked.connect(self.send_message)
        input_layout.addWidget(self.send_btn)
        
        layout.addLayout(input_layout)
        
        self.load_history()
        
    def load_history(self):
        history = get_chat_history(self.session_id)
        for role, content in history:
            if role == "user":
                self.chat_area.append(f"<b style='color:#0066cc'>You:</b> {content}<br>")
            else:
                self.chat_area.append(f"<b style='color:#009900'>AI:</b> {content}<br>")
    
    def send_message(self):
        message = self.input_field.text().strip()
        if not message or self.worker:
            return
        
        self.input_field.clear()
        self.send_btn.setEnabled(False)
        
        self.chat_area.append(f"<b style='color:#0066cc'>You:</b> {message}<br>")
        add_chat_message(self.session_id, "user", message)
        
        self.chat_area.append(f"<b style='color:#009900'>AI:</b> ")
        self.response_start_pos = self.chat_area.textCursor().position()
        
        self.worker = AIWorker(self.assistant, self.session_id, self.session_data, message)
        self.worker.chunk_received.connect(self.on_chunk)
        self.worker.finished.connect(self.on_finished)
        self.worker.error.connect(self.on_error)
        self.worker.start()
    
    def on_chunk(self, chunk):
        cursor = self.chat_area.textCursor()
        cursor.movePosition(QTextCursor.MoveOperation.End)
        cursor.insertText(chunk)
        self.chat_area.setTextCursor(cursor)
        self.chat_area.ensureCursorVisible()
    
    def on_finished(self, full_response):
        self.chat_area.append("<br>")
        add_chat_message(self.session_id, "assistant", full_response)
        self.send_btn.setEnabled(True)
        self.worker = None
    
    def on_error(self, error_msg):
        self.chat_area.append(f"<i style='color:#666'>Error: {error_msg}</i><br>")
        self.send_btn.setEnabled(True)
        self.worker = None
