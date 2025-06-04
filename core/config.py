from modules import JsonManager, FileManager
from core.path.list import JSONC_CONFIG


class Config:
    def __init__(self):
        self.jm = JsonManager(JSONC_CONFIG)
        self.fm = FileManager
        self.indent = 2

        self.generate()

    def generate(self) -> None:
        try:
            r = self.fm(JSONC_CONFIG).read()
            if not r:
                self.fm(JSONC_CONFIG).write(
                    """{
  "theme": "default", // default | twist
  "redner_volume": "  *･ﾟ✧ {volume}% ✧･ﾟ*",
  "content_microphone": "🎤 Microphone Muted" ,
  "volume_mute": "   (づ｡◕‿‿◕｡)づ",

  "notify_id": 9999,
  "notify_timeout": 1000,
  "notify_sound": false,
  "notify_icon": false,
  "notify_progress_bar": true,

  "turn_add": 5, 
  "turn_down": 5,
  "turn_smooth": true,
  "turn_delay": 0.040

}"""
                )
        except Exception as e:
            print(f"Config.generate: {e}")

    def get_option(self, option) -> str:
        try:
            return self.jm.get_data()[option]
        except Exception as e:
            print(f"Config.get_option: {e}")
            return ""
