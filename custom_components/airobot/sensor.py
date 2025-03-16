"""Thermostat sensors."""

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.components.sensor import (
    SensorEntity,
    SensorDeviceClass,
    SensorStateClass,
)


from .coordinator import AirobotCoordinator
from .entity_base import AirobotEntity


async def async_setup_entry(
    hass: HomeAssistant, entry: ConfigEntry, async_add_entities
):
    """Sensor setup."""
    coordinator: AirobotCoordinator = entry.runtime_data

    entities = []
    if coordinator.status.CO2 < 65535:
        entities.append(AirobotCO2(coordinator, entry.title))
        entities.append(AirobotAQI(coordinator, entry.title))

    entities.append(AirobotDeviceUptime(coordinator, entry.title))
    entities.append(AirobotHeatingUptime(coordinator, entry.title))
    entities.append(AirobotErrors(coordinator, entry.title))

    async_add_entities(entities, update_before_add=False)


class AirobotCO2(AirobotEntity, SensorEntity):
    """Measured CO2."""

    _attr_has_entity_name = True

    @property
    def unique_id(self):
        return f"{self.coordinator.settings.DEVICE_ID}_co2"

    @property
    def translation_key(self):
        return "co2"

    @property
    def native_unit_of_measurement(self):
        """Unit of measurement."""
        return "ppm"

    @property
    def device_class(self):
        """Device Class."""
        return SensorDeviceClass.CO2

    @property
    def native_value(self):
        """Sensor Value."""
        return self.coordinator.status.CO2


class AirobotAQI(AirobotEntity, SensorEntity):
    """Calculated AQI."""

    _attr_has_entity_name = True

    @property
    def unique_id(self):
        return f"{self.coordinator.settings.DEVICE_ID}_aqi"

    @property
    def translation_key(self):
        return "aqi"

    @property
    def device_class(self):
        """Device Class."""
        return SensorDeviceClass.AQI

    @property
    def native_value(self):
        """Sensor Value."""
        return self.coordinator.status.AQI


class AirobotDeviceUptime(AirobotEntity, SensorEntity):
    """Thermostat uptime."""

    _attr_has_entity_name = True

    @property
    def unique_id(self):
        return f"{self.coordinator.settings.DEVICE_ID}_device_uptime"

    @property
    def translation_key(self):
        return "device_uptime"

    @property
    def native_unit_of_measurement(self):
        """Unit of measurement."""
        return "s"

    @property
    def device_class(self):
        """Device Class."""
        return SensorDeviceClass.DURATION

    @property
    def state_class(self):
        """State class."""
        return SensorStateClass.MEASUREMENT

    @property
    def native_value(self):
        """Sensor Value."""
        return self.coordinator.status.DEVICE_UPTIME


class AirobotHeatingUptime(AirobotEntity, SensorEntity):
    """Thermostat heating time."""

    _attr_has_entity_name = True

    @property
    def unique_id(self):
        return f"{self.coordinator.settings.DEVICE_ID}_heating_uptime"

    @property
    def translation_key(self):
        return "heating_uptime"

    @property
    def native_unit_of_measurement(self):
        """Unit of measurement."""
        return "s"

    @property
    def device_class(self):
        """Device Class."""
        return SensorDeviceClass.DURATION

    @property
    def state_class(self):
        """State class."""
        return SensorStateClass.MEASUREMENT

    @property
    def native_value(self):
        """Sensor Value."""
        return self.coordinator.status.HEATING_UPTIME


class AirobotErrors(AirobotEntity, SensorEntity):
    """Thermostat errors."""

    _attr_has_entity_name = True

    @property
    def unique_id(self):
        return f"{self.coordinator.settings.DEVICE_ID}_errors"

    @property
    def translation_key(self):
        return "errors"

    @property
    def unique_id(self):
        return self.coordinator.settings.DEVICE_ID

    @property
    def state_class(self):
        """State class."""
        return SensorStateClass.MEASUREMENT

    @property
    def native_value(self):
        """Sensor Value."""
        return self.coordinator.status.ERRORS
