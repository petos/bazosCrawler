import logging
import requests
import re
from datetime import datetime
from urllib.parse import quote

_LOGGER = logging.getLogger(__name__)

BASE_URL = "https://www.bazos.cz/search.php?hledat={term}&crz={offset}"
# ~ BASE_URL = "https://www.bazos.cz/search.php?hledat={term}&crz={offset}&hlokalita=&{psc}humkreis={okoli}&cenaod={cenaod}&cenado={cenado}"

class BazosApi:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update(
            {
                "User-Agent": (
                    "Mozilla/5.0 (X11; Linux x86_64) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) "
                    "Chrome/120.0 Safari/537.36"
                )
            }
        )

    # -------------------------
    # PUBLIC API
    # -------------------------
    def fetch(self, term: str):
        term = quote(f'"{term}"')

        offset = 0
        all_items = []
        seen = set()

        while True:
            url = BASE_URL.format(term=term, offset=offset)
            _LOGGER.debug("GET %s", url)

            r = self.session.get(url, timeout=10)
            html = r.text

            blocks = self._extract_blocks(html)

            _LOGGER.debug("Found blocks: %s", len(blocks))

            if not blocks:
                break

            new_count = 0

            for b in blocks:
                link = self._extract_link(b)
                item_id = self._extract_id(link)

                if not item_id:
                    _LOGGER.debug("Skipping block (no id): %s", str(b)[:200])
                    continue

                if item_id in seen:
                    continue

                seen.add(item_id)
                new_count += 1

                title = self._extract_title(b)
                date = self._extract_date(b)

                all_items.append(
                    {
                        "id": item_id,
                        "title": title,
                        "link": link,
                        "date": date,
                    }
                )

            _LOGGER.debug(
                "Page offset=%s new=%s total=%s",
                offset,
                new_count,
                len(all_items),
            )

            # pagination stop condition
            if len(blocks) < 20:
                break

            offset += 20

        _LOGGER.debug("Total unique items: %s", len(all_items))
        return {"items": all_items}

    # -------------------------
    # BLOCK EXTRACTION
    # -------------------------
    def _extract_blocks(self, html: str):
        """
        NOTE:
        intentionally NOT regex-based anymore for stability
        """
        from bs4 import BeautifulSoup

        soup = BeautifulSoup(html, "html.parser")
        return soup.select("div.inzeraty.inzeratyflex")

    # -------------------------
    # SELF-HEALING LINK
    # -------------------------
    def _extract_link(self, block):
        tag = block.select_one(".inzeratynadpis a")
        if tag and tag.get("href"):
            return tag.get("href")

        tag = block.select_one("a[href*='inzerat']")
        if tag and tag.get("href"):
            return tag.get("href")

        tag = block.find("a")
        if tag and tag.get("href"):
            return tag.get("href")

        return None

    # -------------------------
    # ID EXTRACTION
    # -------------------------
    def _extract_id(self, link: str):
        if not link:
            return None

        match = re.search(r"/(\d+)\.php", link)
        if match:
            return match.group(1)

        match = re.search(r"/(\d{6,})", link)
        if match:
            return match.group(1)

        return None

    # -------------------------
    # TITLE EXTRACTION
    # -------------------------
    def _extract_title(self, block):
        tag = block.select_one(".inzeratynadpis a")
        if tag:
            return tag.get_text(strip=True)

        tag = block.find("h2")
        if tag:
            return tag.get_text(strip=True)

        text = block.get_text(" ", strip=True)
        return text[:120] if text else ""

    # -------------------------
    # DATE EXTRACTION
    # -------------------------
    def _extract_date(self, block):
        text = block.get_text(" ", strip=True)

        match = re.search(
            r"\[(\d{1,2})\.(\d{1,2})\.\s*(\d{4})\]",
            text
        )

        if not match:
            return None

        d, m, y = map(int, match.groups())

        try:
            return datetime(y, m, d).date()
        except ValueError:
            return None
