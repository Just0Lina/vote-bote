from kernel import bot, dp, Event, events, User_state, Event_state
from gateway.controller import insert_event_to_db, get_tags_for_id, get_users_with_tag, get_all_tags, get_user_role, cancel_create_vote_remove_user
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor
from aiogram.types.message import ContentType
from aiogram.utils.markdown import text, bold, italic, code, pre
from aiogram.types import ParseMode
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from aiogram.utils.exceptions import BotBlocked

from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton

# import basicui.keyboards

# header = None
edit_index = dict()
edit_answer_index = dict()
anon_type = dict()
text = dict()
listAnswers = dict()
matrixAnswers = dict()
multiplyAnswers = dict()
eventTags = dict()
tempTags = dict()

# print('==================')
# print(events)
# print(edit_index)
# print(edit_answer_index)
# print(text)
# print(listAnswers)
# print(matrixAnswers)
# print(anon_type)
# print(multiplyAnswers)
# print('==================')

markup_cancel_edit = InlineKeyboardMarkup()
cancel_btn = InlineKeyboardButton('Отмена', callback_data='cancel')
markup_cancel_edit.add(cancel_btn)

done_tags = InlineKeyboardButton('Готово', callback_data='done_tags')

markup_create_poll = InlineKeyboardMarkup()
poll_button = InlineKeyboardButton('Создать опрос', callback_data='create_poll')
markup_create_poll.add(poll_button)

cancel_poll_creation = InlineKeyboardMarkup()
cancel_poll_btn = InlineKeyboardButton('Отмена', callback_data='cancel_poll')
cancel_poll_creation.add(cancel_poll_btn)

answer_creation = InlineKeyboardMarkup()
done_answer_btn = InlineKeyboardButton('Закончить', callback_data='done_answer')
delete_last_btn = InlineKeyboardButton('Удалить последний ответ', callback_data='delete_last_answer')
next_answer_btn = InlineKeyboardButton('Следующий', callback_data='next_answer')
answer_creation.add(done_answer_btn, next_answer_btn, delete_last_btn)

cancel_answer_creation = InlineKeyboardMarkup()
cancel_answer_btn = InlineKeyboardButton('Отмена', callback_data='cancel_answer')
cancel_answer_creation.add(cancel_answer_btn)

anonymous_picker = InlineKeyboardMarkup()
anon_btn = InlineKeyboardButton('Анонимно', callback_data='anon')
deanon_btn = InlineKeyboardButton('Публично', callback_data='deanon')
anonymous_picker.add(anon_btn, deanon_btn)

allows_multiple_answers_picker = InlineKeyboardMarkup()
single_answer = InlineKeyboardButton('Один вариант ответа', callback_data='single_answer')
multiply_answer = InlineKeyboardButton('Несколько вариантов ответа', callback_data='multiply_answer')
allows_multiple_answers_picker.add(multiply_answer, single_answer)

edit_multiple_answers_picker = InlineKeyboardMarkup()
edit_single_answer = InlineKeyboardButton('Один вариант ответа', callback_data='edit_single_answer')
edit_multiply_answer = InlineKeyboardButton('Несколько вариантов ответа', callback_data='edit_multiply_answer')
edit_multiple_answers_picker.add(edit_multiply_answer, edit_single_answer)

new_question_choice = InlineKeyboardMarkup()
another_question_btn = InlineKeyboardButton('Следующий вопрос', callback_data='next_question')
done_question_btn = InlineKeyboardButton('Закончить', callback_data='done_question')
new_question_choice.add(another_question_btn, done_question_btn)

edit_category = InlineKeyboardMarkup()
header_edit = InlineKeyboardButton('Заголовок', callback_data='header_edit')
text_edit = InlineKeyboardButton('Текст вопроса', callback_data='text_edit')
answer_edit = InlineKeyboardButton('Варианты ответа', callback_data='answer_edit')
anon_edit = InlineKeyboardButton('Анонимность', callback_data='anon_edit')
multiply_edit = InlineKeyboardButton('Тип ответов', callback_data='multiply_edit')
add_tags = InlineKeyboardButton('Добавить Теги', callback_data='add_tags')
remove_tags = InlineKeyboardButton('Удалить Теги', callback_data='remove_tags')
edit_category.add(header_edit, text_edit, answer_edit, anon_edit, multiply_edit, cancel_btn, add_tags, remove_tags)

delete_category = InlineKeyboardMarkup()
question_delete = InlineKeyboardButton('Вопрос', callback_data='question_delete')
answer_delete = InlineKeyboardButton('Вариант ответа', callback_data='answer_delete')
delete_category.add(question_delete, answer_delete, cancel_btn)

add_category = InlineKeyboardMarkup()
question_add = InlineKeyboardButton('Вопрос', callback_data='question_add')
answer_add = InlineKeyboardButton('Вариант ответа', callback_data='answer_add')
add_category.add(question_add, answer_add, cancel_btn)

edit_markup = InlineKeyboardMarkup()
edit_poll_btn = InlineKeyboardButton('Редактировать', callback_data='edit_poll')
delete_poll_btn = InlineKeyboardButton('Удалить', callback_data='delete_poll')
add_poll_btn = InlineKeyboardButton('Добавить', callback_data='add_poll')
done_poll_btn = InlineKeyboardButton('Закончить', callback_data='done_poll')
edit_markup.add(edit_poll_btn, delete_poll_btn, add_poll_btn, done_poll_btn)

edit_markup_number = InlineKeyboardMarkup()



@dp.message_handler(text=['Создать новый опрос'], state=User_state.main_menu)
# @dp.callback_query_handler(lambda c: c.data and c.data.startswith('new-'), state='*')
async def process_start_command(message: types.Message):
    await bot.send_message(message.chat.id, 'Придумайте заголовок!', reply_markup=cancel_poll_creation)
    await Event_state.read_header.set()
    print('==================')
    print(events)
    print(edit_index)
    print(edit_answer_index)
    print(text)
    print(listAnswers)
    print(matrixAnswers)
    print(anon_type)
    print(multiplyAnswers)
    print('==================')

