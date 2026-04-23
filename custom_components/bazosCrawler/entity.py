from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN


class BazosEntity(CoordinatorEntity):
    def __init__(self, coordinator, term):
        super().__init__(coordinator)
        self._term = term
        self._slug = "".join(c.lower() if c.isalnum() else "_" for c in term)

    @property
    def device_info(self):
        return {
            "identifiers": {(DOMAIN, self.coordinator.entry.entry_id)},
            "name": f"Bazos {self._term}",
            "manufacturer": "BazosCrawler",
            "model": "Search",
        }
