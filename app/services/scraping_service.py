from dataclasses import dataclass

import requests
from bs4 import BeautifulSoup


@dataclass
class ExchangeRateResult:
    base: str
    target: str
    rate: float
    source: str


class ExchangeRateScraper:
    @staticmethod
    def fetch_rate(base: str, target: str) -> ExchangeRateResult:
        base = base.upper().strip()
        target = target.upper().strip()

        if len(base) != 3 or len(target) != 3:
            raise ValueError("Currency codes must be 3 letters, e.g., USD, EUR")

        url = f"https://www.x-rates.com/table/?from={base}&amount=1"
        headers = {"User-Agent": "Mozilla/5.0 (ExpenseTracker/1.0)"}

        try:
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
        except requests.RequestException as exc:
            raise RuntimeError("Failed to fetch data from exchange rate source") from exc

        soup = BeautifulSoup(response.text, "html.parser")
        rows = soup.select("table.tablesorter.ratesTable tbody tr")

        for row in rows:
            currency_cell = row.select_one("td:nth-child(1)")
            rate_cell = row.select_one("td:nth-child(2) a")
            if not currency_cell or not rate_cell:
                continue

            currency_text = currency_cell.get_text(strip=True).upper()
            if target in currency_text:
                try:
                    rate = float(rate_cell.get_text(strip=True).replace(",", ""))
                    return ExchangeRateResult(base=base, target=target, rate=rate, source=url)
                except ValueError:
                    continue

        raise LookupError(f"Unable to find target currency '{target}' in scraped table")
