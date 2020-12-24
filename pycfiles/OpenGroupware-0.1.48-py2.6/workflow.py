# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/coils/protocol/dav/workflow/workflow.py
# Compiled at: 2012-10-12 07:02:39


class WorkflowPresentation(object):

    def create_message(self, process=None, data=None, label=None):
        return self.context.run_command('message::new', process=process, label=label, data=data)

    def create_process(self, route=None, data=None, priority=200, mimetype=None):
        if mimetype is None:
            mimetype = 'application/octet-stream'
        return self.context.run_command('process::new', values={'route_id': route.object_id, 'data': data, 
           'priority': priority}, mimetype=mimetype)

    def get_input_message(self, process):
        return self.context.run_command('process::get-input-message', process=process)

    def start_process(self, process):
        self.context.run_command('process::start', process=process)

    def get_process_messages(self, process):
        return self.context.run_command('process::get-messages', pid=process.object_id)

    def get_process_urls(self, process):
        return {'self': ('{0}/{1}/input').format(self.get_path(), process.object_id), 'output': ('{0}/{1}/output').format(self.get_path(), process.object_id)}

    def get_message_handle(self, message):
        return self.context.run_command('message::get-handle', uuid=message.uuid)

    def signal_queue_manager(self):
        self.context.send('coils.http.worker/__null:', 'coils.workflow.queueManager/checkQueue:0', None)
        return