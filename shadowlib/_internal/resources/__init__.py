"""
OSRS Game Resources System

Manages downloadable game data (varps, objects, NPCs, items, etc.)
with automatic version checking and updates.

All game data is now managed by a single GameDataResource for atomic updates.
Legacy VarpsResource and ObjectsResource are kept for backward compatibility.

Example:
    from shadowlib._internal.resources import getGameData

    # Get unified resource (recommended)
    game_data = getGameData()
    quest_points = game_data.getVarpByName("quest_points")
    lumbridge_castle = game_data.getById(12345)

    # Or use legacy APIs (backward compatible)
    from shadowlib._internal.resources import getVarps, getObjects
    varps = getVarps()
    objects = getObjects()
"""

from .game_data import GameDataResource

# Keep old imports for backward compatibility (deprecated)
from .objects import ObjectsResource
from .varps import VarpsResource

# Global singleton instance
_game_data_instance = None


def getGameData() -> GameDataResource:
    """
    Get the unified game data resource manager.

    This is the recommended way to access game data.
    Downloads all data atomically to prevent version mismatches.
    """
    global _game_data_instance
    if _game_data_instance is None:
        _game_data_instance = GameDataResource()
    return _game_data_instance


# Backward compatibility: wrap GameDataResource for legacy code
def getVarps() -> GameDataResource:
    """
    Get varps resource (legacy API, wraps GameDataResource).

    Deprecated: Use getGameData() instead.
    """
    return getGameData()


def getObjects() -> GameDataResource:
    """
    Get objects resource (legacy API, wraps GameDataResource).

    Deprecated: Use getGameData() instead.
    """
    return getGameData()


# Convenience: expose resource instance directly
game_data = getGameData()

# Legacy convenience (backward compatible)
varps = game_data
objects = game_data

__all__ = [
    "game_data",
    "varps",
    "objects",
    "getGameData",
    "getVarps",
    "getObjects",
    "GameDataResource",
    "VarpsResource",  # Kept for type hints
    "ObjectsResource",  # Kept for type hints
]
