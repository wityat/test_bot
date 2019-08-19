from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram.types import ParseMode, ContentTypes
from aiogram.utils.markdown import bold, code, italic, text

from config import TOKEN
import keyboard
import func



bot = Bot(token=TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(lambda message: func.chat_id_found(message.chat.id) == False, commands=['start'])
async def welcome_message(message: types.Message):
    func.chat_id_add(message.chat.id)
    func.column_add(message.chat.id, "state", 1234)
    await message.reply("Добро пожаловать!\nПеред Вами *сервис доставки еды на дом*.", reply = False, parse_mode=ParseMode.MARKDOWN)
    await full_name_request(message)
    
@dp.message_handler(lambda message: func.column_take(message.chat.id, "state") == 1234, commands=['start'])
async def full_name_request(message: types.Message):
    full_name = func.check_full_name(message.chat.first_name + " " + message.chat.last_name) if "last_name" in message.chat else None
    if full_name:
        first_name, last_name = full_name
        await message.reply('Вы *%s %s*?\nЕсли имя-фамилия определены неверно, пожалуйста, *напишите правильные* в формате: *Имя Фамилия*.\nЕсли все верно, нажмите "Далее" под этим сообщением\n' % (first_name, last_name), reply = False, parse_mode=ParseMode.MARKDOWN, reply_markup=keyboard.inline("Далее", "#setstate@1235"))
    else:
        await message.reply('Пожалуйста, *напишите имя и фамилию* в формате: *Имя Фамилия*.\n', reply = False, parse_mode=ParseMode.MARKDOWN)

@dp.message_handler(lambda message: func.column_take(message.chat.id, "state") == 1235, commands=['start'])
async def phone_number_again(message: types.Message):
    await message.reply("Для взаимодействия на всех этапах работы с ботом может понадобиться Ваш номер телефона.\nПожалуйста, нажмите на кнопку \"*Поделиться номером*\".", parse_mode=ParseMode.MARKDOWN, reply_markup = keyboard.phone_number("Поделиться номером 📲"), reply = False)

@dp.message_handler(lambda message: func.column_take(message.chat.id, "state") == 1236, commands=['start'])
async def welcome_again(message: types.Message):
    await message.reply("Рад снова Вас видеть, %s!\nПеред Вами *сервис доставки еды на дом*." % (func.column_take(message.chat.id, "first_name")), reply = False, parse_mode=ParseMode.MARKDOWN)

# @dp.message_handler(commands=['help'])
# async def process_help_command(message: types.Message):
#     await message.reply("Напиши мне что-нибудь, и я отправлю этот текст тебе в ответ!")

@dp.message_handler(content_types=ContentTypes.CONTACT)
async def get_contact(message: types.Message):
    if func.column_take(message.chat.id, "state") != 1235: return 0
    func.column_add(message.chat.id, "state", 1236)
    func.column_add(message.chat.id, "phone", message.contact["phone_number"])
    await bot.send_message(message.chat.id, "Спасибо за регистрацию! Теперь Вы можете полноценно пользоваться сервисом!", reply_markup = keyboard.remove())



@dp.message_handler(lambda message: func.column_take(message.chat.id, "state") == 1234)
async def text_message1(message: types.Message):
    full_name = func.check_full_name(message.text)
    if full_name:
        first_name, last_name = full_name
        func.column_add(message.chat.id, "first_name", first_name)
        func.column_add(message.chat.id, "last_name", last_name)
        await take_phone(message)
    else:
        await bot.send_message(message.chat.id, "Неверный формат. Попробуйте снова.")

@dp.message_handler()
async def text_message(message: types.Message):
    await bot.send_message(message.chat.id, message.text, reply_markup=keyboard.reply([["📄 Меню", "🍱 Корзина"], ["👤 Профиль", "💬 Помощь"]] ))


@dp.callback_query_handler(lambda callback_query: "#setstate@1235" in callback_query.data and func.column_take(message.chat.id, "state") == 1234)
async def take_phone_callback(callback: types.CallbackQuery):
    message = callback.message; await callback.answer()
    full_name = func.check_full_name(message.chat.first_name + " " + message.chat.last_name)
    first_name, last_name = full_name
    func.column_add(message.chat.id, "first_name", first_name)
    func.column_add(message.chat.id, "last_name", last_name)
    await take_phone(message)

async def take_phone(message: types.Message):
    func.column_add(message.chat.id, "state", 1235)
    await message.reply("Для взаимодействия на всех этапах работы с ботом может понадобиться Ваш номер телефона.\nПожалуйста, нажмите на кнопку \"*Поделиться номером*\".", parse_mode=ParseMode.MARKDOWN, reply_markup = keyboard.phone_number("Поделиться номером 📲"), reply = False)


@dp.callback_query_handler()
async def any_callback(callback: types.CallbackQuery):
    message = callback.message
    user_id, message_id = message.chat.id, message.message_id
    await bot.send_message(user_id, "callback: " + callback.data)

if __name__ == '__main__':
    executor.start_polling(dp)
