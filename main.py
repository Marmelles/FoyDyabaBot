import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton

API_TOKEN = '7091257664:AAFYbb09SL99Y15b3iS3gUAemSs9gDnySgg'

bot = Bot(token=API_TOKEN)
dp = Dispatcher()

# Добавляем команды в меню
async def set_commands(bot: Bot):
    commands = [
        types.BotCommand(command="/start", description="Запустить бота"),
        types.BotCommand(command="/help", description="Помощь"),
        types.BotCommand(command="/menu", description="Открыть меню")
    ]
    await bot.set_my_commands(commands)

@dp.message(Command("menu"))
async def menu_command(message: types.Message):
    # Создаем обычные кнопки под полем ввода
    reply_keyboard = ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="Кнопка 1")],
            [KeyboardButton(text="Кнопка 2")],
            [KeyboardButton(text="Кнопка 3"), KeyboardButton(text="Кнопка 4")]  # Две кнопки в одной строке
        ],
        resize_keyboard=True  # Уменьшаем размер кнопок
    )

    # Отправляем сообщение с обычными кнопками
    await message.answer("Выберите действие:", reply_markup=reply_keyboard)

# Инлайн-кнопки под сообщением
@dp.message(Command("start"))
async def start_command(message: types.Message):
    # Создаем инлайн-клавиатуру с кнопками
    inline_kb_list = [
        [InlineKeyboardButton(text="Мой хабр", callback_data="Мой хабр")],
        [InlineKeyboardButton(text="Тук тук", callback_data="Тук тук")],
        [
            InlineKeyboardButton(text="Мой хабр", url='https://habr.com/ru/users/yakvenalex/'),
            InlineKeyboardButton(text="Мой Telegram", url='tg://resolve?domain=yakvenalexx')
        ],
    ]
    inline_keyboard = InlineKeyboardMarkup(row_width=2, inline_keyboard=inline_kb_list)  # Указываем, что максимум 2 кнопки в строке

    # Отправляем сообщение с инлайн-кнопками
    await message.answer("Выберите страну:", reply_markup=inline_keyboard)

# Хэндлер для обработки нажатий на инлайн-кнопки
@dp.callback_query()
async def handle_callback(query: types.CallbackQuery):
    await query.message.answer(f"Вы выбрали {query.data}")
    await query.answer()  # Чтобы закрыть индикатор загрузки

async def main():
    try:
        await set_commands(bot)
        await dp.start_polling(bot)
    except Exception as e:
        print(f"Polling error: {e}")
    finally:
        await bot.session.close()

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        print("Bot stopped")
