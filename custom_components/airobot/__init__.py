"""The Airobot thermostat integration."""

from __future__ import annotations

from airobot_api_client.async_api import AsyncAirobotAPI

from homeassistant.config_entries import ConfigEntry
from homeassistant.const import CONF_HOST, CONF_PASSWORD, CONF_USERNAME, Platform
from homeassistant.core import HomeAssistant

from .coordinator import AirobotCoordinator

_PLATFORMS: list[Platform] = [
    Platform.CLIMATE,
    Platform.SENSOR,
    Platform.BUTTON,
    Platform.SWITCH,
]


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Airobot thermostat from a config entry."""

    host = entry.data.get(
        CONF_HOST, f"http://Airobot-Thermostat-{entry.data[CONF_USERNAME]}.local"
    )
    username = entry.data[CONF_USERNAME]
    password = entry.data[CONF_PASSWORD]
    # store = Store(hass, STORAGE_VERSION, STORAGE_KEY)
    api_client = AsyncAirobotAPI(host, username, password)
    coordinator = AirobotCoordinator(hass, entry, api_client)

    if not await api_client.authenticate():
        return False

    entry.runtime_data = coordinator
    await coordinator.async_config_entry_first_refresh()

    await hass.config_entries.async_forward_entry_setups(entry, _PLATFORMS)

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    return await hass.config_entries.async_unload_platforms(entry, _PLATFORMS)
