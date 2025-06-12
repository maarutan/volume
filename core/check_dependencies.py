from shutil import which
from modules import NotifySend

list_dependencies = [
    "pactl",
    "notify-send",
    "mpv",
]

n = NotifySend


def check() -> bool:
    try:
        for i in list_dependencies:
            if not which(i):
                n(f"{i} not found").send()
                print(f"{i} not found")
                return False
        return True
    except Exception as e:
        print(f"check_dependencies: {e}")
        return True
