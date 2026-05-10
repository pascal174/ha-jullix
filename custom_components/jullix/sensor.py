"""Jullix EMS sensor entities."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Callable

from homeassistant.components.sensor import (
    SensorDeviceClass,
    SensorEntity,
    SensorEntityDescription,
    SensorStateClass,
)
from homeassistant.config_entries import ConfigEntry
from homeassistant.const import (
    UnitOfPower,
    UnitOfEnergy,
    UnitOfElectricPotential,
    UnitOfElectricCurrent,
    UnitOfTemperature,
    UnitOfVolume,
    PERCENTAGE,
)
from homeassistant.core import HomeAssistant
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.entity_platform import AddEntitiesCallback
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN
from .coordinator import JullixCoordinator


@dataclass
class JullixSensorEntityDescription(SensorEntityDescription):
    """Extended description with value extractor."""
    value_fn: Callable[[dict], Any] = None
    available_fn: Callable[[dict], bool] = lambda d: True


# ---------------------------------------------------------------------------
# Sensor definitions
# ---------------------------------------------------------------------------

LOCAL_SENSORS: list[JullixSensorEntityDescription] = [
    # Solar
    JullixSensorEntityDescription(
        key="solar_power",
        name="Solar Power",
        native_unit_of_measurement=UnitOfPower.WATT,
        device_class=SensorDeviceClass.POWER,
        state_class=SensorStateClass.MEASUREMENT,
        icon="mdi:solar-power",
        value_fn=lambda d: round(d["solar"].get("power", 0) * 1000, 0),
        available_fn=lambda d: "solar" in d,
    ),
    JullixSensorEntityDescription(
        key="solar_energy",
        name="Solar Energy Total",
        native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
        device_class=SensorDeviceClass.ENERGY,
        state_class=SensorStateClass.TOTAL_INCREASING,
        icon="mdi:solar-power",
        value_fn=lambda d: round(d["solar"].get("energy", 0), 2),
        available_fn=lambda d: "solar" in d,
    ),
    # Battery
    JullixSensorEntityDescription(
        key="battery_power",
        name="Battery Power",
        native_unit_of_measurement=UnitOfPower.WATT,
        device_class=SensorDeviceClass.POWER,
        state_class=SensorStateClass.MEASUREMENT,
        icon="mdi:battery-charging",
        value_fn=lambda d: round(d["battery"].get("power", 0) * 1000, 0),
        available_fn=lambda d: "battery" in d,
    ),
    JullixSensorEntityDescription(
        key="battery_soc",
        name="Battery SOC",
        native_unit_of_measurement=PERCENTAGE,
        device_class=SensorDeviceClass.BATTERY,
        state_class=SensorStateClass.MEASUREMENT,
        value_fn=lambda d: d["battery"].get("battery", {}).get("soc"),
        available_fn=lambda d: "battery" in d,
    ),
    JullixSensorEntityDescription(
        key="battery_voltage",
        name="Battery Voltage",
        native_unit_of_measurement=UnitOfElectricPotential.VOLT,
        device_class=SensorDeviceClass.VOLTAGE,
        state_class=SensorStateClass.MEASUREMENT,
        value_fn=lambda d: d["battery"].get("battery", {}).get("voltage"),
        available_fn=lambda d: "battery" in d,
    ),
    JullixSensorEntityDescription(
        key="energy_charged",
        name="Energy Charged",
        native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
        device_class=SensorDeviceClass.ENERGY,
        state_class=SensorStateClass.TOTAL_INCREASING,
        icon="mdi:battery-arrow-up",
        value_fn=lambda d: d["battery"].get("energy_charged"),
        available_fn=lambda d: "battery" in d,
    ),
    JullixSensorEntityDescription(
        key="energy_discharged",
        name="Energy Discharged",
        native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
        device_class=SensorDeviceClass.ENERGY,
        state_class=SensorStateClass.TOTAL_INCREASING,
        icon="mdi:battery-arrow-down",
        value_fn=lambda d: d["battery"].get("energy_discharged"),
        available_fn=lambda d: "battery" in d,
    ),
    # Meter
    JullixSensorEntityDescription(
        key="power_in",
        name="Grid Power In",
        native_unit_of_measurement=UnitOfPower.WATT,
        device_class=SensorDeviceClass.POWER,
        state_class=SensorStateClass.MEASUREMENT,
        icon="mdi:transmission-tower-import",
        value_fn=lambda d: round(d["meter"].get("power", {}).get("in", 0) * 1000, 0),
        available_fn=lambda d: "meter" in d,
    ),
    JullixSensorEntityDescription(
        key="power_out",
        name="Grid Power Out",
        native_unit_of_measurement=UnitOfPower.WATT,
        device_class=SensorDeviceClass.POWER,
        state_class=SensorStateClass.MEASUREMENT,
        icon="mdi:transmission-tower-export",
        value_fn=lambda d: round(d["meter"].get("power", {}).get("out", 0) * 1000, 0),
        available_fn=lambda d: "meter" in d,
    ),
    JullixSensorEntityDescription(
        key="net_power",
        name="Net Power",
        native_unit_of_measurement=UnitOfPower.WATT,
        device_class=SensorDeviceClass.POWER,
        state_class=SensorStateClass.MEASUREMENT,
        icon="mdi:lightning-bolt",
        value_fn=lambda d: round(
            (d["meter"].get("power", {}).get("in", 0) - d["meter"].get("power", {}).get("out", 0)) * 1000, 0
        ),
        available_fn=lambda d: "meter" in d,
    ),
    JullixSensorEntityDescription(
        key="energy_in_1",
        name="Energy Import T1",
        native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
        device_class=SensorDeviceClass.ENERGY,
        state_class=SensorStateClass.TOTAL_INCREASING,
        value_fn=lambda d: d["meter"].get("energy", {}).get("in_1"),
        available_fn=lambda d: "meter" in d,
    ),
    JullixSensorEntityDescription(
        key="energy_in_2",
        name="Energy Import T2",
        native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
        device_class=SensorDeviceClass.ENERGY,
        state_class=SensorStateClass.TOTAL_INCREASING,
        value_fn=lambda d: d["meter"].get("energy", {}).get("in_2"),
        available_fn=lambda d: "meter" in d,
    ),
    JullixSensorEntityDescription(
        key="energy_out_1",
        name="Energy Export T1",
        native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
        device_class=SensorDeviceClass.ENERGY,
        state_class=SensorStateClass.TOTAL_INCREASING,
        value_fn=lambda d: d["meter"].get("energy", {}).get("out_1"),
        available_fn=lambda d: "meter" in d,
    ),
    JullixSensorEntityDescription(
        key="energy_out_2",
        name="Energy Export T2",
        native_unit_of_measurement=UnitOfEnergy.KILO_WATT_HOUR,
        device_class=SensorDeviceClass.ENERGY,
        state_class=SensorStateClass.TOTAL_INCREASING,
        value_fn=lambda d: d["meter"].get("energy", {}).get("out_2"),
        available_fn=lambda d: "meter" in d,
    ),
    JullixSensorEntityDescription(
        key="voltage_l1",
        name="Voltage L1",
        native_unit_of_measurement=UnitOfElectricPotential.VOLT,
        device_class=SensorDeviceClass.VOLTAGE,
        state_class=SensorStateClass.MEASUREMENT,
        value_fn=lambda d: d["meter"].get("voltage", {}).get("l1"),
        available_fn=lambda d: "meter" in d,
    ),
    JullixSensorEntityDescription(
        key="voltage_l2",
        name="Voltage L2",
        native_unit_of_measurement=UnitOfElectricPotential.VOLT,
        device_class=SensorDeviceClass.VOLTAGE,
        state_class=SensorStateClass.MEASUREMENT,
        value_fn=lambda d: d["meter"].get("voltage", {}).get("l2"),
        available_fn=lambda d: "meter" in d,
    ),
    JullixSensorEntityDescription(
        key="voltage_l3",
        name="Voltage L3",
        native_unit_of_measurement=UnitOfElectricPotential.VOLT,
        device_class=SensorDeviceClass.VOLTAGE,
        state_class=SensorStateClass.MEASUREMENT,
        value_fn=lambda d: d["meter"].get("voltage", {}).get("l3"),
        available_fn=lambda d: "meter" in d,
    ),
    JullixSensorEntityDescription(
        key="water_usage",
        name="Water Usage",
        native_unit_of_measurement=UnitOfVolume.CUBIC_METERS,
        device_class=SensorDeviceClass.WATER,
        state_class=SensorStateClass.TOTAL_INCREASING,
        icon="mdi:water",
        value_fn=lambda d: d["meter"].get("water"),
        available_fn=lambda d: "meter" in d,
    ),
    # EV Charger
    JullixSensorEntityDescription(
        key="ev_power",
        name="EV Charger Power",
        native_unit_of_measurement=UnitOfPower.WATT,
        device_class=SensorDeviceClass.POWER,
        state_class=SensorStateClass.MEASUREMENT,
        icon="mdi:ev-station",
        value_fn=lambda d: round(d["charger"].get("power", 0) * 1000, 0),
        available_fn=lambda d: "charger" in d,
    ),
    JullixSensorEntityDescription(
        key="ev_soc",
        name="EV Battery SOC",
        native_unit_of_measurement=PERCENTAGE,
        device_class=SensorDeviceClass.BATTERY,
        state_class=SensorStateClass.MEASUREMENT,
        icon="mdi:car-electric",
        value_fn=lambda d: d["charger"].get("soc"),
        available_fn=lambda d: "charger" in d,
    ),
    JullixSensorEntityDescription(
        key="ev_temperature",
        name="EV Charger Temperature",
        native_unit_of_measurement=UnitOfTemperature.CELSIUS,
        device_class=SensorDeviceClass.TEMPERATURE,
        state_class=SensorStateClass.MEASUREMENT,
        value_fn=lambda d: round(d["charger"].get("temperature", 0), 1),
        available_fn=lambda d: "charger" in d,
    ),
    JullixSensorEntityDescription(
        key="ev_max_current",
        name="EV Max Current",
        native_unit_of_measurement=UnitOfElectricCurrent.AMPERE,
        device_class=SensorDeviceClass.CURRENT,
        state_class=SensorStateClass.MEASUREMENT,
        value_fn=lambda d: d["charger"].get("max_current"),
        available_fn=lambda d: "charger" in d,
    ),
    JullixSensorEntityDescription(
        key="ev_state",
        name="EV Charger State",
        icon="mdi:car-electric",
        value_fn=lambda d: d["charger"].get("state"),
        available_fn=lambda d: "charger" in d,
    ),
]

CLOUD_SENSORS: list[JullixSensorEntityDescription] = [
    JullixSensorEntityDescription(
        key="cloud_grid_power",
        name="Grid Power (Cloud)",
        native_unit_of_measurement=UnitOfPower.KILO_WATT,
        device_class=SensorDeviceClass.POWER,
        state_class=SensorStateClass.MEASUREMENT,
        icon="mdi:transmission-tower",
        value_fn=lambda d: d.get("cloud_powers", {}).get("grid"),
        available_fn=lambda d: bool(d.get("cloud_powers")),
    ),
    JullixSensorEntityDescription(
        key="cloud_solar_power",
        name="Solar Power (Cloud)",
        native_unit_of_measurement=UnitOfPower.KILO_WATT,
        device_class=SensorDeviceClass.POWER,
        state_class=SensorStateClass.MEASUREMENT,
        icon="mdi:solar-power",
        value_fn=lambda d: d.get("cloud_powers", {}).get("solar"),
        available_fn=lambda d: bool(d.get("cloud_powers")),
    ),
    JullixSensorEntityDescription(
        key="cloud_home_power",
        name="Home Power (Cloud)",
        native_unit_of_measurement=UnitOfPower.KILO_WATT,
        device_class=SensorDeviceClass.POWER,
        state_class=SensorStateClass.MEASUREMENT,
        icon="mdi:home-lightning-bolt",
        value_fn=lambda d: d.get("cloud_powers", {}).get("home"),
        available_fn=lambda d: bool(d.get("cloud_powers")),
    ),
    JullixSensorEntityDescription(
        key="cloud_battery_power",
        name="Battery Power (Cloud)",
        native_unit_of_measurement=UnitOfPower.KILO_WATT,
        device_class=SensorDeviceClass.POWER,
        state_class=SensorStateClass.MEASUREMENT,
        icon="mdi:battery-charging",
        value_fn=lambda d: d.get("cloud_powers", {}).get("battery"),
        available_fn=lambda d: bool(d.get("cloud_powers")),
    ),
    JullixSensorEntityDescription(
        key="cloud_car_power",
        name="EV Power (Cloud)",
        native_unit_of_measurement=UnitOfPower.KILO_WATT,
        device_class=SensorDeviceClass.POWER,
        state_class=SensorStateClass.MEASUREMENT,
        icon="mdi:ev-station",
        value_fn=lambda d: d.get("cloud_powers", {}).get("car"),
        available_fn=lambda d: bool(d.get("cloud_powers")),
    ),
    JullixSensorEntityDescription(
        key="cloud_battery_soc",
        name="Battery SOC (Cloud)",
        native_unit_of_measurement=PERCENTAGE,
        device_class=SensorDeviceClass.BATTERY,
        state_class=SensorStateClass.MEASUREMENT,
        value_fn=lambda d: d.get("cloud_battery", {}).get("battery", {}).get("soc"),
        available_fn=lambda d: bool(d.get("cloud_battery")),
    ),
]


async def async_setup_entry(
    hass: HomeAssistant,
    entry: ConfigEntry,
    async_add_entities: AddEntitiesCallback,
) -> None:
    """Set up Jullix sensors from config entry."""
    coordinator: JullixCoordinator = hass.data[DOMAIN][entry.entry_id]
    use_cloud = entry.data.get("use_cloud", False)

    entities = [
        JullixSensorEntity(coordinator, description, entry)
        for description in LOCAL_SENSORS
    ]

    if use_cloud:
        entities += [
            JullixSensorEntity(coordinator, description, entry)
            for description in CLOUD_SENSORS
        ]

    async_add_entities(entities)


class JullixSensorEntity(CoordinatorEntity[JullixCoordinator], SensorEntity):
    """A Jullix sensor entity."""

    entity_description: JullixSensorEntityDescription
    _attr_has_entity_name = True

    def __init__(
        self,
        coordinator: JullixCoordinator,
        description: JullixSensorEntityDescription,
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
    def native_value(self) -> Any:
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
