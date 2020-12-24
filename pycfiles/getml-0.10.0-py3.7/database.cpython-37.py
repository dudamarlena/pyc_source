# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/getml/database.py
# Compiled at: 2020-03-16 07:21:38
# Size of source mod 2**32: 31738 bytes
"""This module provides communication routines to access various databases.

The :func:`~getml.database.connect_greenplum`,
:func:`~getml.database.connect_mariadb`,
:func:`~getml.database.connect_mysql`,
:func:`~getml.database.connect_postgres`, and
:func:`~getml.database.connect_sqlite3` functions do establish a
connection between a database and the getML engine. During the data
import using either the :meth:`~getml.data.DataFrame.read_db` or
:meth:`~getml.data.DataFrame.read_query` methods of a
:class:`~getml.data.DataFrame` instance or the corresponding
:func:`~getml.data.DataFrame.from_db` class method all data will be
directly loaded from the database into the engine without ever passing
the Python interpreter.

In addition, several auxiliary functions that might be handy during
the analysis and interaction with the database are provided.

Note:

    There can only be one connection to a database be established at
    once. In every subsequent connection the previous one will be
    lost.

"""
import json, os, pandas as pd
import getml.communication as comm

def connect_greenplum(dbname, user, password, host, hostaddr, port=5432, time_formats=[
 '%Y-%m-%dT%H:%M:%s%z', '%Y-%m-%d %H:%M:%S', '%Y-%m-%d']):
    """Creates a new Greenplum database connection.

    But first, make sure your database is running and you can reach it
    from via your command line.

    Args:
        dbname (str): The name of the database to which you want to connect.
        user (str): User name with which to log into the Greenplum database.
        password (str): Password with which to log into the Greenplum database.
        host (str): Host of the Greenplum database.
        hostaddr (str): IP address of the Greenplum database.
        port(int, optional): Port of the Greenplum database.

            The default port used by Greenplum is 5432.

            If you do not know, which port to use, type the following into your
            Greenplum client:

            .. code-block:: sql

                SELECT setting FROM pg_settings WHERE name = 'port';

        time_formats (List[str], optional):

            The list of formats tried when parsing time stamps.

            The formats are allowed to contain the following
            special characters:

            * %w - abbreviated weekday (Mon, Tue, ...)
            * %W - full weekday (Monday, Tuesday, ...)
            * %b - abbreviated month (Jan, Feb, ...)
            * %B - full month (January, February, ...)
            * %d - zero-padded day of month (01 .. 31)
            * %e - day of month (1 .. 31)
            * %f - space-padded day of month ( 1 .. 31)
            * %m - zero-padded month (01 .. 12)
            * %n - month (1 .. 12)
            * %o - space-padded month ( 1 .. 12)
            * %y - year without century (70)
            * %Y - year with century (1970)
            * %H - hour (00 .. 23)
            * %h - hour (00 .. 12)
            * %a - am/pm
            * %A - AM/PM
            * %M - minute (00 .. 59)
            * %S - second (00 .. 59)
            * %s - seconds and microseconds (equivalent to %S.%F)
            * %i - millisecond (000 .. 999)
            * %c - centisecond (0 .. 9)
            * %F - fractional seconds/microseconds (000000 - 999999)
            * %z - time zone differential in ISO 8601 format (Z or +NN.NN)
            * %Z - time zone differential in RFC format (GMT or +NNNN)
            * %% - percent sign

    Note:

        Please note that this feature is **not supported on
        Windows**.

        By selecting an existing table of your database in
        :func:`~getml.data.DataFrame.from_db` function, you can create
        a new :class:`~getml.data.DataFrame` containing all its data.
        Alternatively you can use the
        :meth:`~.getml.data.DataFrame.read_db` and
        :meth:`~.getml.data.DataFrame.read_query` methods to replace
        the content of the current :class:`~getml.data.DataFrame`
        instance or append further rows based on either a table or a
        specific query.

        You can also write your results back into the Greenplum
        database. By providing the name for the destination table in
        :meth:`getml.models.MultirelModel.transform`, the features
        generated from your raw data will be written back. Passing
        them into :meth:`getml.models.MultirelModel.predict`, instead,
        makes predictions of the target variables to new, unseen data
        and stores the result into the corresponding table.

    """
    cmd = dict()
    cmd['name_'] = ''
    cmd['type_'] = 'Database.new'
    cmd['db_'] = 'greenplum'
    cmd['host_'] = host
    cmd['hostaddr_'] = hostaddr
    cmd['port_'] = port
    cmd['dbname_'] = dbname
    cmd['user_'] = user
    cmd['time_formats_'] = time_formats
    s = comm.send_and_receive_socket(cmd)
    comm.send_string(s, password)
    msg = comm.recv_string(s)
    if msg != 'Success!':
        comm.engine_exception_handler(msg)


