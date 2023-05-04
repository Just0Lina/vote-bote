from kernel import bot, dp, User, users, unique_adm_pin, tribes, User_state, Status, Event_state
from gateway.controller import insert_user_to_db, check_registration, get_user_data_from_db, get_vote_by_id, update_user_campus, update_user_role, get_votes_by_tags, update_user_tribe, get_user_role,  get_user_campus, get_user_tags, get_tags_for_id, update_tags, get_votes_by_author
from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.utils import executor
from aiogram.types.message import ContentType
from aiogram.utils.markdown import text, bold, italic, code, pre
from aiogram.types import ParseMode
from aiogram.types import ReplyKeyboardRemove, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.dispatcher.filters.state import State, StatesGroup
from aiogram.contrib.fsm_storage.memory import MemoryStorage

import smtplib
from email.mime.text import MIMEText

import basicui.keyboards as kb

userTags = dict()
tempTags = dict()

User_state.new.set

def send_mail_message(pas):
    receiver_email= users[pas].name + "@student.21-school.ru"
    print(receiver_email)
    sender_email= "telegram_bot_s21@mail.ru"
    password = "6wmsdyGGgzB59qAmAwn0"
    message = "This message is your personal code. Please, do not tell it anybody: " + str(pas)
    msg = MIMEText(message)
    msg['Subject'] = "Verefication message from vote-bot"
    smtp_server = "smtp.mail.ru"
    port = 465
    server = smtplib.SMTP_SSL(smtp_server, port)
    server.connect(smtp_server,465)
    server.ehlo()
    server.login(sender_email, password)
    server.sendmail(sender_email, receiver_email, msg.as_string())
    server.close()

@dp.callback_query_handler(lambda c: c.data == 'markup_request', state = User_state.registration)
async def process_callback_button1(callback_query: types.CallbackQuery):
    await bot.answer_callback_query(callback_query.id) # Если честно и без этого работает, я просто не знаю
    users[callback_query.from_user.id] = User(callback_query.from_user.id)
    await bot.send_message(callback_query.from_user.id,'Выбери свою роль в школе',reply_markup=kb.inline_kb_full)


@dp.callback_query_handler(lambda c: c.data == 'role-ADM', state=User_state.registration)
async def process_callback_button1(callback_query: types.CallbackQuery):
    if callback_query.from_user.id not in users:
        users[callback_query.from_user.id] = User(callback_query.from_user.id)
    users[callback_query.from_user.id].role = callback_query.data[5:]
    await bot.send_message(callback_query.from_user.id,'Введите уникальный код доступа')
    await bot.send_message(callback_query.from_user.id, "Код доступа для АДМ: " + unique_adm_pin)
    await Status.adm_pin.set()

@dp.callback_query_handler(lambda c: c.data == 'fast_markup_request', state=User_state.registration)
async def process_callback_button1(callback_query: types.CallbackQuery):
    await bot.send_message(callback_query.from_user.id,'Введите уникальный ID опроса в котором хотите принять участие')
    await Status.vote_id.set()
    




edit_markup_number = InlineKeyboardMarkup()
done_tags = InlineKeyboardButton('Готово', callback_data='done_tags')

@dp.callback_query_handler(lambda c: c.data == 'add_tag', state = User_state.editing_data_tags)
async def process_callback_kb1btn1(callback_query: types.CallbackQuery):
    global tempTags, userTags
    if callback_query.from_user.id not in tempTags:
        tempTags[callback_query.from_user.id] = list()
    tempTags[callback_query.from_user.id] = get_tags_for_id(callback_query.from_user.id)
    temp = get_user_tags(callback_query.from_user.id)
    userTags[callback_query.from_user.id] = temp
    x = list(set(tempTags[callback_query.from_user.id]) - set(temp))
    for i in range(0, len(x)):
        edit_markup_number.add(InlineKeyboardButton(x[i], callback_data='number_tag' + x[i]))
    edit_markup_number.add(done_tags)   
    tempTags[callback_query.from_user.id] = x
    await User_state.editing_data_tags_add.set()
    await bot.send_message(callback_query.from_user.id, "Выбери тег для добавления!", reply_markup=edit_markup_number)
    edit_markup_number.inline_keyboard.clear()



