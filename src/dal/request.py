import psycopg2
from psycopg2 import Error

def execute_request(connection, postgres_query, record_to_request):
    try:
        cursor = connection.cursor()
        cursor.execute(postgres_query, record_to_request)
        connection.commit()
        if (has_data(cursor)):
            return True
        return False
    except(Exception, psycopg2.Error) as error:
        print(error)
        return False

def execute_query_request(connection, postgres_query, record_to_request):
    try:
        cursor = connection.cursor()
        cursor.execute(postgres_query, record_to_request)
        connection.commit()
        try:
            return cursor.fetchall()
        except:
            return None
    except(Exception, psycopg2.Error) as error:
        print(error)
        return None

def has_data(cursor):
    return cursor.rowcount == 1

def list_to_postgres_array(alist):
    return '{' + ','.join(alist) + '}'