@dp.callback_query_handler(lambda c: c.data == 'cancel_poll', state = Event_state.read_header)
async def process_callback_kb1btn1(callback_query: types.CallbackQuery):
    await bot.send_message(callback_query.from_user.id, "До следующего голосования!")
    await User_state.main_menu.set()
    cancel_create_vote_remove_user(callback_query.from_user.id)
    if callback_query.from_user.id in edit_index:
        edit_index.pop(callback_query.from_user.id)
    if callback_query.from_user.id in edit_answer_index:
        edit_answer_index.pop(callback_query.from_user.id)
    if callback_query.from_user.id in text:
        text.pop(callback_query.from_user.id)
    if callback_query.from_user.id in listAnswers:
        listAnswers.pop(callback_query.from_user.id)
    if callback_query.from_user.id in matrixAnswers:
        matrixAnswers.pop(callback_query.from_user.id)
    # insert_event_to_db(events[callback_query.from_user.id])
    if callback_query.from_user.id in anon_type:
        anon_type.pop(callback_query.from_user.id)
    if callback_query.from_user.id in multiplyAnswers:
        multiplyAnswers.pop(callback_query.from_user.id)
    if callback_query.from_user.id in events:
        events.pop(callback_query.from_user.id)
    if callback_query.from_user.id in tempTags:
        tempTags.pop(callback_query.from_user.id)
    if callback_query.from_user.id in eventTags:
        eventTags.pop(callback_query.from_user.id)
    print('==================')
    print(events)
    print(edit_index)
    print(edit_answer_index)
    print(text)
    print(listAnswers)
    print(matrixAnswers)
    print(anon_type)
    print(multiplyAnswers)
    print('==================')

@dp.message_handler(state=Event_state.read_header)
async def header_creation(message: types.Message):
    if message.from_user.id not in events:
        events[message.from_user.id] = Event(message.from_user.id)
    events[message.from_user.id].header = message.text
    print('==================')
    print(events)
    print(edit_index)
    print(edit_answer_index)
    print(text)
    print(listAnswers)
    print(matrixAnswers)
    print(anon_type)
    print(multiplyAnswers)
    print('==================')
    await bot.send_message(message.chat.id, "Расскажи о вопросе!")
    await Event_state.read_text_poll.set()
    
@dp.message_handler(state=Event_state.read_text_poll)
async def process_start_command(message: types.Message):
    global text
    if message.from_user.id not in text:
        text[message.from_user.id] = list()
    # text[message.from_user.id] = list()
    text[message.from_user.id].append(message.text)
    print('==================')
    print(events)
    print(edit_index)
    print(edit_answer_index)
    print(text)
    print(listAnswers)
    print(matrixAnswers)
    print(anon_type)
    print(multiplyAnswers)
    print('==================')
    await bot.send_message(message.chat.id, "Теперь придумай варианты ответа!")
    await Event_state.wait_answer_creation_button_click.set()

@dp.message_handler(state=Event_state.wait_answer_creation_button_click)
async def process_start_command(message: types.Message):
    global listAnswers
    if message.from_user.id not in listAnswers:
        listAnswers[message.from_user.id] = list()
    # listAnswers[message.from_user.id] = list() 
    listAnswers[message.from_user.id].append(message.text)
    print('==================')
    print(events)
    print(edit_index)
    print(edit_answer_index)
    print(text)
    print(listAnswers)
    print(matrixAnswers)
    print(anon_type)
    print(multiplyAnswers)
    print('==================')
    await bot.send_message(message.chat.id, "Хочешь добавить еще вариант?", reply_markup=answer_creation)

@dp.callback_query_handler(lambda c: c.data == 'next_answer', state = Event_state.wait_answer_creation_button_click)
async def process_callback_kb1btn1(callback_query: types.CallbackQuery):
    await bot.send_message(callback_query.from_user.id, "Жду твой вариант!", reply_markup=cancel_answer_creation)
    await Event_state.wait_answer_creation_button_click.set()

@dp.callback_query_handler(lambda c: c.data == 'delete_last_answer', state = Event_state.wait_answer_creation_button_click)
async def process_callback_kb1btn1(callback_query: types.CallbackQuery):
    global listAnswers
    if len(listAnswers[callback_query.from_user.id]):
        listAnswers[callback_query.from_user.id].pop()
    print('==================')
    print(events)
    print(edit_index)
    print(edit_answer_index)
    print(text)
    print(listAnswers)
    print(matrixAnswers)
    print(anon_type)
    print(multiplyAnswers)
    print('==================')
    await bot.send_message(callback_query.from_user.id, "Хочешь добавить еще вариант?", reply_markup=answer_creation)
    await Event_state.wait_answer_creation_button_click.set()

@dp.callback_query_handler(lambda c: c.data == 'cancel_answer', state = Event_state.wait_answer_creation_button_click)
async def process_callback_kb1btn1(callback_query: types.CallbackQuery):
    global matrixAnswers
    global listAnswers
    if len(listAnswers[callback_query.from_user.id]) < 2:
        await bot.send_message(callback_query.from_user.id, "Жду вариант ответа!", reply_markup=answer_creation)
        await Event_state.wait_answer_creation_button_click.set()
    else:
        matrixAnswers[callback_query.from_user.id].append(listAnswers[callback_query.from_user.id].copy)
        listAnswers[callback_query.from_user.id].clear()
        await bot.send_message(callback_query.from_user.id, "Хочешь добавить еще один вопрос?", reply_markup=new_question_choice)
        await Event_state.wait_new_question_button_click.set()
    print('==================')
    print(events)
    print(edit_index)
    print(edit_answer_index)
    print(text)
    print(listAnswers)
    print(matrixAnswers)
    print(anon_type)
    print(multiplyAnswers)
    print('==================')

@dp.callback_query_handler(lambda c: c.data == 'done_answer', state = Event_state.wait_answer_creation_button_click)
async def process_callback_kb1btn1(callback_query: types.CallbackQuery):
    global matrixAnswers
    global listAnswers
    if callback_query.from_user.id not in matrixAnswers:
        matrixAnswers[callback_query.from_user.id] = list()
    if len(listAnswers[callback_query.from_user.id]) < 2:
        await bot.send_message(callback_query.from_user.id, "Должно быть не меньше двух вариантов ответа\nДобавь еще парочку", reply_markup=answer_creation)
        await Event_state.wait_answer_creation_button_click.set()
    else:
        matrixAnswers[callback_query.from_user.id].append(listAnswers[callback_query.from_user.id].copy())
        listAnswers[callback_query.from_user.id].clear()
        await bot.send_message(callback_query.from_user.id, "Сколько можно выбрать ответов?", reply_markup=allows_multiple_answers_picker)
        await Event_state.allows_multiple_answers_pick.set()
    print('==================')
    print(events)
    print(edit_index)
    print(edit_answer_index)
    print(text)
    print(listAnswers)
    print(matrixAnswers)
    print(anon_type)
    print(multiplyAnswers)
    print('==================')

@dp.callback_query_handler(lambda c: c.data == 'multiply_answer', state = Event_state.allows_multiple_answers_pick)
async def process_callback_kb1btn1(callback_query: types.CallbackQuery):
    global multiplyAnswers
    if callback_query.from_user.id not in multiplyAnswers:
        multiplyAnswers[callback_query.from_user.id] = list()
    multiplyAnswers[callback_query.from_user.id].append(True)
    await bot.send_message(callback_query.from_user.id, "Хочешь добавить еще один вопрос?", reply_markup=new_question_choice)
    await Event_state.wait_new_question_button_click.set()
    print('==================')
    print(events)
    print(edit_index)
    print(edit_answer_index)
    print(text)
    print(listAnswers)
    print(matrixAnswers)
    print(anon_type)
    print(multiplyAnswers)
    print('==================')

