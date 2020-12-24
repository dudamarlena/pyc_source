# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\shaonutil\mysqlDB.py
# Compiled at: 2020-04-06 13:14:23
# Size of source mod 2**32: 26990 bytes
"""Mysql Database"""
from tkinter import ttk, Tk, Label, Entry
import tkinter as tk
from shaonutil.security import generateCryptographicallySecureRandomString
import mysql.connector as mysql
import subprocess, shaonutil, os, pandas

class MySQL:
    __doc__ = 'A class for all mysql actions'

    def __init__(self, config, init_start_server=True, log=False):
        self.log = log
        self.init_start_server = init_start_server
        self.config = config

    def start_mysql_server(self):
        """Start mysql server"""
        mysql_bin_folder = self._config['mysql_bin_folder']
        DETACHED_PROCESS = 8
        pids = shaonutil.process.is_process_exist('mysqld.exe')
        if not pids:
            process = subprocess.Popen([os.path.join(mysql_bin_folder, 'mysqld.exe'), '--standalone', '--debug'], creationflags=DETACHED_PROCESS)
            print('Starting mysql server at pid', process.pid)
            return process
        print('MYSQL Server is already running at pids', pids)

    def stop_mysql_server(self, force=False):
        """Stop MySQL Server"""
        mysql_bin_folder = self._config['mysql_bin_folder']
        user = self._config['user']
        password = self._config['password']
        pids = shaonutil.process.is_process_exist('mysqld.exe')
        if pids:
            print('MYSQL running at pids', pids)
            if force == True:
                shaonutil.process.killProcess_ByAll('mysqld.exe')
                print('Forced stop MySQL Server ...')
            else:
                DETACHED_PROCESS = 8
                process = subprocess.Popen([os.path.join(mysql_bin_folder, 'mysqladmin.exe'), '-u', user, '--password=' + password, 'shutdown'])
                print('Stopping MySQL Server ...')
        else:
            print('MYSQL Server is not already running... , you can not close.')

    def reopen_connection(self):
        """reopen"""
        print('MySQL > Explicitly opening connection ...')
        self.make_cursor()

    def close_connection(self):
        """closing the connection"""
        print('MySQL > Explicitly closing connection ...')
        self._cursor.close()
        self.mySQLConnection.close()

    @property
    def config(self):
        return self._config

    @config.setter
    def config(self, new_value):
        self._config = new_value
        self.filter_config()
        self.make_cursor()

    def filter_config(self):
        mustList = [
         'host', 'user', 'password']
        for key in self._config:
            if key not in mustList:
                ValueError(key, 'should have in passed configuration')
                break

    def make_cursor(self):
        if self.init_start_server:
            self.start_mysql_server()
        try:
            if 'database' in self._config:
                mySQLConnection = mysql.connect(host=(self._config['host']),
                  user=(self._config['user']),
                  passwd=(self._config['password']),
                  database=(self._config['database']))
            else:
                mySQLConnection = mysql.connect(host=(self._config['host']),
                  user=(self._config['user']),
                  passwd=(self._config['password']))
            self.mySQLConnection = mySQLConnection
        except mysql.errors.OperationalError:
            print('Error')
        else:
            self._cursor = mySQLConnection.cursor()

    def is_mysql_user_exist(self, mysql_username):
        """check if mysql user exist return type:boolean"""
        mySQLCursor = self._cursor
        mySqlListUsers = 'select host, user from mysql.user;'
        mySQLCursor.execute(mySqlListUsers)
        userList = mySQLCursor.fetchall()
        foundUser = [user_ for host_, user_ in userList if user_ == mysql_username]
        if len(foundUser) == 0:
            return False
        return True

    def listMySQLUsers--- This code section failed: ---

 L. 130         0  LOAD_FAST                'self'
                2  LOAD_ATTR                _cursor
                4  STORE_FAST               'cursor'

 L. 131         6  LOAD_STR                 'SELECT Host,User FROM MYSQL.USER'
                8  STORE_FAST               'mySqlListUsers'

 L. 132        10  LOAD_FAST                'cursor'
               12  LOAD_METHOD              execute
               14  LOAD_FAST                'mySqlListUsers'
               16  CALL_METHOD_1         1  ''
               18  POP_TOP          

 L. 133        20  LOAD_FAST                'cursor'
               22  LOAD_METHOD              fetchall
               24  CALL_METHOD_0         0  ''
               26  STORE_FAST               'rows'

 L. 134        28  LOAD_GLOBAL              print
               30  LOAD_STR                 'MySQL > Listing MySQL Users ...'
               32  CALL_FUNCTION_1       1  ''
               34  POP_TOP          

 L. 137        36  BUILD_LIST_0          0 

 L. 138        38  BUILD_LIST_0          0 

 L. 136        40  LOAD_CONST               ('Host', 'User')
               42  BUILD_CONST_KEY_MAP_2     2 
               44  STORE_DEREF              'data'

 L. 141        46  LOAD_FAST                'rows'
               48  GET_ITER         
               50  FOR_ITER             76  'to 76'
               52  STORE_DEREF              'row'

 L. 142        54  LOAD_CLOSURE             'data'
               56  LOAD_CLOSURE             'row'
               58  BUILD_TUPLE_2         2 
               60  LOAD_DICTCOMP            '<code_object <dictcomp>>'
               62  LOAD_STR                 'MySQL.listMySQLUsers.<locals>.<dictcomp>'
               64  MAKE_FUNCTION_8          'closure'
               66  LOAD_DEREF               'data'
               68  GET_ITER         
               70  CALL_FUNCTION_1       1  ''
               72  STORE_DEREF              'data'
               74  JUMP_BACK            50  'to 50'

 L. 144        76  LOAD_GLOBAL              pandas
               78  LOAD_METHOD              DataFrame
               80  LOAD_DEREF               'data'
               82  CALL_METHOD_1         1  ''
               84  STORE_FAST               'dbf'

 L. 145        86  LOAD_GLOBAL              print
               88  LOAD_FAST                'dbf'
               90  CALL_FUNCTION_1       1  ''
               92  POP_TOP          

