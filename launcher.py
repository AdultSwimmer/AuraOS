import sys
import threading
import time
import socket

from PyQt6.QtWidgets import QApplication
from PyQt6.QtWebEngineWidgets import QWebEngineView
from PyQt6.QtWebChannel import QWebChannel
from PyQt6.QtCore import QUrl, QObject, pyqtSlot

from server import app


SERVER_ADDRESS = "http://127.0.0.1:8000"
APP_SECRET = "aura-7f4k2-xq91m-dulong-2026-zp38w"


class AuraBridge(QObject):
    def __init__(self, window):
        super().__init__()
        self.window = window

    @pyqtSlot()
    def minimize(self):
        self.window.showMinimized()

    @pyqtSlot()
    def close(self):
        self.window.close()


def run_server():
    app.run(
        host="0.0.0.0",
        port=8000,
        debug=False,
        use_reloader=False,
        threaded=True
    )


def wait_for_server():
    for _ in range(60):
        try:
            s = socket.create_connection(("127.0.0.1", 8000), timeout=1)
            s.close()
            return True
        except:
            time.sleep(0.3)
    return False


def main():
    threading.Thread(target=run_server, daemon=True).start()

    if not wait_for_server():
        print("CRITICAL: Server failed to start.")
        sys.exit(1)

    app_qt = QApplication(sys.argv)
    window = QWebEngineView()
    window.setWindowTitle("AuraOS")
    window.resize(1100, 750)

    # WebChannel Setup
    channel = QWebChannel()
    bridge = AuraBridge(window)
    channel.registerObject("auraBridge", bridge)
    window.page().setWebChannel(channel)

    def on_load_finished(ok):
        if ok:
            window.page().runJavaScript(f'window.AURA_KEY = "{APP_SECRET}";')
            window.page().runJavaScript("""
                window.auraBridge = {
                    minimize: () => window.qt.webChannel.objects.auraBridge.minimize(),
                    close: () => window.qt.webChannel.objects.auraBridge.close()
                };
                console.log('AuraBridge ready');
            """)

    window.loadFinished.connect(on_load_finished)
    window.load(QUrl(SERVER_ADDRESS))
    window.showFullScreen()

    sys.exit(app_qt.exec())


if __name__ == "__main__":
    main()