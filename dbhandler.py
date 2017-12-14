from config import Config
import psycopg2
import urllib
import os
import psycopg2.extras
import time
import datetime

# urllib.parse.uses_netloc.append('postgres')
# url = urllib.parse.urlparse(os.environ.get('DATABASE_URL'))


def query_select(sql_str, variables=None, connection_str=Config.DB_CONNECTION_STR):
    try:
        with psycopg2.connect(connection_str) as connection:
            with connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cursor:
                cursor.execute(sql_str, variables)
                return cursor.fetchall()
    except psycopg2.DatabaseError as exception:
        print(exception)

"""
Runs a modification query.

returns: boolean - True if the query was successful
"""

def query_modify(sql_str, variables=None, connection_str=Config.DB_CONNECTION_STR):
    try:
        with psycopg2.connect(connection_str) as connection:
            with connection.cursor() as cursor:
                cursor.execute(sql_str, variables)
                connection.commit()

                message = sql_str.split()[0] + " done."
                print(message)
                return (True, message)
    except psycopg2.DatabaseError as exception:
        connection.rollback()
        print(exception)
        return (False, str(exception))