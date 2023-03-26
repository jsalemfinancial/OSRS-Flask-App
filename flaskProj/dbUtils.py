import mysql.connector


class DBErrors(Exception):
    pass

class DBCommands():
    def __init__(self, dbConfig: dict) -> None:
        self.config = dbConfig

    def __enter__(self) -> "cursor":
        try:
            self.conn = mysql.connector.connect(**self.config)
            self.cursor = self.conn.cursor()
            return self.cursor
        except mysql.connector.errors.InterfaceError as error:
            raise DBErrors("Interface Error", error)
        except mysql.connector.errors.ProgrammingError as error:
            raise DBErrors("Programming Error", error)

    def __exit__(self, executeType, executeValue, executeTrace) -> None:
        self.conn.commit()
        self.cursor.close()
        self.conn.close()

        if executeType is mysql.connector.errors.ProgrammingError:
            raise DBErrors(executeType)
        elif executeType:
            raise executeType(executeValue)
