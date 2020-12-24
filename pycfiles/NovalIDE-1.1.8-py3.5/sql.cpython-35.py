# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/dummy/sql.py
# Compiled at: 2019-08-16 02:55:35
# Size of source mod 2**32: 737 bytes
CREATE_USER_TABLE_SQL = "\n    CREATE TABLE user (\n        id INTEGER primary key autoincrement,\n        user_id varchar (24),\n        user_name varchar (100),\n        os_bit varchar (50),\n        sn varchar (100),\n        os varchar (260),\n        phone varchar (100),\n        email varchar (300),\n        password text,\n        is_pro BOOLEAN default 0,\n        created_time datetime default (datetime('now', 'localtime'))\n    )\n"
CREATE_USER_DATA_TABLE_SQL = "\n    CREATE TABLE data (\n        id INTEGER primary key autoincrement,\n        user_id int,\n        app_version varchar (100),\n        submited BOOLEAN default 0,\n        start_time datetime default (datetime('now', 'localtime')),\n        end_time datetime\n    )\n"