# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/mercury_agent/rpc.py
# Compiled at: 2018-01-10 00:48:14
# Size of source mod 2**32: 5268 bytes
import logging, threading
from mercury_agent.capabilities import runtime_capabilities
from mercury_agent.task_runner import TaskRunner
from mercury.common.transport import SimpleRouterReqService
LOG = logging.getLogger(__name__)

class SerialLock(object):

    def __init__(self):
        self.task_id = None
        self.lock = threading.Lock()

    def acquire(self, task_id):
        self.task_id = task_id
        return self.lock.acquire(False)

    def release(self):
        self.task_id = None
        self.lock.release()


class AgentService(SimpleRouterReqService):
    serial_lock = SerialLock()

    def __init__(self, bind_address, rpc_backend_url):
        self.rpc_backend_url = rpc_backend_url
        super(AgentService, self).__init__(bind_address)

    @staticmethod
    def error(code, data=''):
        return {'message': {'status':code,  'data':data}}

    @staticmethod
    def sync_response(data):
        return {'message': {'status':0,  'data':data}}

    @staticmethod
    def lookup_method(method):
        return runtime_capabilities.get(method)

    def validate_method_args(self, message, capability):
        num_args = capability.get('num_args')
        if num_args:
            if not len(message.get('args', 0)) == num_args:
                return self.error(4, 'arguments for %s are not satisfied' % capability['name'])
        kwarg_names = capability.get('kwarg_names')
        if kwarg_names:
            message_kwargs = message.get('kwargs', {})
            if not isinstance(message_kwargs, dict):
                return self.error(4, 'kwargs is malformed in message')
            missing = []
            for k in kwarg_names:
                if k not in message_kwargs:
                    missing.append(k)

            if missing:
                return self.error(4, 'missing kwargs in message: %s' % ', '.join(missing))

    def process(self, message):
        LOG.debug('Processing request: %s' % message)
        category = message.get('category')
        if not category:
            return self.error(1, 'missing category, nothing to do')
        if category != 'rpc':
            return self.error(3, 'invalid category')
        method = message.get('method')
        if not method:
            return self.error(3, 'method not defined')
        capability = self.lookup_method(method)
        if not capability:
            return self.error(3, '%s method is not supported' % method)
        LOG.debug('Runtime selected: %s' % capability['name'])
        error = self.validate_method_args(message, capability)
        if error:
            return error
        else:
            args = message.get('args', ())
            kwargs = message.get('kwargs', {})
            task_id = message.get('task_id')
            job_id = message.get('job_id')
            if None in [task_id, job_id]:
                return self.error(3, 'message is incomplete, missing task_id/job_id')
            if capability.get('serial'):
                LOG.info('capability %s is serial, attempting to acquire lock' % capability['name'])
                if not self.serial_lock.acquire(task_id):
                    LOG.info('Could not acquire lock, locked by %s' % task_id)
                    return self.error(5, 'Could not acquire lock, task is already running')
                LOG.info('Lock acquired for %s' % task_id)
                tmp_lock = self.serial_lock
            else:
                tmp_lock = None
            task_runner = TaskRunner(job_id, task_id,
              (capability['entry']),
              (self.rpc_backend_url),
              entry_args=args,
              entry_kwargs=kwargs,
              lock=tmp_lock,
              timeout=(capability['timeout']),
              task_id_kwargs=(capability['task_id_kwargs']))
            task_runner.run()
            return self.sync_response(data=dict(time_started=(task_runner.time_started), message='Hakuna matata'))