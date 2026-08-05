import logging
from aiogram import Bot, Dispatcher, F
from aiogram.types import (
    Message, 
    CallbackQuery, 
    InlineKeyboardMarkup, 
    InlineKeyboardButton,
    FSInputFile
)
from aiogram.filters import CommandStart
import os

# Настройка логирования
logging.basicConfig(level=logging.INFO)

# Инициализация бота
BOT_TOKEN = os.getenv("BOT_TOKEN")
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# Главное меню с новой кнопкой подарка
def get_main_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🎁 Бесплатная практика (5 мин)", callback_data="gift_practice")],
        [InlineKeyboardButton(text="🧠 Гипнотерапия", callback_data="hypno")],
        [InlineKeyboardButton(text="🧘‍♂️ Кармакоррекция", callback_data="karma")],
        [InlineKeyboardButton(text="🧘‍♀️ Космическая йога", callback_data="yoga")],
        [InlineKeyboardButton(text="👥 Групповые сеансы", callback_data="group")],
        [InlineKeyboardButton(text="⭐ Отзывы клиентов", callback_data="reviews")],
        [InlineKeyboardButton(text="💳 Стоимость и оплата", callback_data="pricing")],
        [InlineKeyboardButton(text="🎵 Мой TikTok", url="https://www.tiktok.com/@alexandr27678")],
        [InlineKeyboardButton(text="✍️ Записаться на сеанс", callback_data="start_booking")]
    ])

# Команда /start
@dp.message(CommandStart())
async def cmd_start(message: Message):
    welcome_text = (
        f"Здравствуйте, {message.from_user.first_name}! 🙏\n\n"
        "Я — ваш персональный помощник по записи на сеансы гипнотерапии, "
        "кармакоррекции, космической йоги и звукотерапии.\n\n"
        "Выберите интересующий вас раздел из меню ниже:"
    )
    await message.answer(welcome_text, reply_markup=get_main_keyboard())

# Обработчик кнопки "🎁 Бесплатная практика"
@dp.callback_query(F.data == "gift_practice")
async def send_gift_practice(callback: CallbackQuery):
    # Файл gift.m4a (или точное имя файла в репозитории)
    try:
        audio_file = FSInputFile("gift.m4a")
        caption_text = (
            "🎁 <b>Ваш подарок: Практика «Перезагрузка подсознания за 5 минут»</b>\n\n"
            "Нажмите на аудиозапись ниже, закройте глаза и выделите 5 минут "
            "для снятия стресса и блоков в теле.\n\n"
            "🎧 <i>Рекомендуется слушать в наушниках и в спокойной обстановке.</i>"
        )
        await callback.message.answer_audio(
            audio=audio_file,
            caption=caption_text,
            parse_mode="HTML"
        )
    except Exception as e:
        # Если файл на GitHub назван "Cеанс подарок.m4a" или "Сеанс подарок (1).m4a"
        audio_file = FSInputFile("Cеанс подарок.m4a")
        caption_text = (
            "🎁 <b>Ваш подарок: Практика «Перезагрузка подсознания за 5 минут»</b>\n\n"
            "Нажмите на аудиозапись ниже, закройте глаза и выделите 5 минут "
            "для снятия стресса и блоков в теле.\n\n"
            "🎧 <i>Рекомендуется слушать в наушниках и в спокойной обстановке.</i>"
        )
        await callback.message.answer_audio(
            audio=audio_file,
            caption=caption_text,
            parse_mode="HTML"
        )
    
    await callback.answer()

# Запуск бота
if __name__ == "__main__":
    import asyncio
    asyncio.run(dp.start_polling(bot))