Parse error at or near `LOAD_DICTCOMP' instruction at offset 60

    def createMySQLUser(self, host, userName, password, querynum=0, updatenum=0, connection_num=0):
        """Create a Mysql User"""
        cursor = self._cursor
        try:
            print('MySQL > Creating user', userName)
            sqlCreateUser = "CREATE USER '%s'@'%s' IDENTIFIED BY '%s';" % (userName, host, password)
            cursor.execute(sqlCreateUser)
        except Exception as Ex:
            try:
                print('Error creating MySQL User: %s' % Ex)
            finally:
                Ex = None
                del Ex

    def delete_mysql_user(self, user, host, password=''):
        """Delete a mysql user"""
        cursor = self._cursor
        query = f"DROP USER '{user}'@'{host}'"
        try:
            cursor.execute(query)
        except Exception as Ex:
            try:
                print('Error Deleting MySQL User: %s' % Ex)
            finally:
                Ex = None
                del Ex

    def show_privileges(self, user, host):
        """Show privileges of mysql user"""
        cursor = self._cursor
        try:
            print('MySQL > Showing privilages of user', user)
            query = f"show grants for '{user}'@'{host}';"
            cursor.execute(query)
            lines = cursor.fetchall()
            for line in lines:
                print(line)

        except Exception as Ex:
            try:
                print('Error showing privileges MySQL User: %s' % Ex)
            finally:
                Ex = None
                del Ex

    def check_privileges(self, database, host, username):
        """Check if a mysql user has privileges on a database"""
        pass

    def grant_all_privileges(self, host, userName, privileges='ALL PRIVILEGES', database='*', table='*', querynum=0, updatenum=0, connection_num=0):
        """Grant a user all privilages"""
        cursor = self._cursor
        try:
            print('MySQL > Granting all PRIVILEGES to user', userName)
            query = f"GRANT {privileges} ON {database}.{table} TO '{userName}'@'{host}'"
            print(query)
            cursor.execute(query)
            self.flush_privileges()
        except Exception as Ex:
            try:
                print('Error creating MySQL User: %s' % Ex)
            finally:
                Ex = None
                del Ex

    def grant_privileges(self, user, host, database, privileges, table='*'):
        """Grant specified privileges for a mysql user"""
        cursor = self._cursor
        try:
            print('MySQL > Granting privilages', privileges, 'for user', user)
            query = f"GRANT {privileges} ON `{database}`.{table} TO '{user}'@'{host}';"
            cursor.execute(query)
            lines = cursor.fetchall()
            for line in lines:
                print(line)

        except Exception as Ex:
            try:
                print('Error granting privileges MySQL User: %s' % Ex)
            finally:
                Ex = None
                del Ex

    def remove_all_privileges(self, user, host, privileges='all privileges'):
        """Revoke/Remove all privileges for a mysql user"""
        cursor = self._cursor
        try:
            print('MySQL > Removing all privilages for user', user)
            query = f"revoke {privileges} on *.* from '{user}'@'{host}';"
            cursor.execute(query)
            lines = cursor.fetchall()
            for line in lines:
                print(line)

        except Exception as Ex:
            try:
                print('Error removing privileges MySQL User: %s' % Ex)
            finally:
                Ex = None
                del Ex

    def remove_privileges(self, user, host, privileges):
        """Remove specified privileges for a mysql user"""
        try:
            print('MySQL > Removing privilages', privileges, 'for user', user)
            query = f"REVOKE {privileges} ON *.* FROM '{user}'@'{host}'"
            cursor.execute(query)
            lines = cursor.fetchall()
            for line in lines:
                print(line)

        except Exception as Ex:
            try:
                print('Error granting privileges MySQL User: %s' % Ex)
            finally:
                Ex = None
                del Ex

    def change_privileges(self, user, host, privileges):
        """Change to specified privileges for a mysql user"""
        self.remove_privileges(user, host)
        self.grant_privileges(user, host, privileges)
        self.flush_privileges()

    def flush_privileges(self):
        """Update database permissions/privilages"""
        cursor = self._cursor
        print('MySQL > Flushing privilages ...')
        cursor.execute('FLUSH PRIVILEGES;')

    def add_db_privilages_for_MySQLUSer(self):
        pass

    def change_db_privilages_for_MySQLUSer(self):
        pass

    def is_db_exist(self, dbname):
        """Check if database exist"""
        databases = self.get_databases()
        if dbname not in databases:
            return False
        return True

    def create_database(self, dbname):
        """Create Database"""
        cursor = self._cursor
        print('MySQL > Creating database ' + dbname + ' ...')
        cursor.execute('CREATE DATABASE ' + dbname)

    def delete_database(self, dbname):
        """Delete Database"""
        cursor = self._cursor
        tables = self.get_tables()
        for table in tables:
            self.delete_table(table, dbname)
        else:
            print('MySQL > Deleting database ' + dbname + ' ...')
            cursor.execute('DROP DATABASE ' + dbname)

    def get_databases(self):
        """Get databases names"""
        cursor = self._cursor
        cursor.execute('SHOW DATABASES ')
        databases = cursor.fetchall()
        databases = [x[0] for x in databases]
        return databases

    def create_table(self, tbname, column_info):
        """Create a table under a database"""
        cursor = self._cursor
        print('MySQL > Creating table ' + tbname + ' ...')
        cursor.execute('CREATE TABLE ' + tbname + ' (id INT(11) NOT NULL AUTO_INCREMENT PRIMARY KEY,' + ''.join([' ' + info + ' ' + column_info[info] + ',' for info in column_info])[:-1] + ')')

    def delete_table(self, table, database=''):
        """Delete a table under a database"""
        cursor = self._cursor
        if database == '':
            database = self._config['database']
        print('MySQL > Deleting table ' + table + ' ...')
        query = f"DROP TABLE {database}.{table}"
        cursor.execute(query)

    def get_tables(self, database=''):
        """Get table names"""
        cursor = self._cursor
        if database == '':
            database = self._config['database']
        cursor.execute(f"SHOW TABLES FROM {database}")
        tables = cursor.fetchall()
        tables = [x[0] for x in tables]
        return tables

    def describe_table--- This code section failed: ---

 L. 351         0  LOAD_FAST                'self'
                2  LOAD_ATTR                _cursor
                4  STORE_FAST               'cursor'

 L. 352         6  LOAD_GLOBAL              print
                8  LOAD_STR                 'MySQL > Describing table '
               10  LOAD_FAST                'tbname'
               12  BINARY_ADD       
               14  LOAD_STR                 ' ...'
               16  BINARY_ADD       
               18  CALL_FUNCTION_1       1  ''
               20  POP_TOP          

 L. 353        22  LOAD_STR                 'DESCRIBE '
               24  LOAD_FAST                'tbname'
               26  FORMAT_VALUE          0  ''
               28  BUILD_STRING_2        2 
               30  STORE_FAST               'query'

 L. 354        32  LOAD_FAST                'cursor'
               34  LOAD_METHOD              execute
               36  LOAD_FAST                'query'
               38  CALL_METHOD_1         1  ''
               40  POP_TOP          

 L. 355        42  LOAD_FAST                'cursor'
               44  LOAD_METHOD              fetchall
               46  CALL_METHOD_0         0  ''
               48  STORE_FAST               'rows'

 L. 358        50  BUILD_LIST_0          0 

 L. 359        52  BUILD_LIST_0          0 

 L. 360        54  BUILD_LIST_0          0 

 L. 361        56  BUILD_LIST_0          0 

 L. 362        58  BUILD_LIST_0          0 

 L. 363        60  BUILD_LIST_0          0 

 L. 357        62  LOAD_CONST               ('Field', 'Type', 'Null', 'Key', 'Default', 'Extra')
               64  BUILD_CONST_KEY_MAP_6     6 
               66  STORE_DEREF              'data'

 L. 366        68  LOAD_FAST                'rows'
               70  GET_ITER         
               72  FOR_ITER             98  'to 98'
               74  STORE_DEREF              'row'

 L. 367        76  LOAD_CLOSURE             'data'
               78  LOAD_CLOSURE             'row'
               80  BUILD_TUPLE_2         2 
               82  LOAD_DICTCOMP            '<code_object <dictcomp>>'
               84  LOAD_STR                 'MySQL.describe_table.<locals>.<dictcomp>'
               86  MAKE_FUNCTION_8          'closure'
               88  LOAD_DEREF               'data'
               90  GET_ITER         
               92  CALL_FUNCTION_1       1  ''
               94  STORE_DEREF              'data'
               96  JUMP_BACK            72  'to 72'

 L. 369        98  LOAD_GLOBAL              pandas
              100  LOAD_METHOD              DataFrame
              102  LOAD_DEREF               'data'
              104  CALL_METHOD_1         1  ''
              106  STORE_FAST               'dbf'

 L. 370       108  LOAD_GLOBAL              print
              110  LOAD_FAST                'dbf'
              112  CALL_FUNCTION_1       1  ''
              114  POP_TOP          

Parse error at or near `LOAD_DICTCOMP' instruction at offset 82

    def is_table_exist(self, tbname):
        """Check if table exist"""
        tables = self.get_tables()
        if tbname in tables:
            return True
        return False

    def get_columns(self, tbname):
        """Get column names of a table"""
        cursor = self._cursor
        cursor.execute('SHOW COLUMNS FROM ' + tbname)
        columns = cursor.fetchall()
        return [column_name for column_name, *_ in columns]

    def update_row(self):
        pass

    def delete_row():
        pass

    def add_column(self, tbname, column_name):
        pass

    def delete_column(self, tbname, column_name):
        pass

    def delete_unique_column(self, tbname, column_name):
        pass

    def change_to_unique_column(self):
        pass

    def change_column(self):
        pass

    def rename_column(self, tbname, old_column_name, new_column_name):
        pass

    def backup_all(self):
        pass

    def backup_table(self):
        pass

    def backup_database(self):
        pass

    def restore_table(self):
        pass

    def restore_databalse(self):
        pass

    def load_CSV_into_table(self):
        pass

    def show_table--- This code section failed: ---

 L. 455         0  LOAD_FAST                'self'
                2  LOAD_ATTR                _cursor
                4  STORE_FAST               'cursor'

 L. 456         6  LOAD_GLOBAL              print
                8  LOAD_STR                 'MySQL > Showing data of table '
               10  LOAD_FAST                'tbname'
               12  BINARY_ADD       
               14  LOAD_STR                 ' ...'
               16  BINARY_ADD       
               18  CALL_FUNCTION_1       1  ''
               20  POP_TOP          

 L. 457        22  LOAD_FAST                'cursor'
               24  LOAD_METHOD              execute
               26  LOAD_STR                 'SELECT * FROM '
               28  LOAD_FAST                'tbname'
               30  BINARY_ADD       
               32  CALL_METHOD_1         1  ''
               34  POP_TOP          

 L. 458        36  LOAD_FAST                'cursor'
               38  LOAD_METHOD              fetchall
               40  CALL_METHOD_0         0  ''
               42  STORE_FAST               'rows'

 L. 460        44  LOAD_DICTCOMP            '<code_object <dictcomp>>'
               46  LOAD_STR                 'MySQL.show_table.<locals>.<dictcomp>'
               48  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
               50  LOAD_FAST                'self'
               52  LOAD_METHOD              get_columns
               54  LOAD_FAST                'tbname'
               56  CALL_METHOD_1         1  ''
               58  GET_ITER         
               60  CALL_FUNCTION_1       1  ''
               62  STORE_DEREF              'data'

 L. 461        64  LOAD_FAST                'rows'
               66  GET_ITER         
               68  FOR_ITER             94  'to 94'
               70  STORE_DEREF              'row'

 L. 462        72  LOAD_CLOSURE             'data'
               74  LOAD_CLOSURE             'row'
               76  BUILD_TUPLE_2         2 
               78  LOAD_DICTCOMP            '<code_object <dictcomp>>'
               80  LOAD_STR                 'MySQL.show_table.<locals>.<dictcomp>'
               82  MAKE_FUNCTION_8          'closure'
               84  LOAD_DEREF               'data'
               86  GET_ITER         
               88  CALL_FUNCTION_1       1  ''
               90  STORE_DEREF              'data'
               92  JUMP_BACK            68  'to 68'

 L. 464        94  LOAD_GLOBAL              pandas
               96  LOAD_METHOD              DataFrame
               98  LOAD_DEREF               'data'
              100  CALL_METHOD_1         1  ''
              102  STORE_FAST               'dbf'

 L. 465       104  LOAD_GLOBAL              print
              106  LOAD_FAST                'dbf'
              108  CALL_FUNCTION_1       1  ''
              110  POP_TOP          

