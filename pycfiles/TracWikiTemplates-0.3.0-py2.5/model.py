# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/WikiTemplates/model.py
# Compiled at: 2007-11-10 06:34:56
import time
from trac.core import *
from trac.wiki.api import WikiSystem
from trac.util.text import to_unicode

class WikiTemplate(object):
    """Represents a wiki page (new or existing)."""

    def __init__(self, env, name=None, version=None, db=None, table=None):
        self.env = env
        self.name = name
        self.table = table
        if name:
            self._fetch(name, version, db, table)
        else:
            self.version = 0
            self.text = ''
            self.readonly = 0
        self.old_text = self.text
        self.old_readonly = self.readonly
        self.env.log.debug("WikiTemplate: '%s'", to_unicode(self.__dict__.items()))

    def _fetch(self, name, version=None, db=None, table=None):
        if not db:
            db = self.env.get_db_cnx()
        cursor = db.cursor()
        QUERY = 'SELECT version,text,readonly FROM '
        if table:
            QUERY += '%s ' % table
        else:
            QUERY += 'templates '
        if version:
            cursor.execute(QUERY + 'WHERE name=%s AND version=%s', (
             name, int(version)))
        else:
            cursor.execute(QUERY + 'WHERE name=%s ORDER BY version DESC LIMIT 1', (
             name,))
        row = cursor.fetchone()
        if row:
            (version, text, readonly) = row
            self.version = int(version)
            self.text = text
            self.readonly = readonly and int(readonly) or 0
        else:
            self.version = 0
            self.text = ''
            self.readonly = 0
        self.env.log.debug("WikiTemplate Fetched: '%s'", to_unicode(self.__dict__.items()))

    exists = property(fget=lambda self: self.version > 0)

    def delete(self, version=None, db=None):
        assert self.exists, 'Cannot delete non-existent page'
        if not db:
            db = self.env.get_db_cnx()
            handle_ta = True
        else:
            handle_ta = False
        page_deleted = False
        cursor = db.cursor()
        if version is None:
            cursor.execute('DELETE FROM templates WHERE name=%s', (self.name,))
            self.env.log.info('Deleted page %s' % self.name)
        else:
            cursor.execute('DELETE FROM templates WHERE name=%s and version=%s', (
             self.name, version))
            self.env.log.info('Deleted version %d of page %s' % (
             version, self.name))
        if version is None or version == self.version:
            self._fetch(self.name, None, db)
        if not self.exists:
            from trac.attachment import Attachment
            for attachment in Attachment.select(self.env, 'templates', self.name, db):
                attachment.delete(db)

            for listener in WikiSystem(self.env).change_listeners:
                listener.wiki_page_deleted(self)

        if handle_ta:
            db.commit()
        return

    def save(self, author, comment, remote_addr, t=None, db=None):
        if not db:
            db = self.env.get_db_cnx()
            handle_ta = True
        else:
            handle_ta = False
        if t is None:
            t = time.time()
        if self.text != self.old_text:
            cursor = db.cursor()
            cursor.execute('INSERT INTO templates (name,version,time,author,ipnr,text,comment,readonly) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)', (
             self.name, self.version + 1, t, author,
             remote_addr, self.text, comment, self.readonly))
            self.version += 1
        elif self.readonly != self.old_readonly:
            cursor = db.cursor()
            cursor.execute('UPDATE templates SET readonly=%s WHERE name=%s', (
             self.readonly, self.name))
        else:
            raise TracError('Page not modified')
        if handle_ta:
            db.commit()
        for listener in WikiSystem(self.env).change_listeners:
            if self.version == 1:
                listener.wiki_page_added(self)
            else:
                listener.wiki_page_changed(self, self.version, t, comment, author, remote_addr)

        self.old_readonly = self.readonly
        self.old_text = self.text
        return

    def get_history(self, db=None):
        if not db:
            db = self.env.get_db_cnx()
        cursor = db.cursor()
        cursor.execute('SELECT version,time,author,comment,ipnr FROM templates WHERE name=%s AND version<=%s ORDER BY version DESC', (
         self.name, self.version))
        for (version, time, author, comment, ipnr) in cursor:
            yield (
             version, time, author, comment, ipnr)