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