import logging
from datetime import timedelta
from urllib.parse import quote

from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .const import DOMAIN, DEFAULT_UPDATE_INTERVAL, BASE_URL, CONF_UPDATE_INTERVAL
from .const import CONF_SEARCH_TERM, CONF_PSC, CONF_OKOLI, CONF_CENAOD, CONF_CENADO

from .api import BazosApi

_LOGGER = logging.getLogger(__name__)


class BazosDataUpdateCoordinator(DataUpdateCoordinator):
    def __init__(self, hass, entry):
        self.hass = hass
        self.entry = entry

        update_interval = entry.options.get(
            CONF_UPDATE_INTERVAL,
            entry.data.get(CONF_UPDATE_INTERVAL, DEFAULT_UPDATE_INTERVAL),
        )

        self.api = BazosApi()

        super().__init__(
            hass,
            _LOGGER,
            name=f"{DOMAIN}_{entry.entry_id}",
            update_interval=timedelta(seconds=update_interval),
        )

    async def _async_update_data(self):
        try:
            term = self.entry.data[CONF_SEARCH_TERM]
            psc = self.entry.data[CONF_PSC]
            okoli = self.entry.data[CONF_OKOLI]
            cenaod = self.entry.data[CONF_CENAOD]
            cenado = self.entry.data[CONF_CENADO]

            url=self.url_builder(term, psc, okoli, cenaod, cenado)

            return await self.hass.async_add_executor_job(
                self.api.fetch,
                url
            )

        except Exception as err:
            _LOGGER.exception("Fetch failed")
            raise UpdateFailed(err)

    def url_builder(self, term: str, psc: int, okoli: int, cenaod: int, cenado: int):
        term = quote(f'"{term}"')
        return BASE_URL.format(term=term, psc=psc, okoli=okoli, cenaod=cenaod, cenado=cenado)