def connect_mariadb(dbname, user, password, host, port=3306, unix_socket='/var/run/mysqld/mysqld.sock', time_formats=[
 '%Y-%m-%dT%H:%M:%s%z', '%Y-%m-%d %H:%M:%S', '%Y-%m-%d']):
    """
    Creates a new MariaDB database connection.

    But first, make sure your database is running and you can reach it
    from via your command line.

    Args:
        dbname (str): The name of the database to which you want to connect.
        user (str): User name with which to log into the MariaDB database.
        password (str): Password with which to log into the MariaDB database.
        host (str): Host of the MariaDB database.
        port (int, optional): Port of the MariaDB database.

            The default port for MariaDB is 3306. 

            If you do not know which port to use, type 

            .. code-block:: sql

                SELECT @@port;

            into your MariaDB client.
        unix_socket (str, optional): The UNIX socket used to connect to the MariaDB database.
           
            If you do not know which UNIX socket to use, type 

            .. code-block:: sql

                SELECT @@socket;

            into your MariaDB client.
        time_formats (List[str], optional):

            The list of formats tried when parsing time stamps.

            The formats are allowed to contain the following
            special characters:

            * %w - abbreviated weekday (Mon, Tue, ...)
            * %W - full weekday (Monday, Tuesday, ...)
            * %b - abbreviated month (Jan, Feb, ...)
            * %B - full month (January, February, ...)
            * %d - zero-padded day of month (01 .. 31)
            * %e - day of month (1 .. 31)
            * %f - space-padded day of month ( 1 .. 31)
            * %m - zero-padded month (01 .. 12)
            * %n - month (1 .. 12)
            * %o - space-padded month ( 1 .. 12)
            * %y - year without century (70)
            * %Y - year with century (1970)
            * %H - hour (00 .. 23)
            * %h - hour (00 .. 12)
            * %a - am/pm
            * %A - AM/PM
            * %M - minute (00 .. 59)
            * %S - second (00 .. 59)
            * %s - seconds and microseconds (equivalent to %S.%F)
            * %i - millisecond (000 .. 999)
            * %c - centisecond (0 .. 9)
            * %F - fractional seconds/microseconds (000000 - 999999)
            * %z - time zone differential in ISO 8601 format (Z or +NN.NN)
            * %Z - time zone differential in RFC format (GMT or +NNNN)
            * %% - percent sign

    Note:

        By selecting an existing table of your database in
        :func:`~getml.data.DataFrame.from_db` function, you can create
        a new :class:`~getml.data.DataFrame` containing all its data.
        Alternatively you can use the
        :meth:`~.getml.data.DataFrame.read_db` and
        :meth:`~.getml.data.DataFrame.read_query` methods to replace
        the content of the current :class:`~getml.data.DataFrame`
        instance or append further rows based on either a table or a
        specific query.

        You can also write your results back into the MariaDB
        database. By providing the name for the destination table in
        :meth:`getml.models.MultirelModel.transform`, the features
        generated from your raw data will be written back. Passing
        them into :meth:`getml.models.MultirelModel.predict`, instead,
        makes predictions
        of the target variables to new, unseen data and stores the result into
        the corresponding table.

    """
    cmd = dict()
    cmd['name_'] = ''
    cmd['type_'] = 'Database.new'
    cmd['db_'] = 'mariadb'
    cmd['host_'] = host
    cmd['port_'] = port
    cmd['dbname_'] = dbname
    cmd['user_'] = user
    cmd['unix_socket_'] = unix_socket
    cmd['time_formats_'] = time_formats
    s = comm.send_and_receive_socket(cmd)
    comm.send_string(s, password)
    msg = comm.recv_string(s)
    if msg != 'Success!':
        comm.engine_exception_handler(msg)


