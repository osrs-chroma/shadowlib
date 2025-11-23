"""
Centralized cache management for ShadowLib.

Uses ~/.cache/shadowlib/ for all generated files and resources following XDG Base Directory specification.
"""

import os
from pathlib import Path


class CacheManager:
    """Manages cache directories for ShadowLib resources and generated files."""

    def __init__(self, base_path: Path | None = None):
        """
        Initialize cache manager.

        Args:
            base_path: Optional custom base path. If None, uses ~/.cache/shadowlib
        """
        if base_path is None:
            # Use XDG_CACHE_HOME if set, otherwise default to ~/.cache
            xdg_cache = os.getenv("XDG_CACHE_HOME")
            if xdg_cache:
                self.base_path = Path(xdg_cache) / "shadowlib"
            else:
                self.base_path = Path.home() / ".cache" / "shadowlib"
        else:
            self.base_path = Path(base_path)

        # Define standard cache directories
        self.generated_dir = self.base_path / "generated"
        self.data_dir = self.base_path / "data"
        self.objects_dir = self.data_dir / "objects"
        self.varps_dir = self.data_dir / "varps"

    def ensureDirs(self) -> None:
        """Create all cache directories if they don't exist."""
        self.generated_dir.mkdir(parents=True, exist_ok=True)
        self.objects_dir.mkdir(parents=True, exist_ok=True)
        self.varps_dir.mkdir(parents=True, exist_ok=True)

    def getGeneratedPath(self, filename: str) -> Path:
        """
        Get path for a generated file.

        Args:
            filename: Name of the generated file

        Returns:
            Full path to the file in ~/.cache/shadowlib/generated/
        """
        return self.generated_dir / filename

    def getObjectsPath(self) -> Path:
        """
        Get path for objects data directory.

        Returns:
            Path to ~/.cache/shadowlib/data/objects/
        """
        return self.objects_dir

    def getVarpsPath(self) -> Path:
        """
        Get path for varps data directory.

        Returns:
            Path to ~/.cache/shadowlib/data/varps/
        """
        return self.varps_dir

    def getDataPath(self, resource_type: str) -> Path:
        """
        Get path for a specific resource type.

        Args:
            resource_type: Type of resource (e.g., 'objects', 'varps')

        Returns:
            Path to the resource directory
        """
        return self.data_dir / resource_type

    def clearCache(self) -> None:
        """Clear all cached files (use with caution)."""
        import shutil

        if self.base_path.exists():
            shutil.rmtree(self.base_path)

    def getCacheSize(self) -> int:
        """
        Get total size of cache in bytes.

        Returns:
            Total cache size in bytes
        """
        total = 0
        if self.base_path.exists():
            for path in self.base_path.rglob("*"):
                if path.is_file():
                    total += path.stat().st_size
        return total


# Global cache manager instance
_cache_manager: CacheManager | None = None


def getCacheManager() -> CacheManager:
    """
    Get global cache manager instance.

    Returns:
        Global CacheManager instance
    """
    global _cache_manager
    if _cache_manager is None:
        _cache_manager = CacheManager()
        _cache_manager.ensureDirs()
    return _cache_manager