@dp.callback_query_handler(lambda c: c.data == 'single_answer', state = Event_state.allows_multiple_answers_pick)
async def process_callback_kb1btn1(callback_query: types.CallbackQuery):
    global multiplyAnswers
    if callback_query.from_user.id not in multiplyAnswers:
        multiplyAnswers[callback_query.from_user.id] = list()
    multiplyAnswers[callback_query.from_user.id].append(False)
    await bot.send_message(callback_query.from_user.id, "Хочешь добавить еще один вопрос?", reply_markup=new_question_choice)
    await Event_state.wait_new_question_button_click.set()
    print('==================')
    print(events)
    print(edit_index)
    print(edit_answer_index)
    print(text)
    print(listAnswers)
    print(matrixAnswers)
    print(anon_type)
    print(multiplyAnswers)
    print('==================')
    
@dp.callback_query_handler(lambda c: c.data == 'next_question', state = Event_state.wait_new_question_button_click)
async def process_callback_kb1btn1(callback_query: types.CallbackQuery):
    await bot.send_message(callback_query.from_user.id, "Расскажи о вопросе!")
    await Event_state.read_text_poll.set()
    print('==================')
    print(events)
    print(edit_index)
    print(edit_answer_index)
    print(text)
    print(listAnswers)
    print(matrixAnswers)
    print(anon_type)
    print(multiplyAnswers)
    print('==================')

@dp.callback_query_handler(lambda c: c.data == 'done_question', state = Event_state.wait_new_question_button_click)
async def process_callback_kb1btn1(callback_query: types.CallbackQuery):
    for i in range(0, len(matrixAnswers[callback_query.from_user.id])):
        await bot.send_poll(callback_query.from_user.id, text[callback_query.from_user.id][i], matrixAnswers[callback_query.from_user.id][i], allows_multiple_answers=multiplyAnswers[callback_query.from_user.id][i])
    await bot.send_message(callback_query.from_user.id, "Реши, будет ли этот опрос анонимным", reply_markup=anonymous_picker)
    await Event_state.choice_anon.set()
    print('==================')
    print(events)
    print(edit_index)
    print(edit_answer_index)
    print(text)
    print(listAnswers)
    print(matrixAnswers)
    print(anon_type)
    print(multiplyAnswers)
    print('==================')

@dp.callback_query_handler(lambda c: c.data == 'anon', state = Event_state.choice_anon)
async def process_callback_kb1btn1(callback_query: types.CallbackQuery):
    global anon_type
    anon_type[callback_query.from_user.id] = True
    global tempTags
    if callback_query.from_user.id not in tempTags:
        tempTags[callback_query.from_user.id] = list()
        if get_user_role(callback_query.from_user.id) == "ADM":
            for i in get_all_tags():
                tempTags[callback_query.from_user.id].append(i[0])
        else:
            tempTags[callback_query.from_user.id] = get_tags_for_id(callback_query.from_user.id)
    for i in range(0, len(tempTags[callback_query.from_user.id])):
        edit_markup_number.add(InlineKeyboardButton(tempTags[callback_query.from_user.id][i], callback_data='number_tag' + tempTags[callback_query.from_user.id][i]))
    await bot.send_message(callback_query.from_user.id, "Выбери тег для добавления!", reply_markup=edit_markup_number)
    await Event_state.wait_add_tags.set()
    edit_markup_number.inline_keyboard.clear()
    print('==================')
    print(events)
    print(edit_index)
    print(edit_answer_index)
    print(text)
    print(listAnswers)
    print(matrixAnswers)
    print(anon_type)
    print(multiplyAnswers)
    print('==================')

@dp.callback_query_handler(lambda c: c.data == 'deanon', state = Event_state.choice_anon)
async def process_callback_kb1btn1(callback_query: types.CallbackQuery):
    global anon_type
    anon_type[callback_query.from_user.id] = False
    global tempTags
    if callback_query.from_user.id not in tempTags:
        tempTags[callback_query.from_user.id] = list()
        tempTags[callback_query.from_user.id] = get_tags_for_id(callback_query.from_user.id)
    for i in range(0, len(tempTags[callback_query.from_user.id])):
        edit_markup_number.add(InlineKeyboardButton(tempTags[callback_query.from_user.id][i], callback_data='number_tag' + tempTags[callback_query.from_user.id][i]))
    await bot.send_message(callback_query.from_user.id, "Выбери тег для добавления!", reply_markup=edit_markup_number)
    await Event_state.wait_add_tags.set()
    edit_markup_number.inline_keyboard.clear()
    print('==================')
    print(events)
    print(edit_index)
    print(edit_answer_index)
    print(text)
    print(listAnswers)
    print(matrixAnswers)
    print(anon_type)
    print(multiplyAnswers)
    print('==================')

@dp.callback_query_handler(lambda c: c.data and c.data.startswith('number_tag'), state=Event_state.wait_add_tags)
async def process_callback_kb1btn1(callback_query: types.CallbackQuery):
    tag = callback_query.data.replace('number_tag', '')
    global eventTags
    global tempTags
    tempTags[callback_query.from_user.id].remove(tag)
    if callback_query.from_user.id not in eventTags:
        eventTags[callback_query.from_user.id] = list()
    eventTags[callback_query.from_user.id].append(tag)
    for i in range(0, len(tempTags[callback_query.from_user.id])):
        edit_markup_number.add(InlineKeyboardButton(tempTags[callback_query.from_user.id][i], callback_data='number_tag' + tempTags[callback_query.from_user.id][i]))
    edit_markup_number.add(done_tags)   
    await bot.send_message(callback_query.from_user.id, "Тег добавлен!", reply_markup=edit_markup_number)
    await Event_state.wait_add_tags.set()
    edit_markup_number.inline_keyboard.clear()

@dp.callback_query_handler(lambda c: c.data == 'done_tags', state = Event_state.wait_add_tags)
async def process_callback_kb1btn1(callback_query: types.CallbackQuery):
    await bot.send_message(callback_query.from_user.id, "Опрос завершен!\nПроверь созданный опрос.\nТы можешь изменить его содержание!", reply_markup=edit_markup)
    await Event_state.done_poll_button_click.set()


