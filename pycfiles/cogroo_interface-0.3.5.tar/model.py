# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.darwin-8.8.0-Power_Macintosh/egg/cogplanet/model.py
# Compiled at: 2006-12-30 03:24:31
import feedparser, datetime
from turbogears.database import metadata, session
from sqlalchemy import *
from sqlalchemy.ext.activemapper import *
from turbogears.database import session
from turbogears import identity
from turbogears import scheduler
from BeautifulSoup import BeautifulSoup
from genshi.input import ParseError
from genshi.template import MarkupTemplate
import logging
log = logging.getLogger('cogplanet.model')

class Planet(ActiveMapper):
    __module__ = __name__

    class mapping:
        __module__ = __name__
        __table__ = 'cp_planet'
        id = column(Integer, primary_key=True)
        name = column(Unicode, nullable=False)
        display_entries = column(Integer, default=50, nullable=False)
        update_interval = column(Integer, default=1440, nullable=False)
        feeds = one_to_many('Feed', colname='planet_id')


class Feed(ActiveMapper):
    __module__ = __name__

    class mapping:
        __module__ = __name__
        __table__ = 'cp_feed'
        id = column(Integer, primary_key=True)
        planet_id = column(Integer, foreign_key=ForeignKey('cp_planet.id'))
        name = column(Unicode)
        htmlurl = column(Unicode)
        xmlurl = column(Unicode)
        updated_at = column(DateTime)
        update_interval = column(Integer, default=1440)
        entries = one_to_many('Entry', colname='feed_id')

    def refresh_entries(self):
        log.info('refreshing %s' % self.xmlurl)
        data = None
        self.updated_at = datetime.datetime.now()
        data = feedparser.parse(self.xmlurl)
        for e in data['entries']:
            entries = Entry.select(and_(Entry.c.url == e['link'], Entry.c.feed_id == self.id))
            if len(entries) == 0:
                entry = Entry()
            else:
                entry = entries[0]
            entry.title = e['title']
            try:
                entry.updated_at = datetime.datetime(*e['updated_parsed'][:7])
            except Exception:
                if entry.updated_at == None:
                    entry.updated_at = datetime.datetime.now()

            entry.url = e['link']
            try:
                entry.original = e['summary_detail']['value']
            except KeyError:
                entry.original = e['content'][0]['value']

            soup = BeautifulSoup('<div>%s</div>' % entry.original)
            original = soup.prettify()
            try:
                mt = MarkupTemplate(original)
                stream = mt.generate()
                rendered = stream.render('xhtml')
                entry.content = original
                entry.parsed = True
            except ParseError, pe:
                log.error('exception occurred parsing %s' % entry.title, pe)
                print soup.prettify()

            self.entries.append(entry)

        return data


class Entry(ActiveMapper):
    __module__ = __name__

    class mapping:
        __module__ = __name__
        __table__ = 'cp_entry'
        id = column(Integer, primary_key=True)
        feed_id = column(Integer, foreign_key=ForeignKey('cp_feed.id'))
        url = column(Unicode)
        title = column(Unicode)
        updated_at = column(DateTime)
        original = column(Unicode)
        content = column(Unicode)
        parsed = column(Boolean, default=False)


def refresh_feeds():
    now = None
    feeds = Feed.select()
    for f in feeds:
        trans = session.create_transaction()
        if f.updated_at == None:
            f.refresh_entries()
        else:
            if now == None:
                now = datetime.datetime.now(f.updated_at.tzinfo)
            delta = datetime.timedelta(minutes=f.update_interval)
            if now > f.updated_at + delta:
                f.refresh_entries()
        trans.commit()

    return


scheduler.add_interval_task(refresh_feeds, 600)
visits_table = Table('visit', metadata, Column('visit_key', String(40), primary_key=True), Column('created', DateTime, nullable=False, default=datetime.datetime.now), Column('expiry', DateTime))
visit_identity_table = Table('visit_identity', metadata, Column('visit_key', String(40), primary_key=True), Column('user_id', Integer, ForeignKey('tg_user.user_id'), index=True))
groups_table = Table('tg_group', metadata, Column('group_id', Integer, primary_key=True), Column('group_name', Unicode(16), unique=True), Column('display_name', Unicode(255)), Column('created', DateTime, default=datetime.datetime.now))
users_table = Table('tg_user', metadata, Column('user_id', Integer, primary_key=True), Column('user_name', Unicode(16), unique=True), Column('email_address', Unicode(255), unique=True), Column('display_name', Unicode(255)), Column('password', Unicode(40)), Column('created', DateTime, default=datetime.datetime.now))
permissions_table = Table('permission', metadata, Column('permission_id', Integer, primary_key=True), Column('permission_name', Unicode(16), unique=True), Column('description', Unicode(255)))
user_group_table = Table('user_group', metadata, Column('user_id', Integer, ForeignKey('tg_user.user_id')), Column('group_id', Integer, ForeignKey('tg_group.group_id')))
group_permission_table = Table('group_permission', metadata, Column('group_id', Integer, ForeignKey('tg_group.group_id')), Column('permission_id', Integer, ForeignKey('permission.permission_id')))

class Visit(object):
    __module__ = __name__

    def lookup_visit(cls, visit_key):
        return Visit.get(visit_key)

    lookup_visit = classmethod(lookup_visit)


class VisitIdentity(object):
    __module__ = __name__


class Group(object):
    """
    An ultra-simple group definition.
    """
    __module__ = __name__


class User(object):
    """
    Reasonably basic User definition. Probably would want additional
    attributes.
    """
    __module__ = __name__

    def permissions(self):
        perms = set()
        for g in self.groups:
            perms = perms | set(g.permissions)

        return perms

    permissions = property(permissions)


class Permission(object):
    __module__ = __name__


assign_mapper(session.context, Visit, visits_table)
assign_mapper(session.context, VisitIdentity, visit_identity_table, properties=dict(users=relation(User, backref='visit_identity')))
assign_mapper(session.context, User, users_table)
assign_mapper(session.context, Group, groups_table, properties=dict(users=relation(User, secondary=user_group_table, backref='groups')))
assign_mapper(session.context, Permission, permissions_table, properties=dict(groups=relation(Group, secondary=group_permission_table, backref='permissions')))