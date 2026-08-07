import sys
import threading
import time
import socket
import os

from PyQt6.QtWidgets import QApplication
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtCore import QUrl

from server import app


# =========================
# START SERVER
# =========================
def run_server():
    app.run(
        host="127.0.0.1",
        port=8000,
        debug=False,
        use_reloader=False,
        threaded=True
    )


# =========================
# WAIT FOR SERVER
# =========================
def wait_for_server():
    for _ in range(50):
        try:
            s = socket.create_connection(("127.0.0.1", 8000), timeout=1)
            s.close()
            return True
        except:
            time.sleep(0.2)

    return False


# =========================
# MAIN
# =========================
def main():

    threading.Thread(target=run_server, daemon=True).start()

    if not wait_for_server():
        print("SERVER FAILED TO START")
        sys.exit(1)

    app_qt = QApplication(sys.argv)

    window = QWebEngineView()
    window.setWindowTitle("AuraOS")

    window.load(QUrl("http://127.0.0.1:8000"))

    window.showMaximized()

    sys.exit(app_qt.exec())


if __name__ == "__main__":
    main()