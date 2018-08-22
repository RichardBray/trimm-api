import MySQLdb
import MySQLdb.cursors
import logging
from tornado.options import define, options

define("db_user", default="root")
define("db_host", default="localhost")
define("db_password", default="localhost")
define("db_name", default="trimm-api")

class MySql:
    TABLE = ""

    @staticmethod
    def connect_to_db():
        return MySQLdb.connect(
            options.db_host, options.db_user, options.db_password, options.db_name,
            cursorclass=MySQLdb.cursors.DictCursor)

    @staticmethod
    def simpe_query(query, params=None):
        db = MySql.connect_to_db()
        cursor = db.cursor()
        cursor.execute(query, params)
        logging.info(query)
        logging.info(params)
        db.commit()
        db.close()

    @staticmethod
    def fetchall_query(query, params=None):
        db = MySql.connect_to_db()
        cursor = db.cursor()
        cursor.execute(query, params)
        logging.info(query)
        logging.info(params)
        data = cursor.fetchall()
        db.close()
        return data

    @classmethod
    def insert_into(cls, **kwargs):
        keys = kwargs.keys()
        query = "INSERT INTO {} ({}) VALUES({})".format(
            cls.TABLE, ', '.join(keys), ', '.join(['%s'] * len(keys)))
        MySql.simpe_query(query, kwargs.values())

    @classmethod
    def select_where_and(cls, field, value, field2, value2):
        query = "SELECT * FROM {} WHERE {}=%s AND {}=%s".format(cls.TABLE, field, field2)
        return MySql.fetchall_query(query, (value, value2))

    @classmethod
    def select_where(cls, field, value):
        query = "SELECT * FROM {} WHERE {}=%s".format(cls.TABLE, field)
        return MySql.fetchall_query(query, (value, ))

    @classmethod
    def select_between_dates(cls, **kwargs):
        query = "SELECT * FROM {} WHERE({} BETWEEN %s AND %s) AND {}=%s".format(cls.TABLE, kwargs['date_field'], kwargs['field'])
        return MySql.fetchall_query(query, (kwargs['start_date'], kwargs['end_date'], kwargs['field_val']))

    @classmethod
    def delete_where(cls, field, value):
        query = "DELETE FROM {} WHERE {}=%s".format(cls.TABLE, field)
        MySql.simpe_query(query, (value, ))

    @classmethod
    def update_where(cls, field, value, **kwargs):
        """
        Updates stuff in the database.
            :param field: field where update is made
            :param value: value to compare it against
            :param kwargs: the fields and their values that
            need updating
        Example:
        >>> Users.update_where(user_uuid, data['user_uuid'], user_currency='dollars')
        >>> UPDATE Users SET user_currency WHERE user_uuid='98adfu8u...'
        """
        fields = []

        for key in kwargs:
            fields.append(key + '=%s')
        
        query = "UPDATE {} SET {} WHERE {}=%s".format(
            cls.TABLE, ', '.join(fields), field)
        MySql.simpe_query(query, (*kwargs.values(), value))


class Users(MySql):
    TABLE = "users"


class Spending(MySql):
    TABLE = "spending"


class Categories(MySql):
    TABLE = "categories"
