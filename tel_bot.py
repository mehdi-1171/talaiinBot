import asyncio
import telegram
from dotenv import load_dotenv
import os

from get_data import GoldPriceFetcher


load_dotenv()


class GoldTelegramBot:
    TOKEN = os.getenv("TOKEN")
    CHAT_ID = os.getenv("CHAT_ID")

    def __init__(self):
        self.bot = telegram.Bot(token=self.TOKEN)
        self.chat_id = self.CHAT_ID
        self.fetcher = GoldPriceFetcher()
        self.data = []

    def _format_message(self):
        msg = ""
        for item in self.data:
            msg += f"📊 *{item['title']}*\n"
            msg += f"💰 قیمت خرید: `{item['buy']}` تومان\n"
            msg += f"💸 قیمت فروش: `{item['sell']}` تومان\n"
            msg += f"📈 بیشترین امروز: `{item['max_buy']}` تومان\n"
            msg += f"📉 کمترین امروز: `{item['min_buy']}` تومان\n"
            msg += f"🕐 آخرین بروزرسانی: {item['updated_at']}\n"
        return msg

    async def send(self):
        self.data = self.fetcher.get()
        message = self._format_message()
        await self.bot.send_message(
            chat_id=self.chat_id,
            text=message,
            parse_mode="Markdown"
        )
        print("پیام ارسال شد ✅")


bot = GoldTelegramBot()
asyncio.run(bot.send())