@dp.callback_query_handler(lambda c: c.data.startswith('number_tag'), state = User_state.editing_data_tags_add)
async def process_callback_button1(callback_query: types.CallbackQuery):
    global userTags, tempTags
    if callback_query.from_user.id not in userTags:
        userTags[callback_query.from_user.id] = list()
    tag = callback_query.data.replace('number_tag', '')
    userTags[callback_query.from_user.id].append(tag)
    tempTags[callback_query.from_user.id].remove(tag)
    for i in range(0, len(tempTags[callback_query.from_user.id])):
        edit_markup_number.add(InlineKeyboardButton(tempTags[callback_query.from_user.id][i], callback_data='number_tag' + tempTags[callback_query.from_user.id][i]))
    edit_markup_number.add(done_tags)   
    await bot.send_message(callback_query.from_user.id, "Выбери тег для добавления!", reply_markup=edit_markup_number)
    edit_markup_number.inline_keyboard.clear()


@dp.callback_query_handler(lambda c: c.data == 'delete_tag', state = User_state.editing_data_tags)
async def process_callback_kb1btn1(callback_query: types.CallbackQuery):
    global userTags
    if callback_query.from_user.id not in userTags:
        userTags[callback_query.from_user.id] = list() 
    temp = get_user_tags(callback_query.from_user.id)
    userTags[callback_query.from_user.id] = temp
    for i in range(0, len(temp)):
        edit_markup_number.add(InlineKeyboardButton(temp[i], callback_data='number_tag' + temp[i]))
    edit_markup_number.add(done_tags)   
    await User_state.editing_data_tags_delete.set()
    await bot.send_message(callback_query.from_user.id, "Выбери тег для удаления", reply_markup=edit_markup_number)
    edit_markup_number.inline_keyboard.clear()



@dp.callback_query_handler(lambda c: c.data.startswith('number_tag'), state = User_state.editing_data_tags_delete)
async def process_callback_button1(callback_query: types.CallbackQuery):
    global userTags
    tag = callback_query.data.replace('number_tag', '')
    userTags[callback_query.from_user.id].remove(tag)
    data = userTags[callback_query.from_user.id]
    for i in range(0, len(data)):
        edit_markup_number.add(InlineKeyboardButton(data[i], callback_data='number_tag' + data[i]))
    edit_markup_number.add(done_tags)   
    await bot.send_message(callback_query.from_user.id, "Выбери тег для удаления!", reply_markup=edit_markup_number)
    edit_markup_number.inline_keyboard.clear()


@dp.callback_query_handler(lambda c: c.data.startswith('done_tags'), state = User_state.editing_data_tags_add)
async def process_callback_button1(callback_query: types.CallbackQuery):
    global userTags, tempTags
    update_tags(callback_query.from_user.id, userTags[callback_query.from_user.id])
    userTags.clear()
    tempTags.clear()
    await User_state.editing_data.set()
    mes = 'Теги изменены!\nПродолжить редактирование?' 
    await bot.send_message(callback_query.from_user.id, mes, reply_markup=kb.yes_no_btns)


@dp.callback_query_handler(lambda c: c.data.startswith('done_tags'), state = User_state.editing_data_tags_delete)
async def process_callback_button1(callback_query: types.CallbackQuery):
    global userTags, tempTags
    update_tags(callback_query.from_user.id, userTags[callback_query.from_user.id])
    userTags.clear()
    tempTags.clear()
    await User_state.editing_data.set()
    mes = 'Теги изменены!\nПродолжить редактирование?' 
    await bot.send_message(callback_query.from_user.id, mes, reply_markup=kb.yes_no_btns)




@dp.callback_query_handler(lambda c: c.data == 'change_state', state=User_state.editing_data)
async def process_callback_button1(callback_query: types.CallbackQuery):
    await User_state.main_menu.set()
    await bot.send_message(callback_query.from_user.id,'Редактирование успешно закончено!')

@dp.callback_query_handler(lambda c: c.data.startswith('change_role'), state = User_state.editing_data)
async def process_callback_button(callback_query: types.CallbackQuery):
    if get_user_role(callback_query.from_user.id) == "ADM":
        await bot.send_message(callback_query.from_user.id, 'Чтобы сменить роль с ADM обратись к администратору\nПродолжить редактирование', reply_markup=kb.yes_no_btns)
        await User_state.editing_data.set()
    else:
        await User_state.editing_data_role.set()
        await bot.send_message(callback_query.from_user.id,'Выбери свою роль в школе!', reply_markup=kb.editing_role)

