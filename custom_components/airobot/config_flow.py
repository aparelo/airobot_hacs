"""Config flow for the Airobot thermostat integration."""

from __future__ import annotations

import logging
from typing import Any

import aiohttp
import aiohttp.client_exceptions
from airobot_api_client.async_api import AsyncAirobotAPI
from airobot_api_client.models import ThermostatSettings
import voluptuous as vol

from homeassistant.config_entries import ConfigFlow, ConfigFlowResult
from homeassistant.const import CONF_HOST, CONF_PASSWORD, CONF_USERNAME, CONF_NAME
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import HomeAssistantError

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)

STEP_USER_DATA_SCHEMA = vol.Schema(
    {
        vol.Optional(
            CONF_HOST,
            "Network address of the thermostat. If not provided the hostname will be used instead.",
        ): str,
        vol.Required(CONF_USERNAME): str,
        vol.Required(CONF_PASSWORD): str,
    }
)


async def validate_input(hass: HomeAssistant, data: dict[str, Any]) -> dict[str, Any]:
    """Validate the user input allows us to connect.

    Data has the keys from STEP_USER_DATA_SCHEMA with values provided by the user.
    """
    host = data.get(CONF_HOST, f"http://Airobot-Thermostat-{data[CONF_USERNAME]}.local")

    api_client = AsyncAirobotAPI(host, data[CONF_USERNAME], data[CONF_PASSWORD])

    if not await api_client.authenticate():
        # Try an actual request to get the error code
        try:
            await api_client.get_settings()
        except aiohttp.client_exceptions.ClientResponseError as ex:
            if ex.code == 401:
                await api_client.session.close()
                raise InvalidAuth from ex
        await api_client.session.close()
        raise CannotConnect

    settings: ThermostatSettings = await api_client.get_settings()

    await api_client.session.close()

    device_name = settings.DEVICE_NAME
    device_id = settings.DEVICE_ID

    if device_name:
        final_name = f"{device_name} ({device_id})"
    else:
        final_name = device_id

    # Return info that you want to store in the config entry.
    return {"device_id": final_name}


class ConfigFlow(ConfigFlow, domain=DOMAIN):
    """Handle a config flow for Airobot thermostat."""

    VERSION = 1

    async def async_step_user(
        self, user_input: dict[str, Any] | None = None
    ) -> ConfigFlowResult:
        """Handle the initial step."""
        errors: dict[str, str] = {}
        if user_input is not None:
            try:
                info = await validate_input(self.hass, user_input)
            except CannotConnect:
                errors["base"] = "cannot_connect"
            except InvalidAuth:
                errors["base"] = "invalid_auth"
            except Exception:
                _LOGGER.exception("Unexpected exception")
                errors["base"] = "unknown"
            else:
                return self.async_create_entry(title=info["device_id"], data=user_input)

        return self.async_show_form(
            step_id="user", data_schema=STEP_USER_DATA_SCHEMA, errors=errors
        )


class CannotConnect(HomeAssistantError):
    """Error to indicate we cannot connect."""


class InvalidAuth(HomeAssistantError):
    """Error to indicate there is invalid auth."""
