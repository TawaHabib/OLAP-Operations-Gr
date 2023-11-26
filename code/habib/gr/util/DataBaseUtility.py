import os

import mysql.connector
import util.ExecuterManager as Em
from util.Util import Util
from util.IKillable import Killable


class Connection(object):

    def get_connection(self):
        pass


class MySqlConnection(Connection):
    def __init__(self, file_name: str) -> None:
        #print('in')
        self.file = file_name
        self.connection = MySqlConnection.open_connection(file_name)

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
        if self.connection.is_connected():
            return self.connection
        return MySqlConnection.open_connection(self.file)


def create_connection(path_to_properties: str = '../../../utilities/config.property') -> Connection:
    return MySqlConnection(path_to_properties)


class SqlExecutor(Killable):
    def __init__(self, path_to_sql_code_file: str, sql_section: str,
                 path_to_save_data: str = '../../../utilities/actual_result.csv'):
        self.connection = create_connection()
        self.cursor = self.connection.get_connection().cursor()
        self.sql_file = path_to_sql_code_file
        self.sql_section = sql_section
        self.actual_result = path_to_save_data

    def execute_and_save(self, kay: str):
        sql_code = Util.get_properties_from_file(self.sql_file, 'utf-8', self.sql_section, kay)
        self.cursor.execute(sql_code)
        if os.path.exists(self.actual_result):
            os.remove(self.actual_result)
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

    def kill(self):
        self.connection.get_connection().close()


def get_sql_executor(path_to_sql_code_file: str = '../../../utilities/sql_commands',
                     sql_section: str = 'SQL_CODE',
                     path_to_save_data: str = '../../../utilities/actual_result.csv') -> SqlExecutor:
    return SqlExecutor(path_to_sql_code_file=path_to_sql_code_file,
                       sql_section=sql_section,
                       path_to_save_data=path_to_save_data)
