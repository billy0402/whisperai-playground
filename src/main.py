import pathlib
import time

import whisper


def format_timestamp(seconds: float) -> str:
    milliseconds = int(seconds * 1000)
    hours = milliseconds // 3_600_000
    minutes = (milliseconds % 3_600_000) // 60_000
    seconds = (milliseconds % 60_000) // 1000
    milliseconds = milliseconds % 1000
    return f"{hours:02}:{minutes:02}:{seconds:02},{milliseconds:03}"


start_time = time.perf_counter()

model = whisper.load_model("small")

result = model.transcribe("為什麼要演奏春日影.mp4")
# result = model.transcribe("為什麼要演奏春日影.mp4", task="translate")
print(result)

# segments = [
#     f"[{segment['start']:.2f} --> {segment['end']:.2f}] {segment['text']}"  # pyright: ignore[reportArgumentType]
#     for segment in result["segments"]
# ]

with pathlib.Path("result.srt").open("w+", encoding="utf-8") as f:
    for idx, segment in enumerate(result["segments"], start=1):
        start = format_timestamp(segment["start"])  # pyright: ignore[reportArgumentType]
        end = format_timestamp(segment["end"])  # pyright: ignore[reportArgumentType]
        text = segment["text"].strip()  # pyright: ignore[reportArgumentType]
        f.write(f"{idx}\n{start} --> {end}\n{text}\n\n")

end_time = time.perf_counter()
print(f"Execute time: {end_time - start_time:.6f} seconds")
