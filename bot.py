import os
import asyncio
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import CommandStart
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from aiohttp import web
import edge_tts

# Инициализация бота
BOT_TOKEN = os.getenv("BOT_TOKEN")
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# Главное меню с кнопками
def get_main_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🧠 Гипнотерапия", callback_data="hypno")],
        [InlineKeyboardButton(text="🧘‍♂️ Кармакоррекция", callback_data="karma")],
        [InlineKeyboardButton(text="🧘‍♀️ Космическая йога", callback_data="yoga")],
        [InlineKeyboardButton(text="👥 Групповые сеансы", callback_data="group")]
    ])

# Команда /start
@dp.message(CommandStart())
async def start_cmd(message: types.Message):
    text = (
        "Здравствуйте! Приветствую вас в персональном ассистенте Александра Сазонова — "
        "сертифицированного гипнотерапевта, мастера Кармакоррекции и Космической йоги.\n\n"
        "Я помогу вам узнать подробности о практиках и записаться на консультацию или сеанс.\n\n"
        "Выберите направление ниже:"
    )
    await message.answer(text, reply_markup=get_main_keyboard())

# Обработка нажатий на кнопки (ответ текстом + ГОЛОСОМ)
@dp.callback_query()
async def process_callback(callback: CallbackQuery):
    responses = {
        "hypno": "Гипнотерапия помогает бережно проработать внутренние блоки, тревоги и подсознательные установки.",
        "karma": "Кармакоррекция направлена на выявление и устранение причин повторяющихся жизненных трудностей.",
        "yoga": "Космическая йога способствует гармонизации энергии, оздоровлению тела и глубокому расслаблению.",
        "group": "Групповые сеансы — отличный формат для коллективной работы в сильном энергоинформационном поле."
    }

    reply_text = responses.get(callback.data, "Информация обновляется.")
    
    # Отправляем текстовый ответ
    await callback.message.answer(reply_text)

    # Генерация нейро-голоса (Edge-TTS)
    voice_file = f"voice_{callback.from_user.id}.mp3"
    communicate = edge_tts.Communicate(reply_text, "ru-RU-DmitryNeural")
    await communicate.save(voice_file)

    # Отправка голосового сообщения
    voice_input = types.FSInputFile(voice_file)
    await callback.message.answer_voice(voice_input)

    # Удаляем временный аудиофайл
    if os.path.exists(voice_file):
        os.remove(voice_file)

    await callback.answer()

# Веб-сервер для поддержания работы на Render
async def handle(request):
    return web.Response(text="Bot is running!")

app = web.Application()
app.router.add_get("/", handle)

async def main():
    port = int(os.environ.get("PORT", 8080))
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, "0.0.0.0", port)
    await site.start()

    # Запуск поллинга бота
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