async def cancel_callback_function(callback_query: types.CallbackQuery):
    for i in range(0, len(matrixAnswers[callback_query.from_user.id])):
        await bot.send_poll(callback_query.from_user.id, text[callback_query.from_user.id][i], matrixAnswers[callback_query.from_user.id][i], allows_multiple_answers=multiplyAnswers[callback_query.from_user.id][i])
    await bot.send_message(callback_query.from_user.id, "Опрос завершен!\nПроверь созданный опрос.\nТы можешь изменить его содержание!", reply_markup=edit_markup)
    await Event_state.done_poll_button_click.set()
    print('==================')
    print(events)
    print(edit_index)
    print(edit_answer_index)
    print(text)
    print(listAnswers)
    print(matrixAnswers)
    print(anon_type)
    print(multiplyAnswers)
    print('==================')

@dp.callback_query_handler(lambda c: c.data == 'cancel', state = Event_state.choice_edit_poll_category_click)
async def process_callback_kb1btn1(callback_query: types.CallbackQuery):
    await cancel_callback_function(callback_query)
    
@dp.callback_query_handler(lambda c: c.data == 'cancel', state = Event_state.choice_delete_poll_category_click)
async def process_callback_kb1btn1(callback_query: types.CallbackQuery):
    await cancel_callback_function(callback_query)

@dp.callback_query_handler(lambda c: c.data == 'cancel', state = Event_state.choice_add_poll_category_click)
async def process_callback_kb1btn1(callback_query: types.CallbackQuery):
    await cancel_callback_function(callback_query)

@dp.callback_query_handler(lambda c: c.data == 'cancel', state = Event_state.read_text_poll)
async def process_callback_kb1btn1(callback_query: types.CallbackQuery):
    await cancel_callback_function(callback_query)

@dp.callback_query_handler(lambda c: c.data == 'cancel', state = Event_state.choice_add_answer)
async def process_callback_kb1btn1(callback_query: types.CallbackQuery):
    await cancel_callback_function(callback_query)

@dp.callback_query_handler(lambda c: c.data == 'cancel', state = Event_state.choice_add_answer_button_click)
async def process_callback_kb1btn1(callback_query: types.CallbackQuery):
    await cancel_callback_function(callback_query)

@dp.callback_query_handler(lambda c: c.data == 'cancel', state = Event_state.choice_delete_poll_button_click)
async def process_callback_kb1btn1(callback_query: types.CallbackQuery):
    await cancel_callback_function(callback_query)

@dp.callback_query_handler(lambda c: c.data == 'cancel', state = Event_state.choice_delete_answer_button_click)
async def process_callback_kb1btn1(callback_query: types.CallbackQuery):
    await cancel_callback_function(callback_query)

@dp.callback_query_handler(lambda c: c.data == 'cancel', state = Event_state.delete_answer_button_click)
async def process_callback_kb1btn1(callback_query: types.CallbackQuery):
    await cancel_callback_function(callback_query)

@dp.callback_query_handler(lambda c: c.data == 'cancel', state = Event_state.choice_edit_poll_button_click)
async def process_callback_kb1btn1(callback_query: types.CallbackQuery):
    await cancel_callback_function(callback_query)

@dp.callback_query_handler(lambda c: c.data == 'cancel', state = Event_state.replace_text)
async def process_callback_kb1btn1(callback_query: types.CallbackQuery):
    await cancel_callback_function(callback_query)

@dp.callback_query_handler(lambda c: c.data == 'cancel', state = Event_state.replace_answer)
async def process_callback_kb1btn1(callback_query: types.CallbackQuery):
    await cancel_callback_function(callback_query)

@dp.callback_query_handler(lambda c: c.data == 'cancel', state = Event_state.replace_header)
async def process_callback_kb1btn1(callback_query: types.CallbackQuery):
    await cancel_callback_function(callback_query)





@dp.callback_query_handler(lambda c: c.data == 'edit_poll', state = Event_state.done_poll_button_click)
async def process_callback_kb1btn1(callback_query: types.CallbackQuery):
    await bot.send_message(callback_query.from_user.id, "Выбери категорию редактирования!", reply_markup=edit_category)
    await Event_state.choice_edit_poll_category_click.set()
    print('==================')
    print(events)
    print(edit_index)
    print(edit_answer_index)
    print(text)
    print(listAnswers)
    print(matrixAnswers)
    print(anon_type)
    print(multiplyAnswers)
    print('==================')

@dp.callback_query_handler(lambda c: c.data == 'delete_poll', state = Event_state.done_poll_button_click)
async def process_callback_kb1btn1(callback_query: types.CallbackQuery):
    await bot.send_message(callback_query.from_user.id, "Выбери категорию для удаления!", reply_markup=delete_category)
    await Event_state.choice_delete_poll_category_click.set()
    print('==================')
    print(events)
    print(edit_index)
    print(edit_answer_index)
    print(text)
    print(listAnswers)
    print(matrixAnswers)
    print(anon_type)
    print(multiplyAnswers)
    print('==================')

@dp.callback_query_handler(lambda c: c.data == 'add_poll', state = Event_state.done_poll_button_click)
async def process_callback_kb1btn1(callback_query: types.CallbackQuery):
    await bot.send_message(callback_query.from_user.id, "Выбери категорию для добавления!", reply_markup=add_category)
    await Event_state.choice_add_poll_category_click.set()
    print('==================')
    print(events)
    print(edit_index)
    print(edit_answer_index)
    print(text)
    print(listAnswers)
    print(matrixAnswers)
    print(anon_type)
    print(multiplyAnswers)
    print('==================')

@dp.callback_query_handler(lambda c: c.data == 'question_add', state = Event_state.choice_add_poll_category_click)
async def process_callback_kb1btn1(callback_query: types.CallbackQuery):
    await bot.send_message(callback_query.from_user.id, "Расскажи о вопросе!", reply_markup=markup_cancel_edit)
    await Event_state.read_text_poll.set()
    print('==================')
    print(events)
    print(edit_index)
    print(edit_answer_index)
    print(text)
    print(listAnswers)
    print(matrixAnswers)
    print(anon_type)
    print(multiplyAnswers)
    print('==================')

@dp.callback_query_handler(lambda c: c.data == 'answer_add', state = Event_state.choice_add_poll_category_click)
async def process_callback_kb1btn1(callback_query: types.CallbackQuery):
    for i in range(0, len(matrixAnswers[callback_query.from_user.id])):
        edit_markup_number.add(InlineKeyboardButton(str(i + 1), callback_data='choice_answer_add' + str(i)))
    edit_markup_number.add(cancel_btn)
    await bot.send_message(callback_query.from_user.id, "Выбери номер вопроса!", reply_markup=edit_markup_number)
    await Event_state.choice_add_answer_button_click.set()
    edit_markup_number.inline_keyboard.clear()
    print('==================')
    print(events)
    print(edit_index)
    print(edit_answer_index)
    print(text)
    print(listAnswers)
    print(matrixAnswers)
    print(anon_type)
    print(multiplyAnswers)
    print('==================')

