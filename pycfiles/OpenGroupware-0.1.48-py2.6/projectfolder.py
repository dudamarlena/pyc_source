# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/coils/protocol/dav/groupware/projectfolder.py
# Compiled at: 2012-10-12 07:02:39
from coils.net import DAVFolder, EmptyFolder
from contactsfolder import ContactsFolder
from tasksfolder import TasksFolder
from documentsfolder import DocumentsFolder
from notesfolder import NotesFolder
from rss_feed import ProjectTaskActionsRSSFeed
import projectssubfolder

class ProjectFolder(DAVFolder):

    def __init__(self, parent, name, **params):
        DAVFolder.__init__(self, parent, name, **params)

    def __repr__(self):
        return ('<ProjectFolder contextId="{0}" login="{1}" projectId="{2}" projectName="{3}" contextId="{4}" login="{5}"/>').format(self.context.account_id, self.context.login, self.entity.object_id, self.entity.name, self.context.account_id, self.context.login)

    def _load_contents(self):
        ua = self.context.user_agent_description
        if ua['webdav']['showProjectTasksFolder']:
            self.insert_child('Tasks', None, alias='Tasks')
        if ua['webdav']['showProjectNotesFolder']:
            self.insert_child('Notes', None)
        if ua['webdav']['showProjectContactsFolder']:
            self.insert_child('Contacts', None)
        if ua['webdav']['showProjectDocumentsFolder']:
            self.insert_child('Documents', None)
        if ua['webdav']['showProjectEnterprisesFolder']:
            self.insert_child('Enterprises', None)
        if ua['webdav']['showProjectVersionsFolder']:
            self.insert_child('Versions', None)
        if ua['webdav']['showProjectProjectsFolder']:
            self.insert_child('Projects', None)
        return True

    def object_for_key(self, name, auto_load_enabled=True, is_webdav=False):
        if name == 'actions.rss':
            return ProjectTaskActionsRSSFeed(self, name, self.entity, request=self.request, context=self.context)
        else:
            if name == 'Documents':
                folder = self.context.run_command('project::get-root-folder', project=self.entity)
                if folder is None:
                    self.no_such_path()
                return DocumentsFolder(self, name, entity=folder, parameters=self.parameters, request=self.request, context=self.context)
            else:
                if name == 'Notes':
                    return NotesFolder(self, name, entity=self.entity, parameters=self.parameters, request=self.request, context=self.context)
                if name == 'Tasks':
                    return TasksFolder(self, name, entity=self.entity, parameters=self.parameters, request=self.request, context=self.context)
                if name == 'Contacts':
                    return ContactsFolder(self, name, entity=self.entity, parameters=self.parameters, request=self.request, context=self.context)
                if name == 'Projects':
                    return projectssubfolder.ProjectsSubFolder(self, name, entity=self.entity, parameters=self.parameters, request=self.request, context=self.context)
                return EmptyFolder(self, name, entity=self.entity, parameters=self.parameters, request=self.request, context=self.context)
            return