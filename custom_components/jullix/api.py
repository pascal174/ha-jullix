"""Jullix API client — local only."""
from __future__ import annotations

import logging
import aiohttp

from .const import (
    LOCAL_API_BASE,
    ENDPOINT_SOLAR,
    ENDPOINT_BATTERY,
    ENDPOINT_METER,
    ENDPOINT_CHARGER,
    ENDPOINT_PLUG,
)

_LOGGER = logging.getLogger(__name__)


class JullixApiError(Exception):
    """Raised when the API returns an error."""


class JullixApi:
    """Client to communicate with Jullix EMS locally."""

    def __init__(self, session: aiohttp.ClientSession, local_ip: str) -> None:
        self._session = session
        self._local_base = LOCAL_API_BASE.format(ip=local_ip)

    async def _get_local(self, endpoint: str) -> dict | list:
        url = self._local_base + endpoint
        try:
            async with self._session.get(
                url, timeout=aiohttp.ClientTimeout(total=10)
            ) as resp:
                resp.raise_for_status()
                return await resp.json()
        except Exception as err:
            raise JullixApiError(f"Local request failed {url}: {err}") from err

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

    async def test_local(self) -> bool:
        try:
            await self.get_solar()
            return True
        except JullixApiError:
            return False
