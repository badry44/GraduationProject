import flask
import sys
from flaskext.mysql import MySQL
import logging


class DB:

    def __init__(self, app):
        self.app = app
        self.mysql = MySQL()
        self.mysql.init_app(self.app)
        print('This is standard output', file=sys.stdout)

    def executeCommandWithoutResult(self, query, values):
        try:
            connection = self.mysql.connect()
            cursor = connection.cursor()
            cursor.execute(query, values)
            connection.commit()
            cursor.close()
            connection.close()
            return True
        except Exception as e:
            logging.exception(str(e))
            return False

    def executeCommandWithResult(self, query):
        connection = self.mysql.connect()
        cursor = connection.cursor()
        cursor.execute(query)
        result = cursor.fetchall()
        connection.commit()
        cursor.close()
        connection.close()
        return result
