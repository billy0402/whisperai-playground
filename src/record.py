# ruff: noqa: N806
import wave

import pyaudio


def record_audio(filename: str = "tmp.wav", record_seconds: int = 5) -> None:
    # 設定錄音參數
    FORMAT = pyaudio.paInt16  # 錄音格式
    CHANNELS = 1  # 單聲道
    RATE = 16000  # 採樣率
    CHUNK = 1024  # 資料塊大小
    RECORD_SECONDS = record_seconds  # 錄音時間 (秒)

    audio = pyaudio.PyAudio()
    devices = [
        audio.get_device_info_by_index(i)["name"]
        for i in range(audio.get_device_count())
    ]
    device_index = devices.index("BlackHole 2ch")  # 取得錄音設備的索引

    # 開啟語音串流
    try:
        stream = audio.open(
            format=FORMAT,
            channels=CHANNELS,
            rate=RATE,
            input=True,
            frames_per_buffer=CHUNK,
            input_device_index=device_index,  # 設定錄音設備的索引
        )
    except Exception as e:  # noqa: BLE001
        print(f"無法開啟音訊串流: {e}")
        return

    # 錄音主迴圈
    frames:list[bytes] = []  # 存放錄音資料的陣列
    for _ in range(1, int(RATE / CHUNK * RECORD_SECONDS)):
        data = stream.read(CHUNK)
        frames.append(data)

    # 關閉和釋放資源
    stream.stop_stream()
    stream.close()
    audio.terminate()

    # 儲存錄音檔案
    with wave.open(filename, "wb") as wave_file:
        wave_file.setnchannels(CHANNELS)
        wave_file.setsampwidth(audio.get_sample_size(FORMAT))
        wave_file.setframerate(RATE)
        wave_file.writeframes(b"".join(frames))
