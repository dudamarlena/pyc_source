# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/coils/protocol/dav/davroot.py
# Compiled at: 2012-10-12 07:02:39
from coils.net import *
from groupware import ContactsFolder, CalendarFolder, AccountsFolder, TeamsFolder, TasksFolder, FavoritesFolder, ProjectsFolder, CabinetsFolder, CollectionsFolder
from files import FilesFolder
from workflow import WorkflowFolder
DAV_ROOT_FOLDERS = {'Contacts': 'ContactsFolder', 'Projects': 'ProjectsFolder', 
   'Calendar': 'CalendarFolder', 
   'Journal': 'EmptyFolder', 
   'Collections': 'CollectionsFolder', 
   'Files': 'FilesFolder', 
   'Cabinets': 'CabinetsFolder', 
   'Users': 'AccountsFolder', 
   'Tasks': 'TasksFolder', 
   'Teams': 'TeamsFolder', 
   'Favorites': 'FavoritesFolder', 
   'Workflow': 'WorkflowFolder'}

class DAVRoot(DAVFolder, Protocol):
    """The root of the DAV hierarchy."""
    __pattern__ = [
     'dav', 'DAV']
    __namespace__ = None
    __xmlrpc__ = False

    def __init__(self, parent, **params):
        DAVFolder.__init__(self, parent, 'dav', **params)
        DAVFolder.Root = self
        self.root = self

    def get_name(self):
        return 'dav'

    def _load_contents(self):
        self.init_context()
        for key in DAV_ROOT_FOLDERS.keys():
            classname = DAV_ROOT_FOLDERS[key]
            classclass = eval(classname)
            self.insert_child(key, classclass(self, key, parameters=self.parameters, request=self.request, context=self.context))

        return True

    def get_property_webdav_current_user_principal(self):
        url = self.get_appropriate_href(('/dav/Contacts/{0}.vcf').format(self.context.account_id))
        return ('<D:href>{0}</D:href>').format(url)

    def get_property_caldav_calendar_home_set(self):
        url = self.get_appropriate_href('/dav/Calendar')
        return ('<D:href>{0}</D:href>').format(url)

    def get_property_caldav_calendar_user_address_set(self):
        if isinstance(self.context, AuthenticatedContext):
            tmp = [
             self.context.account_object.get_company_value('email1'),
             self.context.account_object.get_company_value('email2'),
             self.context.account_object.get_company_value('email3')]
            tmp = [ x.string_value for x in tmp if x ]
            tmp = [ ('<D:href>mailto:{0}</D:href>').format(x.strip()) for x in tmp if x ]
            return ('').join(tmp)
        else:
            return