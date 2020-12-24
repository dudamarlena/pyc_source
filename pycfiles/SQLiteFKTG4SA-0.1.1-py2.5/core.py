# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\sqlitefktg4sa\core.py
# Compiled at: 2008-11-21 03:12:02
from sqlalchemy.exc import OperationalError

class SqliteFkTriggerGenerator(object):

    def __init__(self, event, table, bind):
        self._table = table
        self._bind = bind
        if bind.dialect.name == 'sqlite':
            self._handle_event(event)

    def _handle_event(self, event):
        for c in self._table.c:
            for fk in c.foreign_keys:
                if event == 'after-create':
                    self._create(c, fk)
                elif event == 'before-delete':
                    self._drop(fk)

    def _create(self, col, fk):
        self._insert_trigger(fk.column.table.name, fk.column.name, self._table.name, col)
        self._update_trigger(fk.column.table.name, fk.column.name, self._table.name, col)
        if fk.ondelete is None:
            self._delete_trigger(fk.column.table.name, fk.column.name, self._table.name, col.name)
        elif fk.ondelete.lower() == 'cascade':
            self._delete_trigger_cascade(fk.column.table.name, fk.column.name, self._table.name, col.name)
        return

    def _insert_trigger(self, ptname, pcname, ftname, fcol):
        fcname = fcol.name
        trigger_name = self._trigger_name('fki', ptname, pcname, ftname, fcname)
        tsql = '\n        CREATE TRIGGER %s\n        BEFORE INSERT ON %s\n        FOR EACH ROW BEGIN\n          SELECT RAISE(ABORT, \'insert on table "%s" violates foreign key constraint "%s"\')\n          WHERE %s(SELECT %s FROM %s WHERE %s = NEW.%s) IS NULL;\n        END;\n        ' % (trigger_name, ftname, ftname, trigger_name,
         self._null_sql(fcname, fcol), pcname, ptname, pcname, fcname)
        self._bind.execute(tsql)

    def _update_trigger(self, ptname, pcname, ftname, fcol):
        fcname = fcol.name
        trigger_name = self._trigger_name('fku', ptname, pcname, ftname, fcname)
        tsql = '\n        CREATE TRIGGER %s\n        BEFORE UPDATE ON %s\n        FOR EACH ROW BEGIN\n          SELECT RAISE(ABORT, \'update on table "%s" violates foreign key constraint "%s"\')\n          WHERE %s(SELECT %s FROM %s WHERE %s = NEW.%s) IS NULL;\n        END;\n        ' % (trigger_name, ftname, ftname, trigger_name,
         self._null_sql(fcname, fcol), pcname, ptname, pcname, fcname)
        self._bind.execute(tsql)

    def _delete_trigger(self, ptname, pcname, ftname, fcname):
        trigger_name = self._trigger_name('fkd', ptname, pcname, ftname, fcname)
        tsql = '\n        CREATE TRIGGER %s\n        BEFORE DELETE ON %s\n        FOR EACH ROW BEGIN\n          SELECT RAISE(ABORT, \'delete on table "%s" violates foreign key constraint "%s"\')\n          WHERE (SELECT %s FROM %s WHERE %s = OLD.%s) IS NOT NULL;\n        END;\n        ' % (trigger_name, ptname, ptname, trigger_name, fcname, ftname,
         fcname, pcname)
        try:
            drop_sql = 'DROP TRIGGER %s' % trigger_name
            self._bind.execute(drop_sql)
        except OperationalError, e:
            if 'no such trigger' in str(e):
                pass

        self._bind.execute(tsql)

    def _delete_trigger_cascade(self, ptname, pcname, ftname, fcname):
        trigger_name = self._trigger_name('fkdc', ptname, pcname, ftname, fcname)
        tsql = '\n        CREATE TRIGGER %s\n        BEFORE DELETE ON %s\n        FOR EACH ROW BEGIN\n            DELETE FROM %s WHERE %s.%s = OLD.%s;\n        END;\n        ' % (trigger_name, ptname, ftname, ftname, fcname, pcname)
        try:
            drop_sql = 'DROP TRIGGER %s' % trigger_name
            self._bind.execute(drop_sql)
        except OperationalError, e:
            if 'no such trigger' in str(e):
                pass

        self._bind.execute(tsql)

    def _null_sql(self, fcname, col):
        if col.nullable:
            return 'NEW.%s IS NOT NULL AND ' % fcname
        return ''

    def _drop(self, fk):
        pass

    def _trigger_name(self, trigger_type, ptname, pcname, ftname, fcname):
        return '%s__%s__%s__%s__%s__auto' % (ftname, fcname, trigger_type, ptname, pcname)


def auto_assign(metadata, engine=None):
    if engine == None:
        engine = metadata.bind
    if engine.dialect.name != 'sqlite':
        return
    for tname in metadata.tables:
        metadata.tables[tname].append_ddl_listener('after-create', SqliteFkTriggerGenerator)

    return