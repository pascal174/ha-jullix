"""Jullix EMS integration."""
from __future__ import annotations

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.aiohttp_client import async_get_clientsession

from .api import JullixApi
from .coordinator import JullixCoordinator
from .const import (
    DOMAIN,
    CONF_LOCAL_IP,
    CONF_INSTALL_ID,
    CONF_API_TOKEN,
    CONF_USE_CLOUD,
)

PLATFORMS = ["sensor", "binary_sensor"]


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up Jullix EMS from a config entry."""
    session = async_get_clientsession(hass)

    api = JullixApi(
        session=session,
        local_ip=entry.data[CONF_LOCAL_IP],
        install_id=entry.data.get(CONF_INSTALL_ID),
        api_token=entry.data.get(CONF_API_TOKEN),
        use_cloud=entry.data.get(CONF_USE_CLOUD, False),
    )

    coordinator = JullixCoordinator(
        hass=hass,
        api=api,
        use_cloud=entry.data.get(CONF_USE_CLOUD, False),
    )

    await coordinator.async_config_entry_first_refresh()

    hass.data.setdefault(DOMAIN, {})[entry.entry_id] = coordinator

    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)

    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    unload_ok = await hass.config_entries.async_unload_platforms(entry, PLATFORMS)
    if unload_ok:
        hass.data[DOMAIN].pop(entry.entry_id)
    return unload_ok