@dp.callback_query_handler(lambda c: c.data.startswith('change_camp'), state = User_state.editing_data)
async def process_callback_button(callback_query: types.CallbackQuery):
    await User_state.editing_data_city.set()
    await bot.send_message(callback_query.from_user.id, 'Выбери свой кампус!' ,reply_markup=kb.editing_campus)

@dp.callback_query_handler(lambda c: c.data.startswith('change_tribe'), state = User_state.editing_data)
async def process_callback_button(callback_query: types.CallbackQuery): 
    await User_state.editing_data_tribe.set()
    user_data = get_user_data_from_db(callback_query.from_user.id)
    if user_data[3] == 'ADM':
        await User_state.editing_data.set()
        mes1 = text('АДМ сразу принадлежит всем трайбам!', 'Ничего изменить нельзя', 'Продолжить редактирование?', sep = '\n')
        await bot.send_message(callback_query.from_user.id, mes1, parse_mode=ParseMode.MARKDOWN, reply_markup=kb.yes_no_btns)
    else:
        tribe = InlineKeyboardMarkup(row_width=1)
        for i in range(4):
            tribe_name = tribes[user_data[2] + "-" + user_data[3]][i]
            tribe.add(InlineKeyboardButton(tribe_name, callback_data='editing_tribe-' + tribe_name))
        await bot.send_message(callback_query.from_user.id,'Выбери свой трайб!!', reply_markup=tribe)   
       
@dp.callback_query_handler(lambda c: c.data.startswith('change_tags'), state = User_state.editing_data)
async def process_callback_button(callback_query: types.CallbackQuery):
    await User_state.editing_data_tags.set()
    await bot.send_message(callback_query.from_user.id, 'Что нужно сделать c тегами?' ,reply_markup=kb.editing_tags)


@dp.callback_query_handler(lambda c: c.data.startswith('editing_city'), state=User_state.editing_data_city)
async def process_callback_button1(callback_query: types.CallbackQuery):
    tribe = InlineKeyboardMarkup(row_width=1)
    user_data = get_user_data_from_db(callback_query.from_user.id)
    update_user_campus(callback_query.from_user.id, callback_query.data[13:])
    if get_user_role(callback_query.from_user.id) == 'ADM':
        mes = 'Город успешно изменен!\nПродолжить редактирование?' 
        await User_state.editing_data.set()
        await bot.send_message(callback_query.from_user.id, mes, reply_markup=kb.yes_no_btns)
    else:
        user_data = get_user_data_from_db(callback_query.from_user.id)
        await User_state.editing_data_tribe.set()
        tribe = InlineKeyboardMarkup(row_width=1)
        for i in range(4):
            tribe_name = tribes[get_user_campus(callback_query.from_user.id) + "-" + get_user_role(callback_query.from_user.id)][i]
            tribe.add(InlineKeyboardButton(tribe_name, callback_data='editing_tribe-' + tribe_name))
        await bot.send_message(callback_query.from_user.id,'Выбери свой трайб!', reply_markup=tribe)


@dp.callback_query_handler(lambda c: c.data.startswith('editing_role'), state=User_state.editing_data_role)
async def process_callback_button1(callback_query: types.CallbackQuery):
    update_user_role(callback_query.from_user.id, callback_query.data[13:])
    mes = 'Роль успешно изменена!\nПродолжить редактирование?' 
    await User_state.editing_data.set()
    await bot.send_message(callback_query.from_user.id, mes, reply_markup=kb.yes_no_btns)


@dp.callback_query_handler(lambda c: c.data.startswith("editing_tribe"), state=User_state.editing_data_tribe)
async def end_of_registration(callback_query: types.CallbackQuery):
    user_data = get_user_data_from_db(callback_query.from_user.id)
    update_user_tribe(callback_query.from_user.id, callback_query.data[14:])
    mes = 'Трайб успешно изменен!\n Продолжить редактирование?' 
    await User_state.editing_data.set()
    await bot.send_message(callback_query.from_user.id, mes, reply_markup=kb.yes_no_btns)

