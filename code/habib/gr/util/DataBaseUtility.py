import os

import mysql.connector
import util.ExecuterManager as Em
from util.Util import Util
from util.IKillable import Killable


class Connection(object):

    def get_connection(self):
        pass

    def is_connect(self) -> bool:
        pass


class MySqlConnection(Connection):
    def __init__(self, file_name: str) -> None:
        #print('in')
        self.file = file_name
        try:
            self.connection = MySqlConnection.open_connection(file_name)
        except Exception as e:
            print(e)

    @staticmethod
    def open_connection(file_prop: str):
        encoding = 'utf-8'
        connection = None
        host = Util.get_properties_from_file(file_prop, encoding, 'SQL_CONN', 'host')
        database = Util.get_properties_from_file(file_prop, encoding, 'SQL_CONN', 'database')
        user = Util.get_properties_from_file(file_prop, encoding, 'SQL_CONN', 'user')
        password = Util.get_properties_from_file(file_prop, encoding, 'SQL_CONN', 'password')
        try:
            connection = mysql.connector.connect(host=host, database=database, user=user, password=password)
        except Exception as e:
            print(e)
        return connection

    def get_connection(self) -> mysql.connector.MySQLConnection:
        c = None
        try:
            if self.connection.is_connected():
                return self.connection
        except:
            try:
                c = MySqlConnection.open_connection(self.file)
                self.connection = c
            except:
                pass
            finally:
                return c

    def is_connect(self) -> bool:
        res = False
        try:
            res = self.connection.is_connected()
        except:
            res = False
        return res


def create_connection(path_to_properties: str = '../../../utilities/config.property') -> Connection:
    return MySqlConnection(path_to_properties)


class SqlExecutor(Killable):
    def __init__(self, path_to_sql_code_file: str, sql_section: str,
                 path_to_save_data: str = '../../../utilities/actual_result.csv'):
        try:
            self.connection = create_connection()
            self.cursor = self.connection.get_connection().cursor()
            self.sql_file = path_to_sql_code_file
            self.sql_section = sql_section
            self.actual_result = path_to_save_data
        except:
            pass

    def execute_and_save(self, kay: str):
        try:
            if os.path.exists(self.actual_result) and self.connection.get_connection().is_connected():
                os.remove(self.actual_result)
        except:
            return
        sql_code = Util.get_properties_from_file(self.sql_file, 'utf-8', self.sql_section, kay)
        self.cursor.execute(sql_code)
        file = open(self.actual_result, 'a', encoding='utf-8')
        line = ''
        for des in self.cursor.description:
            line = line+str(des[0])+';'
        file.write(line+'\n')
        num_lines=0
        while True:
            try:
                result = self.cursor.fetchone()

                line = ''
                for attribute in result:
                    line = line+str(attribute)+';'
                line = str(line+'\n')
                num_lines += 1
                file.write(line)
            except:
                print('Righe'+str(num_lines))
                file.close()
                break

    def can_execute(self):
        return self.connection.is_connect()

    def kill(self):
        try:
            self.connection.get_connection().close()
        except:
            pass


def get_sql_executor(path_to_sql_code_file: str = '../../../utilities/sql_commands',
                     sql_section: str = 'SQL_CODE',
                     path_to_save_data: str = '../../../utilities/actual_result.csv') -> SqlExecutor:
    return SqlExecutor(path_to_sql_code_file=path_to_sql_code_file,
                       sql_section=sql_section,
                       path_to_save_data=path_to_save_data)
