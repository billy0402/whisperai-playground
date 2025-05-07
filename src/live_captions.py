import whisper

from mac_notify import notify
from record import record_audio

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
    notify("即時字幕", f'{result["text"]}\n翻譯: {translation["text"]}')
