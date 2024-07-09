"""Switch platform for Unifi Access integration."""
from homeassistant.components.switch import SwitchEntity
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from .hub import UnifiAccessHub
from .const import DOMAIN

async def async_setup_entry(
    hass: HomeAssistant, 
    entry: ConfigEntry, 
    async_add_entities: AddEntitiesCallback
) -> None:
    """Set up the Unifi Access switches."""
    hub: UnifiAccessHub = hass.data[DOMAIN][entry.entry_id]
    switches = hub.get_switches()  # Assumes your hub has a method to get switches
    if switches is None or not switches:
        # Add a virtual switch if no switches are available
        switches = [VirtualSwitch("Virtual Switch")]

    async_add_entities([UnifiAccessSwitch(hub, switch) for switch in switches], True)

class UnifiAccessSwitch(SwitchEntity):
    """Representation of a Unifi Access switch."""

    def __init__(self, hub: UnifiAccessHub, switch) -> None:
        """Initialize the switch."""
        self._hub = hub
        self._switch = switch
        self._attr_name = switch.name
        self._attr_is_on = switch.is_on

    async def async_turn_on(self, **kwargs) -> None:
        """Turn on the switch."""
        await self._hub.turn_on_switch(self._switch.id)
        self._attr_is_on = True
        self.async_write_ha_state()

    async def async_turn_off(self, **kwargs) -> None:
        """Turn off the switch."""
        await self._hub.turn_off_switch(self._switch.id)
        self._attr_is_on = False
        self.async_write_ha_state()

class VirtualSwitch:
    """Representation of a virtual switch."""

    def __init__(self, name: str) -> None:
        self._name = name
        self._is_on = False
        self._id = "virtual_switch"

    @property
    def name(self) -> str:
        """Return the name of the switch."""
        return self._name

    @property
    def is_on(self) -> bool:
        """Return true if switch is on."""
        return self._is_on

    @property
    def id(self) -> str:
        """Return the ID of the switch."""
        return self._id

    def turn_on(self) -> None:
        """Turn the switch on."""
        self._is_on = True

    def turn_off(self) -> None:
        """Turn the switch off."""
        self._is_on = False
