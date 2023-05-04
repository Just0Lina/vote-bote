from dal import DB
from kernel import User, users, Event, events

def delete_user_by_id(user_id):
    return DB.delete_user(user_id)

def delete_event_by_id(event_id):
    return DB.delete_vote(event_id)

def add_tag(tag):
    return DB.insert_tag(tag)

def delete_tag(tag):
    return DB.delete_tag(tag)

def get_all_users():
    return DB.get_all_users()

def get_all_events():
    return DB.get_all_votes()

def get_all_tags():
    return DB.get_all_tags()

def get_user_data_from_db(user_id):
    return DB.get_user_data(user_id)

def get_user_role(user_id):
    return DB.get_user_role(user_id)

def get_user_name(user_id):
    return DB.get_user_name(user_id)

def get_user_campus(user_id):
    return DB.get_user_campus(user_id)

def get_user_tribe(user_id):
    return DB.get_user_tribe(user_id)

def update_user_campus(user_id, data):
    return DB.update_user_campus(user_id, data)

def update_user_role(user_id, data):
    return DB.update_user_role(user_id, data)

def update_user_tribe(user_id, data):
    return DB.update_user_tribe(user_id, data)

def get_vote_by_id(vote_id):
    return DB.get_vote_by_id(vote_id)

def update_tags(user_id, data):
    return DB.update_user_tags(user_id, data)

def insert_user_to_db(user: User):
    if DB.insert_user((user.tg_id, user.name, user.city, user.role, user.tribe, user.tags_set)):
        print("User successfully inserted")
    else:
        print("User insert failed")
    users.pop(user.tg_id)
    # done.remove(index)
    print(DB.get_user_data(user.tg_id))

def insert_event_to_db(event: Event):
    if DB.insert_vote((event.author_id, event.header, event.question_id_set, event.tags_set)):
        print("Event successfully inserted")
    else:
        print("Event insert failed")
    events.pop(event.author_id)
    print(DB.get_vote_data(event.author_id))

def check_registration(tg_id):
    print(DB.get_user_data(tg_id))
    if DB.get_user_data(tg_id) == None:
        return False
    return True

def get_users_with_tag(tag):
    return DB.get_users_by_tag(tag)

def get_tags_for_id(user_id):
    return DB.get_user_acces_tags(user_id)

def get_user_tags(user_id):
    return DB.get_user_tags(user_id)

def get_votes_by_tags(tags):
    return DB.get_votes_by_tags(tags)

def get_votes_by_author(author_id):
    return DB.get_vote_data(author_id)

def cancel_create_vote_remove_user(user_id):
    if user_id in users:
        users.pop(user_id)