Parse error at or near `LOAD_DICTCOMP' instruction at offset 78

    def get_unique_id_from_field(self, field_name, key_length, filters=[]):
        """Get a random unique id not registered in a specific field"""
        table = self._config['table']
        cursor = self._cursor
        sid = generateCryptographicallySecureRandomString(stringLength=key_length, filters=filters)
        while True:
            query = 'SELECT * FROM ' + table + ' WHERE `' + field_name + "` = '" + sid + "'"
            cursor.execute(query)
            records = cursor.fetchall()
            for record in records:
                print(record)

            if len(records) > 1:
                print('matched with previously stored sid')
                sid = generateCryptographicallySecureRandomString(stringLength=key_length, filters=filters)
            else:
                print('Got unique sid')
                break

        return sid

    def delete_row(self, delete_dict):
        """Delete a row of data"""
        column_name = delete_dict[0]
        value = delete_dict[column_name]
        cursor = self._cursor
        tbname = self._config['table']
        query = f"DELETE FROM {tbname} WHERE `{column_name}`='{value}';"
        cursor.execute(query)

    def insert_row(self, value_tupple):
        """Insert row of data"""
        cursor = self._cursor
        dbname = self._config['database']
        tbname = self._config['table']
        column_info = self.get_columns(tbname)[1:]
        query = 'INSERT INTO ' + tbname + ' (' + ''.join([key + ', ' for key in column_info])[:-2] + ') VALUES (' + ''.join(['%s, ' for key in column_info])[:-2] + ')'
        values = [
         value_tupple]
        cursor.executemany(query, values)
        self.mySQLConnection.commit()
        print(cursor.rowcount, 'record inserted')