@dp.callback_query_handler(lambda c: c.data.startswith('role'), state=User_state.registration)
async def process_callback_button1(callback_query: types.CallbackQuery):
    if callback_query.from_user.id not in users:
        users[callback_query.from_user.id] = User(callback_query.from_user.id)
    users[callback_query.from_user.id].role = callback_query.data[5:]
    await User_state.nickname.set()
    await bot.send_message(callback_query.from_user.id,'Введи свой ник в школе!')

@dp.message_handler(text=['Посмотреть мои опросы'], state=User_state.main_menu)
async def show_my_votes(message: types.Message):
    await bot.send_message(message.chat.id, "Мои опросы")
    my_votes = ""
    votes = get_votes_by_author(message.from_user.id)
    print(votes)
    if votes != None and len(votes) != 0:
        for i in range(len(votes)):
            my_votes += votes[i][1] + ' / id: ' + str(votes[i][0]) + '\n'
    if my_votes != "":
        await bot.send_message(message.from_user.id, my_votes)
    else:
        await bot.send_message(message.from_user.id, 'Тут пока пусто, создай свой первый опрос с разделе меню \"Создать новый опрос\"')

@dp.message_handler(text=['Посмотреть доступные опросы'], state=User_state.main_menu)
async def process_name(message: types.Message):
    await bot.send_message(message.chat.id, "Доступные опросы")
    tags = get_user_tags(message.chat.id)
    if tags and len(tags) != 0:
        votes = InlineKeyboardMarkup(row_width=1)
        polls = get_votes_by_tags(tags)
        if polls != None:
            for i in range(len(polls)):
                votes.add(InlineKeyboardButton(polls[i][2] + ' / id: ' + str(polls[i][0]), callback_data='vote-' + str(polls[i][0])))
            votes.add(InlineKeyboardButton('Назад', callback_data='back_from_vote'))
            await Status.showing_votes.set()
            await bot.send_message(message.chat.id,'Выбери интересующий опрос!', reply_markup=votes)
        else:
            await bot.send_message(message.from_user.id, 'Пока что для тебя нет подходящих опросов, можешь создать свой в разделе меню \"Создать новый опрос\" или поискать опросы по другим тегам, добавив их себе в разделе меню \"Редактирование\"')
    else:
        await bot.send_message(message.from_user.id, 'У тебя нет ни одного тега по которому можно найти опросы для тебя, добавь их в разделе меню \"Редактирование\"')

@dp.callback_query_handler(lambda c: c.data.startswith("back_from_vote"), state=Status.showing_votes)
async def end_of_registration(callback_query: types.CallbackQuery):
    mes = "Теперь ты снова в меню"
    await User_state.main_menu.set()
    await bot.send_message(callback_query.from_user.id, mes, reply_markup = kb.main_win)

@dp.callback_query_handler(lambda c: c.data.startswith("vote"), state=Status.showing_votes)
async def end_of_registration(callback_query: types.CallbackQuery):
    id_vote = callback_query.data[5:]
    data = get_vote_by_id(id_vote)
    # print(data)
    await bot.send_message(callback_query.from_user.id, data[2])
    if len(data) != 0:
        for poll in data[3]:
            await bot.forward_message(callback_query.from_user.id, data[1], poll)
    mes = "Теперь ты снова в меню"
    await User_state.main_menu.set()
    await bot.send_message(callback_query.from_user.id, mes, reply_markup = kb.main_win)



@dp.message_handler(text=['Найти опрос по ID'], state=User_state.main_menu)
async def process_name(message: types.Message):
    mes = "Введите ID"
    await bot.send_message(message.chat.id, mes)
    await Status.vote_id.set()


@dp.message_handler(text=['Стереть все данные и начать заново'], state="*")
async def process_name(message: types.Message, state: FSMContext):
    await state.finish()
    await bot.send_message(message.chat.id, "Хорошо", reply_markup=ReplyKeyboardRemove())
    if check_registration(message.from_user.id):
        await User_state.main_menu.set()
        await bot.send_message(message.chat.id, "Теперь ты снова в меню", reply_markup = kb.main_win)
    else:
        mes = "Попробуем еще раз"
        await bot.send_message(message.chat.id, mes)
        await process_start_command(message)

