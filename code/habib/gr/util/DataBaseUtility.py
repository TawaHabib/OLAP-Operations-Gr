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
        self.connection = MySqlConnection.open_connection(file_name)

    @staticmethod
    def open_connection(file_prop: str):
        encoding = 'utf-8'
        #connection = None
        host = Util.get_properties_from_file(file_prop, encoding, 'SQL_CONN', 'host')
        database = Util.get_properties_from_file(file_prop, encoding, 'SQL_CONN', 'database')
        user = Util.get_properties_from_file(file_prop, encoding, 'SQL_CONN', 'user')
        password = Util.get_properties_from_file(file_prop, encoding, 'SQL_CONN', 'password')

        connection = mysql.connector.connect(host=host, database=database, user=user, password=password)

        return connection

    def get_connection(self) -> mysql.connector.MySQLConnection:
        try:
            if self.is_connect():
                return self.connection
            self.connection = MySqlConnection.open_connection(self.file)
        except Exception as e:
            print(e)


    def is_connect(self) -> bool:
        res = False
        try:
            res = self.connection.is_connected()
        except Exception as e:
            print(e)
            res = False
        print(res)
        return res


def create_connection(path_to_properties: str = '../../../utilities/config.property') -> Connection:
    return MySqlConnection(path_to_properties)


class SqlExecutor(Killable):
    def __init__(self, path_to_sql_code_file: str, sql_section: str,
                 path_to_save_data: str = '../../../utilities/actual_result.csv'):
        try:
            self.connection = create_connection()
        except:
            self.connection = None
        finally:
            self.sql_file = path_to_sql_code_file
            self.sql_section = sql_section
            self.actual_result = path_to_save_data


    def execute_and_save(self, kay: str):
        try:
            print ('dentro try')
            if os.path.exists(self.actual_result) and self.connection.is_connect():
                print('file remuve')
                os.remove(self.actual_result)
            else :
                x = self.connection.get_connection()
                print(x)
        except Exception as e:
            print(e)
            return
        try:
            sql_code = Util.get_properties_from_file(self.sql_file, 'utf-8', self.sql_section, kay)
            cursor = self.connection.get_connection().cursor()
            cursor.execute(sql_code)
            file = open(self.actual_result, 'a', encoding='utf-8')
            line = ''
            for des in cursor.description:
                line = line+str(des[0])+';'
            file.write(line+'\n')
            num_lines=0
            while True:
                try:
                    result = cursor.fetchone()

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
        except Exception as e1:
            print(e1)

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