@dp.callback_query_handler(lambda c: c.data and c.data.startswith('choice_answer_add'), state=Event_state.choice_add_answer_button_click)
async def process_callback_kb1btn1(callback_query: types.CallbackQuery):
    global edit_index
    edit_index[callback_query.from_user.id] = int(callback_query.data.replace('choice_answer_add', ''))
    await bot.send_message(callback_query.from_user.id, "Напиши, какой вариант хочешь добавить в это голосование", reply_markup=markup_cancel_edit)
    await bot.send_poll(callback_query.from_user.id, text[callback_query.from_user.id][edit_index[callback_query.from_user.id]], matrixAnswers[callback_query.from_user.id][edit_index[callback_query.from_user.id]], allows_multiple_answers=multiplyAnswers[callback_query.from_user.id][edit_index[callback_query.from_user.id]])
    await Event_state.choice_add_answer.set()
    print('==================')
    print(events)
    print(edit_index)
    print(edit_answer_index)
    print(text)
    print(listAnswers)
    print(matrixAnswers)
    print(anon_type)
    print(multiplyAnswers)
    print('==================')

@dp.message_handler(state=Event_state.choice_add_answer)
async def process_start_command(message: types.Message):
    global matrixAnswers
    matrixAnswers[message.from_user.id][edit_index[message.from_user.id]].append(message.text)
    await bot.send_message(message.chat.id, "Вариант добавлен", reply_markup=edit_markup)
    await Event_state.done_poll_button_click.set()
    print('==================')
    print(events)
    print(edit_index)
    print(edit_answer_index)
    print(text)
    print(listAnswers)
    print(matrixAnswers)
    print(anon_type)
    print(multiplyAnswers)
    print('==================')

@dp.callback_query_handler(lambda c: c.data == 'question_delete', state = Event_state.choice_delete_poll_category_click)
async def process_callback_kb1btn1(callback_query: types.CallbackQuery):
    for i in range(0, len(text[callback_query.from_user.id])):
        edit_markup_number.add(InlineKeyboardButton(str(i + 1), callback_data='number_text_delete' + str(i)))
    edit_markup_number.add(cancel_btn)
    await bot.send_message(callback_query.from_user.id, "Выбери номер вопроса для удаления!", reply_markup=edit_markup_number)
    await Event_state.choice_delete_poll_button_click.set()
    edit_markup_number.inline_keyboard.clear()
    print('==================')
    print(events)
    print(edit_index)
    print(edit_answer_index)
    print(text)
    print(listAnswers)
    print(matrixAnswers)
    print(anon_type)
    print(multiplyAnswers)
    print('==================')

@dp.callback_query_handler(lambda c: c.data and c.data.startswith('number_text_delete'), state=Event_state.choice_delete_poll_button_click)
async def process_callback_kb1btn1(callback_query: types.CallbackQuery):
    global edit_index
    edit_index[callback_query.from_user.id] = int(callback_query.data.replace('number_text_delete', ''))
    text[callback_query.from_user.id].pop(edit_index[callback_query.from_user.id])
    matrixAnswers[callback_query.from_user.id].pop(edit_index[callback_query.from_user.id])
    multiplyAnswers[callback_query.from_user.id].pop(edit_index[callback_query.from_user.id])
    if len(text[callback_query.from_user.id]) == 0:
        await bot.send_message(callback_query.from_user.id, 'Создание опроса прервано, создай новый опрос', reply_markup=markup_create_poll)
        await User_state.main_menu.set()
    else:
        for i in range(0, len(matrixAnswers[callback_query.from_user.id])):
            await bot.send_poll(callback_query.from_user.id, text[callback_query.from_user.id][i], matrixAnswers[callback_query.from_user.id][i], allows_multiple_answers=multiplyAnswers[callback_query.from_user.id][i])
        await bot.send_message(callback_query.from_user.id, 'Голосование удалено', reply_markup=edit_markup)
        await Event_state.done_poll_button_click.set()
    print('==================')
    print(events)
    print(edit_index)
    print(edit_answer_index)
    print(text)
    print(listAnswers)
    print(matrixAnswers)
    print(anon_type)
    print(multiplyAnswers)
    print('==================')

@dp.callback_query_handler(lambda c: c.data == 'answer_delete', state = Event_state.choice_delete_poll_category_click)
async def process_callback_kb1btn1(callback_query: types.CallbackQuery):
    for i in range(0, len(matrixAnswers[callback_query.from_user.id])):
        edit_markup_number.add(InlineKeyboardButton(str(i + 1), callback_data='choice_answer_delete' + str(i)))
    edit_markup_number.add(cancel_btn)
    await bot.send_message(callback_query.from_user.id, "Выбери номер вопроса!", reply_markup=edit_markup_number)
    await Event_state.choice_delete_answer_button_click.set()
    edit_markup_number.inline_keyboard.clear()
    print('==================')
    print(events)
    print(edit_index)
    print(edit_answer_index)
    print(text)
    print(listAnswers)
    print(matrixAnswers)
    print(anon_type)
    print(multiplyAnswers)
    print('==================')

@dp.callback_query_handler(lambda c: c.data and c.data.startswith('choice_answer_delete'), state=Event_state.choice_delete_answer_button_click)
async def process_callback_kb1btn1(callback_query: types.CallbackQuery):
    global edit_index
    edit_index[callback_query.from_user.id] = int(callback_query.data.replace('choice_answer_delete', ''))
    if len(matrixAnswers[callback_query.from_user.id][edit_index[callback_query.from_user.id]]) <= 2:
        await bot.send_message(callback_query.from_user.id, "Нельзя оставить один вариант ответа\nПопробуй отредактировать существующие или удали вопрос!", reply_markup=edit_markup)
        await Event_state.done_poll_button_click.set()
    else:
        for i in range(0, len(matrixAnswers[callback_query.from_user.id][edit_index[callback_query.from_user.id]])):
            edit_markup_number.add(InlineKeyboardButton(str(i + 1), callback_data='number_answer_delete' + str(i)))
        edit_markup_number.add(cancel_btn)
        await bot.send_message(callback_query.from_user.id, "Выбери номер ответа для удаления!", reply_markup=edit_markup_number)
        await Event_state.delete_answer_button_click.set()
        edit_markup_number.inline_keyboard.clear()
    print('==================')
    print(events)
    print(edit_index)
    print(edit_answer_index)
    print(text)
    print(listAnswers)
    print(matrixAnswers)
    print(anon_type)
    print(multiplyAnswers)
    print('==================')

