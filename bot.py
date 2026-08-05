import logging
import os
from aiogram import Bot, Dispatcher, F
from aiogram.types import (
    Message,
    CallbackQuery,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
    FSInputFile,
)
from aiogram.filters import CommandStart

# Настройка логирования
logging.basicConfig(level=logging.INFO)

# Инициализация бота
BOT_TOKEN = os.getenv("BOT_TOKEN")
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# Укажите ваш юзернейм в Telegram без символа @
YOUR_TELEGRAM_USERNAME = "sazonov_alexandr"  # Поменяйте на ваш реальный username


# Главное меню с кнопками
def get_main_keyboard():
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="🎁 Бесплатная практика (5 мин)",
                    callback_query_data="gift_practice",
                )
            ],
            [
                InlineKeyboardButton(
                    text="🧠 Гипнотерапия", callback_query_data="hypno"
                ),
                InlineKeyboardButton(
                    text="🧘‍♂️ Кармакоррекция", callback_query_data="karma"
                ),
            ],
            [
                InlineKeyboardButton(
                    text="🧘‍♀️ Космическая йога & Чаши",
                    callback_query_data="yoga_sound",
                )
            ],
            [
                InlineKeyboardButton(
                    text="👥 Групповые сеансы", callback_query_data="group_sessions"
                )
            ],
            [
                InlineKeyboardButton(
                    text="✍️ Записаться на сеанс", callback_query_data="book_session"
                )
            ],
        ]
    )
    return keyboard


# Кнопка возврата в меню
def get_back_keyboard():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="◀️ Назад в меню", callback_query_data="main_menu")]
        ]
    )


# Старт бота
@dp.message(CommandStart())
async def command_start_handler(message: Message):
    welcome_text = (
        f"Здравствуйте, <b>{message.from_user.first_name}</b>!\n\n"
        "Рад приветствовать вас. Я — Александр Сазонов, сертифицированный гипнотерапевт "
        "и энергопрактик.\n\n"
        "Я помогаю освободиться от внутренних блоков, тревоги, психосоматики, "
        "восстановить жизненную энергию и гармонию.\n\n"
        "Заберите ваш подарок ниже или выберите интересующее направление:"
    )
    await message.answer(
        text=welcome_text, reply_markup=get_main_keyboard(), parse_mode="HTML"
    )


# Обработчик кнопки "🎁 Бесплатная практика"
@dp.callback_query(F.data == "gift_practice")
async def send_gift_practice(callback: CallbackQuery):
    audio_file = FSInputFile("gift.m4a")
    caption_text = (
        "🎁 <b>Ваш подарок: Практика «Перезагрузка подсознания за 5 минут»</b>\n\n"
        "Нажмите на аудиозапись ниже, закройте глаза и выделите 5 минут "
        "для снятия стресса и блоков в теле.\n\n"
        "🎧 <i>Рекомендуется слушать в наушниках и в спокойной обстановке.</i>"
    )
    await callback.message.answer_audio(
        audio=audio_file, caption=caption_text, parse_mode="HTML"
    )
    await callback.answer()


# 🧠 Гипнотерапия
@dp.callback_query(F.data == "hypno")
async def hypno_info(callback: CallbackQuery):
    text = (
        "🧠 <b>Сеансы гипнотерапии</b>\n\n"
        "Глубокая индивидуальная работа с подсознанием для устранения "
        "внутренних ограничений, психосоматических проявлений и страхов.\n\n"
        "• Поиск и нейтрализация первопричины проблемы\n"
        "• Освобождение от тревожности и затяжного стресса\n"
        "• Восстановление эмоционального баланса\n\n"
        "⏳ <b>Длительность:</b> 1.5 – 2 часа\n"
        "📌 <b>Формат:</b> Онлайн или очно"
    )
    await callback.message.edit_text(
        text=text, reply_markup=get_back_keyboard(), parse_mode="HTML"
    )
    await callback.answer()


# 🧘‍♂️ Кармакоррекция
@dp.callback_query(F.data == "karma")
async def karma_info(callback: CallbackQuery):
    text = (
        "🧘‍♂️ <b>Сеансы Кармакоррекции</b>\n\n"
        "Метод проработки повторяющихся жизненных сценариев, родовых программ "
        "и энергетических зажимов.\n\n"
        "• Очищение энергетических каналов\n"
        "• Разрыв деструктивных связей и циклов\n"
        "• Гармонизация ключевых сфер жизни\n\n"
        "⏳ <b>Длительность:</b> 1.5 часа"
    )
    await callback.message.edit_text(
        text=text, reply_markup=get_back_keyboard(), parse_mode="HTML"
    )
    await callback.answer()


# 🧘‍♀️ Космическая йога & Чаши
@dp.callback_query(F.data == "yoga_sound")
async def yoga_sound_info(callback: CallbackQuery):
    text = (
        "🧘‍♀️ <b>Космическая йога и Звукотерапия</b>\n\n"
        "Синтез телесно-энергетических практик с погружением в вибрации "
        "планетарных поющих чаш (включая главную чашу Муладхара).\n\n"
        "• Глубокое расслабление нервной системы\n"
        "• Настройка работы чакральной системы\n"
        "• Восстановление и наполнение ресурсом\n\n"
        "⏳ <b>Длительность:</b> 1 – 1.5 часа"
    )
    await callback.message.edit_text(
        text=text, reply_markup=get_back_keyboard(), parse_mode="HTML"
    )
    await callback.answer()


# 👥 Групповые сеансы
@dp.callback_query(F.data == "group_sessions")
async def group_info(callback: CallbackQuery):
    text = (
        "👥 <b>Групповые практики и сеансы</b>\n\n"
        "Групповая работа создаёт сильное общее энергетическое поле, "
        "усиливающее эффект от медитаций и погружений.\n\n"
        "• Групповая гипнотерапия и медитации\n"
        "• Звуковые сеансы с поющими чашами\n"
        "• Совместные практики гармонизации\n\n"
        "📅 <i>Анонсы ближайших дат публикуются в канале.</i>"
    )
    await callback.message.edit_text(
        text=text, reply_markup=get_back_keyboard(), parse_mode="HTML"
    )
    await callback.answer()


# ✍️ Запись на сеанс
@dp.callback_query(F.data == "book_session")
async def book_session_info(callback: CallbackQuery):
    kb = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="💬 Написать Александру",
                    url=f"https://t.me/{YOUR_TELEGRAM_USERNAME}",
                )
            ],
            [
                InlineKeyboardButton(
                    text="◀️ Назад в меню", callback_query_data="main_menu"
                )
            ],
        ]
    )
    text = (
        "✍️ <b>Запись на консультацию и сеансы</b>\n\n"
        "Чтобы записаться на индивидуальный или групповой сеанс, задать вопрос "
        "или подобрать удобное время — нажмите кнопку ниже и напишите мне напрямую:"
    )
    await callback.message.edit_text(text=text, reply_markup=kb, parse_mode="HTML")
    await callback.answer()


# Назад в главное меню
@dp.callback_query(F.data == "main_menu")
async def back_to_main(callback: CallbackQuery):
    welcome_text = (
        "Выберите интересующий вас раздел или практику:"
    )
    await callback.message.edit_text(
        text=welcome_text, reply_markup=get_main_keyboard(), parse_mode="HTML"
    )
    await callback.answer()


# Запуск бота
if __name__ == "__main__":
    import asyncio

    asyncio.run(dp.start_polling(bot))


