import sys
from time import sleep
from threading import Thread

from PySide6.QtGui import QFont
from PySide6.QtWidgets import QApplication, QLabel, QWidget
from PySide6.QtCore import Qt, QPropertyAnimation, QTimer, QEasingCurve, Signal, QObject


class ObjectSignal(QObject):
    signal = Signal(str)

class TextWidget:
    def __init__(self):
        self.widget = None

        self.animation = None
        self.timer_app = None

        self.is_running = False

        self.object_signal = None

    # <--- Lifecycle --->
    def create_widget(self):
        self.widget = QWidget()

        self.widget.setWindowFlags(
            Qt.WindowType.FramelessWindowHint |
            Qt.WindowType.WindowStaysOnTopHint |
            Qt.WindowType.Tool
        )
        self.widget.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        self.widget.label = QLabel(self.widget)
        self.widget.label.setStyleSheet(
            """
            color: rgba(255, 255, 255, 220);
            background-color: rgba(44, 45, 47, 180);
            border: 1px solid rgba(0, 0, 0, 120);
            border-radius: 8px;
            padding: 6px;
            """
        )
        self.widget.label.setFont(QFont("Arial", 12))

    def _show_text(self, text: str):
        self._change_text(text)

        if self.timer_app:
            self.timer_app.stop()
            self._run_timer_app()
            return

        if not self.animation:
            self.start_widget()

    def start_widget(self):
        self.widget.setWindowOpacity(0.0)
        self.widget.show()
        self.widget.raise_()

        self._fade_in()

    def _fade_in(self):
        self.animation = QPropertyAnimation(self.widget, b"windowOpacity")
        self.animation.setDuration(500)
        self.animation.setStartValue(0.0)
        self.animation.setEndValue(1.0)
        self.animation.setEasingCurve(QEasingCurve.Type.InOutQuad)
        self.animation.finished.connect(self._run_timer_app)
        self.animation.start()

    def _run_timer_app(self):
        self.animation = None

        self.timer_app = QTimer(self.widget)
        self.timer_app.setSingleShot(False)
        self.timer_app.timeout.connect(self._fade_out)
        self.timer_app.start(2000)

    def _fade_out(self):
        self.timer_app.stop()
        self.timer_app = None

        self.animation = QPropertyAnimation(self.widget, b"windowOpacity")
        self.animation.setDuration(500)
        self.animation.setStartValue(1.0)
        self.animation.setEndValue(0.0)
        self.animation.setEasingCurve(QEasingCurve.Type.InOutQuad)
        self.animation.finished.connect(self._finish_widget)
        self.animation.start()

    def _finish_widget(self):
        self.widget.close()

        self.animation = None

    # <--- Utils --->
    def _change_text(self, text):
        self.widget.label.setText(text)
        self.widget.label.adjustSize()
        self.widget.resize(self.widget.label.size())

        screen = QApplication.primaryScreen().availableGeometry()
        x = (screen.width() - self.widget.width()) // 2
        y = screen.height() - self.widget.height() - 50
        self.widget.move(x, y)

    # <--- Main --->
    def _main_run(self, text):
        self.is_running = True
        self.object_signal = ObjectSignal()

        app = QApplication(sys.argv)
        self.create_widget()

        self._show_text(text)

        self.object_signal.signal.connect(self._show_text)

        app.exec()
        self.is_running = False

    def show_text(self, text: str):
        if not self.is_running:
            Thread(target=self._main_run, args=(text,), daemon=True).start()
            return

        self.object_signal.signal.emit(text)

if __name__ == "__main__":
    text_widget = TextWidget()

    text_widget.show_text('30')

    sleep(0.4)
    print(40)
    text_widget.show_text('40')

    sleep(1)
    print(50)
    text_widget.show_text('50')

    sleep(3)
    text_widget.show_text('60')
    sleep(5)
    print("end")