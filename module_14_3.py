import os
from dotenv import load_dotenv
import logging
from aiogram import Bot, Dispatcher, executor, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.types import (ReplyKeyboardMarkup, KeyboardButton, \
                           InlineKeyboardMarkup, InlineKeyboardButton)

logging.basicConfig(level=logging.INFO)
"""Используем функцию load_dotenv() для получения токена из файла .env, включенного в файл .gitignore"""
load_dotenv()
TOKEN = os.getenv("TOKEN")
"""создаем экземпляры классов Bot и Dispatcher с атрибутами bot и storage"""
bot = Bot(token=TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())
"""создаем экземпляры кнопок reply клавиатуры и самого класса reply клавиатуры с добавлением кнопок в один ряд"""
b_count = KeyboardButton(text='Рассчитать')
b_info = KeyboardButton(text='Информация')
b_pay = KeyboardButton(text='Купить')
kb = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2).add(b_count, b_info, b_pay)
"""создаем экземпляры кнопок inline клавиатуры и самого класса  inline клавиатуры с добавлением кнопок в два ряда"""
b_in_count = InlineKeyboardButton(text='Рассчитать норму калорий', callback_data='calories')
b_in_formula = InlineKeyboardButton(text='Формулы расчёта', callback_data='formulas')
kb_in = InlineKeyboardMarkup().add(b_in_count)
kb_in.add(b_in_formula)
"""создаем экз Inline клавиатуры с кнопками в один ряд"""
kb_prod1 = InlineKeyboardButton(text='Продукт1', callback_data='product_buying')
kb_prod2 = InlineKeyboardButton(text='Продукт2', callback_data='product_buying')
kb_prod3 = InlineKeyboardButton(text='Продукт3', callback_data='product_buying')
kb_prod4 = InlineKeyboardButton(text='Продукт4', callback_data='product_buying')
prod_kb = InlineKeyboardMarkup(resize_keyboard=True, row_width=4).add(kb_prod1, kb_prod2, kb_prod3, kb_prod4)


class UserState(StatesGroup):
    age = State()
    growth = State()
    weight = State()

@dp.callback_query_handler(text='product_buying')#пользователь нажал inline кнопку с конкретным продуктом
async def set_confirm_message(call):
    await call.message.answer('Вы успешно приобрели продукт!')
    await call.answer()

@dp.callback_query_handler(text='formulas')#пользователь нажал inline кнопку Формулы расчета
async def get_formulas(call):
    await call.message.answer('калории (ккал) = 10 х вес (кг) + 6,25 x рост (см) – 5 х возраст (г) + 5')
    await call.answer()

@dp.callback_query_handler(text='calories')#пользователь нажал inline кнопку Рассчитать норму калорий
async def set_age(call):
    await call.message.answer("Введите свой возраст")
    await UserState.age.set()  # ожидаем ввод возраста в атрибут UserState.age
    await call.answer()

@dp.message_handler(commands=['start'])# пользователь набрал команду /start
async def start(message):
    await message.answer('Привет! Я бот, помогающий твоему здоровью',reply_markup=kb)

@dp.message_handler(text='Купить')# пользователь нажал reply кнопку Купить
async def get_buying_list(message):
    for i in range(1, 5):#добавляем описания продуктов и их рисунки
        await message.answer(f'Название: Product{i} | Описание: описание {i} | Цена: {i * 100}')
        with open(f'products/{i}.jpg', 'rb') as img:
            if i == 4:#пока цикл не дошел до последнего (4-го) продукта - добавляются описания и рисунки продуктов \
                #как цикл дошел до последнего 4-го: появляется текст выбора продуктов и Inline клавиатура
                await message.answer_photo(img)
                await message.answer(text='Выберите продукт для покупки:', reply_markup=prod_kb)
            await message.answer_photo(img)

@dp.message_handler(text='Рассчитать')#пользователь нажал reply кнопку Рассчитать
async def main_menu(message):
    await message.answer(text='Выберите опцию', reply_markup=kb_in)

@dp.message_handler(text='Информация')# пользователь нажал reply кнопку Информация
async def inform(message):
    await message.answer('Информация о боте')

@dp.message_handler(state=UserState.age)# пользователь ввел возраст
async def set_growth(message, state):
    await state.update_data(txt_age=message.text)# обновляем данные в состоянии age
    await message.answer("Введите свой рoст")
    await UserState.growth.set()#ожидаем ввод роста в аттрибут UserState.growth

@dp.message_handler(state=UserState.growth)# пользователь ввел рост
async def set_weight(message, state):
    await state.update_data(txt_growth=message.text)# обновляем данные в состоянии growth
    await message.answer("Введите свой вес")
    await UserState.weight.set()#ожидаем ввод веса в аттрибут UserState.weight

@dp.message_handler(state=UserState.weight)# пользователь ввел вес
async def set_calories(message, state):
    await state.update_data(txt_weight=message.text)# обновляем данные в состоянии weight
    data = await state.get_data()# присваиваем переменной словарь
    res = 10 * int(data['txt_weight']) + 6.25 * int(data['txt_growth']) - 5 * int(data['txt_age']) + 5#формула Миффлина-Сан Жеора
    await message.answer(f"Ваша норма калорий: {res}")
    await state.finish()#останавливаем машину состояний

@dp.message_handler()#произвольный набор символов пользователем
async def all_message(message):
    await message.answer('Введите команду /start, чтобы начать общение')


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)