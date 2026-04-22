# bazosCrawler

Custom component pro Home Assistant – integrace bazosCrawler

## Instalace
- Přes HACS

  [![Open your Home Assistant instance and open a repository inside the Home Assistant Community Store.](https://my.home-assistant.io/badges/hacs_repository.svg)](https://my.home-assistant.io/redirect/hacs_repository/?owner=Petos&repository=ha-vodarenska)

  - Nainstalujte HACS
  - V HACS rozhraní kliknout v pravém horním rohu na tři svislé tečky
  - Kliknout na Vlastní repozitáře
  - Přidat adresu `https://github.com/petos/bazosCrawler` a typ `Integrace`
  - Po přidání repozitáře vyhledat `BazosCrawler` a nainstalovat
  - Po restartu Home Assistenta přidat jako Integraci v Nastavení -> Integrace
- Ručně:
  - `/config/custom_components/bazoscrawler/` + všechny soubory

## Senzory
 - `Celkem` -- Celkovy počet nalezených inzerátů s daným klíčovym slovem
 - `Dnes` -- Počet přidaných inzerátu dnes
 - `Nové dnes` -- Binární sensor - překlopí se do `True` ve chvíli, kdy najde nový, zatím neviděný inzerát. Při dalším běhu, ve výchozím nastavení 5 minut, se překlopí zpět do `False`. 

### Atributy


## Konfigurace
- Přes UI konfiguraci
- Automaticky vytvoří senzory
- Aktualizace hodnot probíhá jednou za 5 minut

## Hlášení chyb
Nejlépe přes https://github.com/petos/bazosCrawler/issues
