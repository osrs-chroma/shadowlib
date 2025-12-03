"""
GameTabs package - contains all game tab modules for OSRS.

Each tab inherits from the base GameTabs class and provides
tab-specific functionality for the Old School RuneScape interface.
"""

from shadowlib.types.gametab import GameTab, GameTabs

from .account import Account
from .combat import Combat
from .emotes import Emotes
from .equipment import Equipment
from .friends import Friends
from .grouping import Grouping
from .inventory import Inventory
from .logout import Logout
from .magic import Magic
from .music import Music
from .prayer import Prayer
from .progress import Progress
from .settings import Settings
from .skills import Skills


class Tabs:
    """Namespace for game tabs with lazy-loading."""

    def __init__(self, client):
        """
        Initialize tabs namespace.

        Args:
            client: The Client instance
        """
        self._client = client
        self._combat: Combat | None = None
        self._skills: Skills | None = None
        self._progress: Progress | None = None
        self._inventory: Inventory | None = None
        self._equipment: Equipment | None = None
        self._prayer: Prayer | None = None
        self._magic: Magic | None = None
        self._grouping: Grouping | None = None
        self._friends: Friends | None = None
        self._account: Account | None = None
        self._settings: Settings | None = None
        self._logout: Logout | None = None
        self._emotes: Emotes | None = None
        self._music: Music | None = None

    @property
    def combat(self) -> Combat:
        """Get combat tab."""
        if self._combat is None:
            self._combat = Combat(client=self._client)
        return self._combat

    @property
    def skills(self) -> Skills:
        """Get skills tab."""
        if self._skills is None:
            self._skills = Skills(client=self._client)
        return self._skills

    @property
    def progress(self) -> Progress:
        """Get progress tab."""
        if self._progress is None:
            self._progress = Progress(client=self._client)
        return self._progress

    @property
    def inventory(self) -> Inventory:
        """Get inventory tab."""
        if self._inventory is None:
            self._inventory = Inventory(client=self._client)
        return self._inventory

    @property
    def equipment(self) -> Equipment:
        """Get equipment tab."""
        if self._equipment is None:
            self._equipment = Equipment(client=self._client)
        return self._equipment

    @property
    def prayer(self) -> Prayer:
        """Get prayer tab."""
        if self._prayer is None:
            self._prayer = Prayer(client=self._client)
        return self._prayer

    @property
    def magic(self) -> Magic:
        """Get magic tab."""
        if self._magic is None:
            self._magic = Magic(client=self._client)
        return self._magic

    @property
    def grouping(self) -> Grouping:
        """Get grouping tab."""
        if self._grouping is None:
            self._grouping = Grouping(client=self._client)
        return self._grouping

    @property
    def friends(self) -> Friends:
        """Get friends tab."""
        if self._friends is None:
            self._friends = Friends(client=self._client)
        return self._friends

    @property
    def account(self) -> Account:
        """Get account tab."""
        if self._account is None:
            self._account = Account(client=self._client)
        return self._account

    @property
    def settings(self) -> Settings:
        """Get settings tab."""
        if self._settings is None:
            self._settings = Settings(client=self._client)
        return self._settings

    @property
    def logout(self) -> Logout:
        """Get logout tab."""
        if self._logout is None:
            self._logout = Logout(client=self._client)
        return self._logout

    @property
    def emotes(self) -> Emotes:
        """Get emotes tab."""
        if self._emotes is None:
            self._emotes = Emotes(client=self._client)
        return self._emotes

    @property
    def music(self) -> Music:
        """Get music tab."""
        if self._music is None:
            self._music = Music(client=self._client)
        return self._music

    def getOpenTab(self) -> GameTab | None:
        """
        Get the currently open tab.

        Returns:
            The currently open GameTab, or None if unknown

        Example:
            >>> tab = client.tabs.getOpenTab()
            >>> if tab == GameTab.INVENTORY:
            ...     print("Inventory is open")
        """
        index = self._client.cache.getVarc(self._client.VarClientID.TOPLEVEL_PANEL)
        return GameTab(index) if index in GameTab._value2member_map_ else None


__all__ = [
    "GameTab",
    "GameTabs",
    "Tabs",
    "Combat",
    "Skills",
    "Progress",
    "Inventory",
    "Equipment",
    "Prayer",
    "Magic",
    "Grouping",
    "Friends",
    "Account",
    "Settings",
    "Logout",
    "Emotes",
    "Music",
]
