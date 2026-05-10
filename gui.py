import sys
import os
import logging
import datetime

from PyQt6.QtWidgets import QApplication
from PyQt6.QtGui import QIcon

from settings.app_settings import settings
from settings.paths import ICONS_DIR
from gui.main_window import MainWindow
from database.sessions import init_db

LOG_DIR = 'logs'
os.makedirs(LOG_DIR, exist_ok=True)
log_filename = os.path.join(
    LOG_DIR, f"gui_{datetime.datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.log"
)
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(log_filename),
        logging.StreamHandler(sys.stdout),
    ],
)

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

logging.info("Fanland OSINT starting...")


def main():
    init_db()
    app = QApplication(sys.argv)

    icon_path = os.path.join(ICONS_DIR, "ico.ico")
    if not os.path.exists(icon_path):
        icon_path = os.path.join(os.path.dirname(__file__), "icons", "ico.ico")
    if os.path.exists(icon_path):
        app.setWindowIcon(QIcon(icon_path))

    window = MainWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        logging.critical(f"Unhandled exception at top level: {e}", exc_info=True)
        sys.exit(1)
