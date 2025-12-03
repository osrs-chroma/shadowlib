"""Navigation module."""

from shadowlib.navigation.pathfinder import Pathfinder


class Navigation:
    """Namespace for navigation systems with lazy-loading."""

    def __init__(self, client):
        """
        Initialize navigation namespace.

        Args:
            client: The Client instance
        """
        self._client = client
        self._pathfinder: Pathfinder | None = None

    @property
    def pathfinder(self) -> Pathfinder:
        """Get pathfinder."""
        if self._pathfinder is None:
            self._pathfinder = Pathfinder(client=self._client)
        return self._pathfinder


__all__ = ["Navigation", "Pathfinder"]
