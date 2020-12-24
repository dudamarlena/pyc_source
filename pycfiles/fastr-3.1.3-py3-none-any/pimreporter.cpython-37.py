# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/hachterberg/dev/fastr/fastr/fastr/resources/plugins/reportingplugins/pimreporter.py
# Compiled at: 2019-06-18 14:37:15
# Size of source mod 2**32: 21923 bytes
from abc import ABCMeta, abstractmethod
from collections import deque
import datetime, getpass, itertools, json
from logging import LogRecord
import os, time
from typing import Dict
from threading import Lock, Thread
import requests, fastr
import fastr.helpers.classproperty as classproperty
from fastr.plugins.reportingplugin import ReportingPlugin
from fastr.execution.job import JobState, Job
from fastr.execution.networkrun import NetworkRun

class BasePimAPI(metaclass=ABCMeta):
    __doc__ = '\n    Base class for PIM API classes which specifies the methods required to function\n    '

    @abstractmethod
    def pim_update_status(self, job: Job):
        """
        Update the status of a job

        :param job: The job which to update
        """
        pass

    @abstractmethod
    def pim_register_run(self, network: NetworkRun):
        """
        Send the basic Network layout to PIM and register the run.

        :param network: The network run to register to PIM
        """
        pass

    @abstractmethod
    def pim_finish_run(self, network: NetworkRun):
        """
        Set the PIM run to finished and clean up

        :param network: The network run to finish
        """
        pass

    @abstractmethod
    def pim_log_line(self, record: LogRecord):
        """
        Send a new line of log record to PIM
        :param record: the log record to send
        """
        pass


