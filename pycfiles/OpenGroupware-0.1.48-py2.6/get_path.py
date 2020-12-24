# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/coils/logic/project/get_path.py
# Compiled at: 2012-10-12 07:02:39
from sqlalchemy import *
from coils.core import *
from coils.core.logic import GetCommand

class GetProjectPath(GetCommand):
    __domain__ = 'project'
    __operation__ = 'get-path'

    def __init__(self):
        GetCommand.__init__(self)

    def parse_parameters(self, **params):
        self._project = params.get('project', None)
        self._path = params.get('path', None)
        self._create = params.get('create', False)
        if self._project is None or self._path is None:
            raise CoilsException('No project or path provided to project::get-path')
        return

    def run(self, **params):
        self.set_single_result_mode()
        if isinstance(self._path, basestring):
            components = self._path.split('/')[1:]
        elif isinstance(self._path, list):
            components = self._path
        else:
            raise CoilsException(('Path of unexpected type "{0}".').format(self._path))
        entity = self._ctx.run_command('project::get-root-folder', project=self._project)
        if not entity:
            raise CoilsException(('Unable to resolve root folder for projectId#{0}').format(self._project.object_id))
        for component in components:
            if entity.__entityName__ == 'Folder':
                result = self._ctx.run_command('folder::ls', id=entity.object_id, name=component)
                if len(result) == 0 and self._create:
                    self.log.debug(('Creating new folder for path; component is "{0}".').format(component))
                    entity = self._ctx.run_command('folder::new', folder=entity, values={'name': component})
                    if not entity.object_id:
                        raise CoilsException('Folder object created with no objectId')
                    if not entity.folder_id:
                        raise CoilsException('Folder object created with no folderId')
                    if entity is None:
                        self.log.debug(('Failed to create path component "{0}" for path "{1}".').format(component, self._path))
                elif len(result) == 1:
                    entity = result[0]
                    self.log.debug(('Found {0} for path component "{1}".').format(entity, component))
                else:
                    entity = None
                    break
            else:
                entity = None
                break

        self.log.debug(('Returning {0} for path "{1}"').format(entity, self._path))
        self.set_return_value(entity)
        return