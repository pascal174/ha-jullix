"""Config flow for Jullix EMS."""
from __future__ import annotations

import voluptuous as vol
import aiohttp

from homeassistant import config_entries
from homeassistant.core import HomeAssistant
from homeassistant.data_entry_flow import FlowResult
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from .api import JullixApi, JullixApiError
from .const import (
    DOMAIN,
    DEFAULT_NAME,
    CONF_LOCAL_IP,
    CONF_INSTALL_ID,
    CONF_API_TOKEN,
    CONF_USE_CLOUD,
)

STEP_LOCAL_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_LOCAL_IP, default="192.168.2.150"): str,
    }
)

STEP_CLOUD_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_USE_CLOUD, default=False): bool,
        vol.Optional(CONF_INSTALL_ID): str,
        vol.Optional(CONF_API_TOKEN): str,
    }
)


class JullixConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle the config flow for Jullix EMS."""

    VERSION = 1
    _local_ip: str = ""

    async def async_step_user(self, user_input=None) -> FlowResult:
        """Step 1: local IP address."""
        errors = {}

        if user_input is not None:
            self._local_ip = user_input[CONF_LOCAL_IP]
            session = async_get_clientsession(self.hass)
            api = JullixApi(session, self._local_ip)

            if await api.test_local():
                return await self.async_step_cloud()
            else:
                errors["base"] = "cannot_connect"

        return self.async_show_form(
            step_id="user",
            data_schema=STEP_LOCAL_SCHEMA,
            errors=errors,
            description_placeholders={"name": DEFAULT_NAME},
        )

    async def async_step_cloud(self, user_input=None) -> FlowResult:
        """Step 2: optional cloud configuration."""
        errors = {}

        if user_input is not None:
            use_cloud = user_input.get(CONF_USE_CLOUD, False)
            install_id = user_input.get(CONF_INSTALL_ID, "")
            api_token = user_input.get(CONF_API_TOKEN, "")

            if use_cloud:
                if not install_id or not api_token:
                    errors["base"] = "cloud_fields_required"
                else:
                    session = async_get_clientsession(self.hass)
                    api = JullixApi(session, self._local_ip, install_id, api_token, True)
                    if not await api.test_cloud():
                        errors["base"] = "cloud_auth_failed"

            if not errors:
                return self.async_create_entry(
                    title=DEFAULT_NAME,
                    data={
                        CONF_LOCAL_IP: self._local_ip,
                        CONF_USE_CLOUD: use_cloud,
                        CONF_INSTALL_ID: install_id,
                        CONF_API_TOKEN: api_token,
                    },
                )

        return self.async_show_form(
            step_id="cloud",
            data_schema=STEP_CLOUD_SCHEMA,
            errors=errors,
        )
