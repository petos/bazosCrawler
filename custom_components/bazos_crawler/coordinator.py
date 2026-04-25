from datetime import timedelta
from urllib.parse import quote

from homeassistant.helpers.update_coordinator import DataUpdateCoordinator

from .const import (
    DOMAIN,
    BASE_URL,
    CONF_SEARCH_TERM,
    CONF_PSC,
    CONF_OKOLI,
    CONF_CENAOD,
    CONF_CENADO,
    CONF_SEARCH_EXACT,
    CONF_UPDATE_INTERVAL,
)


def build_url(exact: bool, term: str, psc, okoli, cenaod, cenado):
    if exact:
        term = quote(f'"{term}"')

    return BASE_URL.format(
        term=term,
        psc=psc or "",
        okoli=okoli or "",
        cenaod=cenaod or "",
        cenado=cenado or "",
    )


class BazosDataUpdateCoordinator(DataUpdateCoordinator):
    def __init__(self, hass, config_entry, api):
        self.config_entry = config_entry
        self.api = api

        update_interval = config_entry.options.get(
            CONF_UPDATE_INTERVAL,
            config_entry.data.get(CONF_UPDATE_INTERVAL),
        )

        super().__init__(
            hass,
            logger=__import__(__name__).__dict__.get("LOGGER"),
            name=DOMAIN,
            update_interval=timedelta(seconds=update_interval),
        )

    @property
    def url(self):
        data = self.config_entry.data
        options = self.config_entry.options

        return build_url(
            options.get(CONF_SEARCH_EXACT, data.get(CONF_SEARCH_EXACT)),
            data.get(CONF_SEARCH_TERM),
            options.get(CONF_PSC, data.get(CONF_PSC)),
            options.get(CONF_OKOLI, data.get(CONF_OKOLI)),
            options.get(CONF_CENAOD, data.get(CONF_CENAOD)),
            options.get(CONF_CENADO, data.get(CONF_CENADO)),
        )

    async def _async_update_data(self):
        url = self.url

        # DEBUG (doporučeno)
        self.logger.debug("Fetching URL: %s", url)

        return await self.api.fetch(url)
