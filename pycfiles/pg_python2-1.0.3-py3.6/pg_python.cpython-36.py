# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pg_python2/pg_python.py
# Compiled at: 2018-08-03 06:01:13
# Size of source mod 2**32: 11506 bytes
from ._db_object import Db
from ._write import make_postgres_write_statement, make_postgres_write_multiple_statement
from ._read import make_postgres_read_statement, prepare_values
from ._update import make_postgres_update_statement
from ._update import make_postgres_update_multiple_statement
from ._delete import make_postgres_delete_statement
import logging
db_dict = {}

def get_db(server='default'):
    db_obj = db_dict.get(server, None)
    return db_obj


print_debug_log = True

def pg_server(db_name, username, password, host_address, debug=True, server='default'):
    global print_debug_log
    params_map = {'dbname':db_name, 
     'user':username, 
     'password':password, 
     'host':host_address}
    db_obj = Db(params_map)
    db_dict[server] = db_obj
    print_debug_log = debug
    return db_obj


def write(table, kv_map, server='default'):
    """
    :param table: String.
    :param kv_map: Key values.
    :param server: Alias of the server
    :return success_bool:
    """
    db_obj = get_db(server)
    connection = db_obj.get_connection()
    cursor = db_obj.get_cursor()
    command, values = make_postgres_write_statement(table, kv_map, print_debug_log)
    try:
        cursor.execute(command, values)
        connection.commit()
    except Exception as e:
        logging.info('Db Cursor Write Error: %s' % e)
        db_obj_reconnect = Db(db_obj.params)
        db_dict.pop(server)
        db_dict[server] = db_obj_reconnect
        return False

    return True


def read(table, keys_to_get, kv_map, limit=None, order_by=None, order_type=None, clause='=', group_by=None, join_clause=' AND ', server='default'):
    """
    :param table: String
    :param keys_to_get: list of strings
    :param kv_map: key value map, if this is None, then limit is maxed at 1000
    :param limit: None or integer
    :param order_by: None or must be of a type String
    :param order_type: String None, "ASC" or "DESC" only
    :return: values in an array of key value maps
    """
    error_return = None
    db_obj = get_db(server)
    cursor = db_obj.get_cursor()
    command, values = make_postgres_read_statement(table, kv_map, keys_to_get, limit, order_by, order_type, print_debug_log, clause, group_by, join_clause)
    try:
        cursor.execute(command, values)
        all_values = cursor.fetchall()
        return prepare_values(all_values, keys_to_get)
    except Exception as e:
        logging.warning('Db Cursor Read Error: %s' % e)
        return []


def update(table, update_kv_map, where_kv_map, clause='=', server='default'):
    """
    :param table: table name, type string
    :param update_kv_map: the NEW keyvalue map for values to be updated
    :param where_kv_map: the kv map to search for values, all values ARE ANDed.
    :return: Success or Failure.
    """
    db_obj = get_db(server)
    connection = db_obj.get_connection()
    cursor = db_obj.get_cursor()
    command, values = make_postgres_update_statement(table, update_kv_map, where_kv_map, clause, print_debug_log)
    try:
        cursor.execute(command, values)
        connection.commit()
    except Exception as e:
        logging.warning('Db Cursor Update Error: %s' % e)
        db_obj_reconnect = Db(db_obj.params)
        db_dict.pop(server)
        db_dict[server] = db_obj_reconnect
        return False

    return True


def read_raw(command, values, server='default'):
    """
    :param table: String
    :param keys_to_get: list of strings
    :param kv_map: key value map, if this is None, then limit is maxed at 1000
    :param limit: None or integer
    :param order_by: None or must be of a type String
    :param order_type: String None, "ASC" or "DESC" only
    :return: values in an array of key value maps
    """
    db_obj = get_db(server)
    cursor = db_obj.get_cursor()
    try:
        if values not in [None, [], {}]:
            cursor.execute(command, values)
        else:
            cursor.execute(command)
        all_values = cursor.fetchall()
        return all_values
    except Exception as e:
        logging.warning('Db Cursor Read Error: %s' % e)
        return []


def write_raw(command, values, server='default'):
    """
    :params command, values. Execution commands dirctly for postgres
    """
    db_obj = get_db(server)
    connection = db_obj.get_connection()
    cursor = db_obj.get_cursor()
    try:
        cursor.execute(command, values)
        connection.commit()
    except Exception as e:
        logging.warning('Db Cursor Write Error: %s' % e)
        db_obj_reconnect = Db(db_obj.params)
        db_dict.pop(server)
        db_dict[server] = db_obj_reconnect
        return False

    return True


def update_raw(command, server='default'):
    """
    Update statement in the raw format,
    :param command: SQL command
    :return: number of rows affected
    """
    db_obj = get_db(server)
    connection = db_obj.get_connection()
    cursor = db_obj.get_cursor()
    try:
        cursor.execute(command)
        rowcount = cursor.rowcount
        connection.commit()
    except Exception as e:
        logging.warning('Db Cursor Update Error: %s' % e)
        db_obj_reconnect = Db(db_obj.params)
        db_dict.pop(server)
        db_dict[server] = db_obj_reconnect
        return -1

    return rowcount


