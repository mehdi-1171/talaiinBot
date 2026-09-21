import requests
from bs4 import BeautifulSoup


class GoldPriceFetcher:
    URL = "https://www.tgju.org/profile/geram18"

    def get(self):
        response = requests.get(
            self.URL,
            headers={
                "User-Agent": (
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                    "AppleWebKit/537.36 Chrome/125 Safari/537.36"
                )
            },
            timeout=20
        )

        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")

        text = soup.get_text(" ", strip=True)

        current = self._extract(text, "نرخ فعلی")
        high = self._extract(text, "بالاترین قیمت روز")
        low = self._extract(text, "پایین ترین قیمت روز")

        return {
            "current": current,
            "low": low,
            "high": high,
        }

    def _extract(self, text, label):
        index = text.find(label)

        if index == -1:
            raise RuntimeError(f"{label} not found")

        part = text[index:index + 100]

        import re

        match = re.search(r"\d[\d,]+", part)

        if not match:
            raise RuntimeError(f"value for {label} not found")

        return int(match.group().replace(",", ""))


if __name__ == "__main__":
    gold = GoldPriceFetcher().get()

#
# class GoldPriceFetcher:
#
#     API_URL = "https://my.tlyn.ir/api/v1/get-price"
#     TEHRAN_OFFSET = timedelta(hours=3, minutes=30)
#
#     def _fetch_raw(self):
#         res = requests.get(
#             self.API_URL,
#             headers={"User-Agent": "Mozilla/5.0"},
#             timeout=10
#         )
#         res.raise_for_status()
#         return res.json()
#
#     def _parse(self, data):
#         items = data['prices'][0]
#         results = []
#
#         for item in items:
#             dt_utc = datetime.fromisoformat(item['price']['date_time'].replace('Z', '+00:00'))
#             dt_tehran = dt_utc + self.TEHRAN_OFFSET
#
#             results.append({
#                 "symbol": item['symbol'],
#                 "title": item['title'],
#                 "sell": f"{item['price']['sell'] // 10:,}",
#                 "buy": f"{item['price']['buy'] // 10:,}",
#                 "max_buy": f"{item['max_price']['buy'] // 10:,}",
#                 "min_buy": f"{item['min_price']['buy'] // 10:,}",
#                 "updated_at": dt_tehran.strftime('%H:%M:%S - %Y/%m/%d'),
#             })
#
#         return results
#
#     def get(self):
#         raw = self._fetch_raw()
#         return self._parse(raw)
#
#
