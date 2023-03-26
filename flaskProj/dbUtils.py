# import mysql.connector
from MySQLdb import _mysql, _exceptions

class DBErrors(Exception):
    pass

class DBCommands():
    def __init__(self, host, user, password, db, port) -> None:
        self.host = host
        self.user = user
        self.password = password
        self.db = db
        self.port = port

    def __enter__(self) -> "cursor":
        try:
            self.conn = _mysql.connect(self.host, self.user, self.password, self.db, self.port)
            self.cursor = self.conn.cursor()
            return self.cursor
        except _exceptions.InterfaceError as error:
            raise DBErrors("Interface Error", error)
        except _exceptions.ProgrammingError as error:
            raise DBErrors("Programming Error", error)

    def __exit__(self, executeType, executeValue, executeTrace) -> None:
        self.conn.commit()
        self.cursor.close()
        self.conn.close()

        if executeType is _exceptions.ProgrammingError:
            raise DBErrors(executeType)
        elif executeType:
            raise executeType(executeValue)
