from aiogram import Bot, Dispatcher, types
import asyncio
import os

TOKEN = ("8231069817:AAGMIZ_8X5fmG7z9W2a06a__COSSjJAU5NI")

bot = Bot(token=TOKEN)
dp = Dispatcher()

@dp.message()
async def start(message: types.Message):
    await message.answer("Jarvis на связи 🔥 Я готов работать!")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
