# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/cltwit/cltwitdb.py
# Compiled at: 2013-02-02 12:49:00
__doc__ = '\nGestion de la base de données sqlite de cltwit\n'
import sqlite3, os, sys, gettext, tweepy
APP_NAME = 'cltwit'
LOC_PATH = os.path.dirname(__file__) + '/locale'
gettext.find(APP_NAME, LOC_PATH)
gettext.install(APP_NAME, LOC_PATH, True)

class cltwitdb:

    def __init__(self, loc, name):
        self.dblocation = loc
        self.table_name = name

    def create(self, api, twittername):
        u""" Créer une base de données """
        if not os.path.exists(self.dblocation):
            conn = sqlite3.connect(self.dblocation)
            c = conn.cursor()
            sql = 'create table if not exists ' + self.table_name + '(id integer PRIMARY KEY, date text, tweet text, id_str text, url text )'
            c.execute(sql)
        conn = sqlite3.connect(self.dblocation)
        c = conn.cursor()
        conn.text_factory = str
        page_list = []
        try:
            for page in tweepy.Cursor(api.user_timeline, count=200, include_rts=True).pages(16):
                page_list.append(page)

            for page in page_list:
                for status in page:
                    self.insert(status.text, status.created_at, status.id_str, twittername, conn, c)

        except Exception as e:
            print str(e) + '\n'

        conn.commit()
        c.close()
        conn.close()

    def update(self, api, twittername):
        u""" Mettre à jour une base de données """
        if not os.path.exists(self.dblocation):
            print _("La base de données n'existe pas, utilisez --database create")
            sys.exit()
        conn = sqlite3.connect(self.dblocation)
        c = conn.cursor()
        c.execute('select id_str from twitter order by date desc limit 1')
        since = c.fetchone()[0]
        nb = 0
        try:
            for status in tweepy.api.user_timeline(twittername, since_id=since):
                nb += 1
                self.insert(status.text, status.created_at, status.id_str, twittername, conn, c)

        except Exception as e:
            print str(e) + '\n'

        conn.commit()
        c.close()
        conn.close()
        return nb

    def insert(self, statustext, statuscreated_at, statusid_str, twittername, conn, c):
        u""" Insérer dans la base """
        conn.text_factory = str
        statusurl = ('https://twitter.com/{0}/status/{1}').format(twittername, statusid_str)
        insert_query = ('INSERT INTO {0} VALUES (null,{1})').format(self.table_name, (',').join('????'))
        try:
            c.execute(insert_query, [str(statuscreated_at),
             statustext.encode('utf-8'), str(statusid_str), str(statusurl)])
        except Exception as e:
            print e

    def search(self, search, champ_recherche):
        """Rechercher un motif dans une table sqlite (retourne un tuple)"""
        conn = sqlite3.connect(self.dblocation)
        conn.text_factory = str
        c = conn.cursor()
        c.execute(('select * from {0} where {1} like ? order by date desc').format(self.table_name, champ_recherche), ['%' + search + '%'])
        result = c.fetchall()
        c.close()
        conn.close()
        return result