@dp.message_handler(text=['Список моих тегов и основных особенностей бота'], state=User_state.main_menu)
async def process_name(message: types.Message):
    mes = bold('Это все твои теги:')+'\n'
    tags = get_user_tags(message.chat.id)
    mes1 = "\n"+bold("Некоторые особенности:")+"\nПри добавлении опроса к нему обязательно выбирать теги. Вопросы рассылаются по хотя бы одному совпадению тегов у пользователя.\nОпросы которые ты создаешь попадают в \"Мои опросы\""
    await bot.send_message(message.chat.id,text(mes+",\n".join(tags)+mes1), parse_mode=ParseMode.MARKDOWN)

@dp.message_handler(text=['Редактирование'], state=User_state.main_menu)
async def process_name(message: types.Message):
    users[message.chat.id] = User(message.chat.id)
    await User_state.editing_data.set()
    await bot.send_message(message.chat.id,'Что требуется изменить?',reply_markup=kb.editing_btns)


@dp.callback_query_handler(lambda c: c.data == 'editing_again', state=User_state.editing_data)
async def end_of_registration(callback_query: types.CallbackQuery):
    users[callback_query.from_user.id] = User(callback_query.from_user.id)
    await User_state.editing_data.set()
    await bot.send_message(callback_query.from_user.id,'Что требуется изменить?',reply_markup=kb.editing_btns)

@dp.callback_query_handler(lambda c: c.data.startswith("back_from_edit"), state=User_state.editing_data)
async def end_of_registration(callback_query: types.CallbackQuery):
    mes = "Теперь ты снова в меню"
    await User_state.main_menu.set()
    await bot.send_message(callback_query.from_user.id, mes, reply_markup = kb.main_win)

@dp.callback_query_handler(lambda c: c.data.startswith("tribe"), state=Status.end_of_sign_up)
async def end_of_registration(callback_query: types.CallbackQuery):
    mes = "Теперь тебе доступно больше новых возможностей! Обратись к кнопкам)"
    if users[callback_query.from_user.id].role == 'ADM':
        if callback_query.from_user.id not in users:
            users[callback_query.from_user.id] = User(callback_query.from_user.id)
        users[callback_query.from_user.id].city = callback_query.data[6:]
        users[callback_query.from_user.id].tribe = 'ADM'
    else:
        if callback_query.from_user.id not in users:
            users[callback_query.from_user.id] = User(callback_query.from_user.id)
        users[callback_query.from_user.id].tribe = callback_query.data[6:]
    insert_user_to_db(users[callback_query.from_user.id])
    await User_state.main_menu.set()
    await bot.send_message(callback_query.from_user.id, mes, reply_markup = kb.main_win)
    

@dp.callback_query_handler(lambda c: c.data.startswith('city'), state=User_state.city)
async def process_callback_button1(callback_query: types.CallbackQuery):
    await User_state.tribe.set()
    code = callback_query.data[5:]
    if callback_query.from_user.id not in users:
        users[callback_query.from_user.id] = User(callback_query.from_user.id)
    users[callback_query.from_user.id].city = code
    tribe = InlineKeyboardMarkup(row_width=1)
    for i in range(4):
        tribe_name = tribes[code + "-" + users[callback_query.from_user.id].role][i]
        tribe.add(InlineKeyboardButton(tribe_name, callback_data='tribe-' + tribe_name))
    await Status.end_of_sign_up.set()
    await bot.send_message(callback_query.from_user.id,'Теперь ты можешь выбрать свой трайб!', reply_markup=tribe)

@dp.message_handler(state=Status.vote_id)
async def process_name(message: types.Message):
    data = None
    if message.text.isdigit():
        data = get_vote_by_id(message.text)
    message_text = "Теперь ты опять на стадии регистрации"
    mes = "Ты опять в меню"
    if data and len(data) !=0 and len(data[3]) != 0:
        print(data)
        for poll in data[3]:
            await bot.forward_message(message.from_user.id, data[1], poll)
    else:
        await bot.send_message(message.from_user.id, "Опрос не найден")
    if check_registration(message.from_user.id):
        await User_state.main_menu.set()
        await bot.send_message(message.from_user.id, mes, reply_markup = kb.main_win)
    else:
        await User_state.registration.set()
        await bot.send_message(message.from_user.id, message_text, parse_mode=ParseMode.MARKDOWN, reply_markup=kb.inline_kb1)
   


