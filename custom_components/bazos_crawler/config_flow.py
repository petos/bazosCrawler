import voluptuous as vol
from homeassistant import config_entries

from .const import DOMAIN, DEFAULT_UPDATE_INTERVAL, CONF_UPDATE_INTERVAL
from .const import CONF_SEARCH_TERM, CONF_PSC, CONF_OKOLI, CONF_CENAOD, CONF_CENADO


def _parse_optional_int(value):
    """Convert empty string to '' and validate int if provided."""
    value = (value or "").strip()
    if value == "":
        return ""
    try:
        return int(value)
    except ValueError:
        raise ValueError


class BazosConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    async def async_step_user(self, user_input=None):
        errors = {}

        schema = vol.Schema(
            {
                vol.Required(CONF_SEARCH_TERM): str,
                vol.Optional(CONF_UPDATE_INTERVAL, default=DEFAULT_UPDATE_INTERVAL): int,
                vol.Optional(CONF_PSC, default=""): str,
                vol.Optional(CONF_OKOLI, default=""): str,
                vol.Optional(CONF_CENAOD, default=""): str,
                vol.Optional(CONF_CENADO, default=""): str,
            }
        )

        if user_input is not None:
            term = user_input[CONF_SEARCH_TERM].strip()

            # --- manual validation ---
            try:
                psc = _parse_optional_int(user_input.get(CONF_PSC))
                okoli = _parse_optional_int(user_input.get(CONF_OKOLI))
                cenaod = _parse_optional_int(user_input.get(CONF_CENAOD))
                cenado = _parse_optional_int(user_input.get(CONF_CENADO))
            except ValueError:
                errors["base"] = "invalid_number"

            if not term:
                errors[CONF_SEARCH_TERM] = "empty"

            if not errors:
                await self.async_set_unique_id(term.lower())
                self._abort_if_unique_id_configured()

                return self.async_create_entry(
                    title=f"Bazos: {term}",
                    data={
                        CONF_SEARCH_TERM: term,
                        CONF_UPDATE_INTERVAL: user_input.get(
                            CONF_UPDATE_INTERVAL, DEFAULT_UPDATE_INTERVAL
                        ),
                        CONF_PSC: psc,
                        CONF_OKOLI: okoli,
                        CONF_CENAOD: cenaod,
                        CONF_CENADO: cenado,
                    },
                    options={},
                )

        return self.async_show_form(
            step_id="user",
            data_schema=schema,
            errors=errors,
        )

    @staticmethod
    def async_get_options_flow(config_entry):
        return BazosOptionsFlow(config_entry)


class BazosOptionsFlow(config_entries.OptionsFlow):
    def __init__(self, config_entry):
        self.config_entry = config_entry

    async def async_step_init(self, user_input=None):
        errors = {}

        schema = vol.Schema(
            {
                vol.Optional(
                    CONF_UPDATE_INTERVAL,
                    default=self.config_entry.options.get(
                        CONF_UPDATE_INTERVAL,
                        self.config_entry.data.get(
                            CONF_UPDATE_INTERVAL, DEFAULT_UPDATE_INTERVAL
                        ),
                    ),
                ): int,
                vol.Optional(
                    CONF_PSC,
                    default=str(self.config_entry.options.get(CONF_PSC, "")),
                ): str,
                vol.Optional(
                    CONF_OKOLI,
                    default=str(self.config_entry.options.get(CONF_OKOLI, "")),
                ): str,
                vol.Optional(
                    CONF_CENAOD,
                    default=str(self.config_entry.options.get(CONF_CENAOD, "")),
                ): str,
                vol.Optional(
                    CONF_CENADO,
                    default=str(self.config_entry.options.get(CONF_CENADO, "")),
                ): str,
            }
        )

        if user_input is not None:
            try:
                psc = _parse_optional_int(user_input.get(CONF_PSC))
                okoli = _parse_optional_int(user_input.get(CONF_OKOLI))
                cenaod = _parse_optional_int(user_input.get(CONF_CENAOD))
                cenado = _parse_optional_int(user_input.get(CONF_CENADO))
            except ValueError:
                errors["base"] = "invalid_number"

            if not errors:
                return self.async_create_entry(
                    title="",
                    data={
                        CONF_UPDATE_INTERVAL: user_input.get(
                            CONF_UPDATE_INTERVAL, DEFAULT_UPDATE_INTERVAL
                        ),
                        CONF_PSC: psc,
                        CONF_OKOLI: okoli,
                        CONF_CENAOD: cenaod,
                        CONF_CENADO: cenado,
                    },
                )

        return self.async_show_form(
            step_id="init",
            data_schema=schema,
            errors=errors,
        )
