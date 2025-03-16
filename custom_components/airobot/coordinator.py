from __future__ import annotations

from datetime import timedelta
import logging

from airobot_api_client.async_api import AsyncAirobotAPI
from airobot_api_client.models import (
    ThermostatSettings,
    ThermostatSettingsUpdateInput,
    ThermostatStatus,
)
import async_timeout

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator

_LOGGER = logging.getLogger(__name__)


class AirobotCoordinator(DataUpdateCoordinator):
    """My custom coordinator."""

    airobot_api: AsyncAirobotAPI
    settings: ThermostatSettings
    status: ThermostatStatus

    def __init__(
        self,
        hass: HomeAssistant,
        config_entry: ConfigEntry,
        my_api: AsyncAirobotAPI,
    ) -> None:
        """Initialize my coordinator."""
        super().__init__(
            hass,
            _LOGGER,
            # Name of the data. For logging purposes.
            name="Airobot",
            config_entry=config_entry,
            # Polling interval. Will only be polled if there are subscribers.
            update_interval=timedelta(seconds=30),
            # Set always_update to `False` if the data returned from the
            # api can be compared via `__eq__` to avoid duplicate updates
            # being dispatched to listeners
            always_update=True,
        )
        self.airobot_api = my_api
        self.settings = None
        self.status = None

    async def _async_setup(self):
        """Set up the coordinator.

        This is the place to set up your coordinator,
        or to load data, that only needs to be loaded once.

        This method will be called automatically during
        coordinator.async_config_entry_first_refresh.
        """
        self.settings = await self.airobot_api.get_settings()
        self.status = await self.airobot_api.get_status()

    async def _async_update_data(self):
        """Fetch data from API endpoint.

        This is the place to pre-process the data to lookup tables
        so entities can quickly look up their data.
        """
        # Note: asyncio.TimeoutError and aiohttp.ClientError are already
        # handled by the data update coordinator.
        async with async_timeout.timeout(20):
            self.settings = await self.airobot_api.get_settings()
            self.status = await self.airobot_api.get_status()

    async def update_settings(self, input: ThermostatSettingsUpdateInput):
        """Update thermostat settings."""
        await self.airobot_api.set_settings(input)

        new_settings = await self.airobot_api.get_settings()
        self.settings = new_settings