def connect_mysql(dbname, user, password, host, port=3306, unix_socket='/var/run/mysqld/mysqld.sock', time_formats=[
 '%Y-%m-%dT%H:%M:%s%z', '%Y-%m-%d %H:%M:%S', '%Y-%m-%d']):
    """
    Creates a new MySQL database connection.

    But first, make sure your database is running and you can reach it
    from via your command line.

    Args:
        dbname (str): The name of the database to which you want to connect.
        user (str): User name with which to log into the MySQL database.
        password (str): Password with which to log into the MySQL database.
        host (str): Host of the MySQL database.
        port (int, optional): Port of the MySQL database.

            The default port for MySQL is 3306. 

            If you do not know which port to use, type 

            .. code-block:: sql

                SELECT @@port;

            into your mysql client.
        unix_socket (str, optional): The UNIX socket used to connect to the MySQL database.

            If you do not know which UNIX socket to use, type 

            .. code-block:: sql

                SELECT @@socket;

            into your mysql client.
        time_formats (List[str], optional):

            The list of formats tried when parsing time stamps.

            The formats are allowed to contain the following
            special characters:

            * %w - abbreviated weekday (Mon, Tue, ...)
            * %W - full weekday (Monday, Tuesday, ...)
            * %b - abbreviated month (Jan, Feb, ...)
            * %B - full month (January, February, ...)
            * %d - zero-padded day of month (01 .. 31)
            * %e - day of month (1 .. 31)
            * %f - space-padded day of month ( 1 .. 31)
            * %m - zero-padded month (01 .. 12)
            * %n - month (1 .. 12)
            * %o - space-padded month ( 1 .. 12)
            * %y - year without century (70)
            * %Y - year with century (1970)
            * %H - hour (00 .. 23)
            * %h - hour (00 .. 12)
            * %a - am/pm
            * %A - AM/PM
            * %M - minute (00 .. 59)
            * %S - second (00 .. 59)
            * %s - seconds and microseconds (equivalent to %S.%F)
            * %i - millisecond (000 .. 999)
            * %c - centisecond (0 .. 9)
            * %F - fractional seconds/microseconds (000000 - 999999)
            * %z - time zone differential in ISO 8601 format (Z or +NN.NN)
            * %Z - time zone differential in RFC format (GMT or +NNNN)
            * %% - percent sign

    Note:
    
        By selecting an existing table of your database in
        :func:`~getml.data.DataFrame.from_db` function, you can create
        a new :class:`~getml.data.DataFrame` containing all its data.
        Alternatively you can use the
        :meth:`~.getml.data.DataFrame.read_db` and
        :meth:`~.getml.data.DataFrame.read_query` methods to replace
        the content of the current :class:`~getml.data.DataFrame`
        instance or append further rows based on either a table or a
        specific query.

        You can also write your results back into the MySQL
        database. By providing the name for the destination table in
        :meth:`getml.models.MultirelModel.transform`, the features
        generated from your raw data will be written back. Passing
        them into :meth:`getml.models.MultirelModel.predict`, instead,
        makes predictions of the target variables to new, unseen data
        and stores the result into the corresponding table.

    """
    cmd = dict()
    cmd['name_'] = ''
    cmd['type_'] = 'Database.new'
    cmd['db_'] = 'mysql'
    cmd['host_'] = host
    cmd['port_'] = port
    cmd['dbname_'] = dbname
    cmd['user_'] = user
    cmd['unix_socket_'] = unix_socket
    cmd['time_formats_'] = time_formats
    s = comm.send_and_receive_socket(cmd)
    comm.send_string(s, password)
    msg = comm.recv_string(s)
    if msg != 'Success!':
        comm.engine_exception_handler(msg)


