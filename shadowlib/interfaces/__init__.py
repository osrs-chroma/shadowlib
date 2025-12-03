"""Overlay windows - bank, GE, shop, dialogue, etc."""

from shadowlib.interfaces.bank import Bank


class Interfaces:
    """Namespace for overlay interfaces with lazy-loading."""

    def __init__(self, client):
        """
        Initialize interfaces namespace.

        Args:
            client: The Client instance
        """
        self._client = client
        self._bank: Bank | None = None

    @property
    def bank(self) -> Bank:
        """Get bank interface."""
        if self._bank is None:
            self._bank = Bank()
        return self._bank


__all__ = ["Interfaces", "Bank"]
