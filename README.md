# HA Vodarenska

Custom component pro Home Assistant – integrace s VAS Vodárenská API.

## Instalace
- Přes HACS

  [![Open your Home Assistant instance and open a repository inside the Home Assistant Community Store.](https://my.home-assistant.io/badges/hacs_repository.svg)](https://my.home-assistant.io/redirect/hacs_repository/?owner=Petos&repository=ha-vodarenska)

  - Nainstalujte HACS
  - V HACS rozhraní kliknout v pravém horním rohu na tři svislé tečky
  - Kliknout na Vlastní repozitáře
  - Přidat adresu `https://github.com/petos/` a typ `Integrace`
  - Po přidání repozitáře vyhledat `BazosCrowler` a nainstalovat
  - Po restartu Home Assistenta přidat jako Integraci v Nastavení -> Integrace
- Ručně:
  - `/config/custom_components/bazoscrowler/` + všechny soubory

## Senzory
- `sensor.vec`: stav vodomeru

### Atributy


## Konfigurace
- Přes UI konfiguraci
- Automaticky vytvoří senzory
- Aktualizace hodnot probíhá jednou za 5 minut

## HelloWorld
- Existuje a je nadefinovany sensor pro HelloWorld, ktery je ovsem deaktivovany (disabled). Slouží především pro debug při problémy s API. 

## Hlášení chyb
Nejlépe přes https://github.com/petos/bazoscrowler/issues