def connect_postgres(dbname, user, password, host, hostaddr, port=5432, time_formats=[
 '%Y-%m-%dT%H:%M:%s%z', '%Y-%m-%d %H:%M:%S', '%Y-%m-%d']):
    """
    Creates a new PostgreSQL database connection.

    But first, make sure your database is running and you can reach it
    from via your command line.

    Args:
        dbname (str): The name of the database to which you want to connect.
        user (str): User name with which to log into the PostgreSQL database.
        password (str): Password with which to log into the PostgreSQL database.
        host (str): Host of the PostgreSQL database.
        hostaddr (str): IP address of the PostgreSQL database.
        port(int, optional): Port of the PostgreSQL database.

            The default port used by PostgreSQL is 5432. 

            If you do not know, which port to use, type the following into your
            PostgreSQL client

            .. code-block:: sql

                SELECT setting FROM pg_settings WHERE name = 'port';

        time_formats (List[str], optional):

            The list of formats tried when parsing time stamps.

            The formats are allowed to contain the following
            special characters:

            * %w - abbreviated weekday (Mon, Tue, ...)
            * %W - full weekday (Monday, Tuesday, ...)
            * %b - abbreviated month (Jan, Feb, ...)
            * %B - full month (January, February, ...)
            * %d - zero-padded day of month (01 .. 31)
            * %e - day of month (1 .. 31)
            * %f - space-padded day of month ( 1 .. 31)
            * %m - zero-padded month (01 .. 12)
            * %n - month (1 .. 12)
            * %o - space-padded month ( 1 .. 12)
            * %y - year without century (70)
            * %Y - year with century (1970)
            * %H - hour (00 .. 23)
            * %h - hour (00 .. 12)
            * %a - am/pm
            * %A - AM/PM
            * %M - minute (00 .. 59)
            * %S - second (00 .. 59)
            * %s - seconds and microseconds (equivalent to %S.%F)
            * %i - millisecond (000 .. 999)
            * %c - centisecond (0 .. 9)
            * %F - fractional seconds/microseconds (000000 - 999999)
            * %z - time zone differential in ISO 8601 format (Z or +NN.NN)
            * %Z - time zone differential in RFC format (GMT or +NNNN)
            * %% - percent sign

    Note: 

        Please note that this feature is **not supported on
        Windows**.

        By selecting an existing table of your database in
        :func:`~getml.data.DataFrame.from_db` function, you can create
        a new :class:`~getml.data.DataFrame` containing all its data.
        Alternatively you can use the
        :meth:`~.getml.data.DataFrame.read_db` and
        :meth:`~.getml.data.DataFrame.read_query` methods to replace
        the content of the current :class:`~getml.data.DataFrame`
        instance or append further rows based on either a table or a
        specific query.

        You can also write your results back into the PostgreSQL
        database. By providing the name for the destination table in
        :meth:`getml.models.MultirelModel.transform`, the features
        generated from your raw data will be written back. Passing
        them into :meth:`getml.models.MultirelModel.predict`, instead,
        makes predictions of the target variables to new, unseen data
        and stores the result into the corresponding table.
    """
    cmd = dict()
    cmd['name_'] = ''
    cmd['type_'] = 'Database.new'
    cmd['db_'] = 'postgres'
    cmd['host_'] = host
    cmd['hostaddr_'] = hostaddr
    cmd['port_'] = port
    cmd['dbname_'] = dbname
    cmd['user_'] = user
    cmd['time_formats_'] = time_formats
    s = comm.send_and_receive_socket(cmd)
    comm.send_string(s, password)
    msg = comm.recv_string(s)
    if msg != 'Success!':
        comm.engine_exception_handler(msg)


