# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/toil/batchSystems/mesos/executor.py
# Compiled at: 2020-04-03 17:41:24
# Size of source mod 2**32: 12706 bytes
from __future__ import absolute_import
from future import standard_library
standard_library.install_aliases()
from builtins import str
import os, os.path, random, socket, signal, sys, threading, logging, psutil, traceback, time, json, resource, subprocess
try:
    from urllib2 import urlopen
except ImportError:
    from urllib.request import urlopen

import addict
from pymesos import MesosExecutorDriver, Executor, decode_data, encode_data
from toil import pickle
from toil.lib.expando import Expando
from toil.lib.threading import cpu_count
from toil.batchSystems.abstractBatchSystem import BatchSystemSupport
from toil.resource import Resource
log = logging.getLogger(__name__)

class MesosExecutor(Executor):
    __doc__ = "\n    Part of Toil's Mesos framework, runs on a Mesos agent. A Toil job is passed to it via the\n    task.data field, and launched via call(toil.command).\n    "

    def __init__(self):
        super(MesosExecutor, self).__init__()
        self.popenLock = threading.Lock()
        self.runningTasks = {}
        self.workerCleanupInfo = None
        log.debug('Preparing system for resource download')
        Resource.prepareSystem()
        self.address = None
        self.id = None
        if not os.getenv('TOIL_WORKDIR'):
            os.environ['TOIL_WORKDIR'] = os.getcwd()

    def registered(self, driver, executorInfo, frameworkInfo, agentInfo):
        """
        Invoked once the executor driver has been able to successfully connect with Mesos.
        """
        self.id = executorInfo.executor_id.get('value', None)
        log.debug('Registered executor %s with framework', self.id)
        self.address = socket.gethostbyname(agentInfo.hostname)
        nodeInfoThread = threading.Thread(target=(self._sendFrameworkMessage), args=[driver], daemon=True)
        nodeInfoThread.start()

    def reregistered(self, driver, agentInfo):
        """
        Invoked when the executor re-registers with a restarted agent.
        """
        log.debug('Re-registered')

    def disconnected(self, driver):
        """
        Invoked when the executor becomes "disconnected" from the agent (e.g., the agent is being
        restarted due to an upgrade).
        """
        log.critical('Disconnected from agent')

    def killTask(self, driver, taskId):
        """
        Kill parent task process and all its spawned children
        """
        try:
            pid = self.runningTasks[taskId.value]
            pgid = os.getpgid(pid)
        except KeyError:
            pass
        else:
            os.killpg(pgid, signal.SIGKILL)

    def shutdown(self, driver):
        log.critical('Shutting down executor ...')
        for taskId in list(self.runningTasks.keys()):
            self.killTask(driver, taskId)

        Resource.cleanSystem()
        BatchSystemSupport.workerCleanup(self.workerCleanupInfo)
        log.critical('... executor shut down.')

    def error(self, driver, message):
        """
        Invoked when a fatal error has occurred with the executor and/or executor driver.
        """
        log.critical('FATAL ERROR: ' + message)

    def _sendFrameworkMessage(self, driver):
        message = None
        while True:
            if message is None:
                message = Expando(address=(self.address))
                psutil.cpu_percent()
            else:
                message.nodeInfo = dict(coresUsed=(float(psutil.cpu_percent()) * 0.01), memoryUsed=(float(psutil.virtual_memory().percent) * 0.01),
                  coresTotal=(cpu_count()),
                  memoryTotal=(psutil.virtual_memory().total),
                  workers=(len(self.runningTasks)))
            log.debug('Send framework message: %s', message)
            driver.sendFrameworkMessage(encode_data(repr(message).encode('utf-8')))
            time.sleep(random.randint(45, 75))

    def launchTask(self, driver, task):
        """
        Invoked by SchedulerDriver when a Mesos task should be launched by this executor
        """
        log.debug('Asked to launch task %s', repr(task))

        def runTask():
            log.debug('Running task %s', task.task_id.value)
            startTime = time.time()
            sendUpdate(task, 'TASK_RUNNING', wallTime=0)
            try:
                taskData = pickle.loads(decode_data(task.data))
            except:
                exc_info = sys.exc_info()
                log.error('Exception while unpickling task: ', exc_info=exc_info)
                exc_type, exc_value, exc_trace = exc_info
                sendUpdate(task, 'TASK_FAILED', wallTime=0, msg=(''.join(traceback.format_exception_only(exc_type, exc_value))))
                return
            else:
                if self.workerCleanupInfo is not None:
                    assert self.workerCleanupInfo == taskData.workerCleanupInfo
                else:
                    self.workerCleanupInfo = taskData.workerCleanupInfo
                try:
                    process = runJob(taskData)
                    self.runningTasks[task.task_id.value] = process.pid
                    try:
                        exitStatus = process.wait()
                        wallTime = time.time() - startTime
                        if 0 == exitStatus:
                            sendUpdate(task, 'TASK_FINISHED', wallTime)
                        else:
                            if -9 == exitStatus:
                                sendUpdate(task, 'TASK_KILLED', wallTime)
                            else:
                                sendUpdate(task, 'TASK_FAILED', wallTime, msg=(str(exitStatus)))
                    finally:
                        del self.runningTasks[task.task_id.value]

                except:
                    wallTime = time.time() - startTime
                    exc_info = sys.exc_info()
                    log.error('Exception while running task:', exc_info=exc_info)
                    exc_type, exc_value, exc_trace = exc_info
                    sendUpdate(task, 'TASK_FAILED', wallTime=wallTime, msg=(''.join(traceback.format_exception_only(exc_type, exc_value))))

                wallTime = time.time() - startTime
                sendUpdate(task, 'TASK_FINISHED', wallTime)

        def runJob(job):
            if job.userScript:
                job.userScript.register()
            log.debug("Invoking command: '%s'", job.command)
            jobEnv = dict((os.environ), **job.environment)
            log.debug('Using environment variables: %s', jobEnv.keys())
            with self.popenLock:
                return subprocess.Popen((job.command), preexec_fn=(lambda : os.setpgrp()),
                  shell=True,
                  env=jobEnv)

        def sendUpdate(task, taskState, wallTime, msg=''):
            update = addict.Dict()
            update.task_id.value = task.task_id.value
            if self.id is not None:
                update.executor_id.value = self.id
            update.state = taskState
            update.message = msg
            labels = addict.Dict()
            labels.labels = [{'key':'wallTime',  'value':str(wallTime)}]
            update.labels = labels
            driver.sendStatusUpdate(update)

        thread = threading.Thread(target=runTask, daemon=True)
        thread.start()

    def frameworkMessage(self, driver, message):
        """
        Invoked when a framework message has arrived for this executor.
        """
        log.debug('Received message from framework: {}'.format(message))


