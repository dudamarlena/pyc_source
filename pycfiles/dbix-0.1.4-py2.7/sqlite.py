# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/dbix/sqlite.py
# Compiled at: 2017-10-18 08:51:51
from .sqlschema import SQLSchema
import sqlite3, os

class SQLITE(SQLSchema):
    _type_conv = dict(enum='varchar', boolean='integer', datetime='timestamp', tinyint='integer', mediumtext='text')
    prelude = '\n\tPRAGMA recursive_triggers=1;\n\t'
    postfix = '\n\tPRAGMA foreign_keys = ON;\n\t'
    query_prefix = '\n\tPRAGMA recursive_triggers=1;\n\t--PRAGMA foreign_keys = Off;\n\t'
    getdate = dict(timestamp="strftime('%Y-%m-%d %H:%M:%f', 'now')", date="strftime('%Y-%m-%d', 'now')", time="strftime('%H:%M:%f', 'now')")
    on_update_trigger = '\n\t\tcreate trigger [tr_%(table)s%%(c)d] \n\t\tafter update \n\t\tof %(other_fields)s \n\t\ton [%(table)s] for each row \n--\t\twhen ([new].[%(field)s]=[old].[%(field)s])\n\t\tbegin\n\t\t\tupdate [%(table)s] \n\t\t\tset [%(field)s]=%(getdate_tr)s\n\t\t\twhere %(where_pk)s;\n\t\tend;\n\t\t'
    dbsuffix = '.sqlite'
    path = None

    def __init__(self, **kw):
        super(SQLITE, self).__init__()
        self.type_render['integer primary key autoincrement'] = self.type_render['integer']
        self.dbsuffixlen = len(self.dbsuffix)
        path = kw.get('path')
        if os.path.exists(path):
            self.path = os.path.abspath(path)

    def render_autoincrement(self, attrs, entity, name):
        attrs, _ = super(SQLITE, self).render_autoincrement(attrs, entity, name)
        if attrs.get('is_auto_increment'):
            attrs['data_type'] = 'integer primary key autoincrement'
            self.this_render_pk = False
        return (
         attrs, '')

    def db_filename(self, dbname):
        return os.path.join(self.path, dbname + self.dbsuffix)

    def isdba(self, **kw):
        return self.path and os.access(self.path, os.W_OK)

    def db_create(self, dbname):
        path = self.db_filename(dbname)
        if os.path.exists(path):
            return False
        open(path, 'w').write('')
        return os.path.exists(path)

    def db_drop(self, dbname):
        if not self.isdba():
            return
        if dbname == self.dbname:
            self.db_disconnect()
        path = self.db_filename(dbname)
        if os.path.exists(path):
            os.remove(path)
        return not os.path.exists(path)

    def db_connect(self, dbname):
        try:
            path = self.db_filename(dbname)
            self.connection = sqlite3.connect(path, detect_types=sqlite3.PARSE_DECLTYPES)
            self.dbname = dbname
            return True
        except:
            self.connection = None
            self.dbname = None
            return False

        return

    def db_disconnect(self):
        if not self.connection:
            return
        else:
            self.connection.close()
            self.connection = None
            self.dbname = None
            return

    def db_commit(self):
        if not self.connection:
            return
        self.connection.commit()

    def db_rollback(self):
        if not self.connection:
            return
        self.connection.rollback()

    def db_name(self):
        return self.dbname

    def db_list(self):
        return [ db[:-self.dbsuffixlen] for db in os.listdir(self.path) if db.endswith(self.dbsuffix)
               ]

    def db_execute(self, script, param=list()):
        if not self.connection:
            return
        cur = self.connection.cursor()
        with self.connection:
            cur.executescript(self.query_prefix)
            cur.execute(script, param)
        return cur

    def db_executemany(self, script, param=list()):
        if not self.connection:
            return
        cur = self.connection.cursor()
        with self.connection:
            cur.executescript(self.query_prefix)
            cur.executemany(script, param)
        return cur

    def db_executescript(self, script):
        if not self.connection:
            return
        cur = self.connection.cursor()
        with self.connection:
            cur.executescript(self.query_prefix + ';' + script)
        return cur

    def perform_insert(self, script, param, pk_fields, table, new_key):
        self.db_execute(script, param)
        if new_key:
            return new_key
        script = 'select %sfrom %s\nwhere rowid=last_insert_rowid()' % (
         (',').join([ self.render_name(field) for field in pk_fields ]),
         self.render_name(table))
        res = self.db_execute(script)
        return res.fetchone()