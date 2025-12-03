"""Interaction systems - menu, clicking, hovering, widgets."""

from shadowlib.interactions.menu import Menu


class Interactions:
    """Namespace for interaction systems with lazy-loading."""

    def __init__(self, client):
        """
        Initialize interactions namespace.

        Args:
            client: The Client instance
        """
        self._client = client
        self._menu: Menu | None = None

    @property
    def menu(self) -> Menu:
        """Get menu interaction handler."""
        if self._menu is None:
            self._menu = Menu()
        return self._menu


__all__ = ["Interactions", "Menu"]
