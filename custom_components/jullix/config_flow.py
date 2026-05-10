"""Config flow for Jullix EMS."""
from __future__ import annotations

import voluptuous as vol

from homeassistant import config_entries
from homeassistant.data_entry_flow import FlowResult
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from .api import JullixApi
from .const import DOMAIN, DEFAULT_NAME, CONF_LOCAL_IP

STEP_LOCAL_SCHEMA = vol.Schema(
    {
        vol.Required(CONF_LOCAL_IP, default="192.168.2.150"): str,
    }
)


class JullixConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle the config flow for Jullix EMS."""

    VERSION = 1

    async def async_step_user(self, user_input=None) -> FlowResult:
        """Step 1: local IP address."""
        errors = {}

        if user_input is not None:
            session = async_get_clientsession(self.hass)
            api = JullixApi(session, user_input[CONF_LOCAL_IP])

            if await api.test_local():
                return self.async_create_entry(
                    title=DEFAULT_NAME,
                    data={CONF_LOCAL_IP: user_input[CONF_LOCAL_IP]},
                )
            else:
                errors["base"] = "cannot_connect"

        return self.async_show_form(
            step_id="user",
            data_schema=STEP_LOCAL_SCHEMA,
            errors=errors,
        )
