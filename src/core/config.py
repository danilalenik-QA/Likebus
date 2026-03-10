from __future__ import annotations

import os
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, Optional

import yaml
from dotenv import load_dotenv


@dataclass(frozen=True)
class Timeouts:
    action_ms: int = 8000
    navigation_ms: int = 30000


@dataclass(frozen=True)
class PlaywrightSettings:
    headless: bool = True
    slow_mo_ms: int = 0


@dataclass(frozen=True)
class AppConfig:
    env_name: str
    base_url: str
    locale: str = "uk"
    timeouts: Timeouts = Timeouts()
    playwright: PlaywrightSettings = PlaywrightSettings()


ALIASES = {
    "like99": "dev",
    "99": "dev",
}


def _str_to_bool(val: Optional[str], default: bool) -> bool:
    if val is None:
        return default
    v = val.strip().lower()
    if v in {"1", "true", "yes", "y", "on"}:
        return True
    if v in {"0", "false", "no", "n", "off"}:
        return False
    return default


def _project_root() -> Path:
    # .../src/core/config.py -> project root = 3 levels up
    return Path(__file__).resolve().parents[2]


def _load_yaml(path: Path) -> Dict[str, Any]:
    if not path.exists():
        raise FileNotFoundError(f"Env config not found: {path}")
    with path.open("r", encoding="utf-8") as f:
        data = yaml.safe_load(f) or {}
    if not isinstance(data, dict):
        raise ValueError(f"Invalid YAML structure in {path}, expected dict at root")
    return data


def load_config() -> AppConfig:
    # 1) load .env if present (local dev). In CI it can be absent.
    load_dotenv(dotenv_path=_project_root() / ".env", override=False)

    # 2) resolve env name with aliases
    env_name_raw = os.getenv("ENV_NAME", "dev").strip()
    env_name = ALIASES.get(env_name_raw, env_name_raw)

    # 3) read yaml for that env
    env_path = _project_root() / "configs" / "env" / f"{env_name}.yaml"
    y = _load_yaml(env_path)

    # required
    base_url = str(y.get("base_url", "")).strip()
    if not base_url:
        raise ValueError(f"`base_url` is required in {env_path}")

    # optional
    locale = str(y.get("locale", "uk")).strip() or "uk"

    # timeouts
    t = y.get("timeouts", {}) or {}
    action_ms = int(t.get("action_ms", 8000))
    navigation_ms = int(t.get("navigation_ms", 30000))

    # playwright settings (yaml defaults)
    p = y.get("playwright", {}) or {}
    headless_yaml = bool(p.get("headless", True))
    slow_mo_yaml = int(p.get("slow_mo_ms", 0))

    # env overrides (highest priority)
    headless_env = _str_to_bool(os.getenv("HEADLESS"), headless_yaml)
    slow_mo_env = int(os.getenv("SLOW_MO_MS", str(slow_mo_yaml)))

    return AppConfig(
        env_name=env_name_raw,  # keep original value user typed (dev/like99/99)
        base_url=base_url,
        locale=locale,
        timeouts=Timeouts(action_ms=action_ms, navigation_ms=navigation_ms),
        playwright=PlaywrightSettings(headless=headless_env, slow_mo_ms=slow_mo_env),
    )