class PimAPIv2(object):
    __doc__ = '\n    Class to publish to PIM\n    '
    PIM_STATUS_MAPPING = {JobState.nonexistent: 5, 
     JobState.created: 0, 
     JobState.queued: 0, 
     JobState.hold: 0, 
     JobState.running: 1, 
     JobState.execution_done: 1, 
     JobState.execution_failed: 1, 
     JobState.processing_callback: 1, 
     JobState.finished: 2, 
     JobState.failed: 3, 
     JobState.cancelled: 4}
    NODE_CLASSES = {'NodeRun':'node', 
     'SourceNodeRun':'source', 
     'ConstantNodeRun':'constant', 
     'SinkNodeRun':'sink'}
    STATUS_TYPES = [
     {'color':'#aaccff', 
      'description':'Jobs that are waiting for input', 
      'title':'idle'},
     {'color':'#daa520', 
      'description':'Jobs that are running', 
      'title':'running'},
     {'color':'#23b22f', 
      'description':'Jobs that finished successfully', 
      'title':'success'},
     {'color':'#dd3311', 
      'description':'Jobs that have failed', 
      'title':'failed'},
     {'color':'#334477', 
      'description':'Jobs which were cancelled', 
      'title':'cancelled'},
     {'color':'#ccaa99', 
      'description':'Jobs with an undefined state', 
      'title':'undefined'}]

    def __init__(self, uri=None):
        self.pim_uri = uri
        self.registered = False
        self.run_id = None
        self.jobs_uri = None
        self.running = True
        self.submit_thread = Thread(target=(self.job_update_loop), name='PimSubmitter', daemon=True)
        self.update_interval = fastr.config.pim_update_interval
        self.batch_size = fastr.config.pim_batch_size
        self.finished_timeout = fastr.config.pim_finished_timeout
        self.queued_job_updates = deque()
        self.submitted_job_updates = []
        self.updates_lock = Lock()
        self.counter = itertools.count()
        self.scopes = {None: 'root'}
        self.nodes = {}
        self.job_states = {}

    def create_job_data(self, job: Job) -> Dict:
        """
        Create a job data json part that is ready to send to PIM

        :param job: the job to convert
        :return:
        """
        try:
            node = self.nodes[job.node_global_id]
        except KeyError:
            fastr.log.info('NODES: {}'.format(self.nodes))
            raise

        pim_job_data = {'path':'{}/{}'.format(node, job.id), 
         'title':'', 
         'customData':{'sample_id':list(job.sample_id), 
          'sample_index':list(job.sample_index), 
          'errors':job.errors}, 
         'status':self.PIM_STATUS_MAPPING[job.status], 
         'description':''}
        fastr.log.debug('Updating PIM job status {} => {} ({})'.format(job.id, job.status, self.PIM_STATUS_MAPPING[job.status]))
        if job.status == JobState.failed or fastr.config.pim_debug:
            if os.path.exists(job.extrainfofile):
                with open(job.extrainfofile) as (extra_info_file):
                    extra_info = json.load(extra_info_file)
                    process = extra_info.get('process')
                    if process:
                        pim_job_data['customData']['__stdout__'] = process.get('stdout')
                        pim_job_data['customData']['__stderr__'] = process.get('stderr')
                        pim_job_data['customData']['command'] = process.get('command')
                        pim_job_data['customData']['returncode'] = process.get('returncode')
                        pim_job_data['customData']['time_elapsed'] = process.get('time_elapsed')
                    pim_job_data['customData']['hostinfo'] = extra_info.get('hostinfo')
                    pim_job_data['customData']['input_hash'] = extra_info.get('input_hash')
                    pim_job_data['customData']['output_hash'] = extra_info.get('output_hash')
                    pim_job_data['customData']['tool_name'] = extra_info.get('tool_name')
                    pim_job_data['customData']['tool_version'] = extra_info.get('tool_version')
        return pim_job_data

    def pim_update_status(self, job):
        if self.pim_uri is None:
            return
        else:
            if not self.registered:
                fastr.log.debug('Did not register a RUN with PIM yet! Cannot send status updates!')
                return
            if job.status not in [
             JobState.created,
             JobState.running,
             JobState.finished,
             JobState.cancelled,
             JobState.failed]:
                return
            if job.id in self.job_states and self.job_states[job.id] == self.PIM_STATUS_MAPPING[job.status]:
                fastr.log.debug('Ignoring non-PIM update')
                return
        self.job_states[job.id] = self.PIM_STATUS_MAPPING[job.status]
        with self.updates_lock:
            self.queued_job_updates.append(self.create_job_data(job))

    def job_update_loop--- This code section failed: ---

 L. 246       0_2  SETUP_LOOP          350  'to 350'
                4  LOAD_FAST                'self'
                6  LOAD_ATTR                running
                8  POP_JUMP_IF_TRUE     40  'to 40'
               10  LOAD_GLOBAL              len
               12  LOAD_FAST                'self'
               14  LOAD_ATTR                submitted_job_updates
               16  CALL_FUNCTION_1       1  '1 positional argument'
               18  LOAD_CONST               0
               20  COMPARE_OP               !=
               22  POP_JUMP_IF_TRUE     40  'to 40'
               24  LOAD_GLOBAL              len
               26  LOAD_FAST                'self'
               28  LOAD_ATTR                queued_job_updates
               30  CALL_FUNCTION_1       1  '1 positional argument'
               32  LOAD_CONST               0
               34  COMPARE_OP               !=
            36_38  POP_JUMP_IF_FALSE   348  'to 348'
             40_0  COME_FROM            22  '22'
             40_1  COME_FROM             8  '8'

 L. 248        40  LOAD_GLOBAL              time
               42  LOAD_METHOD              time
               44  CALL_METHOD_0         0  '0 positional arguments'
               46  STORE_FAST               'last_update'

 L. 251        48  LOAD_FAST                'self'
               50  LOAD_ATTR                updates_lock
               52  SETUP_WITH          124  'to 124'
               54  POP_TOP          

 L. 253        56  LOAD_GLOBAL              min
               58  LOAD_FAST                'self'
               60  LOAD_ATTR                batch_size
               62  LOAD_GLOBAL              len
               64  LOAD_FAST                'self'
               66  LOAD_ATTR                submitted_job_updates
               68  CALL_FUNCTION_1       1  '1 positional argument'
               70  BINARY_SUBTRACT  

 L. 254        72  LOAD_GLOBAL              len
               74  LOAD_FAST                'self'
               76  LOAD_ATTR                queued_job_updates
               78  CALL_FUNCTION_1       1  '1 positional argument'
               80  CALL_FUNCTION_2       2  '2 positional arguments'
               82  STORE_FAST               'number_of_jobs'

 L. 257        84  SETUP_LOOP          120  'to 120'
               86  LOAD_GLOBAL              range
               88  LOAD_FAST                'number_of_jobs'
               90  CALL_FUNCTION_1       1  '1 positional argument'
               92  GET_ITER         
               94  FOR_ITER            118  'to 118'
               96  STORE_FAST               '_'

 L. 258        98  LOAD_FAST                'self'
              100  LOAD_ATTR                submitted_job_updates
              102  LOAD_METHOD              append

 L. 259       104  LOAD_FAST                'self'
              106  LOAD_ATTR                queued_job_updates
              108  LOAD_METHOD              popleft
              110  CALL_METHOD_0         0  '0 positional arguments'
              112  CALL_METHOD_1         1  '1 positional argument'
              114  POP_TOP          
              116  JUMP_BACK            94  'to 94'
              118  POP_BLOCK        
            120_0  COME_FROM_LOOP       84  '84'
              120  POP_BLOCK        
              122  LOAD_CONST               None
            124_0  COME_FROM_WITH       52  '52'
              124  WITH_CLEANUP_START
              126  WITH_CLEANUP_FINISH
              128  END_FINALLY      

 L. 263       130  LOAD_GLOBAL              len
              132  LOAD_FAST                'self'
              134  LOAD_ATTR                submitted_job_updates
              136  CALL_FUNCTION_1       1  '1 positional argument'
              138  LOAD_CONST               0
              140  COMPARE_OP               >
          142_144  POP_JUMP_IF_FALSE   300  'to 300'

 L. 264       146  SETUP_EXCEPT        172  'to 172'

 L. 265       148  LOAD_GLOBAL              requests
              150  LOAD_ATTR                put
              152  LOAD_FAST                'self'
              154  LOAD_ATTR                jobs_uri
              156  LOAD_FAST                'self'
              158  LOAD_ATTR                submitted_job_updates
              160  LOAD_CONST               5
              162  LOAD_CONST               ('json', 'timeout')
              164  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'
              166  STORE_FAST               'response'
              168  POP_BLOCK        
              170  JUMP_FORWARD        260  'to 260'
            172_0  COME_FROM_EXCEPT    146  '146'

 L. 266       172  DUP_TOP          
              174  LOAD_GLOBAL              requests
              176  LOAD_ATTR                ConnectionError
              178  COMPARE_OP               exception-match
              180  POP_JUMP_IF_FALSE   224  'to 224'
              182  POP_TOP          
              184  STORE_FAST               'exception'
              186  POP_TOP          
              188  SETUP_FINALLY       212  'to 212'

 L. 267       190  LOAD_GLOBAL              fastr
              192  LOAD_ATTR                log
              194  LOAD_METHOD              warning
              196  LOAD_STR                 'Could no publish status to PIM, encountered exception: {}'
              198  LOAD_METHOD              format
              200  LOAD_FAST                'exception'
              202  CALL_METHOD_1         1  '1 positional argument'
              204  CALL_METHOD_1         1  '1 positional argument'
              206  POP_TOP          
              208  POP_BLOCK        
              210  LOAD_CONST               None
            212_0  COME_FROM_FINALLY   188  '188'
              212  LOAD_CONST               None
              214  STORE_FAST               'exception'
              216  DELETE_FAST              'exception'
              218  END_FINALLY      
              220  POP_EXCEPT       
              222  JUMP_FORWARD        300  'to 300'
            224_0  COME_FROM           180  '180'

 L. 268       224  DUP_TOP          
              226  LOAD_GLOBAL              requests
              228  LOAD_ATTR                Timeout
              230  COMPARE_OP               exception-match
          232_234  POP_JUMP_IF_FALSE   258  'to 258'
              236  POP_TOP          
              238  POP_TOP          
              240  POP_TOP          

 L. 269       242  LOAD_GLOBAL              fastr
              244  LOAD_ATTR                log
              246  LOAD_METHOD              warning
              248  LOAD_STR                 'Connection to PIM timed out during job update submission'
              250  CALL_METHOD_1         1  '1 positional argument'
              252  POP_TOP          
              254  POP_EXCEPT       
              256  JUMP_FORWARD        300  'to 300'
            258_0  COME_FROM           232  '232'
              258  END_FINALLY      
            260_0  COME_FROM           170  '170'

 L. 271       260  LOAD_FAST                'response'
              262  LOAD_ATTR                status_code
              264  LOAD_CONST               300
              266  COMPARE_OP               >=
          268_270  POP_JUMP_IF_FALSE   294  'to 294'

 L. 272       272  LOAD_GLOBAL              fastr
              274  LOAD_ATTR                log
              276  LOAD_METHOD              warning
              278  LOAD_STR                 'Response of jobs update: [{r.status_code}] {r.text}'
              280  LOAD_ATTR                format
              282  LOAD_FAST                'response'
              284  LOAD_CONST               ('r',)
              286  CALL_FUNCTION_KW_1     1  '1 total positional and keyword args'
              288  CALL_METHOD_1         1  '1 positional argument'
              290  POP_TOP          
              292  JUMP_FORWARD        300  'to 300'
            294_0  COME_FROM           268  '268'

 L. 275       294  BUILD_LIST_0          0 
              296  LOAD_FAST                'self'
              298  STORE_ATTR               submitted_job_updates
            300_0  COME_FROM           292  '292'
            300_1  COME_FROM           256  '256'
            300_2  COME_FROM           222  '222'
            300_3  COME_FROM           142  '142'

 L. 278       300  LOAD_FAST                'last_update'
              302  LOAD_FAST                'self'
              304  LOAD_ATTR                update_interval
              306  BINARY_ADD       
              308  LOAD_GLOBAL              time
              310  LOAD_METHOD              time
              312  CALL_METHOD_0         0  '0 positional arguments'
              314  BINARY_SUBTRACT  
              316  STORE_FAST               'time_to_sleep'

 L. 279       318  LOAD_FAST                'time_to_sleep'
              320  LOAD_CONST               0
              322  COMPARE_OP               >
          324_326  POP_JUMP_IF_FALSE   332  'to 332'
              328  LOAD_FAST                'time_to_sleep'
              330  JUMP_FORWARD        334  'to 334'
            332_0  COME_FROM           324  '324'
              332  LOAD_CONST               0
            334_0  COME_FROM           330  '330'
              334  STORE_FAST               'time_to_sleep'

 L. 280       336  LOAD_GLOBAL              time
              338  LOAD_METHOD              sleep
              340  LOAD_FAST                'time_to_sleep'
              342  CALL_METHOD_1         1  '1 positional argument'
              344  POP_TOP          
              346  JUMP_BACK             4  'to 4'
            348_0  COME_FROM            36  '36'
              348  POP_BLOCK        
            350_0  COME_FROM_LOOP        0  '0'

