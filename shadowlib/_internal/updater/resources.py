#!/usr/bin/env python3
"""
Resource Auto-Updater for Varps and Objects Database

Handles automatic version checking and updating of game resources
separately from RuneLite API updates.
"""

from pathlib import Path
from typing import Tuple


class ResourceUpdater:
    """
    Manages automatic updates for game resources (varps, objects, etc.)
    """

    def __init__(self, project_root: Path | None = None):
        """
        Initialize resource updater.

        Args:
            project_root: Project root directory (auto-detected if None)
        """
        if project_root is None:
            # Auto-detect: go up from this file
            # shadowlib/_internal/updater/resources.py -> need 4 .parent calls
            project_root = Path(__file__).parent.parent.parent.parent

        self.project_root = Path(project_root)
        self.resources_dir = self.project_root / "data" / "resources"

    def shouldUpdate(self) -> Tuple[bool, str]:
        """
        Check if game data needs update.

        Returns:
            Tuple of (should_update, reason)
        """
        from ..resources.game_data import GameDataResource

        try:
            game_data = GameDataResource()
            # Check if needs update (checks remote metadata)
            if game_data._needsUpdate():
                return True, "Game data update available"
            return False, "Game data up to date"
        except Exception as e:
            return True, f"Game data check failed: {e}"

    def updateAll(self, force: bool = False) -> bool:
        """
        Update all game data atomically.

        Downloads varps, varbits, and objects in one atomic operation
        to prevent version mismatches.

        Args:
            force: Force update even if up to date

        Returns:
            True if update successful
        """
        print("=" * 80)
        print("🔄 Game Data Auto-Updater")
        print("=" * 80)

        # Check if update needed BEFORE downloading
        if not force:
            needs_update, reason = self.shouldUpdate()
            if not needs_update:
                print(f"✅ {reason}")
                print("=" * 80)
                return True
            print(f"📦 {reason}")

        print("\n🔄 Updating game data...")

        try:
            from ..resources.game_data import GameDataResource

            game_data = GameDataResource()
            game_data.ensureLoaded(force_update=force)

            print("\n" + "=" * 80)
            print("✅ Game data updated successfully!")
            print("=" * 80)
            return True

        except Exception as e:
            print(f"\n❌ Game data update failed: {e}")
            import traceback

            traceback.print_exc()
            print("\n" + "=" * 80)
            print("❌ Update failed")
            print("=" * 80)
            return False

    def status(self):
        """Print current game data status."""
        print("=" * 80)
        print("📊 Game Data Status")
        print("=" * 80)

        needs_update, reason = self.shouldUpdate()
        if needs_update:
            print(f"\n⚠️  {reason}")
        else:
            print(f"\n✅ {reason}")

        print("\n" + "=" * 80)


def main():
    """Command-line interface for resource updater."""
    import argparse

    parser = argparse.ArgumentParser(
        description="Resource Auto-Updater",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Update all resources
  python -m shadowlib._internal.scraper.resource_updater

  # Force update
  python -m shadowlib._internal.scraper.resource_updater --force

  # Check status only
  python -m shadowlib._internal.scraper.resource_updater --status
""",
    )

    parser.add_argument(
        "--force", "-f", action="store_true", help="Force update even if up to date"
    )

    parser.add_argument(
        "--status", "-s", action="store_true", help="Show status only, do not update"
    )

    args = parser.parse_args()

    updater = ResourceUpdater()

    if args.status:
        updater.status()
    else:
        success = updater.updateAll(force=args.force)
        exit(0 if success else 1)


if __name__ == "__main__":
    main()
