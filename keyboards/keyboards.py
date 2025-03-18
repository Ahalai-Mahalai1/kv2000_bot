from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from lexicon.lexicon_ru import LEXICON_RU

button_1 = KeyboardButton(text=LEXICON_RU['button_tekst'])


# Начальная клава с текстом оставить заявку
game_kb = ReplyKeyboardMarkup(
    keyboard=[[button_1]],
    resize_keyboard=True,
    one_time_keyboard=True
)