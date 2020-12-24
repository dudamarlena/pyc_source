# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/camelot_example/application_admin.py
# Compiled at: 2013-04-11 17:47:52
from camelot.view.art import Icon
from camelot.admin.application_admin import ApplicationAdmin
from camelot.admin.section import Section
from camelot.core.utils import ugettext_lazy as _

class MyApplicationAdmin(ApplicationAdmin):
    name = 'Camelot Video Store'

    def get_sections(self):
        from camelot.model.batch_job import BatchJob
        from camelot.model.memento import Memento
        from camelot.model.party import Person, Organization, PartyCategory
        from camelot.model.i18n import Translation
        from camelot.model.batch_job import BatchJob, BatchJobType
        from camelot_example.model import Movie, Tag, VisitorReport
        from camelot_example.view import VisitorsPerDirector
        from camelot_example.importer import ImportCovers
        return [
         Section(_('Movies'), self, Icon('tango/22x22/mimetypes/x-office-presentation.png'), items=[
          Movie,
          Tag,
          VisitorReport,
          ImportCovers()]),
         Section(_('Relation'), self, Icon('tango/22x22/apps/system-users.png'), items=[
          Person,
          Organization,
          PartyCategory]),
         Section(_('Configuration'), self, Icon('tango/22x22/categories/preferences-system.png'), items=[
          Memento,
          Translation,
          BatchJobType,
          BatchJob])]

    def get_actions(self):
        from camelot.admin.action import OpenNewView
        from camelot_example.model import Movie
        new_movie_action = OpenNewView(self.get_related_admin(Movie))
        new_movie_action.icon = Icon('tango/22x22/mimetypes/x-office-presentation.png')
        return [
         new_movie_action]


class MiniApplicationAdmin(MyApplicationAdmin):
    """An application admin for an application with a reduced number of
    widgets on the main window.
    """

    def get_toolbar_actions(self, toolbar_area):
        from PyQt4.QtCore import Qt
        from camelot.model.party import Person
        from camelot.admin.action import application_action, list_action
        from model import Movie
        movies_action = application_action.OpenTableView(self.get_related_admin(Movie))
        movies_action.icon = Icon('tango/22x22/mimetypes/x-office-presentation.png')
        persons_action = application_action.OpenTableView(self.get_related_admin(Person))
        persons_action.icon = Icon('tango/22x22/apps/system-users.png')
        if toolbar_area == Qt.LeftToolBarArea:
            return [movies_action,
             persons_action,
             list_action.OpenNewView(),
             list_action.OpenFormView(),
             list_action.DeleteSelection(),
             application_action.Exit()]

    def get_actions(self):
        return []

    def get_sections(self):
        return

    def get_main_menu(self):
        return

    def get_stylesheet(self):
        from camelot.view import art
        return art.read('stylesheet/black.qss')