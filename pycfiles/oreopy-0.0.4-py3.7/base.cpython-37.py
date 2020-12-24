# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/oreopy/models/base.py
# Compiled at: 2018-12-29 06:54:41
# Size of source mod 2**32: 2240 bytes
import sqlite3

class Model:
    __doc__ = ' This is Base Model for all ORM Models '

    def __init__(self, **kwargs):
        self.conn = sqlite3.connect('sqlite.db')
        self.cursor = self.conn.cursor()
        self.table_name = self._Model__get_class_name()
        allowed_kwargs = self._Model__get_props()
        allowed_kwargs.append('pk')
        self.values = {}
        for key in kwargs:
            if key not in allowed_kwargs:
                print(key)
            else:
                self.values[key] = kwargs[key]

    def __get_class_name(self):
        return self.__class__.__name__

    def __get_props(self):
        return [i for i in self.__class__.__dict__.keys() if i[:1] != '_']

    def create_table(self):
        create_table = 'CREATE TABLE {} (id INTEGER PRIMARY KEY, '.format(self.table_name)
        for attr in self._Model__get_props():
            create_table += attr + ' ' + str(self.__class__.__dict__[attr]) + ', '

        create_table = create_table[:-2] + ')'
        try:
            self.cursor.execute(create_table)
        except sqlite3.OperationalError:
            pass

    def save(self):
        insert = 'INSERT INTO {} VALUES (null, {})'
        props = ''
        for val in range(len(self.values)):
            props += '?,'

        props = props[:-1]
        insert = insert.format(self.table_name, props)
        values = tuple(self.values.values())
        self.cursor.executemany(insert, [values])
        self.conn.commit()

    def update(self, pk):
        update = 'UPDATE {} SET {} WHERE {}'
        set_str = ''
        for val in self.values:
            set_str += val + '=' + "'" + self.values[val] + "', "

        set_str = set_str[:-2]
        where_str = 'id = ' + str(pk)
        update = update.format(self.table_name, set_str, where_str)
        self.cursor.execute(update)
        self.conn.commit()

    def delete(self, pk):
        delete = 'DELETE FROM {} WHERE {}'
        where_str = 'id = ' + str(pk)
        delete = delete.format(self.table_name, where_str)
        self.cursor.execute(delete)
        self.conn.commit()