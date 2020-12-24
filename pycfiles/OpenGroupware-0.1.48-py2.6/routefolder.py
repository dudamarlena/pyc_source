# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/coils/protocol/dav/workflow/routefolder.py
# Compiled at: 2012-10-12 07:02:39
from coils.core import *
from coils.net import *
from processfolder import ProcessFolder
from bpmlobject import BPMLObject
from versionsfolder import VersionsFolder
from signalobject import SignalObject
from proplistobject import PropertyListObject
from workflow import WorkflowPresentation

class RouteFolder(DAVFolder, WorkflowPresentation):

    def __init__(self, parent, name, **params):
        DAVFolder.__init__(self, parent, name, **params)
        self.entity = params['entity']
        self.route_id = self.entity.object_id
        self.archived = bool(params.get('archived', False))

    def supports_PUT(self):
        return True

    def _load_contents(self):
        self.data = {}
        self.log.debug(('Returning enumeration of processes of route {0}.').format(self.name))
        processes = self.context.run_command('route::get-processes', id=self.route_id, archived=self.archived)
        for process in processes:
            self.insert_child(str(process.object_id), process)

        if not self.archived:
            self.insert_child('markup.xml', None)
            self.insert_child('Versions', None)
            self.insert_child('propertyList.txt', None)
            self.insert_child('Archive', None)
        return True

    def object_for_key(self, name, auto_load_enabled=True, is_webdav=False):
        self.log.debug(('Request for folder key {0}').format(name))
        if name == 'signal':
            return SignalObject(self, name, parameters=self.parameters, entity=self.entity, context=self.context, request=self.request)
        else:
            if name == 'markup.xml':
                return BPMLObject(self, name, parameters=self.parameters, entity=self.entity, context=self.context, request=self.request)
            if name == 'Versions':
                return VersionsFolder(self, name, parameters=self.parameters, entity=self.entity, context=self.context, request=self.request)
            if name == 'Archive':
                return RouteFolder(self, name, parameters=self.parameters, entity=self.entity, context=self.context, archived=True, request=self.request)
            if name == 'propertyList.txt':
                return PropertyListObject(self, name, parameters=self.parameters, entity=self.entity, context=self.context, request=self.request)
            if name in ('.json', '.contents', '.ls'):
                result = []
                for process in self.context.run_command('route::get-processes', id=self.route_id):
                    if process.owner_id in self.context.context_ids:
                        result.append(process)

                if name == '.ls':
                    rendered = False
                else:
                    rendered = True
                return OmphalosCollection(self, name, detailLevel=65535, rendered=rendered, data=result, parameters=self.parameters, context=self.context, request=self.request)
            if self.is_loaded:
                if self.has_child(name):
                    process = self.get_child(name)
                else:
                    process = None
            else:
                try:
                    pid = int(name)
                except:
                    self.no_such_path()

                process = self.context.run_command('process::get', id=pid)
            if process is not None:
                return ProcessFolder(self, name, parameters=self.parameters, entity=process, context=self.context, request=self.request)
            self.no_such_path()
            return

    def do_PUT(self, request_name):
        if self.archived:
            raise CoilsException('PUT not supported in archived context')
        payload = self.request.get_request_payload()
        if request_name in ('markup.xml', 'markup.bpml'):
            self.context.run_command('route::set', object=self.entity, markup=payload)
            self.context.commit()
            self.request.simple_response(201)
        else:
            self.log.debug(('Attempting to create new process from route {0}').format(self.route_id))
            try:
                mimetype = self.request.headers.get('Content-Type', 'application/octet-stream')
                process = self.create_process(route=self.entity, data=payload, priority=201, mimetype=mimetype)
                if len(self.parameters) > 0:
                    for (key, value) in self.parameters.items():
                        key = ('xattr_{0}').format(key.lower().replace(' ', ''))
                        if value is None:
                            value = 'YES'
                        elif len(value) > 0:
                            value = str(value[0])
                        self.context.property_manager.set_property(process, 'http://www.opengroupware.us/oie', key, value)

                self.context.commit()
                self.log.info(('Process {0} created via DAV PUT by {1}.').format(process.object_id, self.context.get_login()))
                message = self.get_input_message(process)
                self.start_process(process)
                self.context.run_command('process::start', process=process)
            except Exception, e:
                self.log.exception(e)
                raise CoilsException('Failed to create process')

            paths = self.get_process_urls(process)
            self.request.simple_response(301, mimetype=message.mimetype, headers={'Location': paths['self'], 
               'X-COILS-WORKFLOW-MESSAGE-UUID': message.uuid, 
               'X-COILS-WORKFLOW-MESSAGE-LABEL': message.label, 
               'X-COILS-WORKFLOW-PROCESS-ID': process.object_id, 
               'X-COILS-WORKFLOW-OUTPUT-URL': paths['output']})
        return

    def do_DELETE(self):
        try:
            self.context.run_command('route::delete', object=self.entity)
            self.commit()
        except:
            self.request.simple_response(500, message='Deletion failed')
        else:
            self.request.simple_response(204, message='No Content')