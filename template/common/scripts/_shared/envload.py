"""Read the project root .env (scripts/_shared — shared by every work folder, no external packages).
Environment variables that are already set take precedence over .env."""
import os
from pathlib import Path

ENV_PATH = Path(__file__).resolve().parent.parent.parent / ".env"


def load_env(path: Path = ENV_PATH) -> None:
    if not path.exists():
        return
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, val = line.split("=", 1)
        key, val = key.strip(), val.strip()
        if len(val) >= 2 and val[0] == val[-1] and val[0] in "'\"":
            val = val[1:-1]
        os.environ.setdefault(key, val)


def get(key: str, default: str = "") -> str:
    return os.environ.get(key, default)


load_env()
