
from aiogram.fsm.state import State, StatesGroup

class CreateCardState(StatesGroup):
    cards = State()
    term = State()
    slaid = State()
    name = State()
    discription = State()
    photo = State()
    contact = State()
   
    style = State()
    invoice = State()
   
    

class DisainerCard(StatesGroup):
    id = State()
    media_group = State()