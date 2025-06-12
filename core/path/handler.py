from modules import FileManager
from .list import *
from . import list as l

check_exists = [
    l.CACHE_FILE_SYSTEM_THEME,
    l.JSONC_CONFIG,
    l.ICONS_THEME_DIR,
    l.RELATIVE_CACHE_FILE_SYSTEM_THEME,
]

try:
    for i in check_exists:
        if not i.exists():
            Fm = FileManager(i)
            Fm.create_if_not_exists()

except Exception as e:
    print(f"Path handler: {e}")
