# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/coils/protocol/dav/workflow/signalobject.py
# Compiled at: 2012-10-12 07:02:39
import io
from StringIO import StringIO
from datetime import datetime
from coils.core import *
from coils.net import *
from coils.net import *
from workflow import WorkflowPresentation

class SignalObject(DAVObject, WorkflowPresentation):
    """ Represent a BPML markup object in WebDAV """

    def __init__(self, parent, name, **params):
        DAVObject.__init__(self, parent, name, **params)

    def do_GET(self):
        if self.entity is None:
            self.signal_queue_manager()
            self.request.simple_response(201)
            return
        else:
            if self.entity.__entityName__ == 'Route':
                route_id = self.entity.object_id
                if 'key' in self.parameters and 'value' in self.parameters:
                    key = self.parameters.get('key')[0].upper()
                    value = self.parameters.get('value')[0]
                    if key == 'INPUTMESSAGE':
                        self.log.debug(('Attempting to create new process from route {0}').format(route_id))
                        try:
                            process = self.create_process(route=self.entity, data=value)
                            for (key, value) in self.parameters.items():
                                if key.startswith('xattr.'):
                                    prop_name = ('xattr_{0}').format(key[6:].lower())
                                    if len(value) > 0:
                                        prop_value = str(value[0])
                                    else:
                                        prop_value = 'YES'
                                    self.context.property_manager.set_property(process, 'http://www.opengroupware.us/oie', prop_name, prop_value)

                            self.context.commit()
                            self.log.info(('Process {0} created via signal by {1}.').format(process.object_id, self.context.get_login()))
                            message = self.get_input_message(process)
                            self.start_process(process)
                        except Exception, e:
                            self.log.exception(e)
                            raise CoilsException('Failed to create process')

                        w = StringIO()
                        paths = self.get_process_urls(process)
                        w.write(('OK PID:{0} MSG{1} WATCH:{2}').format(process.object_id, message.uuid, paths['output']))
                        self.request.simple_response(200, data=w.getvalue(), mimetype='text/plain', headers={'X-COILS-WORKFLOW-MESSAGE-UUID': message.uuid, 'X-COILS-WORKFLOW-MESSAGE-LABEL': message.label, 
                           'X-COILS-WORKFLOW-PROCESS-ID': process.object_id, 
                           'X-COILS-WORKFLOW-OUTPUT-URL': paths['output']})
                        return
                    raise CoilsException(('Workflow presentation object does not understand signal key {0}').format(key))
                else:
                    raise CoilsException('Workflow signals must contain a key and value parameter.')
                self.request.simple_response(201)
            elif self.entity.__entityName__ == Process:
                self.request.simple_response(201)
            else:
                raise NotImplementedException('This workflow presentation object does not support signals.')
            return