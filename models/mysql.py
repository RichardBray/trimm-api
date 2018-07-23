import MySQLdb
import MySQLdb.cursors
import logging


class MySql:
    TABLE = ""

    @staticmethod
    def connect_to_db():
        return MySQLdb.connect(
            "localhost", "root", "", "trimm-api",
            cursorclass=MySQLdb.cursors.DictCursor)

    @staticmethod
    def simpe_query(query, params=None):
        db = MySql.connect_to_db()
        cursor = db.cursor()
        cursor.execute(query, params)
        db.commit()
        db.close()

    @staticmethod
    def fetchall_query(query, params=None):
        db = MySql.connect_to_db()
        cursor = db.cursor()
        cursor.execute(query, params)
        data = cursor.fetchall()
        db.close()
        return data

    @classmethod
    def insert_into(cls, **kwargs):
        keys = kwargs.keys()
        query = "INSERT INTO {} ({}) VALUES({})".format(
            cls.TABLE, ', '.join(keys), ', '.join(['%s'] * len(keys)))
        logging.debug("SQL query: %s %s" % (query, kwargs))
        MySql.simpe_query(query, kwargs.values())

    @classmethod
    def select_where(cls, field, value):
        query = "SELECT * FROM {} WHERE {}=%s".format(cls.TABLE, field)
        return MySql.fetchall_query(query, (value, ))

    # @classmethod
    # def update_where(cls, *args):
    #     query = "UPDATE {} SET {} = '{}' WHERE id = {}".format(
    #         cls.TABLE, args[0], args[1], args[2])
    #     MySql.simpe_query(query)

    # @classmethod
    # def delete_where(cls, id):
    #     query = "DELETE FROM {} WHERE id={}".format(cls.TABLE, id)
    #     MySql.simpe_query(query)


class Users(MySql):
    TABLE = "users"


class Spending(MySql):
    TABLE = "spending"


class Categories(MySql):
    TABLE = "categories"

