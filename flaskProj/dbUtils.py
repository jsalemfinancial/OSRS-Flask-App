# import mysql.connector
from MySQLdb import _exceptions
from flaskProj import mysql

class DBErrors(Exception):
    pass

class DBCommands():
    # def __init__(self, host, user, password, db, port) -> None:
    #     self.host = host
    #     self.user = user
    #     self.password = password
    #     self.db = db
    #     self.port = port

    def __enter__(self) -> "cursor":
        try:
            self.cursor = mysql.connection.cursor()
            return self.cursor
        except _exceptions.InterfaceError as error:
            raise DBErrors("Interface Error", error)
        except _exceptions.ProgrammingError as error:
            raise DBErrors("Programming Error", error)

    def __exit__(self, executeType, executeValue, executeTrace) -> None:
        if executeType is _exceptions.ProgrammingError:
            raise DBErrors(executeType)
        elif executeType:
            raise executeType(executeValue)
