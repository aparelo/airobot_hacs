from homeassistant.components.button import ButtonEntity
from airobot_api_client.models import ThermostatSettingsUpdateInput

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

from .entity_base import AirobotEntity
from .coordinator import AirobotCoordinator


async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities
):
    """Button setup."""
    coordinator: AirobotCoordinator = entry.runtime_data
    entities = []

    entities.append(AirobotReboot(coordinator, entry.title))
    entities.append(AirobotRecalibrateCO2(coordinator, entry.title))

    async_add_entities(entities, update_before_add=False)


class AirobotReboot(AirobotEntity, ButtonEntity):
    """Reboot button."""

    _attr_has_entity_name = True

    @property
    def unique_id(self):
        return f"{self.coordinator.settings.DEVICE_ID}_reboot"

    @property
    def translation_key(self):
        return "reboot_button"

    async def async_press(self) -> None:
        """Handle the button press."""
        inp = ThermostatSettingsUpdateInput(REBOOT=True)
        await self.coordinator.update_settings(inp)


class AirobotRecalibrateCO2(AirobotEntity, ButtonEntity):
    """Recalibrate CO2 button."""

    _attr_has_entity_name = True

    def __init__(self, coordinator, idx):
        """Initialize entity."""
        super().__init__(coordinator, idx)

    @property
    def unique_id(self):
        return f"{self.coordinator.settings.DEVICE_ID}_recalibrate_co2"

    @property
    def translation_key(self):
        return "recalibrate_button"

    async def async_press(self) -> None:
        """Handle the button press."""
        inp = ThermostatSettingsUpdateInput(RECALIBRATE_CO2=True)
        await self.coordinator.update_settings(inp)
