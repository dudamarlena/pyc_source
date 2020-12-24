# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: ./gthnk/__init__.py
# Compiled at: 2017-11-24 17:29:58
# Size of source mod 2**32: 2663 bytes
from datetime import timedelta
from flask_diamond import Diamond
from flask_diamond.facets.database import db
from flask.ext.markdown import Markdown
from mdx_linkify.mdx_linkify import LinkifyExtension
from mdx_journal import JournalExtension
from .models import User, Role, Entry, Day, Page
application = None

class Gthnk(Diamond):

    def init_administration(self):
        from .views.journal_explorer import JournalExplorer
        from .views.administration import DayAdmin, PageAdmin, EntryAdmin
        admin = self.super('administration', user=User, role=Role, index_view='')
        admin.add_view(DayAdmin(Day,
          (db.session),
          name='Days',
          category='Admin'))
        admin.add_view(PageAdmin(Page,
          (db.session),
          name='Pages',
          category='Admin'))
        admin.add_view(EntryAdmin(Entry,
          (db.session),
          name='Entries',
          category='Admin'))
        admin.add_view(JournalExplorer(name='Journal', endpoint='journal'))

    def init_blueprints(self):
        self.super('blueprints')
        from .views.diamond import diamond_blueprint
        self.app.register_blueprint(diamond_blueprint)
        from .views.journal_explorer import journal_blueprint
        self.app.register_blueprint(journal_blueprint)
        from .views.administration import adminbaseview
        self.app.register_blueprint(adminbaseview)


def create_app():
    global application
    if not application:
        application = Gthnk()
        application.facet('configuration')
        application.facet('logs')
        application.facet('database')
        application.facet('marshalling')
        application.facet('blueprints')
        application.facet('accounts')
        application.facet('signals')
        application.facet('forms')
        application.facet('error_handlers')
        application.facet('request_handlers')
        application.facet('administration')
        application.app.permanent_session_lifetime = timedelta(minutes=30)
        application.app.logger.info('starting gthnk server')
        application.app.md = Markdown((application.app), extensions=[
         LinkifyExtension(), JournalExtension()])
    return application.app