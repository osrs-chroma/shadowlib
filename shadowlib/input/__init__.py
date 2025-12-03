"""OS-level input handling - mouse and keyboard."""

from shadowlib.input.keyboard import Keyboard
from shadowlib.input.mouse import Mouse
from shadowlib.input.runelite import RuneLite


class Input:
    """Namespace for input controls with lazy-loading."""

    def __init__(self, client):
        """
        Initialize input namespace.

        Args:
            client: The Client instance
        """
        self._client = client
        self._runelite: RuneLite | None = None
        self._mouse: Mouse | None = None
        self._keyboard: Keyboard | None = None

    @property
    def runelite(self) -> RuneLite:
        """Get RuneLite window manager."""
        if self._runelite is None:
            self._runelite = RuneLite()
        return self._runelite

    @property
    def mouse(self) -> Mouse:
        """Get mouse controller."""
        if self._mouse is None:
            self._mouse = Mouse(runelite=self.runelite)
        return self._mouse

    @property
    def keyboard(self) -> Keyboard:
        """Get keyboard controller."""
        if self._keyboard is None:
            self._keyboard = Keyboard(runelite=self.runelite)
        return self._keyboard


__all__ = ["Input", "Keyboard", "Mouse", "RuneLite"]
