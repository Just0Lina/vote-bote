import os
from socket import AddressInfo
from gateway.controller import delete_user_by_id, delete_event_by_id, add_tag, delete_tag, get_all_events, get_all_tags, get_all_users
from admin import ADMIN_PIN
from kernel import bot, dp
from aiogram import types
from aiogram.types import ParseMode

from kernel import Admin_state, User_state


@dp.message_handler(commands=['admin-' + ADMIN_PIN], state='*')
async def admin_access(message: types.Message):
    await Admin_state.admin.set()
    await bot.send_message(message.from_user.id, "Admin access granted")

@dp.message_handler(commands=['remove-user'], state=Admin_state.admin)
async def remove_user_db(message: types.Message):
    await Admin_state.remove_user.set()
    await bot.send_message(message.from_user.id, "Enter user id to remove")

@dp.message_handler(state=Admin_state.remove_user)
async def read_user_id_to_remove(message: types.Message):
    # remove from db controller call
    await bot.send_message(message.from_user.id, "User to remove id: " + message.text)
    if delete_user_by_id(message.text):
        await bot.send_message(message.from_user.id, "User successfully removed")
    else:
        await bot.send_message(message.from_user.id, "No user found")
    await Admin_state.admin.set()

@dp.message_handler(commands=['remove-event'], state=Admin_state.admin)
async def remove_event_db(message: types.Message):
    await Admin_state.remove_event.set()
    await bot.send_message(message.from_user.id, "Enter event id to remove")

@dp.message_handler(state=Admin_state.remove_event)
async def read_event_id_to_remove(message: types.Message):
    # remove frod db controller call
    await bot.send_message(message.from_user.id, "Event to remove id: " + message.text)
    if delete_event_by_id(message.text):
        await bot.send_message(message.from_user.id, "User successfully removed")
    else:
        await bot.send_message(message.from_user.id, "No event found")
    await Admin_state.admin.set()

@dp.message_handler(commands=['add-tag'], state=Admin_state.admin)
async def add_tag_db(message: types.Message):
    await bot.send_message(message.from_user.id, "Enter tag/role to be added")
    await Admin_state.add_tag.set()

@dp.message_handler(state=Admin_state.add_tag)
async def read_tag_to_add(message: types.Message):
    # add to db controller call
    tag = message.text.split('/')
    await bot.send_message(message.from_user.id, "Tag to be added: " + tag[0] + ' ' + tag[1])
    if add_tag(tag):
        await bot.send_message(message.from_user.id, "Tag successfully added")
    else:
        await bot.send_message(message.from_user.id, "Inserting failed")
    await Admin_state.admin.set()

@dp.message_handler(commands=['remove-tag'], state=Admin_state.admin)
async def add_tag_db(message: types.Message):
    await bot.send_message(message.from_user.id, "Enter tag to be removed")
    await Admin_state.remove_tag.set()

@dp.message_handler(state=Admin_state.remove_tag)
async def read_tag_to_add(message: types.Message):
    # remove from db controller call
    await bot.send_message(message.from_user.id, "Tag to be removed: " + message.text)
    if delete_tag(message.text):
        await bot.send_message(message.from_user.id, "Tag successfully removed")
    else:
        await bot.send_message(message.from_user.id, "No tag found")
    await Admin_state.admin.set()

@dp.message_handler(commands=['get-users'], state=Admin_state.admin)
async def show_users_db(message: types.Message):
    users = get_all_users()
    with open('users.txt', 'w') as f:
        pass
    with open('users.txt', 'a') as f:
        if users != None:
            for user in users:
                f.write(str(user) + '\n')
        else:
            f.write("empty")
    await bot.send_document(message.from_user.id, open('users.txt', 'rb'))
    os.remove("users.txt")
    # write to file and send in chat???

@dp.message_handler(commands=['get-events'], state=Admin_state.admin)
async def show_users_db(message: types.Message):
    events = get_all_events()
    with open('events.txt', 'w') as f:
        pass
    with open('events.txt', 'a') as f:
        if events != None:
            for event in events:
                f.write(str(event) + '\n')
        else:
            f.write('empty')
    await bot.send_document(message.from_user.id, open('events.txt', 'rb'))
    os.remove("events.txt")
    # write to file and send in chat???

@dp.message_handler(commands=['get-tags'], state=Admin_state.admin)
async def show_users_db(message: types.Message):
    tags = get_all_tags()
    with open('tags.txt', 'w') as f:
        pass
    with open('tags.txt', 'a') as f:
        if tags != None:
            for tags in tags:
                f.write(str(tags) + '\n')
        else:
            f.write("empty")
    await bot.send_document(message.from_user.id, open('tags.txt', 'rb'))
    os.remove("tags.txt")
    # write to file and send in chat???

@dp.message_handler(commands=['exit'], state=Admin_state.admin)
async def admin_exit(message: types.Message):
    await bot.send_message(message.from_user.id, "Admin access closed. Type /start to continute in user mode")
    await User_state.new.set()


@dp.message_handler(state='*')
async def unknown_message(msg: types.Message):  
    await msg.reply("Ошибка", parse_mode=ParseMode.MARKDOWN)