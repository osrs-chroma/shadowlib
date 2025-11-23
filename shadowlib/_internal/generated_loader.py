"""
Dynamic loader for generated files from cache.

This module handles importing generated code from ~/.cache/shadowlib/generated/
by adding it to sys.path and providing lazy-loading utilities.
"""

import sys
from pathlib import Path
from typing import Any


def ensureGeneratedInPath() -> Path:
    """
    Ensure the generated cache directory is in sys.path for imports.

    Returns:
        Path to the generated directory
    """
    from .cache_manager import getCacheManager

    cache_manager = getCacheManager()
    generated_dir = cache_manager.generated_dir

    # Add to sys.path if not already there
    generated_str = str(generated_dir)
    if generated_str not in sys.path:
        sys.path.insert(0, generated_str)

    return generated_dir


def loadGeneratedModule(module_name: str) -> Any | None:
    """
    Load a generated module from cache.

    Args:
        module_name: Name of the module (e.g., 'query_proxies', 'constants')

    Returns:
        The loaded module, or None if it doesn't exist

    Example:
        >>> proxies = loadGeneratedModule('query_proxies')
        >>> if proxies:
        >>>     client = proxies.ClientProxy()
    """
    ensureGeneratedInPath()

    try:
        # Try to import the module
        import importlib

        return importlib.import_module(module_name)
    except ImportError:
        return None


def reloadGeneratedModule(module_name: str) -> Any | None:
    """
    Reload a generated module (useful after regeneration).

    Args:
        module_name: Name of the module (e.g., 'query_proxies', 'constants')

    Returns:
        The reloaded module, or None if it doesn't exist
    """
    ensureGeneratedInPath()

    try:
        import importlib

        if module_name in sys.modules:
            return importlib.reload(sys.modules[module_name])
        else:
            return importlib.import_module(module_name)
    except ImportError:
        return None


def hasGeneratedFiles() -> bool:
    """
    Check if generated files exist in cache.

    Returns:
        True if query_proxies.py and constants.py exist
    """
    from .cache_manager import getCacheManager

    cache_manager = getCacheManager()
    generated_dir = cache_manager.generated_dir

    proxy_file = generated_dir / "query_proxies.py"
    constants_file = generated_dir / "constants.py"

    return proxy_file.exists() and constants_file.exists()


def ensureGeneratedFiles():
    """
    Ensure generated files exist, triggering update if necessary.

    This should be called before importing generated modules.
    Raises FileNotFoundError if files can't be generated.
    """
    if not hasGeneratedFiles():
        print("⚠️  Generated files not found in cache, running updater...")
        try:
            from .updater.api import RuneLiteAPIUpdater

            updater = RuneLiteAPIUpdater()
            success = updater.update(force=False, max_age_days=7)

            if not success or not hasGeneratedFiles():
                raise FileNotFoundError(
                    "Failed to generate required files. "
                    "Run 'python -m shadowlib._internal.updater --force' manually."
                )
        except Exception as e:
            raise FileNotFoundError(
                f"Could not generate required files: {e}\n"
                f"Run 'python -m shadowlib._internal.updater --force' manually."
            ) from e


# Initialize on import - ensure generated path is available
ensureGeneratedInPath()
