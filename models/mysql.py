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
    def insert_single(cls, **kwargs):
        keys = kwargs.keys()
        query = "INSERT INTO {} ({}) VALUES({})".format(
            cls.TABLE, ', '.join(keys), ', '.join(['%s'] * len(keys)))
        logging.debug("SQL query: %s %s" % (query, kwargs))
        MySql.simpe_query(query, kwargs.values())

    # @classmethod
    # def query_all(cls):
    #     query = "SELECT * FROM {}".format(cls.TABLE)
    #     return MySql.fetchall_query(query)

    # @classmethod
    # def delete_single(cls, id):
    #     query = "DELETE FROM {} WHERE id={}".format(cls.TABLE, id)
    #     MySql.simpe_query(query)

    @classmethod
    def query_single(cls, *args):
        query = "SELECT * FROM {} WHERE {}='{}'".format(cls.TABLE, args[0], args[1])
        return MySql.fetchall_query(query)

    # @classmethod
    # def update_single(cls, *args):
    #     query = "UPDATE {} SET {} = '{}' WHERE id = {}".format(
    #         cls.TABLE, args[0], args[1], args[2])
    #     MySql.simpe_query(query)


class Users(MySql):
    TABLE = "users"
