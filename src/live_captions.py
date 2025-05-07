import signal
import sys
import threading

import whisper
from PyQt6.QtWidgets import QApplication

from gui import SubtitleWindow
from record import record_audio


def transcription_worker(window: SubtitleWindow) -> None:
    audio_file_name = "tmp.wav"
    model = whisper.load_model("small")
    # model = whisper.load_model("large-v3-turbo")

    while True:
        record_audio(audio_file_name, 5)
        audio = whisper.pad_or_trim(whisper.load_audio(audio_file_name))
        result = whisper.transcribe(model, audio, language="ja", fp16=False)
        if not result["text"]:
            continue
        translation = whisper.transcribe(model, audio, task="translate", fp16=False)
        window.push_subtitle(f'{result["text"]}\n翻譯: {translation["text"]}')


signal.signal(signal.SIGINT, signal.SIG_DFL)
app = QApplication(sys.argv)
window = SubtitleWindow()
window.show()

transcription_thread = threading.Thread(
    target=transcription_worker,
    args=(window,),
    daemon=True,  # 確保主程序退出時線程也會退出
)
transcription_thread.start()

sys.exit(app.exec())
