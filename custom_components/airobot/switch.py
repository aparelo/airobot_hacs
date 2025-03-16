from homeassistant.components.switch import SwitchEntity
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

    entities.append(AirobotActuatorExerciseDisable(coordinator, entry.title))
    entities.append(AirobotChildlock(coordinator, entry.title))

    async_add_entities(entities, update_before_add=False)


class AirobotActuatorExerciseDisable(AirobotEntity, SwitchEntity):
    """Disable actuator exercise functionality."""

    _attr_has_entity_name = True

    @property
    def unique_id(self):
        return f"{self.coordinator.settings.DEVICE_ID}_disable_actuator_exercise"

    @property
    def translation_key(self):
        return "disable_exercise"

    @property
    def is_on(self) -> bool:
        """Switch state."""
        return self.coordinator.settings.ACTUATOR_EXERCISE_DISABLED

    async def async_turn_on(self, **kwargs):
        """Turn the entity on."""
        inp = ThermostatSettingsUpdateInput(ACTUATOR_EXERCISE_DISABLED=True)
        await self.coordinator.update_settings(inp)

    async def async_turn_off(self, **kwargs):
        """Turn the entity off."""
        inp = ThermostatSettingsUpdateInput(ACTUATOR_EXERCISE_DISABLED=False)
        await self.coordinator.update_settings(inp)


class AirobotChildlock(AirobotEntity, SwitchEntity):
    """Disable actuator exercise functionality."""

    _attr_has_entity_name = True

    @property
    def unique_id(self):
        return f"{self.coordinator.settings.DEVICE_ID}_child_lock"

    @property
    def translation_key(self):
        return "child_lock"

    @property
    def is_on(self) -> bool:
        """Switch state."""
        return self.coordinator.settings.CHILDLOCK_ENABLED

    async def async_turn_on(self, **kwargs):
        """Turn the entity on."""
        inp = ThermostatSettingsUpdateInput(CHILDLOCK_ENABLED=True)
        await self.coordinator.update_settings(inp)

    async def async_turn_off(self, **kwargs):
        """Turn the entity off."""
        inp = ThermostatSettingsUpdateInput(CHILDLOCK_ENABLED=False)
        await self.coordinator.update_settings(inp)
