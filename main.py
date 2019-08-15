from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor

from config import TOKEN
import keyboard
import func


bot = Bot(token=TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    if func.chat_id_found(message.chat.id):
        await message.reply("Рад снова Вас видеть!", reply = False)
    else:
        await message.reply("Добро пожаловать!", reply = False)
        func.chat_id_add(message.chat.id)


@dp.message_handler(commands=['help'])
async def process_help_command(message: types.Message):
    await message.reply("Напиши мне что-нибудь, и я отпрпавлю этот текст тебе в ответ!")


@dp.message_handler()
async def echo_message(msg: types.Message):
    await bot.send_message(msg.from_user.id, msg.text, reply_markup=keyboard.reply([["📄 Меню", "🍱 Корзина"], ["👤 Профиль", "💬 Помощь"]] ))


if __name__ == '__main__':
    executor.start_polling(dp)
