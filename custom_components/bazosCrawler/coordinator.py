import logging
from datetime import timedelta

from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .const import DOMAIN, DEFAULT_UPDATE_INTERVAL
from .api import BazosApi

_LOGGER = logging.getLogger(__name__)


class BazosDataUpdateCoordinator(DataUpdateCoordinator):
    def __init__(self, hass, entry):
        self.hass = hass
        self.entry = entry

        update_interval = entry.options.get(
            "update_interval",
            entry.data.get("update_interval", DEFAULT_UPDATE_INTERVAL),
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
            term = self.entry.data["search_term"]

            return await self.hass.async_add_executor_job(
                self.api.fetch,
                term,
            )

        except Exception as err:
            _LOGGER.exception("Fetch failed")
            raise UpdateFailed(err)
