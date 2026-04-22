from homeassistant.components.button import ButtonEntity
from homeassistant.helpers.update_coordinator import CoordinatorEntity

from .const import DOMAIN


async def async_setup_entry(hass, entry, async_add_entities):
    coordinator = hass.data[DOMAIN][entry.entry_id]
    term = entry.data["search_term"]

    async_add_entities([
        BazosOpenSearchButton(coordinator, term)
    ])


class BazosOpenSearchButton(CoordinatorEntity, ButtonEntity):
    def __init__(self, coordinator, term: str):
        super().__init__(coordinator)
        self._term = term
        self._slug = "".join(c.lower() if c.isalnum() else "_" for c in term)

    @property
    def name(self):
        return f"Bazos {self._term} otevřít link"

    @property
    def unique_id(self):
        return f"{DOMAIN}_{self._slug}_open"

    async def async_press(self):
        url = f"https://www.bazos.cz/search.php?hledat=%22{self._term}%22"

        await self.hass.services.async_call(
            "browser_mod",
            "navigate",
            {"url": url},
            blocking=False,
        )
