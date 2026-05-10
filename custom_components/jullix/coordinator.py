"""Jullix DataUpdateCoordinator."""
from __future__ import annotations

import logging
from datetime import timedelta

from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .api import JullixApi, JullixApiError
from .const import DOMAIN, SCAN_INTERVAL_LOCAL

_LOGGER = logging.getLogger(__name__)


class JullixCoordinator(DataUpdateCoordinator):
    """Fetches all Jullix data from the local API."""

    def __init__(self, hass: HomeAssistant, api: JullixApi) -> None:
        self._api = api

        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=timedelta(seconds=SCAN_INTERVAL_LOCAL),
        )

    async def _async_update_data(self) -> dict:
        """Fetch all data from local API."""
        data = {}

        try:
            data["solar"]   = await self._api.get_solar()
            data["battery"] = await self._api.get_battery()
            data["meter"]   = await self._api.get_meter()
            data["charger"] = await self._api.get_charger()
        except JullixApiError as err:
            raise UpdateFailed(f"Local API error: {err}") from err

        # Plug is optional — not present on all installations
        try:
            data["plug"] = await self._api.get_plug()
        except JullixApiError:
            data["plug"] = {}

        return data