def main():
    logging.basicConfig(level=(logging.DEBUG))
    log.debug('Starting executor')
    if not os.environ.get('MESOS_AGENT_ENDPOINT'):
        os.environ['MESOS_AGENT_ENDPOINT'] = os.environ.get('MESOS_SLAVE_ENDPOINT', '127.0.0.1:5051')
        log.warning('Had to fake MESOS_AGENT_ENDPOINT as %s' % os.environ['MESOS_AGENT_ENDPOINT'])
    agent_state = json.loads(urlopen('http://%s/state' % os.environ['MESOS_AGENT_ENDPOINT']).read())
    if 'completed_frameworks' in agent_state:
        del agent_state['completed_frameworks']
    else:
        log.debug('Agent state: %s', str(agent_state))
        log.debug('Virtual memory info in executor: %s' % repr(psutil.virtual_memory()))
        if os.path.exists('/sys/fs/cgroup/memory'):
            for dirpath, dirnames, filenames in os.walk('/sys/fs/cgroup/memory', followlinks=True):
                for filename in filenames:
                    if 'limit_in_bytes' not in filename:
                        pass
                    else:
                        log.debug('cgroup memory info from %s:' % os.path.join(dirpath, filename))
                        try:
                            for line in open(os.path.join(dirpath, filename)):
                                log.debug(line.rstrip())

                        except Exception as e:
                            log.debug('Failed to read file')

        log.debug('DATA rlimit: %s', str(resource.getrlimit(resource.RLIMIT_DATA)))
        log.debug('STACK rlimit: %s', str(resource.getrlimit(resource.RLIMIT_STACK)))
        log.debug('RSS rlimit: %s', str(resource.getrlimit(resource.RLIMIT_RSS)))
        log.debug('AS rlimit: %s', str(resource.getrlimit(resource.RLIMIT_AS)))
        executor = MesosExecutor()
        log.debug('Made executor')
        driver = MesosExecutorDriver(executor, use_addict=True)
        old_on_event = driver.on_event

        def patched_on_event(event):
            log.debug('Event: %s', repr(event))
            old_on_event(event)

        driver.on_event = patched_on_event
        log.debug('Made driver')
        driver.start()
        log.debug('Started driver')
        driver_result = driver.join()
        log.debug('Joined driver')
        exit_value = 0 if driver_result is None or driver_result == 'DRIVER_STOPPED' else 1
        assert len(executor.runningTasks) == 0
    sys.exit(exit_value)