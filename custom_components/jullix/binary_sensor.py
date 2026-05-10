"""Jullix EMS binary sensor entities."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable

from homeassistant.components.binary_sensor import (
    BinarySensorDeviceClass,
    BinarySensorEntity,
    BinarySensorEntityDescription,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN
from .coordinator import JullixCoordinator


@dataclass
class JullixBinarySensorDescription(BinarySensorEntityDescription):
    """Extended description with value extractor."""
    value_fn: Callable[[dict], Any] = None
    available_fn: Callable[[dict], bool] = lambda d: True


BINARY_SENSORS: list[JullixBinarySensorDescription] = [
    JullixBinarySensorDescription(
        key="ev_busy",
        name="EV Charger Occupied",
        device_class=BinarySensorDeviceClass.OCCUPANCY,
        icon="mdi:car",
        value_fn=lambda d: bool(d["charger"].get("busy")),
        available_fn=lambda d: "charger" in d,
    ),
    JullixBinarySensorDescription(
        key="ev_three_phase",
        name="EV Three Phase Active",
        device_class=BinarySensorDeviceClass.POWER,
        icon="mdi:transmission-tower",
        value_fn=lambda d: bool(d["charger"].get("three_phase")),
        available_fn=lambda d: "charger" in d,
    ),
    JullixBinarySensorDescription(
        key="battery_fault",
        name="Battery Fault",
        device_class=BinarySensorDeviceClass.PROBLEM,
        value_fn=lambda d: bool(d["battery"].get("battery", {}).get("fault")),
        available_fn=lambda d: "battery" in d,
    ),
    JullixBinarySensorDescription(
        key="solar_fault",
        name="Solar Fault",
        device_class=BinarySensorDeviceClass.PROBLEM,
        value_fn=lambda d: bool(d["solar"].get("fault")),
        available_fn=lambda d: "solar" in d,
    ),
]


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Jullix binary sensors from config entry."""
    coordinator: JullixCoordinator = hass.data[DOMAIN][entry.entry_id]

    async_add_entities(
        JullixBinarySensorEntity(coordinator, description, entry)
        for description in BINARY_SENSORS
    )


class JullixBinarySensorEntity(CoordinatorEntity[JullixCoordinator], BinarySensorEntity):
    """A Jullix binary sensor entity."""

    entity_description: JullixBinarySensorDescription
    _attr_has_entity_name = True

    def __init__(
        self,
        coordinator: JullixCoordinator,
        description: JullixBinarySensorDescription,
        entry: ConfigEntry,
    ) -> None:
        super().__init__(coordinator)
        self.entity_description = description
        self._attr_unique_id = f"{entry.entry_id}_{description.key}"
        self._attr_device_info = DeviceInfo(
            identifiers={(DOMAIN, entry.entry_id)},
            name="Jullix EMS",
            manufacturer="Jullix",
            model="EMS Gateway",
            configuration_url="https://mijn.jullix.be",
        )

    @property
    def is_on(self) -> bool | None:
        if self.coordinator.data is None:
            return None
        try:
            return self.entity_description.value_fn(self.coordinator.data)
        except (KeyError, TypeError, IndexError):
            return None

    @property
    def available(self) -> bool:
        if not self.coordinator.last_update_success or self.coordinator.data is None:
            return False
        try:
            return self.entity_description.available_fn(self.coordinator.data)
        except Exception:
            return False
