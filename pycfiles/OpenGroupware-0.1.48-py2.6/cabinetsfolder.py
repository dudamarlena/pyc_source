# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/coils/protocol/dav/groupware/cabinetsfolder.py
# Compiled at: 2012-10-12 07:02:39
import urlparse, urllib
from coils.core import Folder
from uuid import uuid4
from documentsfolder import DocumentsFolder

class CabinetsFolder(DocumentsFolder):

    def __init__(self, parent, name, **params):
        DocumentsFolder.__init__(self, parent, name, **params)

    def _load_contents(self):
        contents = self.context.run_command('account::get-cabinets')
        for entity in contents:
            self.insert_child(entity.name, entity)

        return True

    def do_MKCOL(self, name):
        """
           TODO: Implement a good failure response 
           
           201 (Created) - The collection or structured resource was created in
           its entirety.
           
           403 (Forbidden) - This indicates at least one of two conditions: 1)
           the server does not allow the creation of collections at the given
           location in its namespace, or 2) the parent collection of the
           Request-URI exists but cannot accept members.

           405 (Method Not Allowed) - MKCOL can only be executed on a
           deleted/non-existent resource.

           409 (Conflict) - A collection cannot be made at the Request-URI until
           one or more intermediate collections have been created.

           415 (Unsupported Media Type)- The server does not support the request
           type of the body.

           507 (Insufficient Storage) - The resource does not have sufficient
           space to record the state of the resource after the execution of this
           method.
        """
        project_name = uuid4().hex
        project = self.context.run_command('project::new', values={'name': project_name, 'number': project_name, 
           'is_fake': 1, 
           'kind': 'opengroupware.coils.cabinet'})
        self.context.run_command('project::set-contacts', project=project, contact_ids=[self.context.account_id])
        self.context.run_command('object::set-acl', object=project, context_id=self.context.account_id, permissions='rwasdlc')
        folder = self.context.run_command('project::get-root-folder', project=project)
        folder.name = name
        self._update_properties(folder)
        self.context.commit()
        self.request.simple_response(201)

    def do_DELETE(self, name):
        if self.load_contents():
            if self.has_child(name):
                child = self.get_child(name)
                self.log.debug(('Request to delete {0}').format(child))
                if isinstance(child, Folder):
                    self.log.debug(('Request to delete folder "{0}"').format(name))
                    project = self.context.run_command('project::get', id=child.project_id)
                    self.context.run_command('project::delete', object=project)
                    self.context.commit()
        self.request.simple_response(204)

    def do_MOVE(self, name):
        """ MOVE /dav/Projects/Application%20-%20BIE/Documents/87031000 HTTP/1.1
            Content-Length: 0
            Destination: http://172.16.54.1:8080/dav/Projects/Application%20-%20BIE/Documents/%5B%5DSheet1
            Overwrite: T
            translate: f
            User-Agent: Microsoft-WebDAV-MiniRedir/6.0.6001
            Host: 172.16.54.1:8080
            Connection: Keep-Alive
            Authorization: Basic YWRhbTpmcmVkMTIz

            RESPONSE
               201 (Created) - Created a new resource
               204 (No Content) - Moved to an existing resource
               403 (Forbidden) - The source and destination URIs are the same.
               409 - Conflict
               412 - Precondition failed
               423 - Locked
               502 - Bad Gateway
            """
        source = self.object_for_key(name)
        overwrite = self.request.headers.get('Overwrite', 'F').upper()
        if overwrite == 'T':
            overwrite = True
        else:
            overwrite = False
        destination = self.request.headers.get('Destination')
        destination = urlparse.urlparse(destination).path
        destination = urllib.unquote(destination)
        destination = destination.split('/', 64)[2:]
        target_name = destination[-1:][0]
        target_path = destination[:-1]
        if len(target_path) != 1 or target_path[0] != 'Cabinets':
            self.request.simple_response(403, data='Cabinet folders cannot be moved from the Cabinets folder')
            return
        else:
            destination = None
            target = self.root
            try:
                for component in target_path:
                    target = target.object_for_key(component)

            except:
                pass

            self.log.debug(('Request to move "{0}" to "{1}" as "{2}".').format(source, target, target_name))
            if source.entity:
                if isinstance(source.entity, Folder):
                    target = self.context.run_command('folder::move', folder=source.entity, to_folder=None, to_filename=target_name)
                    self._update_properties(target)
                    self.context.commit()
                    self.request.simple_response(207)
                    return
                raise CoilsException(('Moving {0} via Cabinets [WebDAV] is not supported').format(source.entity))
            raise NotImplementedException()
            return

    def _update_properties(self, folder):
        cabinet_name = folder.name.lower().replace(' ', '_').replace('-', '_')
        self.context.property_manager.set_property(folder, 'http://www.opengroupware.us/cabinets', 'name', cabinet_name)
        project = self.context.run_command('project::get', id=folder.project_id)
        if project:
            self.context.property_manager.set_property(project, 'http://www.opengroupware.us/cabinets', 'name', cabinet_name)