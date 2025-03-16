"""Entity base class."""

from homeassistant.helpers.device_registry import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN
from .coordinator import AirobotCoordinator


class AirobotEntity(CoordinatorEntity):
    """Base class for all Airobot entities."""

    def __init__(self, coordinator: AirobotCoordinator, idx) -> None:
        """Pass coordinator to CoordinatorEntity."""
        super().__init__(coordinator)
        self.coordinator = coordinator
        self.idx = idx

    async def async_will_remove_from_hass(self):
        """Close api session when deleted."""
        await self.coordinator.airobot_api.session.close()

    # Properties
    @property
    def device_info(self) -> DeviceInfo:
        """Return the device info."""
        if self.coordinator.settings.DEVICE_NAME:
            device_name = self.coordinator.settings.DEVICE_NAME
        else:
            device_name = self.coordinator.settings.DEVICE_ID
        return DeviceInfo(
            identifiers={
                # Serial numbers are unique identifiers within a specific domain
                (DOMAIN, self.coordinator.status.DEVICE_ID)
            },
            name=device_name,
            manufacturer="Airobot",
            model="TE1",
            model_id="TE1",
            hw_version=self.coordinator.status.HW_VERSION,
            sw_version=self.coordinator.status.FW_VERSION,
            serial_number=self.coordinator.status.DEVICE_ID,
        )