@dp.callback_query_handler(lambda c: c.data and c.data.startswith('number_answer_delete'), state=Event_state.delete_answer_button_click)
async def process_callback_kb1btn1(callback_query: types.CallbackQuery):
    global edit_number_index
    edit_number_index[callback_query.from_user.id] = int(callback_query.data.replace('number_answer_delete', ''))
    matrixAnswers[callback_query.from_user.id][edit_index[callback_query.from_user.id]].pop(edit_number_index[callback_query.from_user.id])
    for i in range(0, len(matrixAnswers[callback_query.from_user.id])):
        await bot.send_poll(callback_query.from_user.id, text[callback_query.from_user.id][i], matrixAnswers[callback_query.from_user.id][i],allows_multiple_answers=multiplyAnswers[callback_query.from_user.id][i])
    await bot.send_message(callback_query.from_user.id, "Вариант ответа удален!", reply_markup=edit_markup)
    await Event_state.done_poll_button_click.set()
    edit_markup_number.inline_keyboard.clear()
    print('==================')
    print(events)
    print(edit_index)
    print(edit_answer_index)
    print(text)
    print(listAnswers)
    print(matrixAnswers)
    print(anon_type)
    print(multiplyAnswers)
    print('==================')

@dp.callback_query_handler(lambda c: c.data == 'text_edit', state = Event_state.choice_edit_poll_category_click)
async def process_callback_kb1btn1(callback_query: types.CallbackQuery):
    for i in range(0, len(text[callback_query.from_user.id])):
        edit_markup_number.add(InlineKeyboardButton(str(i + 1), callback_data='number_text' + str(i)))
    edit_markup_number.add(cancel_btn)   
    await bot.send_message(callback_query.from_user.id, "Выбери номер вопроса для редактирования!", reply_markup=edit_markup_number)
    await Event_state.choice_edit_poll_button_click.set()
    edit_markup_number.inline_keyboard.clear()
    print('==================')
    print(events)
    print(edit_index)
    print(edit_answer_index)
    print(text)
    print(listAnswers)
    print(matrixAnswers)
    print(anon_type)
    print(multiplyAnswers)
    print('==================')

@dp.callback_query_handler(lambda c: c.data == 'add_tags', state = Event_state.choice_edit_poll_category_click)
async def process_callback_kb1btn1(callback_query: types.CallbackQuery):
    global tempTags
    if callback_query.from_user.id not in tempTags:
        tempTags[callback_query.from_user.id] = list()
        tempTags[callback_query.from_user.id] = get_tags_for_id(callback_query.from_user.id)
    for i in range(0, len(tempTags[callback_query.from_user.id])):
        edit_markup_number.add(InlineKeyboardButton(tempTags[callback_query.from_user.id][i], callback_data='number_tag' + tempTags[callback_query.from_user.id][i]))
    edit_markup_number.add(done_tags)   
    await bot.send_message(callback_query.from_user.id, "Выбери тег для добавления!", reply_markup=edit_markup_number)
    await Event_state.wait_add_tags.set()
    edit_markup_number.inline_keyboard.clear()
    print('==================')
    print(events)
    print(edit_index)
    print(edit_answer_index)
    print(text)
    print(listAnswers)
    print(matrixAnswers)
    print(anon_type)
    print(multiplyAnswers)
    print('==================')

@dp.callback_query_handler(lambda c: c.data and c.data.startswith('number_tag'), state=Event_state.wait_add_tags)
async def process_callback_kb1btn1(callback_query: types.CallbackQuery):
    tag = callback_query.data.replace('number_tag', '')
    global eventTags
    global tempTags
    tempTags[callback_query.from_user.id].remove(tag)
    if callback_query.from_user.id not in eventTags:
        eventTags[callback_query.from_user.id] = list()
    eventTags[callback_query.from_user.id].append(tag)
    for i in range(0, len(tempTags[callback_query.from_user.id])):
        edit_markup_number.add(InlineKeyboardButton(tempTags[callback_query.from_user.id][i], callback_data='number_tag' + tempTags[callback_query.from_user.id][i]))
    edit_markup_number.add(done_tags)   
    await bot.send_message(callback_query.from_user.id, "Тег добавлен!", reply_markup=edit_markup_number)
    await Event_state.wait_add_tags.set()
    edit_markup_number.inline_keyboard.clear()

@dp.callback_query_handler(lambda c: c.data == 'done_tags', state = Event_state.wait_add_tags)
async def process_callback_kb1btn1(callback_query: types.CallbackQuery):
    await bot.send_message(callback_query.from_user.id, "Теги добавлены", reply_markup=edit_markup)
    await Event_state.done_poll_button_click.set()

@dp.callback_query_handler(lambda c: c.data == 'remove_tags', state = Event_state.choice_edit_poll_category_click)
async def process_callback_kb1btn1(callback_query: types.CallbackQuery):
    global eventTags
    if callback_query.from_user.id not in eventTags:
        eventTags[callback_query.from_user.id] = list()
    for tag in eventTags[callback_query.from_user.id]:
        edit_markup_number.add(InlineKeyboardButton(tag, callback_data='number_tag' + tag))
    edit_markup_number.add(done_tags)   
    await bot.send_message(callback_query.from_user.id, "Выбери тег для удаления!", reply_markup=edit_markup_number)
    await Event_state.wait_delete_tags.set()
    edit_markup_number.inline_keyboard.clear()
    print('==================')
    print(events)
    print(edit_index)
    print(edit_answer_index)
    print(text)
    print(listAnswers)
    print(matrixAnswers)
    print(anon_type)
    print(multiplyAnswers)
    print('==================')

@dp.callback_query_handler(lambda c: c.data and c.data.startswith('number_tag'), state=Event_state.wait_delete_tags)
async def process_callback_kb1btn1(callback_query: types.CallbackQuery):
    tag = callback_query.data.replace('number_tag', '')
    global eventTags
    # global tempTags
    # tempTags[callback_query.from_user.id].remove(tag)
    if callback_query.from_user.id not in eventTags:
        eventTags[callback_query.from_user.id] = list()
    eventTags[callback_query.from_user.id].remove(tag)
    for i in range(0, len(eventTags[callback_query.from_user.id])):
        edit_markup_number.add(InlineKeyboardButton(eventTags[callback_query.from_user.id][i], callback_data='number_tag' + eventTags[callback_query.from_user.id][i]))
    edit_markup_number.add(done_tags)   
    await bot.send_message(callback_query.from_user.id, "Тег удален!", reply_markup=edit_markup_number)
    await Event_state.wait_delete_tags.set()
    edit_markup_number.inline_keyboard.clear()

@dp.callback_query_handler(lambda c: c.data == 'done_tags', state = Event_state.wait_delete_tags)
async def process_callback_kb1btn1(callback_query: types.CallbackQuery):
    await bot.send_message(callback_query.from_user.id, "Теги удалены", reply_markup=edit_markup)
    await Event_state.done_poll_button_click.set()

