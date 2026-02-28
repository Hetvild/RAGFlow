from aiogram.fsm.state import State, StatesGroup


class MenuStates(StatesGroup):
    main_menu = State()


class DialogStates(StatesGroup):
    active = State()
