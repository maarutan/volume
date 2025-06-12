import dataclasses
from pathlib import Path
from dataclasses import dataclass
from core.config import Config
from modules import (
    Volume,
    FileManager,
)
from core.path.list import (
    ICONS_THEME_DIR,
    CACHE_FILE_SYSTEM_THEME,
    RELATIVE_CACHE_FILE_SYSTEM_THEME,
)


@dataclass
class IconsTheme:
    icons: dict = dataclasses.field(default_factory=dict)


class IconPath(IconsTheme):
    def __init__(self):
        super().__init__()
        self.conf = Config()
        self.fm = FileManager
        self.current_theme = self.conf.get_option("theme")
        self.vol = Volume()
        self.theme_list = self.get_theme(only_name=True)
        if self.current_theme in self.theme_list:
            self.path = ICONS_THEME_DIR / self.current_theme / self.get_system_theme()
            self.icons = {i: f"vol_{i}.svg" for i in range(1, 101)}
            self.icons.update(
                {
                    "micro_off": "vol_micro_off.svg",
                    "micro_on": "vol_micro_on.svg",
                    "mute": "vol_mute.svg",
                }
            )

    def get_theme(self, only_name: bool) -> list:
        """if `only_name=true` return only theme name else absolute path"""
        themes = []
        for i in ICONS_THEME_DIR.iterdir():
            themes.append(i.name if only_name else i.absolute())
        return themes

    def get_system_theme(self) -> str:
        if not CACHE_FILE_SYSTEM_THEME.exists():
            CACHE_FILE_SYSTEM_THEME.parent.mkdir(parents=True, exist_ok=True)
            CACHE_FILE_SYSTEM_THEME.write_text("dark")
        return (
            CACHE_FILE_SYSTEM_THEME.read_text().strip()
            if CACHE_FILE_SYSTEM_THEME
            else RELATIVE_CACHE_FILE_SYSTEM_THEME.read_text().strip()
        )

    def get_micro_mute_icon(self) -> Path:
        if self.vol.is_micro_muted():
            return self.path / self.icons["micro_on"]
        else:
            return self.path / self.icons["micro_off"]

    def get_volume_icon(self) -> Path | None:
        volume = self.vol.get_volume()
        int_keys = sorted(
            [k for k in self.icons.keys() if isinstance(k, int)], reverse=True
        )

        for key in int_keys:
            if volume >= key:
                result = self.path / self.icons[key]
                if self.fm(Path(result)).is_exists():
                    return result
                for alt_key in range(key - 1, 0, -1):
                    if alt_key in self.icons:
                        alt_result = self.path / self.icons[alt_key]
                        if self.fm(Path(alt_result)).is_exists():
                            return Path(alt_result)
                break

        fallback = self.path / self.icons.get(10, "vol_10.svg")
        return fallback if self.fm(fallback).is_exists() else None

    def get_volume_mute_icon(self) -> Path | None:
        if self.vol.is_volume_muted():
            return self.path / self.icons["mute"]
        else:
            return self.get_volume_icon()
