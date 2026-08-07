import sys
import threading
import subprocess
import time
import socket
from PyQt6.QtWidgets import QApplication
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtCore import QUrl


# =========================
# START FLASK SERVER
# =========================
def start_server():
    subprocess.Popen(
        ["python", "app.py"],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL
    )


# =========================
# WAIT FOR SERVER
# =========================
def wait_for_server(host="127.0.0.1", port=8000, timeout=15):
    start = time.time()

    while time.time() - start < timeout:
        try:
            with socket.create_connection((host, port), timeout=1):
                return True
        except:
            time.sleep(0.3)

    return False


# =========================
# MAIN APP
# =========================
def main():
    threading.Thread(target=start_server, daemon=True).start()

    print("Starting AuraOS server...")

    if not wait_for_server():
        print("Server failed to start.")
        sys.exit(1)

    app = QApplication(sys.argv)

    window = QWebEngineView()
    window.setWindowTitle("AuraOS")

    window.load(QUrl("http://127.0.0.1:8000"))

    window.showFullScreen()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()