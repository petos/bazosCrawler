import requests
import re
import logging
from urllib.parse import quote
from datetime import datetime

_LOGGER = logging.getLogger(__name__)

HEADERS = {
    "User-Agent": "Mozilla/5.0"
}


class BazosApi:
    PAGE_SIZE = 20
    MAX_PAGES = 25

    def fetch(self, term: str, exact: bool = True) -> list[dict]:
        """Public method: returns deduplicated list of items."""
        all_items = []
        seen_ids = set()

        offset = 0
        page = 0

        while True:
            html = self._fetch_page(term, offset, exact)
            items = self._parse(html, term)

            _LOGGER.debug(
                "Page %s: fetched=%s unique=%s",
                page, len(items), len(seen_ids)
            )

            new_items = []
            for item in items:
                item_id = item.get("id")
                if item_id and item_id not in seen_ids:
                    seen_ids.add(item_id)
                    new_items.append(item)

            all_items.extend(new_items)

            # stop conditions
            if len(items) < self.PAGE_SIZE:
                break

            if not new_items:
                break

            page += 1
            if page >= self.MAX_PAGES:
                _LOGGER.warning("Paging limit reached")
                break

            offset += self.PAGE_SIZE

        _LOGGER.debug("Total unique items: %s", len(all_items))
        return all_items

    def _fetch_page(self, term: str, offset: int, exact: bool) -> str:
        q = quote(f'"{term}"' if exact else term)
        url = f"https://www.bazos.cz/search.php?hledat={q}&crz={offset}"

        _LOGGER.debug("GET %s", url)

        r = requests.get(url, headers=HEADERS, timeout=20)
        r.raise_for_status()

        return r.text

    def _parse(self, html: str, term: str) -> list[dict]:
        items = []

        blocks = re.findall(
            r'<div class="inzeraty inzeratyflex">(.*?)</div>\s*</div>',
            html,
            re.S,
        )

        _LOGGER.debug("Found blocks: %d", len(blocks))

        for b in blocks:
            link_match = re.search(
                r'href="([^"]+/inzerat/(\d+)/[^"]+)"',
                b
            )

            if not link_match:
                continue

            name_match = re.search(
                r'<h2 class=nadpis><a[^>]*>(.*?)</a>',
                b
            )

            price_match = re.search(
                r'<div class="inzeratycena">(.*?)</div>',
                b,
                re.S,
            )

            date = self._parse_date(b)

            items.append({
                "id": link_match.group(2),
                "link": link_match.group(1),
                "name": re.sub(r"<.*?>", "", name_match.group(1)) if name_match else "",
                "price": price_match.group(1).strip() if price_match else "",
                "date": date,
                "keyword": term,
            })

        return items

    def _parse_date(self, block: str):
        match = re.search(r"\[(\d{1,2}\.\d{1,2}\.\s*\d{4})\]", block)
        if not match:
            return None

        raw = match.group(1).replace(" ", "")  # e.g. 21.4.2026

        try:
            return datetime.strptime(raw, "%d.%m.%Y").date()
        except ValueError:
            _LOGGER.debug("Failed to parse date: %s", raw)
            return None
