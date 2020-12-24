# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/snurtle/bundles/process.py
# Compiled at: 2012-09-10 09:51:50
import os, base64
from snurtle.cmd2 import options, make_option
from clibundle import CLIBundle
from StringIO import StringIO as ByteIO
PROCESS_LIST_TEMPLATE = "<%objectid = '{:<12}'.format(report['objectid'])\nroutename = '{:<40}'.format(report['routeName'])\nstate = '{:^10}'.format(report['state'])\nownerid = '{:^12}'.format(report['ownerObjectId'])\n%>${objectid} ${routename} ${state} ${ownerid}"
PS_HEADER = "<%objectid = '{:<12}'.format('PID')\nroutename='{:<40}'.format('Route')\nusername='{:<12}'.format('Context')\nsingleton='{:^9}'.format('Singleton')\n%>${objectid} ${username} ${routename} ${singleton}"
PS_TEMPLATE = '<%objectid = \'{:<12}\'.format(report[\'processId\'])\nroutename=\'{:<40}\'.format(\'{0}/{1}\'.format(report[\'routeGroup\'],report[\'routeName\'],))\nusername=\'{:<12}\'.format(report[\'contextName\'])\nif report[\'singleton\']:\n    singleton="Y"\nelse:\n    singleton="N"\n%>${objectid} ${username} ${routename} S=${singleton} ${report[\'registered\']} ${report[\'updated\']}'

class ProcessCLIBundle(CLIBundle):

    @options([
     make_option('--initialized', action='store_true', help='List Processes in an init state.'),
     make_option('--queued', action='store_true', help='List Processes in a queued state.'),
     make_option('--parked', action='store_true', help='List Processes in a parked state.'),
     make_option('--completed', action='store_true', help='List Processes in a completed state.'),
     make_option('--failed', action='store_true', help='List Processes in a failed state.'),
     make_option('--zombie', action='store_true', help='List Processes in a zombie state.'),
     make_option('--routeid', type='int', help='ObjectId of Route entity')])
    def do_list_processes(self, arg, opts=None):
        """List OIE processes."""
        if not (opts.initialized or opts.queued or opts.parked or opts.completed or opts.failed or opts.zombie):
            print 'setting all options to true'
            opts.initialize = opts.queued = opts.parked = opts.completed = opts.failed = opts.zombie = True
        callid = self.server.search_for_objects(entity='Process', criteria='list', detail=16, callback=self.callback)
        response = self.get_response(callid)
        if response:
            ps = []
            for process in response.payload:
                if opts.routeid:
                    if opts.routeid != process['routeobjectid']:
                        continue
                if opts.initialized and process['state'] == 'initialized':
                    ps.append(process)
                elif opts.queued and process['state'] == 'queued':
                    ps.append(process)
                elif opts.parked and process['state'] == 'parked':
                    ps.append(process)
                elif opts.completed and process['state'] == 'completed':
                    ps.append(process)
                elif opts.failed and process['state'] == 'failed':
                    ps.append(process)
                elif opts.zombie and process['state'] == 'zombie':
                    ps.append(process)

            self.set_result(ps, template=PROCESS_LIST_TEMPLATE)

    @options([make_option('--routeid', type='int', help='ObjectId of Route entity'),
     make_option('--queue', action='store_true', help='Immediately queue for execution'),
     make_option('--inputdata', type='string', help='Process input data'),
     make_option('--inputfile', type='string', help='File to read as input data')])
    def do_create_process(self, arg, opts=None):
        """Create a new OIE Process.
           create-process --routeid=14236550 --queue --inputfile=Repeated301Issue.pcap"""
        if not opts.routeid:
            self.set_result('--routeid parameter is required', error=True)
            return
        else:
            input_stream = ByteIO()
            if opts.inputfile:
                if os.path.isfile(opts.inputfile):
                    file_stream = open(opts.inputfile, 'rb')
                    while True:
                        data = file_stream.read(4096)
                        if data:
                            input_stream.write(data)
                        else:
                            break

                else:
                    self.set_result(('No such file as "{0}".').format(opts.inputfile), error=True)
                    return
            elif opts.inputdata:
                input_stream.write(opts.inputdata)
            else:
                input_stream.write('')
            input_data = base64.encodestring(input_stream.getvalue())
            input_stream.close()
            payload = {'entityName': 'Process', 'routeId': opts.routeid, 
               'data': input_data, 
               'state': 'Q' if opts.queue else 'I'}
            callid = self.server.put_object(payload=payload, callback=self.callback, state=None, feedback=self.pfeedback)
            response = self.get_response(callid)
            if response:
                self.set_result(response)
            return

    @options([make_option('--processid', type='int', help='ObjectId of Process entity')])
    def do_list_messages(self, arg, opts=None):
        if not opts.processid:
            self.set_result('--processid parameter is required', error=True)
            return
        response = self._get_entity(opts.processid, expected_type='Process', detail_level=65535)
        if response:
            response = response.payload['_messages']
            self.set_result(response)

    @options([make_option('--processid', type='int', help='ObjectId of Process entity'),
     make_option('--mimetype', type='string', help='MIME-type of message data'),
     make_option('--inputdata', type='string', help='Message data'),
     make_option('--label', type='string', help='Message label'),
     make_option('--inputfile', type='string', help='File to read as message data')])
    def do_create_message(self, arg, opts=None):
        """create-message --processid=18442450 --inputdata=Repeated301Issue.pcap --label=fred"""
        if not opts.processid:
            self.set_result('--processid parameter is required', error=True)
            return
        else:
            input_stream = ByteIO()
            if opts.inputfile:
                if os.path.isfile(opts.inputfile):
                    file_stream = open(opts.inputfile, 'rb')
                    while True:
                        data = file_stream.read(4096)
                        if data:
                            input_stream.write(data)
                        else:
                            break

                else:
                    self.set_result(('No such file as "{0}".').format(opts.inputfile), error=True)
                    return
            elif opts.inputdata:
                input_stream.write(opts.inputdata)
            else:
                input_stream.write('')
            input_data = base64.encodestring(input_stream.getvalue())
            input_stream.close()
            if not opts.mimetype:
                opts.mimetype = 'application/octet-stream'
            payload = {'entityName': 'message', 'processid': opts.processid, 'mimetype': opts.mimetype, 
               'data': input_data}
            if opts.label:
                payload['label'] = opts.label
            callid = self.server.put_object(payload=payload, callback=self.callback, state=None, feedback=self.pfeedback)
            response = self.get_response(callid)
            if response:
                self.set_result(response)
            return

    @options([
     make_option('--objectid', type='int', help='ObjectId of Process entity to delete.')])
    def do_delete_process(self, arg, opts=None):
        """Delete a process."""
        response = self._get_entity(opts.objectid, expected_type='Process')
        if response:
            callid = self.server.delete_object(objectid=opts.objectid, callback=self.callback)
            response = self.get_response(callid)
            if response:
                self.set_result(response)

    def do_ps(self, arg, opts=None):
        """List currently running processes"""
        callid = self.server.get_process_list(callback=self.callback)
        response = self.get_response(callid)
        if response:
            self.set_result(response, template=PS_TEMPLATE, header=PS_HEADER)