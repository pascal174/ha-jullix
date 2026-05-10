"""Jullix API client."""
from __future__ import annotations

import logging
import aiohttp

from .const import (
    LOCAL_API_BASE,
    CLOUD_API_BASE,
    ENDPOINT_SOLAR,
    ENDPOINT_BATTERY,
    ENDPOINT_METER,
    ENDPOINT_CHARGER,
    ENDPOINT_PLUG,
    ENDPOINT_CLOUD_POWER_SUMMARY,
    ENDPOINT_CLOUD_BATTERY_DETAIL,
    ENDPOINT_CLOUD_CHARGER_DETAIL,
    ENDPOINT_CLOUD_GRID_DETAIL,
    ENDPOINT_CLOUD_SOLAR_DETAIL,
    ENDPOINT_CLOUD_HOME_DETAIL,
)

_LOGGER = logging.getLogger(__name__)


class JullixApiError(Exception):
    """Raised when the API returns an error."""


class JullixApi:
    """Client to communicate with Jullix EMS (local + cloud)."""

    def __init__(
        self,
        session: aiohttp.ClientSession,
        local_ip: str,
        install_id: str | None = None,
        api_token: str | None = None,
        use_cloud: bool = False,
    ) -> None:
        self._session = session
        self._local_base = LOCAL_API_BASE.format(ip=local_ip)
        self._install_id = install_id
        self._api_token = api_token
        self._use_cloud = use_cloud

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------

    async def _get_local(self, endpoint: str) -> dict | list:
        url = self._local_base + endpoint
        try:
            async with self._session.get(url, timeout=aiohttp.ClientTimeout(total=10)) as resp:
                resp.raise_for_status()
                return await resp.json()
        except Exception as err:
            raise JullixApiError(f"Local request failed {url}: {err}") from err

    async def _get_cloud(self, endpoint: str) -> dict:
        if not self._api_token:
            raise JullixApiError("No API token configured for cloud access")
        url = CLOUD_API_BASE + endpoint.format(install_id=self._install_id)
        headers = {"Authorization": f"Bearer {self._api_token}"}
        try:
            async with self._session.get(
                url, headers=headers, timeout=aiohttp.ClientTimeout(total=15)
            ) as resp:
                resp.raise_for_status()
                return await resp.json()
        except Exception as err:
            raise JullixApiError(f"Cloud request failed {url}: {err}") from err

    # ------------------------------------------------------------------
    # Local endpoints
    # ------------------------------------------------------------------

    async def get_solar(self) -> dict:
        data = await self._get_local(ENDPOINT_SOLAR)
        return data[0] if isinstance(data, list) else data

    async def get_battery(self) -> dict:
        data = await self._get_local(ENDPOINT_BATTERY)
        return data[0] if isinstance(data, list) else data

    async def get_meter(self) -> dict:
        return await self._get_local(ENDPOINT_METER)

    async def get_charger(self) -> dict:
        data = await self._get_local(ENDPOINT_CHARGER)
        return data[0] if isinstance(data, list) else data

    async def get_plug(self) -> dict:
        data = await self._get_local(ENDPOINT_PLUG)
        return data[0] if isinstance(data, list) else data

    # ------------------------------------------------------------------
    # Cloud endpoints
    # ------------------------------------------------------------------

    async def get_cloud_power_summary(self) -> dict:
        data = await self._get_cloud(ENDPOINT_CLOUD_POWER_SUMMARY)
        return data.get("data", {}).get("powers", {})

    async def get_cloud_battery_detail(self) -> dict:
        data = await self._get_cloud(ENDPOINT_CLOUD_BATTERY_DETAIL)
        return self._extract_first(data)

    async def get_cloud_charger_detail(self) -> dict:
        data = await self._get_cloud(ENDPOINT_CLOUD_CHARGER_DETAIL)
        return self._extract_first(data)

    async def get_cloud_grid_detail(self) -> dict:
        data = await self._get_cloud(ENDPOINT_CLOUD_GRID_DETAIL)
        return self._extract_first(data)

    async def get_cloud_solar_detail(self) -> dict:
        data = await self._get_cloud(ENDPOINT_CLOUD_SOLAR_DETAIL)
        return self._extract_first(data)

    async def get_cloud_home_detail(self) -> dict:
        data = await self._get_cloud(ENDPOINT_CLOUD_HOME_DETAIL)
        return self._extract_first(data)

    @staticmethod
    def _extract_first(data: dict) -> dict:
        """Safely extract first item from data, whether it's a list or dict."""
        payload = data.get("data", {})
        if isinstance(payload, list):
            return payload[0] if payload else {}
        if isinstance(payload, dict):
            return payload
        return {}

    # ------------------------------------------------------------------
    # Test connectivity
    # ------------------------------------------------------------------

    async def test_local(self) -> bool:
        try:
            await self.get_solar()
            return True
        except JullixApiError:
            return False

    async def test_cloud(self) -> bool:
        try:
            await self.get_cloud_power_summary()
            return True
        except JullixApiError:
            return False
