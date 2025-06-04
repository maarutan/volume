import re
from subprocess import CalledProcessError, run, check_output


class Volume:
    def get_volume(self) -> int:
        result = run(
            ["pactl", "get-sink-volume", "@DEFAULT_SINK@"],
            capture_output=True,
            text=True,
            check=True,
        ).stdout
        match = re.search(r"(\d+)%", result)
        return int(match.group(1)) if match else 0

        # def get_volume(self) -> int:
        #     result = run(
        #         "pactl get-sink-volume @DEFAULT_SINK@ | grep -oP '\\d+%' | head -n 1 | tr -d '%'",
        #         shell=True,
        #         capture_output=True,
        #         text=True,
        #         check=True,
        #     ).stdout.strip()
        # return int(result) if result.isdigit() else 0

    def just_add(self, delta: int):
        current_volume = self.get_volume()
        new_volume = max(0, min(100, current_volume + delta))

        run(["pactl", "set-sink-mute", "@DEFAULT_SINK@", "0"])
        run(["pactl", "set-sink-volume", "@DEFAULT_SINK@", f"{new_volume}%"])
        return new_volume

    def is_micro_muted(self) -> bool:
        try:
            output = run(
                ["pactl", "get-source-mute", "@DEFAULT_SOURCE@"],
                capture_output=True,
                text=True,
                check=True,
            ).stdout.lower()
            return "yes" in output
        except CalledProcessError as e:
            print(f"[ERROR] pactl failed: {e}")
        except Exception as e:
            print(f"[EXCEPTION] Unexpected error in is_micro_muted: {e}")
        return False

    def micro_mute(self, is_mute: bool) -> None:
        try:
            run(
                ["pactl", "set-source-mute", "@DEFAULT_SOURCE@", str(int(is_mute))],
                check=True,
            )
        except CalledProcessError as e:
            print(f"[ERROR] Failed to set mic mute: {e}")

    def toggle_micro_mute(self) -> bool:
        new_state = not self.is_micro_muted()
        self.micro_mute(new_state)
        return new_state

    def is_volume_muted(self):
        try:
            output = run(
                ["pactl", "get-sink-mute", "@DEFAULT_SINK@"],
                capture_output=True,
                text=True,
                check=True,
            ).stdout.lower()
            return "yes" in output
        except Exception:
            return False

    def volume_mute(self, is_mute: bool):
        run(["pactl", "set-sink-mute", "@DEFAULT_SINK@", str(int(is_mute))])

    def toggle_volume_mute(self) -> bool:
        current = self.is_volume_muted()
        self.volume_mute(not current)
        return not current


Vol = Volume()
# print(Vol.get_volume())
