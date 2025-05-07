import whisper

from record import record_audio

audio_file_name = "tmp.wav"
model = whisper.load_model("small")
# model = whisper.load_model("large-v3-turbo")

while True:
    record_audio(audio_file_name, 5)
    audio = whisper.pad_or_trim(whisper.load_audio(audio_file_name))
    result = whisper.transcribe(model, audio, language="ja", fp16=False)
    translation = whisper.transcribe(model, audio, task="translate", fp16=False)
    print(result["text"])
    print("翻譯:", translation["text"])
