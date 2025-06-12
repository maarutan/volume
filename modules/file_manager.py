from pathlib import Path
from shutil import rmtree


class FileManager:
    def __init__(self, path: Path) -> None:
        self.path = path

    def write(self, data):
        try:
            with open(self.path, "w") as f:
                f.write(data)
        except Exception as e:
            print(f"FIleManager: {e}")

    def read(self) -> str:
        try:
            with open(self.path, "r") as f:
                return f.read()
        except Exception as e:
            print(f"FIleManager: {e}")
            return ""

    def append(self, data):
        try:
            with open(self.path, "a") as f:
                f.write(data)
        except Exception as e:
            print(f"FIleManager: {e}")

    def is_file(self) -> bool:
        try:
            return self.path.is_file()
        except Exception as e:
            print(f"FIleManager: {e}")
            return False

    def is_dir(self) -> bool:
        try:
            return self.path.is_dir()
        except Exception as e:
            print(f"FIleManager: {e}")
            return False

    def delete(self) -> None:
        try:
            is_file = self.is_file()
            is_dir = self.is_dir()

            if is_file:
                self.path.unlink()
            elif is_dir:
                rmtree(self.path)
        except Exception as e:
            print(f"FIleManager: {e}")

    def is_exists(self) -> bool:
        try:
            return self.path.exists()
        except Exception as e:
            print(f"FIleManager: {e}")
            return False

    def create_if_not_exists(self) -> None:
        try:
            if self.path.suffix:
                if not self.is_exists():
                    self.path.parent.mkdir(exist_ok=True, parents=True)
                    self.path.touch(exist_ok=True)
            else:
                if not self.is_exists():
                    self.path.mkdir(parents=True, exist_ok=True)
        except Exception as e:
            print(f"FIleManager: {e}")
            return
