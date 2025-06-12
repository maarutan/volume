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
                    """// ┬  ┬┌─┐┬  ┬ ┬┌┬┐┌─┐  ┌─┐┌─┐┌┐┌┌─┐┬┌─┐
// └┐┌┘│ ││  │ ││││├┤   │  │ ││││├┤ ││ ┬
//  └┘ └─┘┴─┘└─┘┴ ┴└─┘  └─┘└─┘┘└┘└  ┴└─┘
//--------------------------------------------------------------------
// Copyright (c) 2025 maarutan \\ Marat Arzymatov. All Rights Reserved.
// https://github.com/maarutan/volume
//
{
  // ┬─┐┌─┐┌┐┌┌┬┐┌─┐┬─┐
  // ├┬┘├┤ │││ ││├┤ ├┬┘
  // ┴└─└─┘┘└┘─┴┘└─┘┴└─

  // Theme settings
  "theme": "twist",  // Add custom themes (default options: "default" | "twist")
  
  // Volume display settings
  "redner_volume": "  *･ﾟ✧ {volume}% ✧･ﾟ*",  // Customize volume output (use {volume} placeholder)
  
  // Microphone status indicators
  "microphone_mute": "🎤 Microphone Muted",    // Displayed when mic is muted
  "microphone_unmute": "🎤  (づ｡◕‿‿◕｡)づ",    // Displayed when mic is active
  
  // Volume mute indicator
  "volume_mute": "   (づ｡◕‿‿◕｡)づ",          // Displayed when audio is muted
  
  // ┌┬┐┬ ┬┌┐┌┌─┐┌┬┐┬┌─┐  ┌─┐┌─┐┬ ┬┌┐┌┌┬┐
  //  ││└┬┘│││├─┤│││││    └─┐│ ││ ││││ ││
  // ─┴┘ ┴ ┘└┘┴ ┴┴ ┴┴└─┘  └─┘└─┘└─┘┘└┘─┴┘

  // Sound effects configuration
  "sound_path": "{relative_dir}/.sound/pop.mp3",  // Path to sound file (relative to script directory)
  "sound_enable": true,       // Enable sound effects globally
  "sound_volume": 100,        // Volume level for sound effects (0-100)
  
  // Startup sound settings
  "sound_start_vol": {        // Sound when volume adjustment begins
    "enable" : true,          // Toggle startup sound
    "vol_level" : 30          // Volume level to trigger this sound
  },
  
  // Completion sound settings
  "sound_end_vol": {          // Sound when volume adjustment ends
    "enable" : true,          // Toggle completion sound
    "vol_level" : 80          // Volume level to trigger this sound
  }, 

  // ┌┐┌┌─┐┌┬┐┬┌─┐┬ ┬  ┌─┐┌─┐┌┐┌┌┬┐
  // ││││ │ │ │├┤ └┬┘  └─┐├┤ │││ ││
  // ┘└┘└─┘ ┴ ┴└   ┴   └─┘└─┘┘└┘─┴┘
  
  // Notification settings
  "notify_id": 9999,          // Unique notification ID (prevents stacking)
  "notify_timeout": 1000,     // Notification display duration (milliseconds)
  "notify_icon": true,        // Show theme icons in notifications
  "notify_progress_bar": false, // Display volume progress bar
  
  // ┌─┐┌─┐┌┐┌┌┬┐┬─┐┌─┐┬
  // │  │ ││││ │ ├┬┘│ ││
  // └─┘└─┘┘└┘ ┴ ┴└─└─┘┴─┘

  // Volume control parameters
  "turn_add": 5,              // Volume increase step (--up command)
  "turn_sub": 5,              // Volume decrease step (--down command)
  "turn_smooth": true,        // Enable smooth volume transitions
  "turn_delay": 0.01          // Smooth transition speed (seconds per step)
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
