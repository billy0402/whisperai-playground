import subprocess

CMD = """
on run argv
  display notification (item 2 of argv) with title (item 1 of argv)
end run
"""


def notify(title: str, text: str) -> None:
    subprocess.call(["osascript", "-e", CMD, title, text])  # noqa: S603, S607
