"""
Unified Game Data resource manager.

Handles downloading and querying all OSRS game data (varps, varbits, objects)
from a single source with atomic updates.
"""

import json
import sqlite3
from pathlib import Path
from typing import Any, Dict, List, Tuple

from ..utils.packed_position import packPositionSigned, unpackPosition
from .base import BaseResource


class GameDataResource(BaseResource):
    """
    Manages all OSRS game data with automatic version checking and updates.

    Combines varps, varbits, and objects into a single atomic resource
    to prevent version mismatches and duplicate downloads.
    """

    def __init__(self):
        super().__init__("game_data")

        # Override base URL - data is actually stored in varps directory
        from .base import BASE_URL

        self.base_url = f"{BASE_URL}/varps/latest"

        # Migrate old cache structure if needed
        self._migrateOldCache()

        # Varps/varbits data
        self._varps_data = None
        self._varbits_data = None

        # Objects database
        self._db_connection = None

    def _migrateOldCache(self):
        """
        Migrate files from old cache structure to new unified structure.

        Old structure:
          ~/.cache/shadowlib/data/varps/  (metadata.json, varps.json, varbits.json)
          ~/.cache/shadowlib/data/objects/  (objects.db)

        New structure:
          ~/.cache/shadowlib/data/game_data/  (all files together)
        """
        import shutil

        cache_base = Path.home() / ".cache" / "shadowlib" / "data"
        old_varps_dir = cache_base / "varps"
        old_objects_dir = cache_base / "objects"
        new_dir = cache_base / "game_data"

        # Check if migration needed
        if not (old_varps_dir.exists() or old_objects_dir.exists()):
            return  # Nothing to migrate

        if new_dir.exists() and list(new_dir.glob("*")):
            return  # New structure already populated

        print("🔄 Migrating cache to new structure...")
        new_dir.mkdir(parents=True, exist_ok=True)

        # Migrate from varps directory
        if old_varps_dir.exists():
            for file in ["metadata.json", "varps.json", "varbits.json"]:
                old_file = old_varps_dir / file
                if old_file.exists():
                    shutil.copy2(old_file, new_dir / file)
                    print(f"  ✅ Migrated {file}")

        # Migrate from objects directory
        if old_objects_dir.exists():
            old_db = old_objects_dir / "objects.db"
            if old_db.exists():
                shutil.copy2(old_db, new_dir / "objects.db")
                print("  ✅ Migrated objects.db")

        # Remove old directories
        if old_varps_dir.exists():
            shutil.rmtree(old_varps_dir)
            print("  🗑️  Removed old varps directory")

        if old_objects_dir.exists():
            shutil.rmtree(old_objects_dir)
            print("  🗑️  Removed old objects directory")

        print("✅ Cache migration complete!")

    def getRemoteFiles(self) -> Dict[str, str]:
        """Specify which files to download."""
        return {
            "varps.json": "varps.json",
            "varbits.json": "varbits.json",
            "objects.db": "objects.db.gz",  # Will be decompressed automatically
            "metadata.json": "metadata.json",
        }

    def _loadDataFiles(self):
        """Load all game data files."""
        try:
            # Load varps
            varps_file = self.cache_dir / "varps.json"
            if varps_file.exists():
                with open(varps_file) as f:
                    raw_varps = json.load(f)
                # Convert list to dict indexed by ID
                if isinstance(raw_varps, list):
                    self._varps_data = {item["id"]: item for item in raw_varps if "id" in item}
                else:
                    self._varps_data = raw_varps
                print(f"✅ Loaded {len(self._varps_data)} varps")

            # Load varbits
            varbits_file = self.cache_dir / "varbits.json"
            if varbits_file.exists():
                with open(varbits_file) as f:
                    raw_varbits = json.load(f)
                # Convert list to dict indexed by ID
                if isinstance(raw_varbits, list):
                    self._varbits_data = {item["id"]: item for item in raw_varbits if "id" in item}
                else:
                    self._varbits_data = raw_varbits
                print(f"✅ Loaded {len(self._varbits_data)} varbits")

            # Load objects database
            db_file = self.cache_dir / "objects.db"
            if db_file.exists():
                # Close existing connection if any
                if self._db_connection:
                    self._db_connection.close()

                # Open new connection
                self._db_connection = sqlite3.connect(str(db_file))
                self._db_connection.row_factory = sqlite3.Row  # Enable column access by name
                print("✅ Loaded objects database")

        except Exception as e:
            print(f"❌ Failed to load game data: {e}")
            raise

    # ===== Varps/Varbits Methods =====

    def getVarpValue(self, varp_id: int) -> int | None:
        """
        Get the current value of a varp from the event cache.

        Uses cached varp values (updated from varbit_changed events)
        instead of direct API queries for better performance.

        Args:
            varp_id: The varp ID to read

        Returns:
            The 32-bit integer value, or None if not available
        """
        try:
            # Get from event cache instead of direct query
            from shadowlib.globals import getClient

            client = getClient()
            if hasattr(client, "event_cache"):
                return client.event_cache.getVarp(varp_id)
            return None
        except Exception:
            return None

    def extractBits(self, value: int, start_bit: int, end_bit: int) -> int:
        """
        Extract bits from a value (for varbits).

        Args:
            value: The 32-bit value to extract from
            start_bit: Starting bit position (0-31)
            end_bit: Ending bit position (0-31)

        Returns:
            Extracted bits as integer
        """
        # Create mask: ((1 << (end_bit - start_bit + 1)) - 1)
        num_bits = end_bit - start_bit + 1
        mask = (1 << num_bits) - 1
        # Shift right by start_bit and apply mask
        return (value >> start_bit) & mask

    def getVarbitInfo(self, varbit_id: int) -> Dict[str, Any] | None:
        """
        Get varbit definition including which varp it maps to.

        Args:
            varbit_id: The varbit ID

        Returns:
            Dict with keys: id, name, varp_id, start_bit, end_bit
        """
        self.ensureLoaded()
        if self._varbits_data:
            return self._varbits_data.get(varbit_id)
        return None

    def getVarpByName(self, name: str) -> int | None:
        """
        Look up varp ID by name.

        Args:
            name: Varp name (case-sensitive)

        Returns:
            Varp ID or None if not found
        """
        self.ensureLoaded()
        if not self._varps_data:
            return None

        for varp_id, varp_info in self._varps_data.items():
            if varp_info.get("name") == name:
                return varp_id
        return None

    def getVarpByIndex(self, varp_id: int) -> int | None:
        """
        Get current value of a varp by its ID.

        Args:
            varp_id: The varp ID

        Returns:
            Current varp value or None
        """
        return self.getVarpValue(varp_id)

    def getVarbitByIndex(self, varbit_id: int) -> int | None:
        """
        Get current value of a varbit by extracting from its varp.

        Args:
            varbit_id: The varbit ID

        Returns:
            Current varbit value or None
        """
        varbit_info = self.getVarbitInfo(varbit_id)
        if not varbit_info:
            return None

        varp_value = self.getVarpValue(varbit_info["varp_id"])
        if varp_value is None:
            return None

        return self.extractBits(varp_value, varbit_info["start_bit"], varbit_info["end_bit"])

    def getVarbitByName(self, name: str) -> int | None:
        """
        Look up varbit value by name.

        Args:
            name: Varbit name (case-sensitive)

        Returns:
            Current varbit value or None if not found
        """
        self.ensureLoaded()
        if not self._varbits_data:
            return None

        for varbit_id, varbit_info in self._varbits_data.items():
            if varbit_info.get("name") == name:
                return self.getVarbitByIndex(varbit_id)
        return None

    def listVarps(self, filter_name: str | None = None) -> Dict[int, Dict[str, Any]]:
        """
        List all varps, optionally filtered by name substring.

        Args:
            filter_name: Optional substring to filter by name

        Returns:
            Dict mapping varp_id -> varp_info
        """
        self.ensureLoaded()
        if not self._varps_data:
            return {}

        if filter_name is None:
            return self._varps_data

        return {
            varp_id: info
            for varp_id, info in self._varps_data.items()
            if filter_name.lower() in info.get("name", "").lower()
        }

    def listVarbits(self, filter_name: str | None = None) -> Dict[int, Dict[str, Any]]:
        """
        List all varbits, optionally filtered by name substring.

        Args:
            filter_name: Optional substring to filter by name

        Returns:
            Dict mapping varbit_id -> varbit_info
        """
        self.ensureLoaded()
        if not self._varbits_data:
            return {}

        if filter_name is None:
            return self._varbits_data

        return {
            varbit_id: info
            for varbit_id, info in self._varbits_data.items()
            if filter_name.lower() in info.get("name", "").lower()
        }

    # ===== Objects Methods =====

    def _ensureConnection(self):
        """Ensure database is loaded and connected."""
        if self._db_connection is None:
            self.ensureLoaded()

    def getById(self, object_id: int) -> Dict[str, Any] | None:
        """
        Get object definition by ID.

        Args:
            object_id: The object ID

        Returns:
            Dict with object properties or None if not found
        """
        self._ensureConnection()
        cursor = self._db_connection.execute("SELECT * FROM objects WHERE id = ?", (object_id,))
        row = cursor.fetchone()
        return dict(row) if row else None

    def getByName(self, name: str, exact: bool = False) -> List[Dict[str, Any]]:
        """
        Search objects by name.

        Args:
            name: Object name to search for
            exact: If True, match exactly; if False, match substring (case-insensitive)

        Returns:
            List of matching object dicts
        """
        self._ensureConnection()
        if exact:
            query = "SELECT * FROM objects WHERE name = ? COLLATE NOCASE"
            params = (name,)
        else:
            query = "SELECT * FROM objects WHERE name LIKE ? COLLATE NOCASE"
            params = (f"%{name}%",)

        cursor = self._db_connection.execute(query, params)
        return [dict(row) for row in cursor.fetchall()]

    def getLocations(self, object_id: int) -> List[Tuple[int, int, int]]:
        """
        Get all locations where an object spawns.

        Args:
            object_id: The object ID

        Returns:
            List of (x, y, plane) tuples
        """
        self._ensureConnection()
        cursor = self._db_connection.execute(
            "SELECT packed_position FROM object_locations WHERE object_id = ?", (object_id,)
        )
        return [unpackPosition(row[0]) for row in cursor.fetchall()]

    def getNearby(self, x: int, y: int, plane: int = 0, radius: int = 10) -> List[Dict[str, Any]]:
        """
        Find all objects within radius of a position.

        Args:
            x: X coordinate (world coordinate)
            y: Y coordinate (world coordinate)
            plane: Plane (0-3)
            radius: Search radius in tiles

        Returns:
            List of dicts with object data + location
        """
        self._ensureConnection()

        # Calculate bounding box
        min_x, max_x = x - radius, x + radius
        min_y, max_y = y - radius, y + radius

        # Pack corners
        min_packed = packPositionSigned(min_x, min_y, plane)
        max_packed = packPositionSigned(max_x, max_y, plane)

        query = """
            SELECT o.*, l.packed_position
            FROM object_locations l
            JOIN objects o ON l.object_id = o.id
            WHERE l.packed_position >= ? AND l.packed_position <= ?
        """

        cursor = self._db_connection.execute(query, (min_packed, max_packed))
        results = []

        for row in cursor.fetchall():
            obj_dict = dict(row)
            # Unpack position for result
            ox, oy, op = unpackPosition(obj_dict["packed_position"])

            # Distance check (since packed position is approximate)
            if abs(ox - x) <= radius and abs(oy - y) <= radius and op == plane:
                obj_dict["x"] = ox
                obj_dict["y"] = oy
                obj_dict["plane"] = op
                results.append(obj_dict)

        return results

    def searchByAction(self, action: str) -> List[Dict[str, Any]]:
        """
        Find all objects with a specific action.

        Args:
            action: Action name to search for (e.g., "Mine", "Chop")

        Returns:
            List of object dicts
        """
        self._ensureConnection()

        # Actions stored as JSON array, need to search within
        query = """
            SELECT * FROM objects
            WHERE actions LIKE ?
        """

        cursor = self._db_connection.execute(query, (f'%"{action}"%',))
        return [dict(row) for row in cursor.fetchall()]

    def countObjects(self) -> int:
        """Get total number of objects in database."""
        self._ensureConnection()
        cursor = self._db_connection.execute("SELECT COUNT(*) FROM objects")
        return cursor.fetchone()[0]

    def countLocations(self) -> int:
        """Get total number of object spawn locations."""
        self._ensureConnection()
        cursor = self._db_connection.execute("SELECT COUNT(*) FROM object_locations")
        return cursor.fetchone()[0]

    def executeQuery(self, query: str, params: tuple = ()) -> List[Dict[str, Any]]:
        """
        Execute a custom SQL query on the objects database.

        Args:
            query: SQL query string
            params: Query parameters

        Returns:
            List of result dicts
        """
        self._ensureConnection()
        cursor = self._db_connection.execute(query, params)
        return [dict(row) for row in cursor.fetchall()]

    def close(self):
        """Close database connection."""
        if self._db_connection:
            self._db_connection.close()
            self._db_connection = None

    def __del__(self):
        """Cleanup on deletion."""
        self.close()
