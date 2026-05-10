from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QLineEdit, QTextEdit, QComboBox, QProgressBar
from PyQt6.QtCore import Qt, QThread, pyqtSignal
from PyQt6.QtGui import QFont
from script.tools.osint_tools import (
    run_maigret, run_holehe, run_toutatis, 
    run_sherlock, run_blackbird, run_ghunt, run_phoneinfoga,
    run_spiderfoot, run_theharvester, run_whatsmyname, run_socialscan
)

class OSINTWorker(QThread):
    finished = pyqtSignal(dict)
    progress = pyqtSignal(str)
    
    def __init__(self, tool, query):
        super().__init__()
        self.tool = tool
        self.query = query
        
    def run(self):
        self.progress.emit(f"Running {self.tool}...")
        
        tools_map = {
            "maigret": run_maigret,
            "holehe": run_holehe,
            "toutatis": run_toutatis,
            "sherlock": run_sherlock,
            "blackbird": run_blackbird,
            "ghunt": run_ghunt,
            "phoneinfoga": run_phoneinfoga,
            "spiderfoot": run_spiderfoot,
            "theharvester": run_theharvester,
            "whatsmyname": run_whatsmyname,
            "socialscan": run_socialscan
        }
        
        func = tools_map.get(self.tool)
        if func:
            result = func(self.query)
        else:
            result = {"error": "Unknown tool"}
            
        self.finished.emit(result)

class OSINTSearchWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Fanland OSINT Tools")
        self.resize(1000, 700)
        self.init_ui()
        
    def init_ui(self):
        layout = QVBoxLayout()
        
        header = QLabel("🔍 Fanland OSINT Multi-Tool")
        header.setFont(QFont("Arial", 18, QFont.Weight.Bold))
        header.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(header)
        
        desc = QLabel("Maigret • Sherlock • Holehe • GHunt • Blackbird • PhoneInfoga • Toutatis • SpiderFoot • theHarvester • WhatsMyName • SocialScan")
        desc.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(desc)
        
        input_layout = QHBoxLayout()
        self.query_input = QLineEdit()
        self.query_input.setPlaceholderText("Enter username, email, phone or domain...")
        input_layout.addWidget(QLabel("Query:"))
        input_layout.addWidget(self.query_input)
        layout.addLayout(input_layout)
        
        tool_layout = QHBoxLayout()
        self.tool_combo = QComboBox()
        self.tool_combo.addItems([
            "maigret (3000+ sites)",
            "sherlock (400+ sites)", 
            "blackbird (600+ sites)",
            "holehe (email check)",
            "ghunt (Google OSINT)",
            "phoneinfoga (phone)",
            "toutatis (Instagram)",
            "spiderfoot (OSINT automation)",
            "theharvester (domain recon)",
            "whatsmyname (username search)",
            "socialscan (social media)"
        ])
        tool_layout.addWidget(QLabel("Tool:"))
        tool_layout.addWidget(self.tool_combo)
        layout.addLayout(tool_layout)
        
        self.search_btn = QPushButton("🚀 Start Search")
        self.search_btn.clicked.connect(self.start_search)
        layout.addWidget(self.search_btn)
        
        self.progress_bar = QProgressBar()
        self.progress_bar.setVisible(False)
        layout.addWidget(self.progress_bar)
        
        self.status_label = QLabel("Ready")
        layout.addWidget(self.status_label)
        
        self.results_text = QTextEdit()
        self.results_text.setReadOnly(True)
        layout.addWidget(self.results_text)
        
        self.setLayout(layout)
        
    def start_search(self):
        query = self.query_input.text().strip()
        if not query:
            self.status_label.setText("❌ Enter a query")
            return
            
        tool = self.tool_combo.currentText().split()[0]
        
        self.search_btn.setEnabled(False)
        self.progress_bar.setVisible(True)
        self.progress_bar.setRange(0, 0)
        self.results_text.clear()
        
        self.worker = OSINTWorker(tool, query)
        self.worker.finished.connect(self.on_result)
        self.worker.progress.connect(self.on_progress)
        self.worker.start()
        
    def on_progress(self, message):
        self.status_label.setText(message)
        
    def on_result(self, result):
        self.progress_bar.setVisible(False)
        self.search_btn.setEnabled(True)
        
        if "error" in result:
            self.results_text.append(f"❌ Error: {result['error']}")
            self.status_label.setText("Error occurred")
        else:
            self.results_text.append(result.get("output", "No output"))
            if result.get("error"):
                self.results_text.append(f"\nStderr: {result['error']}")
            self.status_label.setText("✅ Complete")
