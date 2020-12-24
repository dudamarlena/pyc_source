# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/coils/protocol/dav/workflow/labelfolder.py
# Compiled at: 2012-10-12 07:02:39
from coils.core import *
from coils.net import *
from messagefolder import MessageFolder

class LabelFolder(MessageFolder):

    def __init__(self, parent, name, **params):
        MessageFolder.__init__(self, parent, name, **params)

    @property
    def label_type(self):
        return 'label'

    def supports_PUT(self):
        return True

    def _load_contents(self):
        self.data = {}
        self.log.debug(('Loading labeled messages of process {0}.').format(self.process_id))
        messages = self.context.run_command('process::get-messages', pid=self.process_id)
        for message in messages:
            if message.label != message.uuid:
                if message.scope is None:
                    self.insert_child(message.label, message)
                else:
                    self.insert_child(('{0}.{1}').format(message.label, message.scope), message)

        return True

    def do_PUT(self, request_name):
        if self.entity.state in ('C', 'F'):
            raise AccessForbiddenException('Cannot create message in completed or failed process.')
        self.log.debug(('Requested label is {0}.').format(request_name))
        payload = self.request.get_request_payload()
        self.log.debug(('Attempting to create new labeled message in process {0}').format(self.process_id))
        try:
            message = self.create_message(process=self.entity, label=request_name, data=payload)
            self.context.commit()
            self.log.info(('Message {0} created via DAV PUT by {1}.').format(message.uuid, self.context.get_login()))
            self.context.run_command('process::start', process=self.entity)
        except Exception, e:
            self.log.exception(e)
            raise CoilsException('Failed to create labeled message')

        my_path = ('/dav/Routes/{0}/{1}/Messages/{2}').format(self.entity.route.name, self.process_id, message.uuid[1:-1])
        self.request.simple_response(201, mimetype='text/plain', headers={'Content-Length': str(message.size), 'Location': my_path})