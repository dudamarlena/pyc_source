# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/coils/protocol/dav/groupware/collectionfolder.py
# Compiled at: 2012-10-12 07:02:39
import hashlib
from coils.core import Contact, Enterprise, Document, Folder, Note, Project, Task
from coils.net import DAVFolder, DAVObject, DAVFolder
from projectfolder import ProjectFolder
from documentsfolder import DocumentsFolder
from documentobject import DocumentObject
from contactobject import ContactObject
from eventobject import EventObject
BANNED_OBJECT_IDS = [
 10000, 8999]
TYPE_FACTORY = {'Project': ProjectFolder, 'Folder': DocumentsFolder, 
   'Contact': ContactObject, 
   'Appointment': EventObject, 
   'Document': DocumentObject}

class CollectionFolder(DAVFolder):
    """ Provides a WebDAV collection containing all the projects (as
        subfolders) which the current account has access to,"""

    def __init__(self, parent, name, **params):
        DAVFolder.__init__(self, parent, name, **params)

    def _load_contents(self):
        """ Enumerates projects using account::get-projects."""
        contents = self.context.run_command('collection::get-assignments', collection=self.entity, as_entity=True)
        if contents is not None:
            for entity in contents:
                if entity.__entityName__ in TYPE_FACTORY and entity.object_id not in BANNED_OBJECT_IDS:
                    display_name = entity.get_display_name()
                    if display_name is not None:
                        self.insert_child(entity.object_id, entity, alias=display_name)

            return True
        else:
            return False
            return

    def get_property_unknown_getctag(self):
        return self.get_property_caldav_getctag()

    def get_property_webdav_getctag(self):
        return self.get_property_caldav_getctag()

    def get_property_caldav_getctag(self):
        return self._get_ctag()

    def _get_ctag(self):
        return ('{0}:{1}').format(self.entity.object_id, self.entity.version)

    def object_for_key(self, name, auto_load_enabled=True, is_webdav=False):
        if name == '.ctag':
            return StaticObject(self, '.ctag', context=self.context, request=self.request, payload=self._get_ctag(), mimetype='text/plain')
        if auto_load_enabled:
            if self.load_contents():
                if self.has_child(name):
                    tmp = self.get_child(name)
                    if tmp:
                        if tmp.__entityName__ in TYPE_FACTORY:
                            return TYPE_FACTORY[tmp.__entityName__](self, name, entity=tmp, parameters=self.parameters, request=self.request, context=self.context)
        self.no_such_path()