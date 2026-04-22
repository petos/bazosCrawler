import logging
import requests
import re
from datetime import datetime

_LOGGER = logging.getLogger(__name__)

BASE_URL = "https://www.bazos.cz/search.php?hledat={term}&crz={offset}"


class BazosApi:
    def __init__(self):
        self.session = requests.Session()

    def fetch(self, term: str):
        term = requests.utils.quote(f'"{term}"')

        offset = 0
        all_items = []
        seen = set()

        while True:
            url = BASE_URL.format(term=term, offset=offset)
            _LOGGER.debug("GET %s", url)

            r = self.session.get(url, timeout=10)
            html = r.text

            blocks = re.findall(r'<div class="inzeraty inzeratyflex">(.*?)</div>', html, re.S)

            _LOGGER.debug("Found blocks: %s", len(blocks))

            if not blocks:
                break

            new_count = 0

            for b in blocks:
                href = re.search(r'href="([^"]+)"', b)
                if not href:
                    continue

                link = href.group(1)
                id_match = re.search(r"/(\d+)\.php", link)

                if not id_match:
                    continue

                item_id = id_match.group(1)

                if item_id in seen:
                    continue

                seen.add(item_id)
                new_count += 1

                title = re.search(r'class="nadpis".*?>(.*?)</a>', b, re.S)
                title = title.group(1).strip() if title else ""

                date_match = re.search(r"\[(\d{1,2})\.(\d{1,2})\.\s*(\d{4})\]", b)
                date = None
                if date_match:
                    d, m, y = map(int, date_match.groups())
                    date = datetime(y, m, d).date()

                all_items.append(
                    {
                        "id": item_id,
                        "title": title,
                        "link": link,
                        "date": date,
                    }
                )

            _LOGGER.debug("Page offset=%s new=%s total=%s", offset, new_count, len(all_items))

            if len(blocks) < 20:
                break

            offset += 20

        _LOGGER.debug("Total unique items: %s", len(all_items))
        return {"items": all_items}
