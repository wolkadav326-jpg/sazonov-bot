import os
import asyncio
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import CommandStart
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiohttp import web
import edge_tts

# Вставьте ваш Telegram ID (число без кавычек)
MY_CHAT_ID = 1675177350 # Замените на ваш ID от @userinfobot

BOT_TOKEN = os.getenv("BOT_TOKEN")
bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# -------------------------------------------------------------------
# СОСТОЯНИЯ (FSM) ДЛЯ СБОРА ЗАЯВКИ
# -------------------------------------------------------------------
class BookingState(StatesGroup):
    waiting_for_name = State()
    waiting_for_category = State()
    waiting_for_phone = State()
    waiting_for_issue = State()

# -------------------------------------------------------------------
# КЛАВИАТУРЫ
# -------------------------------------------------------------------
def get_main_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🧠 Гипнотерапия", callback_data="hypno")],
        [InlineKeyboardButton(text="🧘‍♂️ Кармакоррекция", callback_data="karma")],
        [InlineKeyboardButton(text="🧘‍♀️ Космическая йога", callback_data="yoga")],
        [InlineKeyboardButton(text="👥 Групповые сеансы", callback_data="group")],
        [InlineKeyboardButton(text="⭐ Отзывы клиентов", callback_data="reviews")],
        [InlineKeyboardButton(text="💳 Стоимость и оплата", callback_data="pricing")],
        [InlineKeyboardButton(text="🎵 Мой TikTok", url="https://www.tiktok.com/@user737125029"
        [InlineKeyboardButton(text="✍️ Записаться на сеанс", callback_data="start_booking")]
    ])

def get_back_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="✍️ Записаться на сеанс", callback_data="start_booking")],
        [InlineKeyboardButton(text="⬅️ Назад в меню", callback_data="back_to_main")]
    ])

def get_category_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🧠 Гипнотерапия", callback_data="cat_hypno")],
        [InlineKeyboardButton(text="🧘‍♂️ Кармакоррекция", callback_data="cat_karma")],
        [InlineKeyboardButton(text="🧘‍♀️ Космическая йога", callback_data="cat_yoga")],
        [InlineKeyboardButton(text="👥 Групповой сеанс", callback_data="cat_group")]
    ])

# -------------------------------------------------------------------
# /START И НАВИГАЦИЯ
# -------------------------------------------------------------------
@dp.message(CommandStart())
async def start_cmd(message: types.Message, state: FSMContext):
    await state.clear()
    text = (
        "Здравствуйте! Приветствую вас в персональном ассистенте Александра Сазонова — "
        "сертифицированного гипнотерапевта, мастера Кармакоррекции и Космической йоги.\n\n"
        "Я помогу вам узнать подробности о практиках, ознакомиться с прайсом и записаться на сеанс.\n\n"
        "Выберите интересующий раздел ниже:"
    )
    await message.answer(text, reply_markup=get_main_keyboard())

# -------------------------------------------------------------------
# ПОШАГОВАЯ ЗАПИСЬ (ОПРОСНИК)
# -------------------------------------------------------------------
@dp.callback_query(F.data == "start_booking")
async def start_booking(callback: CallbackQuery, state: FSMContext):
    await state.set_state(BookingState.waiting_for_name)
    await callback.message.answer("Шаг 1 из 4: Как к вам обращаться? Напишите ваше имя:")
    await callback.answer()

@dp.message(BookingState.waiting_for_name)
async def process_name(message: types.Message, state: FSMContext):
    await state.update_data(name=message.text)
    await state.set_state(BookingState.waiting_for_category)
    await message.answer("Шаг 2 из 4: Выберите направление, которое вас интересует:", reply_markup=get_category_keyboard())

@dp.callback_query(BookingState.waiting_for_category, F.data.startswith("cat_"))
async def process_category(callback: CallbackQuery, state: FSMContext):
    categories = {
        "cat_hypno": "Гипнотерапия",
        "cat_karma": "Кармакоррекция",
        "cat_yoga": "Космическая йога",
        "cat_group": "Групповые сеансы"
    }
    selected_cat = categories.get(callback.data, "Не указано")
    await state.update_data(category=selected_cat)
    await state.set_state(BookingState.waiting_for_phone)
    
    await callback.message.answer("Шаг 3 из 4: Напишите ваш номер телефона или Никнейм в Telegram для связи:")
    await callback.answer()

@dp.message(BookingState.waiting_for_phone)
async def process_phone(message: types.Message, state: FSMContext):
    await state.update_data(phone=message.text)
    await state.set_state(BookingState.waiting_for_issue)
    await message.answer("Шаг 4 из 4: Вкратце опишите ваш запрос или проблему, с которой хотите обратиться:")

