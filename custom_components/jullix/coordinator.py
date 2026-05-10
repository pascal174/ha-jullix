"""Jullix DataUpdateCoordinator."""
from __future__ import annotations

import logging
from datetime import timedelta

from homeassistant.core import HomeAssistant
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .api import JullixApi, JullixApiError
from .const import DOMAIN, SCAN_INTERVAL_LOCAL, SCAN_INTERVAL_CLOUD

_LOGGER = logging.getLogger(__name__)


class JullixCoordinator(DataUpdateCoordinator):
    """Fetches all Jullix data in one coordinator."""

    def __init__(self, hass: HomeAssistant, api: JullixApi, use_cloud: bool) -> None:
        self._api = api
        self._use_cloud = use_cloud

        interval = SCAN_INTERVAL_CLOUD if use_cloud else SCAN_INTERVAL_LOCAL

        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=timedelta(seconds=interval),
        )

    async def _async_update_data(self) -> dict:
        """Fetch all data from local and/or cloud API."""
        data = {}

        # --- Local data (always fetched if available) ---
        try:
            data["solar"]   = await self._api.get_solar()
            data["battery"] = await self._api.get_battery()
            data["meter"]   = await self._api.get_meter()
            data["charger"] = await self._api.get_charger()
        except JullixApiError as err:
            raise UpdateFailed(f"Local API error: {err}") from err

        # Optionally fetch plug (may not be present on all installations)
        try:
            data["plug"] = await self._api.get_plug()
        except JullixApiError:
            data["plug"] = {}

        # --- Cloud data (only if configured) ---
        if self._use_cloud:
            try:
                data["cloud_powers"]  = await self._api.get_cloud_power_summary()
                data["cloud_battery"] = await self._api.get_cloud_battery_detail()
                data["cloud_charger"] = await self._api.get_cloud_charger_detail()
                data["cloud_grid"]    = await self._api.get_cloud_grid_detail()
                data["cloud_solar"]   = await self._api.get_cloud_solar_detail()
                data["cloud_home"]    = await self._api.get_cloud_home_detail()
            except JullixApiError as err:
                _LOGGER.warning("Cloud API error (local data still available): %s", err)
                data["cloud_powers"]  = {}
                data["cloud_battery"] = {}
                data["cloud_charger"] = {}
                data["cloud_grid"]    = {}
                data["cloud_solar"]   = {}
                data["cloud_home"]    = {}

        return data
