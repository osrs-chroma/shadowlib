"""Game viewport entities - NPCs, objects, players, items visible in 3D world."""

from shadowlib.world.ground_items import GroundItems


class World:
    """Namespace for 3D world entities with lazy-loading."""

    def __init__(self, client):
        """
        Initialize world namespace.

        Args:
            client: The Client instance
        """
        self._client = client
        self._ground_items: GroundItems | None = None

    @property
    def ground_items(self) -> GroundItems:
        """Get ground items accessor."""
        if self._ground_items is None:
            self._ground_items = GroundItems(client=self._client)
        return self._ground_items


__all__ = ["World", "GroundItems"]
