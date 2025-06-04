import re
import json

from dataclasses import dataclass
from pathlib import Path


@dataclass
class JsonManagerArgs:
    path: Path


class JsonManager(JsonManagerArgs):
    def __init__(self, path: Path):
        super().__init__(path)

    def read(self) -> dict:
        with open(self.path, "r") as f:
            jsonc_content = f.read()
            jsonc_content = re.sub(r"//.*", "", jsonc_content)
            jsonc_content = re.sub(r",\s*(]|})", r"\1", jsonc_content)
            data = json.loads(jsonc_content)
            return data

    def write(self, data: dict, indent: int) -> None:
        with open(self.path, "w") as f:
            json.dump(data, f, indent=indent)

    def get_data(self) -> dict:
        if self.path.exists():
            return self.read()
        return {}

    def update_json(self, data: dict) -> None:
        existing = self.get_data()
        existing.update(data)
        self.write(existing, 2)
