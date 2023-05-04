import basicui

from aiogram import Bot
from aiogram.dispatcher import Dispatcher
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher.filters.state import State, StatesGroup

# Bot initialize
TOKEN = '5432840231:AAEgT6GKL9FtjdVuBlyqDhbIWOec--rgPZA'
# TOKEN = '5578683944:AAEzcWugqa9kjgvBomA9VbL_L2CxLvinAas'
# TOKEN = '5413630252:AAFQ3GXLe74hLKGDgnslU9LmKrZP5dC338w'

bot = Bot(token=TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())

# Classes to keep data
class User:
    tg_id = None
    name = None
    city = None
    role = None
    tribe = None
    tags_set = None

    def __init__(self):
        self.tg_id = 0
        self.name = "name"
        self.role = "role"
        self.city = "city"
        self.tribe = "tribe"
        self.tags_set = set()

    def __init__(self, id):
        self.tg_id = id
        self.name = "name"
        self.role = "role"
        self.city = "city"
        self.tribe = "tribe"
        self.tags_set = set()

    def __repr__(self):
        return str(self.tg_id) + ", " + str(self.name) + ", " + str(self.role) + ", " + str(self.city) + ", " + str(self.tribe) + ", " + str(self.tags_set) 

    def __str__(self):
        return str(self.tg_id) + ", " + str(self.name) + ", " + str(self.role) + ", " + str(self.city) + ", " + str(self.tribe) + ", " + str(self.tags_set) 

class Event:
    author_id = None
    header = None
    question_id_set = None
    tags_set = None

    def __init__(self):
        self.author_id = 0
        self.header = "header"
        self.question_id_set = list()
        self.tags_set = set()

    def __init__(self, id):
        self.author_id = id
        self.header = "header"
        self.question_id_set = list()
        self.tags_set = set()

    def __repr__(self):
        return str(self.author_id) + ", " + str(self.header) + ", " + str(self.question_id_set) + ", " + str(self.tags_set)

    def __str__(self):
        return str(self.author_id) + ", " + str(self.header) + ", " + str(self.question_id_set) + ", " + str(self.tags_set)
    
    


# Dictionaries for data from many users
users = dict()
events = dict()


# ADM registration config
unique_adm_pin = "Violetta_crash"


# names of tribes // move to DB???
tribes = {"Kazan-student" : ['Terra', 'Aqua', 'Aer', 'Ignis'],
"Novosibirsk-student" : ['Diamonds', 'Emeralds', 'Rubies', 'Sapphires'],
"Moscow-student" : ['Alpacas', 'Сapybaras', 'Honey Badgers', 'Salamanders'],
"Kazan-applicant" : ['Morays', 'Scorpionfishs', 'Anglers', 'Ignis'],
"Novosibirsk-applicant" : ['Photons', 'Quarks', 'Leptons', 'Gluons'],
"Moscow-applicant" : ['Axolotls', 'Slugs', 'Tardigrades', 'Trionics']}


# states
class User_state(StatesGroup):
    email = State()
    nickname = State()
    adm_name = State()
    city = State()
    tribe = State()
    registration = State()
    main_menu = State()
    editing_data = State()
    editing_data_role = State()
    editing_data_city = State()
    editing_data_tribe = State()
    editing_data_tags = State()
    editing_data_tags_add = State()
    editing_data_tags_delete = State()
    new = State()

class Status(StatesGroup):
    fast_pin = State()
    adm_pin = State()
    showing_votes = State()
    end_of_sign_up = State()
    end_of_fast_sign_up = State()
    trash = State()
    vote_id = State()

class Event_state(StatesGroup):
    start = State()
    read_header = State()
    read_text_poll = State()
    wait_answer_creation_button_click = State()
    wait_anon_pick_button_click = State()
    wait_duration_button_click = State()
    wait_tag_button_click = State()
    wait_new_question_button_click = State()
    choice_edit_poll_category_click = State()
    choice_edit_poll_button_click = State()
    replace_header = State()
    replace_text = State()
    replace_answer = State()
    choice_delete_poll_category_click = State()
    choice_delete_poll_button_click = State()
    done_poll_button_click = State()
    choice_delete_answer_button_click = State()
    delete_answer_button_click = State()
    choice_add_poll_category_click = State()
    choice_add_answer_button_click = State()
    choice_add_answer = State()
    choice_anon = State()
    allows_multiple_answers_pick = State()
    wait_multiple_answers_button_click = State()
    change_multiple_answers_button_click = State()
    wait_add_tags = State()
    wait_delete_tags = State()

class Admin_state(StatesGroup):
    admin = State()
    remove_user = State()
    remove_event = State()
    add_tag = State()
    remove_tag = State()

import kernel.registration
import kernel.event_create
