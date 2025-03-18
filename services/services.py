from aiogram.fsm.state import State, StatesGroup
# Cоздаем класс, наследуемый от StatesGroup, для группы состояний нашей FSM
class FSMFillForm(StatesGroup):
    fill_name = State()        # Состояние ожидания ввода имени
    fill_number = State()         # Состояние ожидания ввода номера телефона
    fill_dates = State()      # Состояние ожидания ввода дат заезда и выезда
    fill_details = State()     # Состояние ожидания подробностей
