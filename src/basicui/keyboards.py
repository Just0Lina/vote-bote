from aiogram.types import ReplyKeyboardRemove, \
    ReplyKeyboardMarkup, KeyboardButton, \
    InlineKeyboardMarkup, InlineKeyboardButton

inline_btn_adm = InlineKeyboardButton('ADM', callback_data='role-ADM')
inline_btn_stud = InlineKeyboardButton('Student', callback_data='role-student')
inline_btn_abit = InlineKeyboardButton('Интенсивист я, с меня нечего взять', callback_data='role-applicant')
inline_kb_full= InlineKeyboardMarkup().add(inline_btn_adm, inline_btn_stud, inline_btn_abit)

editing_role_stud = InlineKeyboardButton('Student', callback_data='editing_role-student')
editing_role_abit = InlineKeyboardButton('Интенсивист я, с меня нечего взять', callback_data='editing_role-applicant')
editing_role = InlineKeyboardMarkup().add(editing_role_stud, editing_role_abit)

registr_btn = InlineKeyboardButton('Время зарегистрироваться!', callback_data='markup_request')
fast_registr_btn = InlineKeyboardButton('Быстрый старт', callback_data='fast_markup_request')
inline_kb1 = InlineKeyboardMarkup().add(registr_btn, fast_registr_btn)

inline_msk_btn = InlineKeyboardButton("Москва", callback_data='city-Moscow')
inline_nsk_btn = InlineKeyboardButton("Новосибирск", callback_data='city-Novosibirsk')
inline_kazan_btn = InlineKeyboardButton("Казань", callback_data='city-Kazan')
campus = InlineKeyboardMarkup(row_width=1).add(inline_kazan_btn).add(inline_nsk_btn).add(inline_msk_btn)
editing_msk_btn = InlineKeyboardButton("Москва", callback_data='editing_city-Moscow')
editing_nsk_btn = InlineKeyboardButton("Новосибирск", callback_data='editing_city-Novosibirsk')
editing_kazan_btn = InlineKeyboardButton("Казань", callback_data='editing_city-Kazan')
editing_campus = InlineKeyboardMarkup(row_width=1).add(editing_kazan_btn).add(editing_nsk_btn).add(editing_msk_btn)

adm_inline_msk_btn = InlineKeyboardButton("Москва", callback_data='tribe-Moscow')
adm_inline_nsk_btn = InlineKeyboardButton("Новосибирск", callback_data='tribe-Novosibirsk')
adm_inline_kazan_btn = InlineKeyboardButton("Казань", callback_data='tribe-Kazan')
adm_campus = InlineKeyboardMarkup(row_width=1).add(adm_inline_kazan_btn).add(adm_inline_nsk_btn).add(adm_inline_msk_btn)

trash = KeyboardButton("Стереть все данные и начать заново")
trash_btn = ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=True).add(trash)

create_vote = InlineKeyboardButton("Создать новый опрос", callback_data='none')
my_votes = InlineKeyboardButton("Посмотреть мои опросы", callback_data='none')
help_btn = InlineKeyboardButton("Список моих тегов и основных особенностей бота", callback_data='none')
get_votes = InlineKeyboardButton("Посмотреть доступные опросы", callback_data='none')
fast_start = InlineKeyboardButton("Найти опрос по ID", callback_data='none')
editing_btn = InlineKeyboardButton("Редактирование", callback_data='none')
main_win = ReplyKeyboardMarkup(row_width = 1, resize_keyboard=True).add(create_vote).add(my_votes).add(get_votes).add(fast_start).add(help_btn,  editing_btn)

editing_role_btn = InlineKeyboardButton("Роль", callback_data='change_role')
editing_camp_btn = InlineKeyboardButton("Кампус", callback_data='change_camp')
editing_tribe_btn = InlineKeyboardButton("Трайб", callback_data='change_tribe')
editing_tag_btn = InlineKeyboardButton("Теги", callback_data='change_tags')
editing_back_btn = InlineKeyboardButton("Назад", callback_data='back_from_edit')
editing_btns = InlineKeyboardMarkup(row_width = 1).add(editing_role_btn, editing_camp_btn, editing_tribe_btn, editing_tag_btn, editing_back_btn)

no_btn = InlineKeyboardButton("Завершить редактрование", callback_data='change_state')
yes_btn = InlineKeyboardButton("Продолжить", callback_data='editing_again')
yes_no_btns = InlineKeyboardMarkup(row_width = 2).add(yes_btn, no_btn)

tag_yes_btn = InlineKeyboardButton("Добавить", callback_data='add_tag')
tag_no_btn = InlineKeyboardButton("Удалить", callback_data='delete_tag')
editing_tags = InlineKeyboardMarkup(row_width = 2).add(tag_yes_btn, tag_no_btn)