@dp.callback_query_handler(lambda c: c.data and c.data.startswith('number_text'), state=Event_state.choice_edit_poll_button_click)
async def process_callback_kb1btn1(callback_query: types.CallbackQuery):
    global edit_index
    edit_index[callback_query.from_user.id] = int(callback_query.data.replace('number_text', ''))
    await bot.send_message(callback_query.from_user.id, 'На что ты хочешь изменить данное сообщение?\n' + text[callback_query.from_user.id][edit_index[callback_query.from_user.id]], reply_markup=markup_cancel_edit)
    await Event_state.replace_text.set()
    print('==================')
    print(events)
    print(edit_index)
    print(edit_answer_index)
    print(text)
    print(listAnswers)
    print(matrixAnswers)
    print(anon_type)
    print(multiplyAnswers)
    print('==================')

@dp.message_handler(state=Event_state.replace_text)
async def process_start_command(message: types.Message):
    global text
    text[message.from_user.id][edit_index[message.from_user.id]] = message.text
    await Event_state.done_poll_button_click.set()
    for i in range(len(matrixAnswers[message.from_user.id])):
        await bot.send_poll(message.chat.id, text[message.from_user.id][i], matrixAnswers[message.from_user.id][i], allows_multiple_answers=multiplyAnswers[message.from_user.id][i])
    await bot.send_message(message.chat.id, "Проверь измененный опрос.\nТы можешь изменить его содержание, нажав \"Редактировать\"!", reply_markup=edit_markup)
    print('==================')
    print(events)
    print(edit_index)
    print(edit_answer_index)
    print(text)
    print(listAnswers)
    print(matrixAnswers)
    print(anon_type)
    print(multiplyAnswers)
    print('==================')

@dp.callback_query_handler(lambda c: c.data == 'answer_edit', state = Event_state.choice_edit_poll_category_click)
async def process_callback_kb1btn1(callback_query: types.CallbackQuery):
    for i in range(len(text[callback_query.from_user.id])):
        edit_markup_number.add(InlineKeyboardButton(str(i + 1), callback_data='number_quest' + str(i)))
    edit_markup_number.add(cancel_btn)
    await bot.send_message(callback_query.from_user.id, "Выбери номер вопроса для редактирования!", reply_markup=edit_markup_number)
    await Event_state.choice_edit_poll_button_click.set()
    edit_markup_number.inline_keyboard.clear()
    print('==================')
    print(events)
    print(edit_index)
    print(edit_answer_index)
    print(text)
    print(listAnswers)
    print(matrixAnswers)
    print(anon_type)
    print(multiplyAnswers)
    print('==================')

@dp.callback_query_handler(lambda c: c.data and c.data.startswith('number_quest'), state=Event_state.choice_edit_poll_button_click)
async def process_callback_kb1btn1(callback_query: types.CallbackQuery):
    global edit_index
    edit_index[callback_query.from_user.id] = int(callback_query.data.replace('number_quest', ''))
    for i in range(0, len(matrixAnswers[callback_query.from_user.id][edit_index[callback_query.from_user.id]])):
        edit_markup_number.add(InlineKeyboardButton(str(i + 1), callback_data='number_answer' + str(i)))
    edit_markup_number.add(cancel_btn)
    await bot.send_message(callback_query.from_user.id, "Выбери номер ответа для редактирования!", reply_markup=edit_markup_number)
    await Event_state.choice_edit_poll_button_click.set()
    edit_markup_number.inline_keyboard.clear()
    print('==================')
    print(events)
    print(edit_index)
    print(edit_answer_index)
    print(text)
    print(listAnswers)
    print(matrixAnswers)
    print(anon_type)
    print(multiplyAnswers)
    print('==================')

@dp.callback_query_handler(lambda c: c.data and c.data.startswith('number_answer'), state=Event_state.choice_edit_poll_button_click)
async def process_callback_kb1btn1(callback_query: types.CallbackQuery):
    global edit_answer_index
    edit_answer_index[callback_query.from_user.id] = int(callback_query.data.replace('number_answer', ''))
    await bot.send_message(callback_query.from_user.id, 'На что ты хочешь изменить данный ответ?\n' + matrixAnswers[callback_query.from_user.id][edit_index[callback_query.from_user.id]][edit_answer_index[callback_query.from_user.id]], reply_markup=markup_cancel_edit)
    await Event_state.replace_answer.set()
    print('==================')
    print(events)
    print(edit_index)
    print(edit_answer_index)
    print(text)
    print(listAnswers)
    print(matrixAnswers)
    print(anon_type)
    print(multiplyAnswers)
    print('==================')

@dp.message_handler(state=Event_state.replace_answer)
async def process_start_command(message: types.Message):
    global matrixAnswers
    matrixAnswers[message.from_user.id][edit_index[message.from_user.id]][edit_answer_index[message.from_user.id]] = message.text
    await Event_state.done_poll_button_click.set()
    for i in range(0, len(matrixAnswers[message.from_user.id])):
        await bot.send_poll(message.chat.id, text[message.from_user.id][i], matrixAnswers[message.from_user.id][i], allows_multiple_answers=multiplyAnswers[message.from_user.id][i])
    await bot.send_message(message.chat.id, "Проверь измененный опрос.\nТы можешь изменить его содержание, нажав \"Редактировать\"!", reply_markup=edit_markup)
    print('==================')
    print(events)
    print(edit_index)
    print(edit_answer_index)
    print(text)
    print(listAnswers)
    print(matrixAnswers)
    print(anon_type)
    print(multiplyAnswers)
    print('==================')

@dp.callback_query_handler(lambda c: c.data == 'header_edit', state = Event_state.choice_edit_poll_category_click)
async def process_callback_kb1btn1(callback_query: types.CallbackQuery):
    await bot.send_message(callback_query.from_user.id, "На что хочешь поменять заголовок " + events[callback_query.from_user.id].header, reply_markup = markup_cancel_edit)
    await Event_state.replace_header.set()
    print('==================')
    print(events)
    print(edit_index)
    print(edit_answer_index)
    print(text)
    print(listAnswers)
    print(matrixAnswers)
    print(anon_type)
    print(multiplyAnswers)
    print('==================')

