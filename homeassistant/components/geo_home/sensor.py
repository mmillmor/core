from __future__ import annotations
from homeassistant.components.geo_home.geohome import GeoHomeHub
import logging
import async_timeout

from homeassistant.components.sensor import (
    SensorEntity,
    SensorEntityDescription,
    SensorStateClass,
    SensorDeviceClass,
)
from homeassistant.const import ENERGY_KILO_WATT_HOUR
from homeassistant.helpers.entity import DeviceInfo
from homeassistant.helpers.update_coordinator import CoordinatorEntity
from homeassistant.helpers.update_coordinator import (
    CoordinatorEntity,
    DataUpdateCoordinator,
    UpdateFailed,
)
from datetime import timedelta


from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)


async def async_setup_entry(hass, config_entry, async_add_entities):

    username = config_entry.data.get("username")
    password = config_entry.data.get("password")
    hub = GeoHomeHub(username, password, hass)

    async def async_update_data():
        async with async_timeout.timeout(300):
            return await hub.get_device_data()

    coordinator = DataUpdateCoordinator(
        hass,
        _LOGGER,
        # Name of the data. For logging purposes.
        name="sensor",
        update_method=async_update_data,
        # Polling interval. Will only be polled if there are subscribers.
        update_interval=timedelta(seconds=30),
    )

    await coordinator.async_config_entry_first_refresh()

    async_add_entities(
        [
            GeoHomeGasSensor(coordinator, hub),
            GeoHomeElectricitySensor(coordinator, hub),
            GeoHomeGasPriceSensor(coordinator, hub),
            GeoHomeElectricityPriceSensor(coordinator, hub),
        ]
    )


class GeoHomeGasSensor(CoordinatorEntity, SensorEntity):
    def __init__(self, coordinator: CoordinatorEntity, hub: GeoHomeHub):
        super().__init__(coordinator)
        self.hub = hub
        self.entity_description: SensorEntityDescription(
            key="totalgas",
            device_class=SensorDeviceClass.ENERGY,
            native_unit_of_measurement=ENERGY_KILO_WATT_HOUR,
            state_class=SensorStateClass.TOTAL,
            name="Total Gas",
        )

    @property
    def name(self):
        """Return the name of the sensor."""
        return "Gas"

    @property
    def unique_id(self):
        """Return the unique id of the sensor."""
        return "geo_home_gas"

    @property
    def native_value(self):
        """Return the state of the sensor."""
        return self.hub.gasReading

    @property
    def native_unit_of_measurement(self):
        """Return the state of the sensor."""
        return "kWh"

    @property
    def icon(self):
        """Icon to use in the frontend, if any."""
        return "mdi:fire"


class GeoHomeGasPriceSensor(CoordinatorEntity, SensorEntity):
    def __init__(self, coordinator: CoordinatorEntity, hub: GeoHomeHub):
        super().__init__(coordinator)
        self.hub = hub
        self.entity_description: SensorEntityDescription(
            key="gasprice",
            device_class=SensorDeviceClass.MONETARY,
            state_class=SensorStateClass.MEASUREMENT,
            name="Gas Price",
        )

    @property
    def name(self):
        """Return the name of the sensor."""
        return "Gas Price"

    @property
    def unique_id(self):
        """Return the unique id of the sensor."""
        return "geo_home_gas_price"

    @property
    def native_value(self):
        """Return the state of the sensor."""
        return self.hub.gasPrice

    @property
    def icon(self):
        """Icon to use in the frontend, if any."""
        return "mdi:currency-gbp"


class GeoHomeElectricitySensor(CoordinatorEntity, SensorEntity):
    def __init__(self, coordinator: CoordinatorEntity, hub: GeoHomeHub):
        super().__init__(coordinator)
        self.hub = hub
        self.entity_description: SensorEntityDescription(
            key="totalelectricity",
            device_class=SensorDeviceClass.ENERGY,
            native_unit_of_measurement=ENERGY_KILO_WATT_HOUR,
            state_class=SensorStateClass.TOTAL,
            name="Total Electricity",
        )

    @property
    def name(self):
        """Return the name of the sensor."""
        return "Electriciy"

    @property
    def unique_id(self):
        """Return the unique id of the sensor."""
        return "geo_home_electricity"

    @property
    def native_value(self):
        """Return the state of the sensor."""
        return self.hub.electricityReading

    @property
    def native_unit_of_measurement(self):
        """Return the state of the sensor."""
        return "kWh"

    @property
    def icon(self):
        """Icon to use in the frontend, if any."""
        return "mdi:flash"


class GeoHomeElectricityPriceSensor(CoordinatorEntity, SensorEntity):
    def __init__(self, coordinator: CoordinatorEntity, hub: GeoHomeHub):
        super().__init__(coordinator)
        self.hub = hub
        self.entity_description: SensorEntityDescription(
            key="electricityprice",
            device_class=SensorDeviceClass.MONETARY,
            state_class=SensorStateClass.MEASUREMENT,
            name="Electricity Price",
        )

    @property
    def name(self):
        """Return the name of the sensor."""
        return "Electricity Price"

    @property
    def unique_id(self):
        """Return the unique id of the sensor."""
        return "geo_home_electricity_price"

    @property
    def native_value(self):
        """Return the state of the sensor."""
        return self.hub.electricityPrice

    @property
    def icon(self):
        """Icon to use in the frontend, if any."""
        return "mdi:currency-gbp"
