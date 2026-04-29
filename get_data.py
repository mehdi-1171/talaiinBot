import requests
from datetime import datetime, timedelta


class GoldPriceFetcher:

    API_URL = "https://my.tlyn.ir/api/v1/get-price"
    TEHRAN_OFFSET = timedelta(hours=3, minutes=30)

    def _fetch_raw(self):
        res = requests.get(
            self.API_URL,
            headers={"User-Agent": "Mozilla/5.0"},
            timeout=10
        )
        res.raise_for_status()
        return res.json()

    def _parse(self, data):
        items = data['prices'][0]
        results = []

        for item in items:
            dt_utc = datetime.fromisoformat(item['price']['date_time'].replace('Z', '+00:00'))
            dt_tehran = dt_utc + self.TEHRAN_OFFSET

            results.append({
                "symbol": item['symbol'],
                "title": item['title'],
                "sell": f"{item['price']['sell'] // 10:,}",
                "buy": f"{item['price']['buy'] // 10:,}",
                "max_buy": f"{item['max_price']['buy'] // 10:,}",
                "min_buy": f"{item['min_price']['buy'] // 10:,}",
                "updated_at": dt_tehran.strftime('%H:%M:%S - %Y/%m/%d'),
            })

        return results

    def get(self):
        raw = self._fetch_raw()
        return self._parse(raw)


