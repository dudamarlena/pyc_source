# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/coils/protocol/dav/groupware/projectssubfolder.py
# Compiled at: 2012-10-12 07:02:39
import hashlib
from coils.net import DAVFolder
from coils.core import Project, CoilsException
from groupwarefolder import GroupwareFolder
import projectfolder

class ProjectsSubFolder(DAVFolder, GroupwareFolder):
    """ Provides a WebDAV collection containing all the projects (as
        subfolders) which the current account has access to,"""

    def __init__(self, parent, name, **params):
        DAVFolder.__init__(self, parent, name, **params)

    def __repr__(self):
        return ('<ProjectsSubFolder projectId="{0}" projectName="{1} projectNumber="{2}"/>').format(self.entity.object_id, self.entity.name, self.entity.number)

    def _load_contents(self):
        children = self.context.run_command('project::get-projects', project=self.entity)
        for project in children:
            self.insert_child(project.number, project, alias=project.object_id)

        return True

    def _get_project_for_key(self, key):
        try:
            object_id = int(str(key).split('.')[0])
        except:
            pass

        project = self.context.run_command('project::get', id=object_id)

    def _get_project_for_name(self, name):
        project = self.context.run_command('project::get', number=name)
        if not project:
            project = self.context.run_command('project::get', name=name)
            if not project:
                try:
                    project = self.context.run_command('project::get', id=int(name))
                except:
                    project = None

        if project:
            if project.parent_id == self.entity.object_id:
                return project
        return

    def get_property_unknown_getctag(self):
        return self.get_property_caldav_getctag()

    def get_property_webdav_getctag(self):
        return self.get_property_caldav_getctag()

    def get_property_caldav_getctag(self):
        return self._get_ctag()

    def _get_ctag(self):
        if self.load_contents():
            m = hashlib.md5()
            for entry in self.get_children():
                m.update(('{0}:{1}').format(entry.object_id, entry.version))

            return unicode(m.hexdigest())
        return '0'

    def object_for_key(self, name, auto_load_enabled=True, is_webdav=False):
        if self.is_loaded:
            project = self.get_child(name)
        else:
            project = self._get_project_for_name(name)
            if project is None:
                name = name.replace('(', '%28').replace(')', '%29')
                project = self._get_project_for_name(name)
        if project is None:
            self.no_such_path()
        else:
            return projectfolder.ProjectFolder(self, project.number, entity=project, parameters=self.parameters, request=self.request, context=self.context)
        return

    def do_MKCOL(self, name):
        """ Create a collection with the specified name. """
        project = self.context.run_command('project::get', number=name)
        if project:
            project = self.context.run_command('project::set', object=project, values={'parent_id': self.entity.object_id})
        else:
            project = self.context.run_command('project::new', values={'name': name, 'number': name, 
               'parent_id': self.entity.object_id})
            self.context.run_command('project::set-contacts', project=project, contact_ids=[
             self.context.account_id])
        self.context.commit()
        self.request.simple_response(201)

    def do_MOVE(self, name):
        (source, target, target_name, overwrite) = self.move_helper(name)
        self.log.debug(('Request to move "{0}" to "{1}" as "{2}".').format(source, target, target_name))
        if isinstance(source.entity, Project) and source.entity != self.entity:
            if overwrite:
                pass
            values = {'number': target_name, 'parent_id': self.entity.object_id}
            if source.entity.name == 'Untitled Folder':
                values['name'] = target_name
            result = self.context.run_command('project::set', object=source.entity, values=values)
            self.context.commit()
            self.request.simple_response(204)
            return
        raise CoilsException(('Moving {0} via WebDAV is not supported in this context').format(source.entity))