def connect_sqlite3(name=':memory:', time_formats=[
 '%Y-%m-%dT%H:%M:%s%z', '%Y-%m-%d %H:%M:%S', '%Y-%m-%d']):
    """Creates a new SQLite3 database connection.

    SQLite3 is a popular in-memory database. It is faster than
    distributed ones, like PostgreSQL, but less stable under massive
    parallel access, consumes more memory and requires all contained
    data sets to be loaded into memory, which might fill up too much
    of your RAM, especially for large data set.

    Args:
        name (str, optional): Name of the sqlite3 file.  If the file does not exist, it
            will be created. Set to ":memory:" for a purely in-memory SQLite3
            database.
        time_formats (List[str], optional):

            The list of formats tried when parsing time stamps.

            The formats are allowed to contain the following
            special characters:

            * %w - abbreviated weekday (Mon, Tue, ...)
            * %W - full weekday (Monday, Tuesday, ...)
            * %b - abbreviated month (Jan, Feb, ...)
            * %B - full month (January, February, ...)
            * %d - zero-padded day of month (01 .. 31)
            * %e - day of month (1 .. 31)
            * %f - space-padded day of month ( 1 .. 31)
            * %m - zero-padded month (01 .. 12)
            * %n - month (1 .. 12)
            * %o - space-padded month ( 1 .. 12)
            * %y - year without century (70)
            * %Y - year with century (1970)
            * %H - hour (00 .. 23)
            * %h - hour (00 .. 12)
            * %a - am/pm
            * %A - AM/PM
            * %M - minute (00 .. 59)
            * %S - second (00 .. 59)
            * %s - seconds and microseconds (equivalent to %S.%F)
            * %i - millisecond (000 .. 999)
            * %c - centisecond (0 .. 9)
            * %F - fractional seconds/microseconds (000000 - 999999)
            * %z - time zone differential in ISO 8601 format (Z or +NN.NN)
            * %Z - time zone differential in RFC format (GMT or +NNNN)
            * %% - percent sign

    Note:

        By selecting an existing table of your database in
        :func:`~getml.data.DataFrame.from_db` function, you can create
        a new :class:`~getml.data.DataFrame` containing all its data.
        Alternatively you can use the
        :meth:`~.getml.data.DataFrame.read_db` and
        :meth:`~.getml.data.DataFrame.read_query` methods to replace
        the content of the current :class:`~getml.data.DataFrame`
        instance or append further rows based on either a table or a
        specific query.

        You can also write your results back into the SQLite3
        database. By providing the name for the destination table in
        :meth:`getml.models.MultirelModel.transform`, the features
        generated from your raw data will be written back. Passing
        them into :meth:`getml.models.MultirelModel.predict`, instead,
        makes predictions of the target variables to new, unseen data
        and stores the result into the corresponding table.

    """
    cmd = dict()
    cmd['name_'] = os.path.abspath(name)
    cmd['type_'] = 'Database.new'
    cmd['db_'] = 'sqlite3'
    cmd['time_formats_'] = time_formats
    s = comm.send_and_receive_socket(cmd)
    comm.send_string(s, 'none')
    msg = comm.recv_string(s)
    if msg != 'Success!':
        comm.engine_exception_handler(msg)


def drop_table(name):
    """
    Drops a table from the database.

    Args:
        name (str): The table to be dropped.
    """
    cmd = dict()
    cmd['name_'] = name
    cmd['type_'] = 'Database.drop_table'
    comm.send(cmd)


def get(query):
    """
    Executes an SQL query on the database and returns the result as 
    a pandas dataframe.

    Args:
        query (str): The SQL query to be executed.
    """
    cmd = dict()
    cmd['name_'] = ''
    cmd['type_'] = 'Database.get'
    s = comm.send_and_receive_socket(cmd)
    comm.send_string(s, query)
    msg = comm.recv_string(s)
    if msg != 'Success!':
        comm.engine_exception_handler(msg)
    json_str = comm.recv_string(s)
    s.close()
    return pd.read_json(json_str)


