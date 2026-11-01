import json
from pathlib import Path
from typing import Any


def get_json(path: Path) -> Any:
    content = path.read_text()
    return json.loads(content)
