from aiogram import F, Router, Bot
from aiogram.filters import Command, CommandStart, StateFilter
from aiogram.types import CallbackQuery, Message
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import default_state, State, StatesGroup
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from keyboards.keyboards import game_kb
from lexicon.lexicon_ru import LEXICON_RU
from services.services import FSMFillForm
from config_data.config import Config, load_config

config: Config = load_config()
bot = Bot(
    token=config.tg_bot.token,
    default=DefaultBotProperties(parse_mode=ParseMode.HTML)
)
user_id = 406802660
router = Router()

# Создаем "базу данных" пользователей
user_dict: dict[int, dict[str, str , str , str]] = {}

# Этот хэндлер срабатывает на команду /start
@router.message(CommandStart())
async def process_start_command(message: Message):
    await message.answer(text=LEXICON_RU['/start'], reply_markup=game_kb)




# Этот хэндлер срабатывает на нажатие кнопки оставить заявку в дефолтном состоянии
@router.message(F.text == LEXICON_RU['button_tekst'], StateFilter(default_state))
async def process_yes_answer(message: Message, state: FSMContext):
    await message.answer(text=LEXICON_RU['dai_name'])
    # Устанавливаем состояние ожидания ввода имени
    await state.set_state(FSMFillForm.fill_name)

# Этот хэндлер будет срабатывать, если введено корректное имя
# и переводить в состояние ожидания ввода возраста
@router.message(StateFilter(FSMFillForm.fill_name))
async def process_name_sent(message: Message, state: FSMContext):
    # Cохраняем введенное имя в хранилище по ключу "name"
    await state.update_data(name=message.text)
    await message.answer(text=LEXICON_RU['dai_number'])
    # Устанавливаем состояние ожидания ввода номера
    await state.set_state(FSMFillForm.fill_number)


# Этот хэндлер будет срабатывать, если введен корректный номер телефона
# и переводить в состояние выбора дат
@router.message(StateFilter(FSMFillForm.fill_number))
async def process_number_sent(message: Message, state: FSMContext):
    # Cохраняем номер в хранилище по ключу "number"
    await state.update_data(number=message.text)
    await message.answer(text=LEXICON_RU['dai_dates'])
    # Устанавливаем состояние ожидания выбора дат
    await state.set_state(FSMFillForm.fill_dates)

# Этот хэндлер будет срабатывать, если введены даты
# и переводить в состояние указания деталей
@router.message(StateFilter(FSMFillForm.fill_dates))
async def process_dates_sent(message: Message, state: FSMContext):
    # Cохраняем даты в хранилище по ключу "dates"
    await state.update_data(dates=message.text)
    await message.answer(text=LEXICON_RU['dai_details'])
    # Устанавливаем состояние ожидания выбора дат
    await state.set_state(FSMFillForm.fill_details)

#Этот хендлер будет срабатывать когда введены детали и будет отправлять всю эту тему
#в тг и на почту
@router.message(StateFilter(FSMFillForm.fill_details))
async def process_details_sent(message: Message, state: FSMContext):
    # Cохраняем детали в хранилище по ключу "details"
    await message.answer(text=LEXICON_RU['botik_answer'])
    await state.update_data(details=message.text)
    user_dict[message.from_user.id] = await state.get_data()
    a=user_dict[message.from_user.id]
    await bot.send_message(user_id, f'{a}')
    # грузим всё в словарь
    # Завершаем машину состояний
    await state.clear()