@dp.callback_query_handler(lambda c: c.data == 'anon_edit', state = Event_state.choice_edit_poll_category_click)
async def process_callback_kb1btn1(callback_query: types.CallbackQuery):
    for i in range(0, len(matrixAnswers[callback_query.from_user.id])):
        await bot.send_poll(callback_query.from_user.id, text[callback_query.from_user.id][i], matrixAnswers[callback_query.from_user.id][i], anon_type[callback_query.from_user.id], allows_multiple_answers=multiplyAnswers[callback_query.from_user.id][i])
    await bot.send_message(callback_query.from_user.id, "Реши, будет ли этот опрос анонимным", reply_markup=anonymous_picker)
    await Event_state.choice_anon.set()
    print('==================')
    print(events)
    print(edit_index)
    print(edit_answer_index)
    print(text)
    print(listAnswers)
    print(matrixAnswers)
    print(anon_type)
    print(multiplyAnswers)
    print('==================')

@dp.callback_query_handler(lambda c: c.data == 'multiply_edit', state = Event_state.choice_edit_poll_category_click)
async def process_callback_kb1btn1(callback_query: types.CallbackQuery):
    for i in range(0, len(matrixAnswers[callback_query.from_user.id])):
        edit_markup_number.add(InlineKeyboardButton(str(i + 1), callback_data='number_multiply' + str(i)))
    edit_markup_number.add(cancel_btn)
    await bot.send_message(callback_query.from_user.id, "Выбери номер вопроса для редактирования!", reply_markup=edit_markup_number)
    await Event_state.choice_edit_poll_button_click.set()
    edit_markup_number.inline_keyboard.clear()
    print('==================')
    print(events)
    print(edit_index)
    print(edit_answer_index)
    print(text)
    print(listAnswers)
    print(matrixAnswers)
    print(anon_type)
    print(multiplyAnswers)
    print('==================')

@dp.callback_query_handler(lambda c: c.data and c.data.startswith('number_multiply'), state = Event_state.choice_edit_poll_button_click)
async def process_callback_kb1btn1(callback_query: types.CallbackQuery):
    global edit_index
    edit_index[callback_query.from_user.id] = int(callback_query.data.replace('number_multiply', ''))
    await bot.send_message(callback_query.from_user.id, "Выбери тип голосования!", reply_markup=edit_multiple_answers_picker)
    await Event_state.change_multiple_answers_button_click.set()
    edit_markup_number.inline_keyboard.clear()
    print('==================')
    print(events)
    print(edit_index)
    print(edit_answer_index)
    print(text)
    print(listAnswers)
    print(matrixAnswers)
    print(anon_type)
    print(multiplyAnswers)
    print('==================')


@dp.callback_query_handler(lambda c: c.data == 'edit_multiply_answer', state = Event_state.change_multiple_answers_button_click)
async def process_callback_kb1btn1(callback_query: types.CallbackQuery):
    multiplyAnswers[callback_query.from_user.id][edit_index[callback_query.from_user.id]] = True
    await bot.send_message(callback_query.from_user.id, "Тип изменен", reply_markup=edit_markup)
    await Event_state.done_poll_button_click.set()
    print('==================')
    print(events)
    print(edit_index)
    print(edit_answer_index)
    print(text)
    print(listAnswers)
    print(matrixAnswers)
    print(anon_type)
    print(multiplyAnswers)
    print('==================')

@dp.callback_query_handler(lambda c: c.data == 'edit_single_answer', state = Event_state.change_multiple_answers_button_click)
async def process_callback_kb1btn1(callback_query: types.CallbackQuery):
    multiplyAnswers[callback_query.from_user.id][edit_index[callback_query.from_user.id]] = False
    await bot.send_message(callback_query.from_user.id, "Тип изменен", reply_markup=edit_markup)
    await Event_state.done_poll_button_click.set()
    print('==================')
    print(events)
    print(edit_index)
    print(edit_answer_index)
    print(text)
    print(listAnswers)
    print(matrixAnswers)
    print(anon_type)
    print(multiplyAnswers)
    print('==================')

@dp.message_handler(state=Event_state.replace_header)
async def process_start_command(message: types.Message):
    events[message.from_user.id].header = message.text
    await Event_state.done_poll_button_click.set()
    await bot.send_message(message.chat.id, "Заголовок изменился", reply_markup=edit_markup)
    print('==================')
    print(events)
    print(edit_index)
    print(edit_answer_index)
    print(text)
    print(listAnswers)
    print(matrixAnswers)
    print(anon_type)
    print(multiplyAnswers)
    print('==================')

@dp.callback_query_handler(lambda c: c.data == 'done_poll', state = Event_state.done_poll_button_click)
async def process_callback_kb1btn1(callback_query: types.CallbackQuery):
    global text
    global matrixAnswers
    await bot.send_message(callback_query.from_user.id, "Опрос окончен, отправляю остальным участникам")
    events[callback_query.from_user.id].question_id_set = list()
    for i in range(0, len(eventTags[callback_query.from_user.id])):
        events[callback_query.from_user.id].tags_set.add(eventTags[callback_query.from_user.id][i])
    for i in range(0, len(matrixAnswers[callback_query.from_user.id])):
        poll_id = await bot.send_poll(callback_query.from_user.id, text[callback_query.from_user.id][i], matrixAnswers[callback_query.from_user.id][i], anon_type[callback_query.from_user.id], allows_multiple_answers=multiplyAnswers[callback_query.from_user.id][i])
        events[callback_query.from_user.id].question_id_set.append(poll_id.message_id)
    users_with_tag = get_users_with_tag(eventTags[callback_query.from_user.id])
    for user in users_with_tag:
        try:
            await bot.send_message(user, "Новый опрос, проверяй!")
        except BotBlocked:
            pass
    await User_state.main_menu.set()
    if callback_query.from_user.id in edit_index:
        edit_index.pop(callback_query.from_user.id)
    if callback_query.from_user.id in edit_answer_index:
        edit_answer_index.pop(callback_query.from_user.id)
    if callback_query.from_user.id in text:
        text.pop(callback_query.from_user.id)
    if callback_query.from_user.id in listAnswers:
        listAnswers.pop(callback_query.from_user.id)
    if callback_query.from_user.id in matrixAnswers:
        matrixAnswers.pop(callback_query.from_user.id)
    if callback_query.from_user.id in anon_type:
        anon_type.pop(callback_query.from_user.id)
    if callback_query.from_user.id in multiplyAnswers:
        multiplyAnswers.pop(callback_query.from_user.id)
    if callback_query.from_user.id in tempTags:
        tempTags.pop(callback_query.from_user.id)
    if callback_query.from_user.id in eventTags:
        eventTags.pop(callback_query.from_user.id)
    if callback_query.from_user.id in events:
        insert_event_to_db(events[callback_query.from_user.id])
    print('==================')
    print(events)
    print(edit_index)
    print(edit_answer_index)
    print(text)
    print(listAnswers)
    print(matrixAnswers)
    print(anon_type)
    print(multiplyAnswers)
    print('==================')
    await User_state.main_menu.set()


if __name__ == '__main__': #опрос сервиса на наличие обновлений
	executor.start_polling(dp)
