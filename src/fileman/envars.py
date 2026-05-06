"""Cross-project environment loader: system env → global .env → project .env.

Use this module in any Python project to load secrets/configuration without
duplicating .env files across repositories.

Resolution order (highest priority wins):
    1. Already-set OS environment variables (e.g. from shell/User env)
    2. Global .env file in the user's home directory:  ~/.env
    3. Project-local .env file:  <project_root>/.env

python-dotenv is used with override=False so system env vars always take
precedence over file values.

Usage:
    from claude_babysitter.env_loader import load_env
    load_env()
    # Now os.environ["OLLAMA_API_KEY"] is available from whichever source.
"""

from __future__ import annotations

import os
from pathlib import Path

from dotenv import load_dotenv


# Ordered by priority (system env is already top, then these files)
_DEFAULT_ENV_SEARCH_ORDER = [
    "user_home",
    "project_local",
]


def _global_env_path() -> Path:
    """Return the standard global .env path: ~/.env"""
    return Path.home() / ".env"


def _find_project_root(start: Path | None = None) -> Path | None:
    """Walk up from *start* looking for a directory that contains a .env file.

    Falls back to the package root if nothing found.
    """
    if start is None:
        start = Path(__file__).resolve().parent

    for directory in [start, *start.parents]:
        candidate = directory / ".env"
        if candidate.is_file():
            return directory
    return None


def load_env(
    *,
    global_env: Path | None = None,
    project_env: Path | None = None,
    search_order: list[str] | None = None,
) -> list[Path]:
    """Load .env files into os.environ with system-env precedence.

    1. Already-set OS env vars are never overwritten.
    2. Loads files in *search_order*; later files do NOT override earlier ones
       because override=False.

    Args:
        global_env: Path to the global/shared .env file.  Defaults to ~/.env.
        project_env: Path to the project-local .env file.  Defaults to the
            closest .env found walking up from this module's directory.
        search_order: Which sources to try and in which order.  Each item is
            one of "user_home", "project_local".  Defaults to both in that
            order.

    Returns:
        A list of file paths that were actually loaded.
    """
    loaded: list[Path] = []

    if search_order is None:
        search_order = _DEFAULT_ENV_SEARCH_ORDER

    for source in search_order:
        if source == "user_home":
            env_path = global_env if global_env else _global_env_path()
            if env_path.is_file():
                load_dotenv(env_path, override=False)
                loaded.append(env_path)

        elif source == "project_local":
            if project_env is not None:
                env_path = project_env
                if env_path.is_file():
                    load_dotenv(env_path, override=False)
                    loaded.append(env_path)
            else:
                project_root = _find_project_root()
                if project_root is not None:
                    env_path = project_root / ".env"
                    if env_path.is_file():
                        load_dotenv(env_path, override=False)
                        loaded.append(env_path)

    return loaded
