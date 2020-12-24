# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /mnt/develop/NodeDefender/NodeDefender/manage/setup/database.py
# Compiled at: 2018-03-09 03:40:48
# Size of source mod 2**32: 2533 bytes
from NodeDefender.manage.setup import manager, print_message, print_topic, print_info
from flask_script import prompt
import NodeDefender

@manager.command
def database():
    print_topic('Database')
    print_info('Database is used to store presistant data.')
    print_info('By having it disabled the data will be store in run-time RAM for the               session')
    enabled = None
    while enabled is None:
        enabled = prompt('Enable Database(Y/N)').upper()
        if 'Y' in enabled:
            enabled = True
        elif 'N' in enabled:
            enabled = False
        else:
            enabled = None

    if not enabled:
        NodeDefender.config.database.set(enabled=False)
        if NodeDefender.config.database.write():
            print_info('Database- config successfully written')
        return False
    supported_databases = ['mysql', 'sqlite']
    engine = None
    while engine is None:
        engine = prompt('Enter DB Engine(SQLite, MySQL)').lower()
        if engine not in supported_databases:
            engine = None
            continue

    host = None
    port = None
    username = None
    password = None
    database = None
    if engine == 'mysql':
        while not host:
            host = prompt('Enter Server Address')

        while not port:
            port = prompt('Enter Server Port')

        while not username:
            username = prompt('Enter Username')

        while not password:
            password = prompt('Enter Password')

        while not database:
            database = prompt('Enter Database Name')

    filepath = None
    if engine == 'sqlite':
        while not filepath:
            print_info('Filename for SQLite Database')
            print_info('SQLite will be stored as file in data- folder')
            print_info(NodeDefender.config.datafolder)
            print_info('Do not use any slashes in the filename')
            filepath = prompt('Enter File Path')

    NodeDefender.config.database.set(enabled=True, engine=engine, host=host, port=port, username=username, password=password, database=database, filepath=filepath)
    if NodeDefender.config.database.write():
        print_info('Database- config successfully written')
    return True