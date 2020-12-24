# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/coils/protocol/dav/groupware/collectionsfolder.py
# Compiled at: 2012-10-12 07:02:39
import hashlib
from coils.core import Collection
from coils.net import DAVFolder, DAVObject, DAVFolder, EmptyFolder
from collectionfolder import CollectionFolder
from groupwarefolder import GroupwareFolder

class CollectionsFolder(DAVFolder, GroupwareFolder):

    def __init__(self, parent, name, **params):
        DAVFolder.__init__(self, parent, name, **params)

    def _load_contents(self):
        content = self.context.run_command('collection::list', properties=[Collection])
        if content is not None:
            for collection in content:
                if collection.dav_enabled:
                    self.insert_child(collection.object_id, collection, alias=collection.title)

        else:
            return False
        return True

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
            if self.has_child(name):
                collection = self.get_child(name)
            else:
                collection = None
        else:
            collection = self.context.run_command('collection::get', name=name)
        if collection is not None:
            if collection.dav_enabled:
                return CollectionFolder(self, name, entity=collection, parameters=self.parameters, request=self.request, context=self.context)
        else:
            print ('Failed to load collection "{0}".').format(name)
        self.no_such_path()
        return

    def do_MKCOL(self, name):
        """ Create a collection with the specified name. """
        collection = self.context.run_command('collection::new', values={'name': name, 'davenabled': 1})
        self.context.commit()
        self.request.simple_response(201)

    def do_MOVE(self, name):
        """ MOVE /dav/Projects/Application%20-%20BIE/Documents/87031000 HTTP/1.1

            RESPONSE
               201 (Created) - Created a new resource
               204 (No Content) - Moved to an existing resource
               403 (Forbidden) - The source and destination URIs are the same.
               409 - Conflict
               412 - Precondition failed
               423 - Locked
               502 - Bad Gateway
            """
        (source, target, target_name, overwrite) = self.move_helper(name)
        self.log.debug(('Request to move "{0}" to "{1}" as "{2}".').format(source, target, target_name))
        if isinstance(source.entity, Collection) and target == self:
            if overwrite:
                pass
            values = {'name': target_name}
            result = self.context.run_command('collection::set', object=source.entity, values=values)
            self.context.commit()
            self.request.simple_response(204)
            return
        raise CoilsException(('Moving {0} via WebDAV is not supported').format(source.entity))