@dp.message(BookingState.waiting_for_issue)
async def process_issue(message: types.Message, state: FSMContext):
    await state.update_data(issue=message.text)
    user_data = await state.get_data()
    
    await message.answer("Благодарим! Ваша заявка успешно отправлена Александру. Он свяжется с вами в ближайшее время для согласования времени и деталей оплаты.", reply_markup=get_main_keyboard())

    if MY_CHAT_ID != 000000000:
        admin_text = (
            "📥 **НОВАЯ ЗАЯВКА НА СЕАНС!**\n\n"
            f"👤 **Имя:** {user_data.get('name')}\n"
            f"🎯 **Направление:** {user_data.get('category')}\n"
            f"📞 **Контакт:** {user_data.get('phone')}\n"
            f"💬 **Запрос:** {user_data.get('issue')}\n"
            f"🔗 **Профиль:** @{message.from_user.username if message.from_user.username else 'нет юзернейма'}"
        )
        try:
            await bot.send_message(chat_id=MY_CHAT_ID, text=admin_text, parse_mode="Markdown")
        except Exception as e:
            print(f"Ошибка отправки уведомления: {e}")

    await state.clear()

# -------------------------------------------------------------------
# ОПЛАТА И ОТЗЫВЫ
# -------------------------------------------------------------------
@dp.callback_query(F.data == "reviews")
async def process_reviews(callback: CallbackQuery):
    text = (
        "⭐ **Отзывы и результаты клиентов**\n\n"
        "Здесь вы можете ознакомиться с реальными историями изменений "
        "и результатами моих клиентов после индивидуальных и групповых сеансов.\n\n"
        "Переходите в наш профиль и смотри видео-отзывы!"
    )
    await callback.message.answer(text, parse_mode="Markdown", reply_markup=get_back_keyboard())
    await callback.answer()

@dp.callback_query(F.data == "pricing")
async def process_pricing(callback: CallbackQuery):
    text = (
        "💳 **Стоимость практик и сеансов**\n\n"
        "🧘‍♀️ **Космическая йога:** €25 / сеанс\n\n"
        "🧠 **Гипнотерапия:**\n"
        "• 1 сессия — €350\n"
        "• Курс из 5 сессий — €1750\n\n"
        "🧘‍♂️ **Кармакоррекция:**\n"
        "• Комплексный курс (8 сеансов) — €1200\n\n"
        "📌 **Способы оплаты:**\n"
        "Принимаются PayPal, Zelle, банковские переводы и карты.\n"
        "_Реквизиты и подтверждение бронирования предоставляются персонально мастеру после отправки заявки._"
    )
    await callback.message.answer(text, parse_mode="Markdown", reply_markup=get_back_keyboard())
    await callback.answer()

# -------------------------------------------------------------------
# ИНФОРМАЦИЯ О НАПРАВЛЕНИЯХ (ОТВЕТ ТЕКСТОМ И ГОЛОСОМ)
# -------------------------------------------------------------------
@dp.callback_query(F.data.in_({"hypno", "karma", "yoga", "group"}))
async def process_info_callbacks(callback: CallbackQuery):
    responses = {
        "hypno": "Гипнотерапия помогает бережно проработать внутренние блоки, тревоги и подсознательные установки.",
        "karma": "Кармакоррекция направлена на выявление и устранение причин повторяющихся жизненных трудностей.",
        "yoga": "Космическая йога способствует гармонизации энергии, оздоровлению тела и глубокому расслаблению.",
        "group": "Групповые сеансы — отличный формат для коллективной работы в сильном энергоинформационном поле."
    }

    reply_text = responses.get(callback.data, "Информация обновляется.")
    await callback.message.answer(reply_text, reply_markup=get_back_keyboard())

    # Озвучка
    voice_file = f"voice_{callback.from_user.id}.mp3"
    communicate = edge_tts.Communicate(reply_text, "ru-RU-DmitryNeural")
    await communicate.save(voice_file)

    voice_input = types.FSInputFile(voice_file)
    await callback.message.answer_voice(voice_input)

    if os.path.exists(voice_file):
        os.remove(voice_file)

    await callback.answer()

@dp.callback_query(F.data == "back_to_main")
async def process_back(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    text = (
        "Здравствуйте! Приветствую вас в персональном ассистенте Александра Сазонова — "
        "сертифицированного гипнотерапевта, мастера Кармакоррекции и Космической йоги.\n\n"
        "Выберите направление ниже:"
    )
    await callback.message.answer(text, reply_markup=get_main_keyboard())
    await callback.answer()

# -------------------------------------------------------------------
# СЕРВЕР RENDER
# -------------------------------------------------------------------
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

    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())


