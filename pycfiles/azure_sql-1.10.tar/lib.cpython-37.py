# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/shinsheel/Documents/Data-Gathering/Pypi/azure_sql/azure_sql/lib.py
# Compiled at: 2019-09-18 05:00:50
# Size of source mod 2**32: 3852 bytes
import datetime, urllib, pyodbc, pandas as pd
from sqlalchemy import create_engine

def connection_string(username, password, database, server, port=1477, driver='{ODBC Driver 17 for SQL Server}'):
    con_str = 'DRIVER={driver};SERVER={server};PORT={port};DATABASE={database};UID={username};PWD={password}'
    con_str = con_str.format(username=username, password=password, database=database, server=server,
      port=port,
      driver=driver)
    return con_str


def read_sql_to_df(query='', username='', password='', database='', server='', driver='{ODBC Driver 17 for SQL Server}'):
    connection_string = connection_string(username, password, database, server)
    params = urllib.parse.quote_plus(connection_string)
    engine = create_engine(('mssql+pyodbc:///?odbc_connect=%s' % params), fast_executemany=True)
    temp_df = pd.read_sql(query, engine)
    return temp_df


sql_df = read_sql_to_df

def write_df_to_sql(df, table='', username='', password='', database='', server='', if_exists='append', chunksize=10000, driver='{ODBC Driver 17 for SQL Server}', update_date=True):
    if update_date:
        df.insert(0, 'update_date', datetime.date.today())
    connection_string = connection_string(username, password, database, server)
    params = urllib.parse.quote_plus(connection_string)
    engine = create_engine(('mssql+pyodbc:///?odbc_connect=%s' % params), fast_executemany=True)
    df.to_sql(table, con=engine, if_exists=if_exists, index=False, chunksize=chunksize)


df_sql = write_df_to_sql

def query_sql_without_return(query='', username='', password='', database='', server='', driver='{ODBC Driver 17 for SQL Server}'):
    connection_string = connection_string(username, password, database, server)
    params = urllib.parse.quote_plus(connection_string)
    engine = create_engine(('mssql+pyodbc:///?odbc_connect=%s' % params), fast_executemany=True)
    connection = engine.connect()
    connection.execute(query)
    connection.close()


query = query_sql_without_return

def connect(username, password, database, server, port=1477, driver='{ODBC Driver 17 for SQL Server}'):
    con_str = connection_string(username, password, database, server, port, driver)
    cnxn = pyodbc.connect(con_str)
    c = cnxn.cursor()
    return (cnxn, c)


def insert(cursor, table, object, replace=None, commit=None):
    c = cursor
    if replace:
        c.execute('delete from {} where {} = ?'.format(table, replace), object[replace])
    sql = 'insert into {} ({})VALUES({})'.format(table, ','.join(list(object.keys())), ','.join(['?'] * len(object)))
    print(sql)
    (c.execute)(sql, *list(object.values()))
    if commit:
        commit.commit()
    return c


if __name__ == '__main__':
    creds = [
     'vlad@#####sqlserver', '#####', '#####_team', '#####sqlserver.database.windows.net']
    table = '#####_item_attrs_temp'
    sql = 'select TOP(10) * from {}'.format(table)
    print(sql_df(sql, *creds))
    df = pd.DataFrame([{'Artykul': '101-404-451'}])
    print(df_sql(df, table, *creds))
    query('delete from {}'.format(table), *creds)
    cnxn, c = connect(*creds)
    insert(c, table, {'Artykul':'101-404-451',  'Brand':'Huawei'})
    insert(c, table, {'Artykul':'101-404-451',  'Brand':'Apple'}, commit=cnxn, replace='Artykul')