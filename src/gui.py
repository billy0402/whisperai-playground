import typing as t

from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QLabel, QMainWindow, QVBoxLayout, QWidget


class SubtitleWindow(QMainWindow):
    subtitles: t.ClassVar[list[str]] = []

    def __init__(self) -> None:
        super().__init__()
        self.setWindowFlags(self.windowFlags() | Qt.WindowType.WindowStaysOnTopHint)
        self.setWindowTitle("即時字幕")
        self.setGeometry(100, 100, 800, 400)

        self.subtitle_label = QLabel("準備接收字幕...", self)
        self.subtitle_label.setAlignment(
            Qt.AlignmentFlag.AlignTop | Qt.AlignmentFlag.AlignLeft
        )

        layout = QVBoxLayout()
        layout.addWidget(self.subtitle_label)
        container = QWidget()
        container.setLayout(layout)
        self.setCentralWidget(container)

        self.history: list[str] = []

    def push_subtitle(self, text: str) -> None:
        self.subtitles.append(text)
        self.subtitle_label.setText("\n".join(self.subtitles))
