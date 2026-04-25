import voluptuous as vol
from homeassistant import config_entries
from homeassistant.helpers import config_validation as cv

from .const import DOMAIN, DEFAULT_UPDATE_INTERVAL, CONF_UPDATE_INTERVAL
from .const import CONF_SEARCH_TERM, CONF_PSC, CONF_OKOLI, CONF_CENAOD, CONF_CENADO, CONF_SEARCH_EXACT


def _parse_optional_int(value, field):
    """Convert empty string to '' and validate int if provided.

    Raises ValueError(field) to allow precise error mapping.
    """
    value = (value or "").strip()
    if value == "":
        return ""
    try:
        return int(value)
    except ValueError:
        raise ValueError(field)


def _validate_psc(psc):
    """Validate PSC is 5-digit number."""
    if psc == "":
        return True
    return 10000 <= psc <= 99999


class BazosConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    VERSION = 1

    async def async_step_user(self, user_input=None):
        errors = {}

        schema = vol.Schema(
            {
                vol.Required(CONF_SEARCH_TERM): str,
                vol.Optional(CONF_UPDATE_INTERVAL, default=DEFAULT_UPDATE_INTERVAL): cv.positive_int,
                vol.Optional(CONF_SEARCH_EXACT, default=False): bool,
                vol.Optional(CONF_PSC, default=""): str,
                vol.Optional(CONF_OKOLI, default="25"): str,
                vol.Optional(CONF_CENAOD, default=""): str,
                vol.Optional(CONF_CENADO, default=""): str,
            }
        )

        if user_input is not None:
            term = user_input[CONF_SEARCH_TERM].strip()

            # --- manual validation per field ---
            try:
                psc = _parse_optional_int(user_input.get(CONF_PSC), CONF_PSC)
                if not _validate_psc(psc):
                    errors[CONF_PSC] = "invalid_psc"
            except ValueError as e:
                errors[e.args[0]] = "invalid_number"
                psc = ""

            try:
                okoli = _parse_optional_int(user_input.get(CONF_OKOLI), CONF_OKOLI)
            except ValueError as e:
                errors[e.args[0]] = "invalid_number"
                okoli = ""

            try:
                cenaod = _parse_optional_int(user_input.get(CONF_CENAOD), CONF_CENAOD)
            except ValueError as e:
                errors[e.args[0]] = "invalid_number"
                cenaod = ""

            try:
                cenado = _parse_optional_int(user_input.get(CONF_CENADO), CONF_CENADO)
            except ValueError as e:
                errors[e.args[0]] = "invalid_number"
                cenado = ""

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
                        CONF_SEARCH_EXACT: user_input.get(CONF_SEARCH_EXACT, False),
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
                ): cv.positive_int,
                vol.Optional(
                    CONF_SEARCH_EXACT,
                    default=self.config_entry.options.get(
                        CONF_SEARCH_EXACT,
                        self.config_entry.data.get(CONF_SEARCH_EXACT, False),
                    ),
                ): bool,
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
                psc = _parse_optional_int(user_input.get(CONF_PSC), CONF_PSC)
                if not _validate_psc(psc):
                    errors[CONF_PSC] = "invalid_psc"
            except ValueError as e:
                errors[e.args[0]] = "invalid_number"
                psc = ""

            try:
                okoli = _parse_optional_int(user_input.get(CONF_OKOLI), CONF_OKOLI)
            except ValueError as e:
                errors[e.args[0]] = "invalid_number"
                okoli = ""

            try:
                cenaod = _parse_optional_int(user_input.get(CONF_CENAOD), CONF_CENAOD)
            except ValueError as e:
                errors[e.args[0]] = "invalid_number"
                cenaod = ""

            try:
                cenado = _parse_optional_int(user_input.get(CONF_CENADO), CONF_CENADO)
            except ValueError as e:
                errors[e.args[0]] = "invalid_number"
                cenado = ""

            if not errors:
                return self.async_create_entry(
                    title="",
                    data={
                        CONF_UPDATE_INTERVAL: user_input.get(
                            CONF_UPDATE_INTERVAL, DEFAULT_UPDATE_INTERVAL
                        ),
                        CONF_SEARCH_EXACT: user_input.get(CONF_SEARCH_EXACT, False),
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
