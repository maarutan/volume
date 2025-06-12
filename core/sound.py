from subprocess import run
from core.config import Config
from pathlib import Path
from modules import Volume
import os, re


class Sound:
    def __init__(self) -> None:
        self.vol = Volume()
        self.conf = Config()
        self.option_name = "sound_path"
        self.variables = {"relative_dir": Path(__file__).parent.parent.resolve()}
        self._played = False

    def resolve_path(self) -> Path | bool:
        raw_path = self.conf.get_option(self.option_name)
        if isinstance(raw_path, bool):
            return raw_path

        path = str(raw_path).strip()

        if path.lower() == "false":
            return False

        match = re.match(r"^\{(\w+)\}/(.*)", path)
        if match:
            var_name, relative_part = match.groups()
            base = self.variables.get(var_name)
            if base is None:
                raise ValueError(f"Unknown variable: {{{var_name}}}")
            return Path(base) / relative_part

        return Path(os.path.expanduser(path)).resolve()

    def is_sound_enabled(self) -> bool:
        enabled = self.conf.get_option("sound_enable")
        if isinstance(enabled, bool):
            return enabled
        if isinstance(enabled, str):
            return enabled.lower() == "true"
        return False

    def sound_run(self) -> None:
        path = self.resolve_path()
        if not path or path is False or not path.exists():
            return
        volume = self.conf.get_option("sound_volume")
        try:
            vol = int(volume)
        except (TypeError, ValueError):
            vol = 100

        run(
            ["mpv", f"--volume={vol}", str(path)],
        )

    def sound_start_handler(self, current_vol) -> None:
        sound_conf = self.conf.get_option("sound_start_vol")

        if not isinstance(sound_conf, dict):
            return

        if sound_conf.get("enable", False):
            try:
                limit_vol = int(sound_conf.get("vol_level", 100))
            except (TypeError, ValueError):
                limit_vol = 100

            if current_vol == limit_vol:
                if not self._played:
                    self.sound_run()
                    self._played = True
            else:
                self._played = False

    def sound_end_handler(self, current_vol) -> None:
        sound_conf = self.conf.get_option("sound_end_vol")

        if not isinstance(sound_conf, dict):
            return

        if sound_conf.get("enable", False):
            try:
                limit_vol = int(sound_conf.get("vol_level", 100))
            except (TypeError, ValueError):
                limit_vol = 100

            if current_vol == limit_vol:
                if not self._played:
                    self.sound_run()
                    self._played = True
            else:
                self._played = False