def execute(query):
    """
    Executes an SQL query on the database.
    Please note that this is not meant to return results. If you want to 
    get results, use database.get(...) instead.

    Args:
        query (str): The SQL query to be executed.
    """
    cmd = dict()
    cmd['name_'] = ''
    cmd['type_'] = 'Database.execute'
    s = comm.send_and_receive_socket(cmd)
    comm.send_string(s, query)
    msg = comm.recv_string(s)
    s.close()
    if msg != 'Success!':
        comm.engine_exception_handler(msg)


def get_colnames(name):
    """
    Lists the colnames of a table held in the database.

    Args:
        name (str): The name of the database.
    """
    cmd = dict()
    cmd['name_'] = name
    cmd['type_'] = 'Database.get_colnames'
    s = comm.send_and_receive_socket(cmd)
    msg = comm.recv_string(s)
    if msg != 'Success!':
        s.close()
        comm.engine_exception_handler(msg)
    arr = json.loads(comm.recv_string(s))
    s.close()
    return arr


def list_tables():
    """
    Lists all tables and views currently held in the database.
    """
    cmd = dict()
    cmd['name_'] = ''
    cmd['type_'] = 'Database.list_tables'
    s = comm.send_and_receive_socket(cmd)
    msg = comm.recv_string(s)
    if msg != 'Success!':
        s.close()
        comm.engine_exception_handler(msg)
    arr = json.loads(comm.recv_string(s))
    s.close()
    return arr


def read_csv(name, fnames, header=True, quotechar='"', sep=',', skip=0):
    """
    Reads a CSV file into the database.

    Args:
        name (str): Name of the table in which the data is to be inserted.
        fnames (List[str]): The list of CSV file names to be read.
        header (bool, optional): Whether the CSV file contains a header with the column names. Default to True.
        quotechar (str, optional): The character used to wrap strings. Default:`"`
        sep (str, optional): The separator used for separating fields. Default:`,`
        skip (int, optional): Number of lines to skip at the beginning of each
            file (Default: 0). If *header* is True, the lines will be skipped
            before the header.
    """
    fnames_ = [os.path.abspath(_) for _ in fnames]
    cmd = dict()
    cmd['name_'] = name
    cmd['type_'] = 'Database.read_csv'
    cmd['fnames_'] = fnames_
    cmd['header_'] = header
    cmd['quotechar_'] = quotechar
    cmd['sep_'] = sep
    cmd['skip_'] = skip
    comm.send(cmd)


def sniff_csv(name, fnames, header=True, num_lines_sniffed=1000, quotechar='"', sep=',', skip=0):
    """
    Sniffs a list of CSV files.

    Args:
        name (str): Name of the table in which the data is to be inserted.
        fnames (List[str]): The list of CSV file names to be read.
        header (bool, optional): Whether the CSV file contains a header with the column names. Default to True.
        quotechar (str, optional): The character used to wrap strings. Default:`"`
        sep (str, optional): The separator used for separating fields. Default:`,`
        skip (int, optional): Number of lines to skip at the beginning of each
            file (Default: 0). If *header* is True, the lines will be skipped
            before the header.

    Returns:
        str: Appropriate `CREATE TABLE` statement.
    """
    fnames_ = [os.path.abspath(_) for _ in fnames]
    cmd = dict()
    cmd['name_'] = name
    cmd['type_'] = 'Database.sniff_csv'
    cmd['fnames_'] = fnames_
    cmd['header_'] = header
    cmd['num_lines_sniffed_'] = num_lines_sniffed
    cmd['quotechar_'] = quotechar
    cmd['sep_'] = sep
    cmd['skip_'] = skip
    s = comm.send_and_receive_socket(cmd)
    msg = comm.recv_string(s)
    if msg != 'Success!':
        s.close()
        comm.engine_exception_handler(msg)
    query = comm.recv_string(s)
    s.close()
    return query