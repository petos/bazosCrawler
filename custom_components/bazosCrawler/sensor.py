from homeassistant.components.sensor import SensorEntity
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN


class BazosEntity(CoordinatorEntity):
    def __init__(self, coordinator, term):
        super().__init__(coordinator)
        self._term = term
        self._slug = "".join(c.lower() if c.isalnum() else "_" for c in term)


class BazosTotalSensor(BazosEntity, SensorEntity):
    @property
    def name(self):
        return f"Bazos {self._term} celkem"

    @property
    def unique_id(self):
        return f"{DOMAIN}_{self._slug}_total"

    @property
    def state(self):
        return len(self.coordinator.data.get("items", []))


class BazosTodaySensor(BazosEntity, SensorEntity):
    @property
    def name(self):
        return f"Bazos {self._term} dnes"

    @property
    def unique_id(self):
        return f"{DOMAIN}_{self._slug}_today"

    @property
    def state(self):
        items = self.coordinator.data.get("items", [])
        return sum(1 for i in items if i.get("date") is not None)
