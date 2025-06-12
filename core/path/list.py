from pathlib import Path

HOME = Path.home()
CURRENT_DIR = Path(__file__).parent.parent.parent

CACHE_FILE_SYSTEM_THEME = HOME / ".cache" / "system_theme"
ICONS_THEME_DIR = CURRENT_DIR / ".icons"
JSONC_CONFIG = CURRENT_DIR / "config.jsonc"
