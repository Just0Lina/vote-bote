import psycopg2
import getpass
from psycopg2 import Error
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
from dal.tables import *

class Database:
    def __init__(self):
        self.__connection = None
        self.__connect_to_server()
        self.__init_tables()

    def close_connection():
        if (self.__connection is not None):
            self.__connection.cursor().close()
            self.__connection.close()

    def isConnected(self):
        return self.__connection is not None

    def insert_user(self, data):
        return self.__users_table.insert(data)
        
    def insert_vote(self, data):
        return self.__votes_table.insert(data)

    def insert_tag(self, data):
        return self.__tags_table.insert(data)

    def update_user_campus(self, user_id, data):
        return self.__users_table.update_data(user_id, data, "campus")

    def update_user_role(self, user_id, data):
        return self.__users_table.update_data(user_id, data, "role")

    def update_user_tribe(self, user_id, data):
        return self.__users_table.update_data(user_id, data, "tribe")

    def update_user_tags(self, user_id, data):
        return self.__users_table.update_tags(user_id, data)

    # def delete_user_tags(self, user_id, data):
        # return self.__users_table.delete_tags(user_id, data)

    def get_vote_by_id(self, vote_id):
        return self.__votes_table.query_by_id(vote_id)

    def delete_user(self, user_id):
        return self.__users_table.delete(user_id)
        
    def delete_vote(self, data):
        return self.__votes_table.delete(data)

    def delete_tag(self, data):
        return self.__tags_table.delete(data)

    def get_all_users(self):
        return self.__users_table.query_all()

    def get_user_data(self, user_id):
        return self.__users_table.query(user_id)

    def get_user_name(self, user_id):
        return self.__users_table.query_attribute(user_id, "username")

    def get_user_role(self, user_id):
        return self.__users_table.query_attribute(user_id, "role")

    def get_user_campus(self, user_id):
        return self.__users_table.query_attribute(user_id, "campus")

    def get_user_tribe(self, user_id):
        return self.__users_table.query_attribute(user_id, "tribe")

    def get_user_tags(self, user_id):
        return self.__users_table.query_tags_by_user_id(user_id)

    def get_user_acces_tags(self, user_id):
        user_role = self.get_user_role(user_id)
        return self.__tags_table.query_by_role(user_role)

    def get_users_by_tag(self, tags):
        return self.__users_table.query_by_tag(tags)

    def get_user_by_tag_id(self, tag_id):
        return self.__tags_table.query(tag_id)

    def get_all_votes(self):
        return self.__votes_table.query_all()

    def get_vote_data(self, user_id):
        return self.__votes_table.query_by_author(user_id)

    def get_votes_by_tags(self, tags):
        return self.__votes_table.query_by_tags(tags)
    
    def get_all_tags(self):
        return self.__tags_table.query_all()

    def get_tags_for_all(self):
        return self.__tags_table.query_all()

    def get_tags_for_role(self, role):
        return self.__tags_table.query_by_role(role)
    
    def insert_tribes(self, data):
        return self.__tribes_table.insert(data)

    def delete_tribes(self, data):
        return self.__tribes_table.delete(data)

    def get_tribes_by_role(self, data, role):
        return self.__tribes_table.query_by_role(data, role)
    
    def get_campuses(self):
        return self.__tribes_table.query_campuses()

    def __init_tables(self):
        if (self.__connection is not None):
            self.__users_table = UsersTable(self.__connection)
            self.__votes_table = VotesTable(self.__connection)
            self.__tags_table = TagsTable(self.__connection)
            self.__tribes_table = TribesTable(self.__connection)
    
    def __connect_to_server(self):
        self.__connection = self.__connect_to_database()
        if (self.__connection is not None):
            self.__connect_to_alive_server()

    def __connect_to_database(self):
        try:
            return psycopg2.connect(
                    user=getpass.getuser(),
                    password="1111",
                    host="127.0.0.1",
                    port="5432",
                    database="postgres"
            )
        except:
            return None
        
    def __connect_to_alive_server(self):
        cursor = self.__connection.cursor()
        try:
            sql_create_database = 'create database postgres'
            cursor.execute(sql_create_database)
        except:
            self.__connection.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
