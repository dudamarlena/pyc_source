# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/coils/logic/workflow/create_process.py
# Compiled at: 2012-10-12 07:02:39
import pickle, shutil, traceback
from xml.sax import make_parser
from bpml_handler import BPMLSAXHandler
from coils.core import *
from coils.core.logic import CreateCommand
from keymap import COILS_PROCESS_KEYMAP
from utility import filename_for_process_markup, filename_for_process_code, filename_for_route_markup, parse_property_encoded_acl_list

class CreateProcess(CreateCommand):
    __domain__ = 'process'
    __operation__ = 'new'

    def __init__(self):
        CreateCommand.__init__(self)

    def prepare(self, ctx, **params):
        self.keymap = COILS_PROCESS_KEYMAP
        self.entity = Process
        CreateCommand.prepare(self, ctx, **params)

    def parse_parameters(self, **params):
        CreateCommand.parse_parameters(self, **params)
        self.do_rewind = params.get('rewind', True)
        if 'data' in params:
            self.values['data'] = params['data']
        elif 'filename' in params:
            self.values['handle'] = os.open(params['filename'], 'rb')
        elif 'handle' in params:
            self.values['handle'] = params['handle']
        self._mimetype = params.get('mimetype', 'application/octet-stream')

    def copy_markup(self, route):
        source = BLOBManager.Open(filename_for_route_markup(route), 'rb')
        target = BLOBManager.Create(filename_for_process_markup(self.obj))
        shutil.copyfileobj(source, target)
        target.flush()
        source.seek(0)
        bpml = source.read()
        BLOBManager.Close(source)
        BLOBManager.Close(target)
        self.obj.set_markup(bpml)

    def compile_markup(self):
        handle = BLOBManager.Open(filename_for_process_markup(self.obj), 'rb', encoding='binary')
        parser = make_parser()
        handler = BPMLSAXHandler()
        parser.setContentHandler(handler)
        parser.parse(handle)
        code = handler.get_processes()
        BLOBManager.Close(handle)
        handle = BLOBManager.Create(filename_for_process_code(self.obj), encoding='binary')
        pickle.dump(code, handle)
        BLOBManager.Close(handle)

    def copy_default_acls_from_route(self, process, route):
        default_acls = self._ctx.property_manager.get_property(route, 'http://www.opengroupware.us/oie', 'defaultProcessACLs')
        if default_acls:
            try:
                acls = parse_property_encoded_acl_list(default_acls.get_value())
                if acls:
                    for acl in acls:
                        self._ctx.run_command('object::set-acl', object=process, context_id=int(acl[0]), action=acl[1], permissions=acl[2])
                        self.log.debug(('Applied default ACL for contextId#{0}').format(int(acl[0])))

            except CoilsException, e:
                message = traceback.format_exc()
                self.log.exception(e)
                if self._ctx.amq_available:
                    self._ctx.send_administrative_notice(category='workflow', urgency=7, subject=('Unable to apply defaultProcessACLs value to processId#{0}').format(process.object_id), message=message)
                return False
            else:
                return True
        else:
            return True

    def run(self, **params):
        CreateCommand.run(self, **params)
        route = None
        if self.obj.route_id:
            route = self._ctx.run_command('route::get', id=self.obj.route_id, access_check=self.access_check)
        if route:
            message = None
            if 'data' in self.values:
                message = self._ctx.run_command('message::new', process=self.obj, mimetype=self._mimetype, label='InputMessage', data=self.values['data'])
            elif 'handle' in self.values:
                message = self._ctx.run_command('message::new', process=self.obj, mimetype=self._mimetype, label='InputMessage', rewind=self.do_rewind, handle=self.values['handle'])
            else:
                raise CoilsException('Cannot create process without input')
            self.obj.input_message = message.uuid
            self.copy_markup(route)
            self.compile_markup()
            self.save()
            shelf = BLOBManager.OpenShelf(uuid=self.obj.uuid)
            shelf.close()
            self.copy_default_acls_from_route(self.obj, route)
        else:
            raise CoilsException('No such route or route not available')
        return