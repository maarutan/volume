from modules import (
    NotifySend,
    Volume,
    SmoothTurn,
)
from core.config import Config
from core.icons import IconPath
from core.sound import Sound


class Render:
    def __init__(self):
        self.vol = Volume()
        self.ntsend = NotifySend
        self.conf = Config()
        self.st = SmoothTurn
        self.ip = IconPath()
        self.sound = Sound()

        ntsend_icon = self.conf.get_option("notify_icon")
        self.icons_vol = self.ip.get_volume_icon() if ntsend_icon else None
        self.icons_micro = self.ip.get_micro_mute_icon() if ntsend_icon else None
        self.icons_vol_mute = self.ip.get_volume_mute_icon() if ntsend_icon else None

    async def add_volume(self, status: str):
        status = "-" if status == "-" else ""
        delta = (
            -int(self.conf.get_option("turn_sub"))
            if status == "-"
            else int(self.conf.get_option("turn_add"))
        )

        if self.conf.get_option("turn_smooth"):
            st_instance = self.st(
                delay=float(self.conf.get_option("turn_delay")),
                stop_step=abs(delta),
                function_st=lambda: (
                    self.ntsend(
                        icon=self.icons_vol,
                        message=self.conf.get_option("redner_volume").format(
                            volume=self.vol.just_add(1 if delta > 0 else -1)
                        ),
                        timeout=int(self.conf.get_option("notify_timeout")),
                        id=int(self.conf.get_option("notify_id")),
                        progress=bool(self.conf.get_option("notify_progress_bar")),
                        progress_value=self.vol.get_volume(),
                    ).send(),
                    self.sound.sound_start_handler(self.vol.get_volume()),
                    self.sound.sound_end_handler(self.vol.get_volume()),
                ),
            )
            await st_instance.run()
        else:
            new_volume = self.vol.just_add(delta)

            self.ntsend(
                icon=self.icons_vol,
                message=self.conf.get_option("redner_volume").format(volume=new_volume),
                timeout=int(self.conf.get_option("notify_timeout")),
                id=int(self.conf.get_option("notify_id")),
                progress=bool(self.conf.get_option("notify_progress_bar")),
                progress_value=new_volume,
            ).send()
            self.sound.sound_start_handler(self.vol.get_volume())
            self.sound.sound_end_handler(self.vol.get_volume())

    def toggle_micro(self):
        self.vol.toggle_micro_mute()
        state_micro_messagge = (
            self.conf.get_option("microphone_unmute")
            if not self.vol.is_micro_muted()
            else self.conf.get_option("microphone_mute")
        )
        self.ntsend(
            icon=self.icons_micro,
            message=state_micro_messagge,
            timeout=int(self.conf.get_option("notify_timeout")),
            id=int(self.conf.get_option("notify_id")),
        ).send()

    def toggle_volume(self):
        new_state = self.vol.toggle_volume_mute()
        current_volume = self.vol.get_volume()
        icon = (
            self.ip.get_volume_mute_icon() if new_state else self.ip.get_volume_icon()
        )

        message = (
            self.conf.get_option("volume_mute")
            if new_state
            else self.conf.get_option("redner_volume").format(volume=current_volume)
        )

        self.ntsend(
            message=message or "",
            icon=icon,
            timeout=int(self.conf.get_option("notify_timeout")),
            id=int(self.conf.get_option("notify_id")),
            progress=(
                bool(self.conf.get_option("notify_progress_bar"))
                if not self.vol.is_volume_muted()
                else None
            ),
            progress_value=(current_volume if not self.vol.is_volume_muted() else None),
        ).send()
