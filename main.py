import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton, FSInputFile

API_TOKEN = '7091257664:AAFYbb09SL99Y15b3iS3gUAemSs9gDnySgg'

bot = Bot(token=API_TOKEN)
dp = Dispatcher()

# Добавляем команды в меню
async def set_commands(bot: Bot):
    commands = [
        types.BotCommand(command="/start", description="Запустить бота | Главное меню")
    ]
    await bot.set_my_commands(commands)

@dp.message(Command("start"))
async def start_command(message: types.Message):
    user_name = message.from_user.first_name  # Имя пользователя
    gif_path = 'media/Welcome.gif'  # Относительный путь к GIF

    # Создаем обычные кнопки под полем ввода
    keyboard = [
        [InlineKeyboardButton(text="💲 Курс доллара", callback_data="dollar_cost")],
        [InlineKeyboardButton(text="💱 Выбрать пару обмена", callback_data="dollar_cost")],
        [InlineKeyboardButton(text="📞 Связаться со мной", url="https://example.com")],
        [
            InlineKeyboardButton(text="👤 Профиль", callback_data="dollar_cost"),
            InlineKeyboardButton(text="ℹ️ О FoyDyabaBot", callback_data="dollar_cost")
         ]  # Две кнопки в одной строке
    ]
    inline_keyboard = InlineKeyboardMarkup(row_width=2, inline_keyboard=keyboard)

    # Отправляем сообщение с обычными кнопками
    gif_file = FSInputFile(gif_path)
    await message.answer_animation(animation=gif_file, caption=f"👋 Рад видеть тебя, @{user_name}", reply_markup=inline_keyboard)

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
