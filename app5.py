import sys
import os
from PyQt6.QtWidgets import QApplication
from PyQt6.QtCore import QUrl
from PyQt6.QtWebEngineWidgets import QWebEngineView


class AuraOS:
    def __init__(self):
        self.app = QApplication(sys.argv)

        self.view = QWebEngineView()

        base_path = os.path.dirname(os.path.abspath(__file__))
        file_path = os.path.join(base_path, "index.html")

        self.view.setUrl(QUrl.fromLocalFile(file_path))

        self.view.setWindowTitle("AuraOS")
        self.view.showMaximized()

    def run(self):
        sys.exit(self.app.exec())


if __name__ == "__main__":
    window = AuraOS()
    window.run()