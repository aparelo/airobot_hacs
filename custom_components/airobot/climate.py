from airobot_api_client.models import ThermostatSettingsUpdateInput, WorkingMode

from homeassistant.components.climate import (
    ClimateEntity,
    ClimateEntityFeature,
    HVACAction,
    HVACMode,
    UnitOfTemperature,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import ATTR_TEMPERATURE
from homeassistant.core import HomeAssistant


from .entity_base import AirobotEntity


async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities
):
    """Thermostat entry."""
    coordinator = entry.runtime_data

    entity = AirobotThermostat(coordinator, entry.title)
    async_add_entities([entity], update_before_add=False)


class AirobotThermostat(AirobotEntity, ClimateEntity):
    """An entity using CoordinatorEntity."""

    _attr_has_entity_name = True

    @property
    def unique_id(self):
        return self.coordinator.settings.DEVICE_ID

    @property
    def translation_key(self):
        return "thermostat"

    @property
    def current_humidity(self) -> float | None:
        return self.coordinator.status.HUM_AIR

    @property
    def current_temperature(self) -> float | None:
        return self.coordinator.status.TEMP_AIR

    @property
    def hvac_action(self) -> HVACAction:
        heating_on = self.coordinator.status.HEATING_ON
        if heating_on:
            return HVACAction.HEATING
        return HVACAction.IDLE

    @property
    def hvac_mode(self) -> HVACMode:
        return HVACMode.HEAT

    @property
    def hvac_modes(self) -> list[HVACMode]:
        return [HVACMode.HEAT, HVACMode.OFF]

    @property
    def preset_mode(self) -> str:
        if self.coordinator.settings.BOOST_ENABLED:
            return "BOOST"
        preset = self.coordinator.settings.MODE
        return preset.name

    @property
    def preset_modes(self) -> list[str]:
        presets = WorkingMode._member_names_
        presets.append("BOOST")
        return presets

    @property
    def target_temperature(self) -> float | None:
        mode = self.coordinator.settings.MODE
        if mode is WorkingMode.HOME:
            return self.coordinator.settings.SETPOINT_TEMP
        else:
            return self.coordinator.settings.SETPOINT_TEMP_AWAY

    @property
    def target_temperature_step(self) -> float | None:
        return 0.1

    @property
    def temperature_unit(self) -> str:
        return UnitOfTemperature.CELSIUS

    @property
    def supported_features(self):
        return (
            ClimateEntityFeature.TARGET_TEMPERATURE | ClimateEntityFeature.PRESET_MODE
        )

    async def async_set_preset_mode(self, preset_mode: str):
        """Set new target preset mode."""
        if preset_mode == WorkingMode.HOME.name:
            inp = ThermostatSettingsUpdateInput(MODE=WorkingMode.HOME)
        elif preset_mode == WorkingMode.AWAY.name:
            inp = ThermostatSettingsUpdateInput(MODE=WorkingMode.AWAY)
        elif preset_mode == "BOOST":
            inp = ThermostatSettingsUpdateInput(BOOST_ENABLED=True)
        else:
            raise KeyError(f"Unknown preset_mode {preset_mode}")

        await self.coordinator.update_settings(inp)

    async def async_set_temperature(self, **kwargs):
        """Set new target temperature."""
        if kwargs.get(ATTR_TEMPERATURE) is None:
            return

        temp = kwargs.get(ATTR_TEMPERATURE)
        preset_mode = self.coordinator.settings.MODE

        if preset_mode == WorkingMode.HOME:
            inp = ThermostatSettingsUpdateInput(SETPOINT_TEMP=temp)
        else:
            inp = ThermostatSettingsUpdateInput(SETPOINT_TEMP_AWAY=temp)

        await self.coordinator.update_settings(inp)
