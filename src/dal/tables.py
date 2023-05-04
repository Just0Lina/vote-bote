from dal.request import execute_request
from dal.request import execute_query_request
from dal.request import list_to_postgres_array

class UsersTable:
    def __init__(self, connection):
        self.__connection = connection

    def insert(self, data):
        postgres_insert_query = """insert into users (id, username, campus, role, tribe, tags) values (%s,%s,%s,%s,%s,%s)"""
        record_to_insert = (data[0], data[1], data[2], data[3], data[4], list_to_postgres_array(data[5]))
        insert_data_res = execute_request(self.__connection, postgres_insert_query, record_to_insert)
        tags = [data[2], data[4]]
        update_tags_res = self.__update_user_tags(data[0], tags)
        return insert_data_res and update_tags_res

    def delete(self, user_id):
        postgres_delete_query = """delete from users where id = %s """
        return execute_request(self.__connection, postgres_delete_query, (user_id,))

    def update_data(self, user_id, data, attr):
        postgres_update_query = "update users set " + attr + " = %s where id = %s"
        request = (data, (user_id,))
        return execute_request(self.__connection, postgres_update_query, request)

    def update_tags(self, user_id, data):
        # user_data = self.query(user_id)
        # user_tags = user_data[5]
        # for tag in data:
            # if (tag not in user_tags):
                # user_tags.append(tag)
        # return self.__update_user_tags(user_id, user_tags)
        return self.__update_user_tags(user_id, data)

    # def delete_tags(self, user_id, data):
        # user_data = self.query(user_id)
        # user_tags = user_data[5]
        # for tag in data:
            # if (tag in user_tags):
                # user_tags.remove(tag)
        # return self.__update_user_tags(user_id, user_tags)
        # return self.__update_user_tags(user_id, data)

    def __update_user_tags(self, user_id, user_tags):
        postgres_update_query = "update users set tags = %s where id = %s """
        request = (user_tags, (user_id,))
        return execute_request(self.__connection, postgres_update_query, request)

    def query_all(self):
        postgres_query = "select * from users"""
        result = execute_query_request(self.__connection, postgres_query, "")
        if (len(result)):
            return result
        return None

    def query(self, user_id):
        postgres_query = "select * from users where id = %s """
        result = execute_query_request(self.__connection, postgres_query, (user_id,))
        if (len(result)):
            return result[0]
        return None
    
    def query_attribute(self, user_id, attr):
        postgres_query = "select " + attr + " from users where id = %s """
        result = execute_query_request(self.__connection, postgres_query, (user_id,))
        if (len(result)):
            return result[0][0]
        return None

    def query_by_tag(self, tags):
        users_query = """select id from users"""
        users_id = execute_query_request(self.__connection, users_query, "")
        tags_query = """select tags from users where id = %s """
        users = []
        for usr in users_id:
            user_tags = execute_query_request(self.__connection, tags_query, usr)[0][0]
            if (is_tag_in_list(user_tags, tags)):
                users.append(usr[0])
        return users
    
    def query_by_tag_id(self, tag_id):
        postgres_query = """select * from users where id = %s """
        result = execute_query_request(self.__connection, postgres_query, (tag_id,))
        if (len(result)):
            return result[0]
        return None

    def query_tags_by_user_id(self, user_id):
        postgres_query = """select tags from users where id = %s """
        result = execute_query_request(self.__connection, postgres_query, (user_id,))
        return result[0][0] if result is not None else None