@dp.message_handler(state=Status.adm_pin)
async def process_name(message: types.Message):
    await Status.trash.set()
    if message.text == unique_adm_pin:
        mes = 'Ты ввел верный код, отлично\nПришло время узнать друг друга поближе)\nКак я могу к тебе обращаться?'
        await bot.send_message(message.chat.id, mes)
        if message.chat.id not in users:
            users[message.chat.id] = User(message.from_chat.id)
        users[message.chat.id].role = "ADM"
        #print(users)
        await User_state.adm_name.set()
    else:
        await Status.adm_pin.set()
        mes = 'Пароль не подходит, попробуйте снова или нажмите сброс'
        await bot.send_message(message.chat.id, mes, reply_markup=kb.trash_btn)

@dp.message_handler(state=User_state.adm_name)
async def process_name(message: types.Message):
    mes1 = "Приятно познакомиться, " + message.text + '!'
    mes = "\nВыбери свой кампус!"
    if message.from_user.id not in users:
        users[message.from_user.id] = User(message.from_user.id)
    users[message.from_user.id].name = message.text
    #print(users)
    await User_state.city.set()
    await Status.end_of_sign_up.set()
    await bot.send_message(message.from_user.id, mes1 + mes,reply_markup=kb.adm_campus)

@dp.message_handler(state=User_state.email)
async def process_name(message: types.Message):
    await User_state.new.set()
    if str(message.chat.id) == message.text:
        await bot.send_message(message.chat.id, 'Ты ввел верный код, отлично')
        mes = "Выбери свой кампус!"
        await bot.send_message(message.chat.id, mes,reply_markup=kb.campus)
        await User_state.city.set()
    else:
        mes = 'Код не подходит, попробуйте снова или нажмите сброс'
        await User_state.email.set()
        await bot.send_message(message.chat.id, mes, reply_markup=kb.trash_btn)


@dp.message_handler(state=User_state.nickname)
async def process_name(message: types.Message):
    await User_state.new.set()
    if message.from_user.id not in users:
        users[message.from_user.id] = User(message.from_user.id)
    users[message.from_user.id].name = message.text
    #print(users)
    mes1 = text("Тебе на почту, привязанную к учетной записи, отравлено письмо с уникальным кодом доступа")
    mes2 = text("Пришли его в чат!")
    await bot.send_message(message.from_user.id, mes1+'\n'+mes2)
    await bot.send_message(message.from_user.id, "Это код который был отправлен тебе на почту: " + str(message.from_user.id))
    print(message.from_user.id)
    send_mail_message(message.from_user.id)
    await User_state.email.set()



@dp.message_handler(commands=['start'], state='*') #need to add states
async def process_start_command(message: types.Message):
    mes1 = text(bold('Привет'), 'Ты попал в бота школы 21\n', sep='\n')
    mes2 = text( 'Этот бот дает тебе возможность принять участие во всевозможных опросах и ничего не упустить!', sep='\n')
    mes = "Наконец-то мы можем заняться опросами! Обратись к кнопкам)"
    message_text = mes1+mes2
    if check_registration(message.from_user.id):
        await User_state.main_menu.set()
        await bot.send_message(message.from_user.id, mes, reply_markup = kb.main_win)
    else:
        await User_state.registration.set()
        await bot.send_message(message.from_user.id, message_text, parse_mode=ParseMode.MARKDOWN, reply_markup=kb.inline_kb1)


@dp.message_handler(state="*",commands=['help'])
async def process_help_command(message: types.Message):
    mes1 = "Этот бот предназначен для опрашивания мнений студентов и сотрудников школы 21 :eyes:\n"
    mes2 = "Bсе доступные тебе команды можно посмотреть в пуле с кнопками, после регистрации будет доступна кнопка с более полным описанием возможностей"
    await message.reply(mes1+mes2)


if __name__ == '__main__': #опрос сервиса на наличие обновлений
    executor.start_polling(dp)



