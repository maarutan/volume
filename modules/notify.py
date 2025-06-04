from subprocess import run
from pathlib import Path
from typing import Optional


class NotifySend:
    def __init__(
        self,
        message: Optional[str],
        icon: Optional[Path] = None,
        timeout: Optional[int] = None,
        id: Optional[int] = None,
        progress: Optional[bool] = None,
        progress_value: Optional[int] = None,
    ):
        if not message:
            raise ValueError("Message cannot be None or empty.")
        self.message = message
        self.icon = icon
        self.timeout = timeout
        self.id = id
        self.progress = progress
        self.progress_value = progress_value

    def send(self):
        args = ["notify-send"]

        if self.icon:
            args += ["-i", self.icon]

        if self.timeout:
            args += ["-t", str(self.timeout)]

        if self.id:
            args += ["-r", str(self.id)]

        if self.progress:
            args += ["-h", f"int:value:{self.progress_value}"]

        args.append(self.message)
        run(args)
