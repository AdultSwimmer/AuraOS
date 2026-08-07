import sys
import threading
import time
import socket

from PyQt6.QtWidgets import QApplication
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtCore import QUrl

from server import app


# =========================
# YOUR PUBLIC SERVER ADDRESS
# Change this to your domain or public IP before building the .exe
# Examples:
#   "http://192.168.1.100:8000"   (local network testing)
#   "http://yourdomain.duckdns.org:8000"   (public)
# =========================
SERVER_ADDRESS = "http://127.0.0.1:8000"

# =========================
# APP SECRET
# Must match server.py exactly.
# This gets baked into the .exe at build time.
# =========================
APP_SECRET = "aura-7f4k2-xq91m-dulong-2026-zp38w"


# =========================
# START FLASK SERVER
# Runs in background thread so the Qt window can open
# =========================
def run_server():
    app.run(
        host="0.0.0.0",
        port=8000,
        debug=False,
        use_reloader=False,
        threaded=True
    )


# =========================
# WAIT FOR SERVER TO BE READY
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
# INJECT SECRET INTO PAGE
# Runs after every page load.
# Sets window.AURA_KEY so every fetch() in index.html
# can attach it as the X-Aura-Key header.
# =========================
def inject_secret(view):
    view.page().runJavaScript(f'window.AURA_KEY = "{APP_SECRET}";')


# =========================
# MAIN
# =========================
def main():

    # Start the server in the background
    threading.Thread(target=run_server, daemon=True).start()

    # Wait until it's actually ready
    if not wait_for_server():
        print("CRITICAL: Server failed to start.")
        sys.exit(1)

    # Launch the Qt window
    app_qt = QApplication(sys.argv)

    window = QWebEngineView()
    window.setWindowTitle("AuraOS")

    # Inject the secret key every time a page finishes loading
    window.loadFinished.connect(lambda ok: inject_secret(window))

    # Point to your server
    window.load(QUrl(SERVER_ADDRESS))

    window.showFullScreen()

    sys.exit(app_qt.exec())


if __name__ == "__main__":
    main()