class bcolors:
    HEADER = '\x1b[95m'
    OKBLUE = '\x1b[94m'
    OKGREEN = '\x1b[92m'
    WARNING = '\x1b[93m'
    FAIL = '\x1b[91m'
    ENDC = '\x1b[0m'
    BOLD = '\x1b[1m'
    UNDERLINE = '\x1b[4m'


def print_ok(s):
    print(bcolors.OKGREEN + s + bcolors.ENDC)


def print_warn(s):
    print(bcolors.WARNING + s + bcolors.ENDC)


def print_fail(s):
    print(bcolors.FAIL + s + bcolors.ENDC)


def close(server='default'):
    logging.info('Closing connection for server %s' % server)
    db_obj = get_db(server)
    connection = db_obj.get_connection()
    cursor = db_obj.get_cursor()
    db_obj.close_cursor(cursor)
    db_obj.close_connection()


def close_all():
    for server in db_dict.keys():
        close(server)


def delete(table, where_kv_map, server='default'):
    """
    Delete the rows resulting from the mentined kv map. No limit.
    :param table: table name, must be string
    :param where_kv_map: the kv map to search for values, all values ARE ANDed.
    :return: True or False
    """
    db_obj = get_db(server)
    connection = db_obj.get_connection()
    cursor = db_obj.get_cursor()
    command, values = make_postgres_delete_statement(table, where_kv_map, print_debug_log)
    try:
        cursor.execute(command, values)
        connection.commit()
    except Exception as e:
        logging.warning('Db Cursor Delete Error: %s' % e)
        db_obj_reconnect = Db(db_obj.params)
        db_dict.pop(server)
        db_dict[server] = db_obj_reconnect
        return False

    return True


def check_parameters(column_to_update, columns_to_query_lst, query_values_dict_lst):
    """
    check_prarameters checks whether the passed parameters are valid or not.
    :param column_to_update: name of column that is to be updated.
    :param columns_to_query_lst: list of column names that is used in where clause.
    :param query_values_dict_lst: list of dictionaries containing values for where clause and target column.
    :return: boolean
    """
    expected_length = 1 + len(columns_to_query_lst)
    all_columns_name = ['update'] + columns_to_query_lst
    flag = 0
    for dict_val in query_values_dict_lst:
        if len(dict_val) != expected_length:
            logging.error("%s doesn't match the dimensions" % dict_val)
            return False
        for column in all_columns_name:
            if column not in dict_val:
                logging.error("%s column isn't present in dictionary" % column)
                return False

    return True


def update_multiple(table, column_to_update, columns_to_query_lst, query_values_dict_lst, server='default'):
    """
    Multiple update support in pg_python
    :param table: table to update into
    :param column_to_update: Single column for set clause
    :param columns_to_query_lst: column names for where clause
    :param query_values_dict_lst: values for where and Set.
    :return:
    """
    db_obj = get_db(server)
    connection = db_obj.get_connection()
    cursor = db_obj.get_cursor()
    is_parameters_correct = check_parameters(column_to_update, columns_to_query_lst, query_values_dict_lst)
    if not is_parameters_correct:
        logging.error('ERROR in parameters passsed')
        return
    else:
        command, values = make_postgres_update_multiple_statement(table, column_to_update, columns_to_query_lst, query_values_dict_lst, print_debug_log)
        try:
            cursor.execute(command, values)
            connection.commit()
        except Exception as e:
            logging.warning('Db Cursor update_multiple Error: %s' % e)
            db_obj_reconnect = Db(db_obj.params)
            db_dict.pop(server)
            db_dict[server] = db_obj_reconnect
            return False

        return True


def check_multiple_insert_param(columns_to_insert, insert_values_dict_lst):
    """
    Checks if the pararmeter passed are of correct order.
    :param columns_to_insert:
    :param insert_values_dict_lst:
    :return:
    """
    column_len = len(columns_to_insert)
    for row in insert_values_dict_lst:
        if column_len != len(row):
            logging.error("%s doesn't match the dimensions" % row)
            return False
        for column in columns_to_insert:
            if column not in row:
                logging.error("%s column isn't present in dictionary" % column)
                return False

    return True


def insert_multiple(table, columns_to_insert_lst, insert_values_dict_lst, server='default'):
    """
    Multiple row insert in pg_python
    :param table: table to insert into.
    :param columns_to_insert_lst: columns value provided.
    :param insert_values_dict_lst: values of corresponding columns.
    :return:
    """
    db_obj = get_db(server)
    connection = db_obj.get_connection()
    cursor = db_obj.get_cursor()
    is_pararmeters_correct = check_multiple_insert_param(columns_to_insert_lst, insert_values_dict_lst)
    if not is_pararmeters_correct:
        logging.error('ERROR in parameters passsed')
        return
    else:
        command, values = make_postgres_write_multiple_statement(table, columns_to_insert_lst, insert_values_dict_lst, print_debug_log)
        try:
            cursor.execute(command, values)
            connection.commit()
        except Exception as e:
            logging.error('Db Cursor Write Error: %s' % e)
            db_obj_reconnect = Db(db_obj.params)
            db_dict.pop(server)
            db_dict[server] = db_obj_reconnect
            return False

        return True