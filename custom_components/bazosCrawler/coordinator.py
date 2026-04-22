from __future__ import annotations

import logging
from datetime import timedelta

from homeassistant.core import HomeAssistant
from homeassistant.config_entries import ConfigEntry
from homeassistant.helpers.update_coordinator import DataUpdateCoordinator, UpdateFailed

from .const import DOMAIN, DEFAULT_UPDATE_INTERVAL
from .api import BazosApi

_LOGGER = logging.getLogger(__name__)


class BazosDataUpdateCoordinator(DataUpdateCoordinator):
    def __init__(self, hass: HomeAssistant, entry: ConfigEntry):
        self.hass = hass
        self.entry = entry
        self.api = BazosApi()

        update_interval = entry.options.get(
            "update_interval",
            entry.data.get("update_interval", DEFAULT_UPDATE_INTERVAL),
        )

        super().__init__(
            hass,
            _LOGGER,
            name=DOMAIN,
            update_interval=timedelta(seconds=update_interval),
        )

    async def _async_update_data(self):
        term = self.entry.data["search_term"]

        try:
            items = await self.hass.async_add_executor_job(
                self.api.fetch,
                term,
                True,
            )

            return {
                "items": items
            }

        except Exception as err:
            raise UpdateFailed(f"Error fetching data: {err}") from err
