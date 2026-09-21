import asyncio
import os

import telegram
from dotenv import load_dotenv

from get_data import GoldPriceFetcher


load_dotenv(".env")


class GoldTelegramBot:
    TOKEN = os.getenv("TOKEN")
    CHAT_ID = os.getenv("CHAT_ID")

    def __init__(self):
        if not self.TOKEN:
            raise RuntimeError("TOKEN is not set")

        if not self.CHAT_ID:
            raise RuntimeError("CHAT_ID is not set")

        self.bot = telegram.Bot(token=self.TOKEN)
        self.chat_id = self.CHAT_ID
        self.fetcher = GoldPriceFetcher()
        self.data = {}

    def _format_message(self):
        current = self.data["current"] // 10
        low = self.data["low"] // 10
        high = self.data["high"] // 10

        return (
            "🪙 *قیمت طلای ۱۸ عیار*\n\n"
            f"💰 قیمت فعلی: `{current:,}` تومان\n"
            f"📉 کمترین امروز: `{low:,}` تومان\n"
            f"📈 بیشترین امروز: `{high:,}` تومان"
        )

    async def send(self):
        print("در حال دریافت قیمت طلا...")

        self.data = self.fetcher.get()

        print("Data:", self.data)

        message = self._format_message()

        await self.bot.send_message(
            chat_id=self.chat_id,
            text=message,
            parse_mode="Markdown"
        )

        print("پیام ارسال شد ✅")


async def main():
    bot = GoldTelegramBot()
    await bot.send()


if __name__ == "__main__":
    asyncio.run(main())