class VotesTable:
    def __init__(self, connection):
        self.__connection = connection

    def query_by_id(self, vote_id):
        postgres_query = "select * from votes where id = %s """
        result = execute_query_request(self.__connection, postgres_query, (vote_id,))
        if (len(result)):
            return result[0]
        return None


    def insert(self, data):
        postgres_insert_query = """ insert into votes (author, header, questions, tags) values (%s,%s,%s,%s)"""
        record_to_insert = (data[0], data[1], data[2], list_to_postgres_array(data[3]))
        return execute_request(self.__connection, postgres_insert_query, record_to_insert)

    def delete(self, vote_id):
        postgres_delete_query = """delete from votes where id = %s """
        return execute_request(self.__connection, postgres_delete_query, (vote_id,))

    def query_all(self):
        postgres_query = "select * from votes"""
        result = execute_query_request(self.__connection, postgres_query, "")
        if (len(result)):
            return result
        return None

    def query_by_author(self, author_id):
        postgres_query = """select id, author, header from votes"""
        vote_data = execute_query_request(self.__connection, postgres_query, "")
        result = []
        for vote in vote_data:
            if (author_id in vote):
                result.append((vote[0], vote[2]))
        if (len(result)):
            return result
        return None

    def query_by_tags(self, tags):
        all_data_query = """select * from votes"""
        all_data_query_result = execute_query_request(self.__connection, all_data_query, "")
        if (all_data_query_result is not None):
            return self.__get_votes_by_tags(all_data_query_result, tags)
        else:
            return None

    def __get_votes_by_tags(self, all_data_query_result, tags):
        result_votes = []
        for vote in all_data_query_result:
            if (is_tag_in_list(vote[4], tags)):
                result_votes.append((vote))
        if (len(result_votes)):
            return result_votes
        return None
 
class TagsTable:
    def __init__(self, connection):
        self.__connection = connection

    def insert(self, data):
        postgres_insert_query = """ insert into vote_tags (tag, role) values (%s,%s) """
        record_to_insert = (data[0], data[1])
        return execute_request(self.__connection, postgres_insert_query, record_to_insert)

    def delete(self, tag_name):
        postgres_delete_query = """delete from vote_tags where tag = %s """
        return execute_request(self.__connection, postgres_delete_query, tag_name)

    def query_all(self):
        postgres_query = "select * from vote_tags"""
        result = execute_query_request(self.__connection, postgres_query, "")
        if (len(result)):
            return result
        return None

    def query_by_role(self, role):
        result = []
        if (role == "ADM"):
            result = self.__tags_for_adm()
        else:
            result = self.__tags_for_students(role)
        if (len(result)):
            return result
        return None

    def __tags_for_adm(self):
        postgres_query = """select * from vote_tags """
        all_tags = execute_query_request(self.__connection, postgres_query, "")
        result_tags = []
        for tag in all_tags:
            result_tags.append(tag[0])
        return result_tags

    def __tags_for_students(self, role):
        postgres_query = """select * from vote_tags"""
        all_tags = execute_query_request(self.__connection, postgres_query, "")
        result_tags = []
        for tag in all_tags:
            if role == tag[1]:
                result_tags.append(tag[0])
        return result_tags

class TribesTable:
    def __init__(self, connection):
        self.__connection = connection

    def insert(self, data):
        postgres_insert_query = """ insert into tribes (campus, students_list, abiturients_list) values (%s,%s,%s) """
        record_to_insert = (data[0], list_to_postgres_array(data[1]), list_to_postgres_array(data[2]))
        return execute_request(self.__connection, postgres_insert_query, record_to_insert)

    def delete(self, campus):
        postgres_delete_query = """delete from tribes where campus = %s """
        return execute_request(self.__connection, postgres_delete_query, (campus,))

    def query_by_role(self, data, role):
        tribes_list = "abiturients_list"
        if (role == "student"):
            tribes_list = "students_list"
        postgres_query = """select """ + tribes_list + """ from tribes where campus = %s"""
        result = execute_query_request(self.__connection, postgres_query, (data,))
        return result[0] if result is not None else None

    def query_campuses(self):
        postgres_query = "select campus from tribes" 
        return execute_query_request(self.__connection, postgres_query, "")


def is_tag_in_list(data_tags, user_tags):
    for tag in data_tags:
        if tag in user_tags:
            return True
    return False

