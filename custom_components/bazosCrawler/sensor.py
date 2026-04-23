from homeassistant.components.sensor import SensorEntity
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN
from .entity import BazosEntity

async def async_setup_entry(hass, entry, async_add_entities):
    coordinator = hass.data[DOMAIN][entry.entry_id]
    term = entry.data["search_term"]

    async_add_entities(
        [
            BazosTotalSensor(coordinator, term),
            BazosTodaySensor(coordinator, term),
        ]
    )

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

    @property
    def extra_state_attributes(self):
        return {
            "search_url": f"https://www.bazos.cz/search.php?hledat=%22{self._term}%22"
        }

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
