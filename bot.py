import asyncio
import logging
import os
from aiohttp import web
from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart
from aiogram.types import (
    CallbackQuery,
    FSInputFile,
    InlineKeyboardButton,
    InlineKeyboardMarkup,
    Message,
)

# Настройка логирования
logging.basicConfig(level=logging.INFO)

# Инициализация бота
BOT_TOKEN = os.getenv("BOT_TOKEN")
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# Юзернейм в Telegram без символа @
YOUR_TELEGRAM_USERNAME = "alex910usa"


# --- ВЕБ-СЕРВЕР ДЛЯ RENDER ---
async def handle_ping(request):
    return web.Response(text="Bot is running!")


async def start_web_server():
    app = web.Application()
    app.router.add_get("/", handle_ping)
    app.router.add_get("/health", handle_ping)
    runner = web.AppRunner(app)
    await runner.setup()
    port = int(os.getenv("PORT", 8080))
    site = web.TCPSite(runner, "0.0.0.0", port)
    await site.start()
    logging.info(f"Web server started on port {port}")


# --- МЕНЮ И КНОПКИ ---
def get_main_keyboard():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="🎁 Бесплатная практика (5 мин)",
                    callback_data="gift_practice",
                )
            ],
            [
                InlineKeyboardButton(
                    text="🧠 Гипнотерапия", callback_data="hypno"
                ),
                InlineKeyboardButton(
                    text="🧘‍♂️ Кармакоррекция", callback_data="karma"
                ),
            ],
            [
                InlineKeyboardButton(
                    text="🧘‍♀️ Космическая йога & Чаши",
                    callback_data="yoga_sound",
                )
            ],
            [
                InlineKeyboardButton(
                    text="👥 Групповые сеансы", callback_data="group_sessions"
                )
            ],
            [
                InlineKeyboardButton(
                    text="✍️ Записаться на сеанс", callback_data="book_session"
                )
            ],
        ]
    )


def get_back_keyboard():
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="◀️ Назад в меню", callback_data="main_menu"
                )
            ]
        ]
    )


# --- ОБРАБОТЧИКИ КОМАНД И КНОПОК ---
@dp.message(CommandStart())
async def command_start_handler(message: Message):
    welcome_text = (
        f"Здравствуйте, <b>{message.from_user.first_name}</b>!\n\n"
        "Рад приветствовать вас. Я — Александр Сазонов, сертифицированный "
        "гипнотерапевт и энергопрактик.\n\n"
        "Я помогаю освободиться от внутренних блоков, тревоги, психосоматики, "
        "восстановить жизненную энергию и гармонию.\n\n"
        "Заберите ваш подарок ниже или выберите интересующее направление:"
    )
    await message.answer(
        text=welcome_text, reply_markup=get_main_keyboard(), parse_mode="HTML"
    )


# ОБРАБОТЧИК ПОДАРКА
@dp.callback_query(F.data == "gift_practice")
async def send_gift_practice(callback: CallbackQuery):
    await callback.answer("Загружаем аудиопрактику...")
    try:
        audio_file = FSInputFile("gift.m4a", filename="gift.m4a")
        caption_text = (
            "🎁 <b>Ваш подарок: Практика «Перезагрузка подсознания за 5 минут»</b>\n\n"
            "Нажмите на аудиозапись ниже, закройте глаза и выделите 5 минут "
            "для снятия стресса и блоков в теле.\n\n"
            "🎧 <i>Рекомендуется слушать в наушниках и в спокойной обстановке.</i>"
        )
        await callback.message.answer_audio(
            audio=audio_file, caption=caption_text, parse_mode="HTML"
        )
    except Exception as e:
        logging.error(f"Ошибка при отправке аудио: {e}")
        await callback.message.answer(
            "⚠️ Не удалось загрузить файл `gift.m4a`. Убедитесь, что файл с таким именем загружен на GitHub."
        )


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
                    text="◀️ Назад в меню", callback_data="main_menu"
                )
            ],
        ]
    )
    text = (
        "✍️ <b>Запись на консультацию и сеансы</b>\n\n"
        "Чтобы записаться на индивидуальный или групповой сеанс, задать "
        "вопрос или подобрать удобное время — нажмите кнопку ниже и "
        "напишите мне напрямую:"
    )
    await callback.message.edit_text(text=text, reply_markup=kb, parse_mode="HTML")
    await callback.answer()


@dp.callback_query(F.data == "main_menu")
async def back_to_main(callback: CallbackQuery):
    welcome_text = "Выберите интересующий вас раздел или практику:"
    await callback.message.edit_text(
        text=welcome_text, reply_markup=get_main_keyboard(), parse_mode="HTML"
    )
    await callback.answer()


# --- ЗАПУСК ---
async def main():
    await start_web_server()
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())