Parse error at or near `POP_BLOCK' instruction at offset 348

    def pim_serialize_node(self, node, scope, links):
        if type(node).__name__ == 'MacroNodeRun':
            return self.pim_serialize_macro(node, scope, links)
        node_data = {'name':node.id, 
         'title':node.id, 
         'children':[],  'customData':{},  'inPorts':[{'name':output.id,  'title':output.id,  'customData':{'input_group':output.input_group,  'datatype':output.datatype.id,  'dimension_names':[x.name for x in output.dimensions]}} for output in node.inputs.values()], 
         'outPorts':[{'name':output.id,  'title':output.id,  'customData':{'datatype':output.resulting_datatype.id,  'dimension_names':[x.name for x in output.dimensions]}} for output in node.outputs.values()], 
         'type':type(node).__name__}
        if type(node).__name__ == 'SourceNodeRun':
            node_data['inPorts'].append({'name':'input', 
             'title':'input', 
             'customData':{'datatype':node.output.datatype.id, 
              'dimension_names':[
               node.id]}})
        if type(node).__name__ == 'SinkNodeRun':
            node_data['outPorts'].append({'name':'output', 
             'title':'output', 
             'customData':{'datatype':node.input.datatype.id, 
              'dimension_names':node.dimnames}})
        self.nodes[node.global_id] = '{}/{}'.format(scope, node.id)
        return node_data

    def pim_serialize_macro(self, node, scope, links):
        new_scope = '{}/{}'.format(scope, node.id)
        self.nodes[node.global_id] = new_scope
        node_data = {'name':node.id, 
         'title':node.id, 
         'children':[],  'customData':{},  'inPorts':[],  'outPorts':[],  'type':type(node).__name__}
        self.pim_serialize_network(node.network_run, new_scope, node_data, links)
        return node_data

    def pim_serialize_network(self, network, scope, parent, links):
        visited_nodes = set()
        for step_name, step_nodes in network.stepids.items():
            step_data = {'name':step_name, 
             'title':step_name, 
             'children':[],  'customData':{},  'inPorts':[],  'outPorts':[],  'type':'NetworkStep'}
            parent['children'].append(step_data)
            for node in step_nodes:
                step_data['children'].append(self.pim_serialize_node(node, '{}/{}'.format(scope, step_name), links))
                visited_nodes.add(node.id)

        for node in network.nodelist.values():
            if node.id not in visited_nodes:
                parent['children'].append(self.pim_serialize_node(node, scope, links))

        for link in network.linklist.values():
            links.append(self.pim_serialize_link(link))

    def pim_serialize_link(self, link):
        if type(link.source.node).__name__ == 'MacroNodeRun':
            from_port = '{}/{}/output'.format(self.nodes[link.source.node.global_id], link.source.id)
        else:
            from_port = '{}/{}'.format(self.nodes[link.source.node.global_id], link.source.id)
        if type(link.target.node).__name__ == 'MacroNodeRun':
            to_port = '{}/{}/input'.format(self.nodes[link.target.node.global_id], link.target.id)
        else:
            to_port = '{}/{}'.format(self.nodes[link.target.node.global_id], link.target.id)
        link_data = {'customData':{'expand':link.expand, 
          'collapse':link.collapse}, 
         'description':'', 
         'fromPort':from_port, 
         'name':link.id, 
         'title':link.id, 
         'toPort':to_port, 
         'dataType':link.source.resulting_datatype.id}
        return link_data

    def pim_register_run(self, network):
        if self.pim_uri is None:
            fastr.log.warning('No valid PIM uri known. Cannot register to PIM!')
            return
        self.run_id = network.id
        pim_run_data = {'title':self.run_id, 
         'name':self.run_id, 
         'assignedTo':[],  'user':fastr.config.pim_username, 
         'root':{'name':'root', 
          'title':network.network_id, 
          'description':'', 
          'children':[],  'customData':{},  'inPorts':[],  'outPorts':[],  'type':'NetworkRun'}, 
         'links':[],  'description':'Run of {} started at {}'.format(network.id, network.timestamp), 
         'customData':{'workflow_engine':'fastr', 
          'tmpdir':network.tmpdir}, 
         'statusTypes':self.STATUS_TYPES}
        self.pim_serialize_network(network=network, scope='root',
          parent=(pim_run_data['root']),
          links=(pim_run_data['links']))
        uri = '{pim}/api/runs/'.format(pim=(fastr.config.pim_host))
        fastr.log.info('Registering {} with PIM at {}'.format(self.run_id, uri))
        fastr.log.debug('Send PUT to pim at {}:\n{}'.format(uri, json.dumps(pim_run_data, indent=2)))
        self.jobs_uri = '{pim}/api/runs/{run_id}/jobs'.format(pim=(fastr.config.pim_host), run_id=(self.run_id))
        try:
            response = requests.post(uri, json=pim_run_data)
            if response.status_code in (200, 201):
                self.registered = True
                self.submit_thread.start()
                fastr.log.info('Run registered in PIM at {}/runs/{}'.format(fastr.config.pim_host, self.run_id))
            else:
                fastr.log.warning('Could not register run at PIM, got a {} response'.format(response.status_code))
                fastr.log.warning('Response: {}'.format(response.text))
        except requests.ConnectionError as exception:
            try:
                fastr.log.error('Could no register network to PIM, encountered exception: {}'.format(exception))
            finally:
                exception = None
                del exception

        root_job_data = {'path':'root/master', 
         'title':'', 
         'customData':{},  'status':self.PIM_STATUS_MAPPING[JobState.running], 
         'description':''}
        self.queued_job_updates.append(root_job_data)

    def pim_finish_run(self, run):
        root_job_data = {'path':'root/master', 
         'title':'', 
         'customData':{},  'status':self.PIM_STATUS_MAPPING[JobState.finished if run.result else JobState.failed], 
         'description':''}
        self.queued_job_updates.append(root_job_data)
        self.running = False
        run_finished = datetime.datetime.now()
        while len(self.queued_job_updates) != 0 or len(self.submitted_job_updates) != 0:
            timer = datetime.datetime.now() - run_finished
            if timer.seconds > self.finished_timeout:
                fastr.log.warning('Not all PIM updates sent, timeout reached!')
                break
            time.sleep(self.update_interval)
            fastr.log.info('Waiting for all jobs to be published to PIM...')

    def pim_log_line(self, record: LogRecord):
        timestamp = datetime.datetime.utcfromtimestamp(record.created).strftime('%Y-%m-%d %H:%M:%S.%f')
        root_job_data = {'path':'root/master', 
         'customData':{'__log__': {timestamp: {'process_name':record.processName, 
                                  'thread_name':record.threadName, 
                                  'level_name':record.levelname, 
                                  'module':record.module, 
                                  'function':record.funcName, 
                                  'lineno':record.lineno, 
                                  'message':record.msg}}}}
        self.queued_job_updates.append(root_job_data)


class PimReporter(ReportingPlugin):
    SUPPORTED_APIS = {2: PimAPIv2}

    def __init__(self):
        self.pim_uri = None
        super().__init__()
        self.api = None

    def activate(self):
        super().activate()
        if fastr.config.pim_host == '':
            fastr.log.info('No valid PIM host given, PIM publishing will be disabled!')
            self.pim_uri = None
            self.api = None
            return
        self.pim_uri = fastr.config.pim_host
        try:
            response = requests.get('{pim}/api/info'.format(pim=(self.pim_uri)))
            if response.status_code >= 300:
                version = 1
            else:
                version = response.json().get('version', 1)
        except requests.ConnectionError as exception:
            try:
                fastr.log.error('Could no publish status to PIM, encountered exception: {}'.format(exception))
                return
            finally:
                exception = None
                del exception

        try:
            api_class = self.SUPPORTED_APIS[version]
            fastr.log.info('Using PIM API version {}'.format(version))
        except KeyError:
            fastr.log.error('PIM API version {} not supported!'.format(version))
            return
        else:
            self.api = api_class(self.pim_uri)

    @classproperty
    def configuration_fields(cls):
        return {'pim_host':(
          str, '', 'The PIM host to report to'), 
         'pim_username':(
          str, getpass.getuser(), 'Username to send to PIM',
          'Username of the currently logged in user'), 
         'pim_update_interval':(
          float, 2.5, 'The interval in which to send jobs to PIM'), 
         'pim_batch_size':(
          int, 100, 'Maximum number of jobs that can be send to PIM in a single interval'), 
         'pim_debug':(
          bool, False, 'Setup PIM debug mode to send stdout stderr on job success'), 
         'pim_finished_timeout':(
          int, 10, 'Maximum number of seconds after the network finished in which PIM tries to synchronize all remaining jobs')}

    def job_updated(self, job: Job):
        if self.pim_uri:
            if self.api:
                self.api.pim_update_status(job)

    def run_started(self, run: NetworkRun):
        if self.pim_uri:
            if self.api:
                self.api.pim_register_run(run)

    def run_finished(self, run: NetworkRun):
        if self.pim_uri:
            if self.api:
                self.api.pim_finish_run(run)

    def log_record_emitted(self, record: LogRecord):
        if self.pim_uri:
            if self.api:
                if self.api.running:
                    self.api.pim_log_line(record)