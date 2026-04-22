import voluptuous as vol
from homeassistant import config_entries

from .const import DOMAIN, DEFAULT_UPDATE_INTERVAL

CONF_SEARCH_TERM = "search_term"
CONF_UPDATE_INTERVAL = "update_interval"


class BazosConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    async def async_step_user(self, user_input=None):
        errors = {}

        if user_input is not None:
            term = user_input[CONF_SEARCH_TERM].strip()

            await self.async_set_unique_id(term.lower())
            self._abort_if_unique_id_configured()

            return self.async_create_entry(
                title=f"Bazos: {term}",
                data={
                    CONF_SEARCH_TERM: term,
                    CONF_UPDATE_INTERVAL: user_input[CONF_UPDATE_INTERVAL],
                },
                options={},
            )

        schema = vol.Schema(
            {
                vol.Required(CONF_SEARCH_TERM): str,
                vol.Optional(CONF_UPDATE_INTERVAL, default=DEFAULT_UPDATE_INTERVAL): int,
            }
        )

        return self.async_show_form(step_id="user", data_schema=schema, errors=errors)

    @staticmethod
    def async_get_options_flow(config_entry):
        return BazosOptionsFlow(config_entry)


class BazosOptionsFlow(config_entries.OptionsFlow):
    def __init__(self, config_entry):
        self.config_entry = config_entry

    async def async_step_init(self, user_input=None):
        if user_input is not None:
            return self.async_create_entry(title="", data=user_input)

        schema = vol.Schema(
            {
                vol.Optional(
                    CONF_UPDATE_INTERVAL,
                    default=self.config_entry.options.get(
                        CONF_UPDATE_INTERVAL,
                        self.config_entry.data.get(
                            CONF_UPDATE_INTERVAL,
                            DEFAULT_UPDATE_INTERVAL,
                        ),
                    ),
                ): int
            }
        )

        return self.async_show_form(step_id="init", data_schema=schema)