def create_configuration(option='cli', file_name='private/config.ini'):
    """Creating Configuration"""
    if option == 'cli':
        print('Getting your configurations to save it.\n')
        print('\nDatabase configurations -')
        dbhost = input('Give your db host : ')
        dbuser = input('Give your db user : ')
        dbpassword = input('Give your db password : ')
        dbname = input('Give your db name : ')
        dbtable = input('Give your db table : ')
        mysql_bin_folder = input('Give your path of mysql bin folder : ')
        configstr = f"; config file\n[DB_INITIALIZE]\nmysql_bin_folder = {mysql_bin_folder}\nhost = localhost\nuser = root\npassword = \n[DB_AUTHENTICATION]\nmysql_bin_folder = {mysql_bin_folder}\nhost = {dbhost}\nuser = {dbuser}\npassword = {dbpassword}\ndatabase = {dbname}\ntable = {dbtable}\n[MYSQL]\nmysql_bin_folder = {mysql_bin_folder}"
        shaonutil.file.write_file(file_name, configstr)
    else:
        if option == 'gui':
            window = Tk()
            window.title('Welcome to DB Config')
            window.geometry('400x400')
            window.configure(background='grey')
            FB_LABEL = Label(window, text='MYSQL Config').grid(row=0, column=0, columnspan=2)
            a = Label(window, text='MYSQL bin folder').grid(row=1, column=0)
            DB_LABEL = Label(window, text='Database Authentication').grid(row=3, column=0, columnspan=2)
            c = Label(window, text='Host').grid(row=4, column=0)
            d = Label(window, text='User').grid(row=5, column=0)
            d = Label(window, text='Password').grid(row=6, column=0)
            d = Label(window, text='Database').grid(row=7, column=0)
            d = Label(window, text='Table').grid(row=8, column=0)
            mysqlbinfolder_ = tk.StringVar(window)
            fbpassword_ = tk.StringVar(window)
            dbhost_ = tk.StringVar(window)
            dbuser_ = tk.StringVar(window)
            dbpassword_ = tk.StringVar(window)
            dbname_ = tk.StringVar(window)
            dbtable_ = tk.StringVar(window)
            Entry(window, textvariable=mysqlbinfolder_).grid(row=1, column=1)
            Entry(window, textvariable=dbhost_).grid(row=4, column=1)
            Entry(window, textvariable=dbuser_).grid(row=5, column=1)
            Entry(window, show='*', textvariable=dbpassword_).grid(row=6, column=1)
            Entry(window, textvariable=dbname_).grid(row=7, column=1)
            Entry(window, textvariable=dbtable_).grid(row=8, column=1)

            def clicked():
                mysql_bin_folder = mysqlbinfolder_.get()
                dbhost = dbhost_.get()
                dbuser = dbuser_.get()
                dbpassword = dbpassword_.get()
                dbname = dbname_.get()
                dbtable = dbtable_.get()
                configstr = f"; config file\n[DB_INITIALIZE]\nmysql_bin_folder = {mysql_bin_folder}\nhost = localhost\nuser = root\npassword = \n[DB_AUTHENTICATION]\nmysql_bin_folder = {mysql_bin_folder}\nhost = {dbhost}\nuser = {dbuser}\npassword = {dbpassword}\ndatabase = {dbname}\ntable = {dbtable}\n[MYSQL]\nmysql_bin_folder = {mysql_bin_folder}"
                shaonutil.file.write_file(file_name, configstr)
                window.destroy()

            btn = ttk.Button(window, text='Submit', command=clicked).grid(row=9, column=0)
            window.mainloop()


def remove_aria_log(mysql_data_dir):
    """Removing aria_log.### files to in mysql data dir to restart mysql"""
    aria_log_files = [file for file in os.listdir(mysql_data_dir) if 'aria_log.' in file]
    for aria_log in aria_log_files:
        aria_log = os.path.join(mysql_data_dir, aria_log)
        os.remove(aria_log)


def get_mysql_datadir(mysql_bin_folder, user, pass_=''):
    """Get mysql data directory"""
    process = subprocess.Popen([os.path.join(mysql_bin_folder, 'mysql'), '--user=' + user, '--password=' + pass_, '-e', 'select @@datadir;'], stdout=(subprocess.PIPE))
    out, err = process.communicate()
    out = [line for line in out.decode('utf8').replace('\r\n', '\n').split('\n') if line != ''][(-1)]
    datadir = out.replace('\\\\', '\\')
    return datadir