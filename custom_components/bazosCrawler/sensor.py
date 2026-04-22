import logging
from datetime import datetime

from homeassistant.components.sensor import SensorEntity
from homeassistant.components.binary_sensor import BinarySensorEntity
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN

_LOGGER = logging.getLogger(__name__)


def _slugify(value: str) -> str:
    return "".join(c.lower() if c.isalnum() else "_" for c in value).strip("_")


# =========================
# SETUP
# =========================

async def async_setup_entry(hass, entry, async_add_entities):
    coordinator = hass.data[DOMAIN][entry.entry_id]
    term = entry.data["search_term"]

    async_add_entities(
        [
            BazosTotalSensor(coordinator, term),
            BazosTodaySensor(coordinator, term),
            BazosNewTodayBinarySensor(coordinator, term),
        ]
    )


# =========================
# BASE ENTITY (DEVICE-CENTRIC)
# =========================

class BazosEntity(CoordinatorEntity):
    def __init__(self, coordinator, term: str):
        super().__init__(coordinator)
        self._term = term
        self._slug = _slugify(term)

    @property
    def device_info(self):
        return {
            "identifiers": {(DOMAIN, self._slug)},
            "name": f"Bazos {self._term}",
            "manufacturer": "BazosCrawler",
            "model": "Search",
        }


# =========================
# 1) CELKEM
# =========================

class BazosTotalSensor(BazosEntity, SensorEntity):
    _attr_name = "Celkem"
    _attr_native_unit_of_measurement = "items"

    @property
    def native_value(self):
        return len(self.coordinator.data.get("items", []))

    @property
    def unique_id(self):
        return f"{DOMAIN}_{self._slug}_total"


# =========================
# 2) DNES
# =========================

class BazosTodaySensor(BazosEntity, SensorEntity):
    _attr_name = "Dnes"
    _attr_native_unit_of_measurement = "items"

    def _is_today(self, item: dict) -> bool:
        if not item.get("date"):
            return False
        return item["date"] == datetime.now().date()

    @property
    def native_value(self):
        items = self.coordinator.data.get("items", [])
        return len([i for i in items if self._is_today(i)])

    @property
    def unique_id(self):
        return f"{DOMAIN}_{self._slug}_today"


# =========================
# 3) NOVÉ DNES (BINARY SENSOR)
# =========================

class BazosNewTodayBinarySensor(BazosEntity, BinarySensorEntity):
    _attr_name = "Nové dnes"

    def __init__(self, coordinator, term: str):
        super().__init__(coordinator, term)
        self._last_ids = set()

    def _is_today(self, item: dict) -> bool:
        if not item.get("date"):
            return False
        return item["date"] == datetime.now().date()

    @property
    def is_on(self):
        items = self.coordinator.data.get("items", [])

        current_ids = {i["id"] for i in items if "id" in i}
        new_ids = current_ids - self._last_ids

        # update snapshot
        self._last_ids = current_ids

        if not new_ids:
            return False

        for item in items:
            if item.get("id") in new_ids and self._is_today(item):
                return True

        return False

    @property
    def unique_id(self):
        return f"{DOMAIN}_{self._slug}_new_today"
