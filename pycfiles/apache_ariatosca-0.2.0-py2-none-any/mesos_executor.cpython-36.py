# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/contrib/executors/mesos_executor.py
# Compiled at: 2019-09-11 03:47:34
# Size of source mod 2**32: 12805 bytes
from future import standard_library
from builtins import str
from queue import Queue
import mesos.interface
from mesos.interface import mesos_pb2
import mesos.native
from airflow import configuration
from airflow.executors.base_executor import BaseExecutor
from airflow.settings import Session
from airflow.utils.state import State
from airflow.exceptions import AirflowException
standard_library.install_aliases()
DEFAULT_FRAMEWORK_NAME = 'Airflow'
FRAMEWORK_CONNID_PREFIX = 'mesos_framework_'

def get_framework_name():
    if not configuration.conf.get('mesos', 'FRAMEWORK_NAME'):
        return DEFAULT_FRAMEWORK_NAME
    else:
        return configuration.conf.get('mesos', 'FRAMEWORK_NAME')


class AirflowMesosScheduler(mesos.interface.Scheduler):
    """AirflowMesosScheduler"""

    def __init__(self, task_queue, result_queue, task_cpu=1, task_mem=256):
        self.task_queue = task_queue
        self.result_queue = result_queue
        self.task_cpu = task_cpu
        self.task_mem = task_mem
        self.task_counter = 0
        self.task_key_map = {}
        if configuration.get('mesos', 'DOCKER_IMAGE_SLAVE'):
            self.mesos_slave_docker_image = configuration.get('mesos', 'DOCKER_IMAGE_SLAVE')

    def registered(self, driver, frameworkId, masterInfo):
        self.log.info('AirflowScheduler registered to Mesos with framework ID %s', frameworkId.value)
        if configuration.conf.getboolean('mesos', 'CHECKPOINT'):
            if configuration.conf.get('mesos', 'FAILOVER_TIMEOUT'):
                from airflow.models import Connection
                session = Session()
                conn_id = FRAMEWORK_CONNID_PREFIX + get_framework_name()
                connection = Session.query(Connection).filter_by(conn_id=conn_id).first()
                if connection is None:
                    connection = Connection(conn_id=conn_id, conn_type='mesos_framework-id', extra=(frameworkId.value))
                else:
                    connection.extra = frameworkId.value
                session.add(connection)
                session.commit()
                Session.remove()

    def reregistered(self, driver, masterInfo):
        self.log.info('AirflowScheduler re-registered to mesos')

    def disconnected(self, driver):
        self.log.info('AirflowScheduler disconnected from mesos')

    def offerRescinded(self, driver, offerId):
        self.log.info('AirflowScheduler offer %s rescinded', str(offerId))

    def frameworkMessage(self, driver, executorId, slaveId, message):
        self.log.info('AirflowScheduler received framework message %s', message)

    def executorLost(self, driver, executorId, slaveId, status):
        self.log.warning('AirflowScheduler executor %s lost', str(executorId))

    def slaveLost(self, driver, slaveId):
        self.log.warning('AirflowScheduler slave %s lost', str(slaveId))

    def error(self, driver, message):
        self.log.error('AirflowScheduler driver aborted %s', message)
        raise AirflowException('AirflowScheduler driver aborted %s' % message)

    def resourceOffers(self, driver, offers):
        for offer in offers:
            tasks = []
            offerCpus = 0
            offerMem = 0
            for resource in offer.resources:
                if resource.name == 'cpus':
                    offerCpus += resource.scalar.value
                else:
                    if resource.name == 'mem':
                        offerMem += resource.scalar.value

            self.log.info('Received offer %s with cpus: %s and mem: %s', offer.id.value, offerCpus, offerMem)
            remainingCpus = offerCpus
            remainingMem = offerMem
            while not self.task_queue.empty() and remainingCpus >= self.task_cpu and remainingMem >= self.task_mem:
                key, cmd = self.task_queue.get()
                tid = self.task_counter
                self.task_counter += 1
                self.task_key_map[str(tid)] = key
                self.log.info('Launching task %d using offer %s', tid, offer.id.value)
                task = mesos_pb2.TaskInfo()
                task.task_id.value = str(tid)
                task.slave_id.value = offer.slave_id.value
                task.name = 'AirflowTask %d' % tid
                cpus = task.resources.add()
                cpus.name = 'cpus'
                cpus.type = mesos_pb2.Value.SCALAR
                cpus.scalar.value = self.task_cpu
                mem = task.resources.add()
                mem.name = 'mem'
                mem.type = mesos_pb2.Value.SCALAR
                mem.scalar.value = self.task_mem
                command = mesos_pb2.CommandInfo()
                command.shell = True
                command.value = ' '.join(cmd)
                task.command.MergeFrom(command)
                if self.mesos_slave_docker_image:
                    network = mesos_pb2.ContainerInfo.DockerInfo.Network.Value('BRIDGE')
                    docker = mesos_pb2.ContainerInfo.DockerInfo(image=(self.mesos_slave_docker_image),
                      force_pull_image=False,
                      network=network)
                    container = mesos_pb2.ContainerInfo(type=(mesos_pb2.ContainerInfo.DOCKER),
                      docker=docker)
                    task.container.MergeFrom(container)
                tasks.append(task)
                remainingCpus -= self.task_cpu
                remainingMem -= self.task_mem

            driver.launchTasks(offer.id, tasks)

    def statusUpdate(self, driver, update):
        self.log.info('Task %s is in state %s, data %s', update.task_id.value, mesos_pb2.TaskState.Name(update.state), str(update.data))
        try:
            key = self.task_key_map[update.task_id.value]
        except KeyError:
            self.log.warning('Unrecognised task key %s', update.task_id.value)
            return
        else:
            if update.state == mesos_pb2.TASK_FINISHED:
                self.result_queue.put((key, State.SUCCESS))
                self.task_queue.task_done()
            if update.state == mesos_pb2.TASK_LOST or update.state == mesos_pb2.TASK_KILLED or update.state == mesos_pb2.TASK_FAILED:
                self.result_queue.put((key, State.FAILED))
                self.task_queue.task_done()


class MesosExecutor(BaseExecutor):
    """MesosExecutor"""

    def start(self):
        self.task_queue = Queue()
        self.result_queue = Queue()
        framework = mesos_pb2.FrameworkInfo()
        framework.user = ''
        if not configuration.conf.get('mesos', 'MASTER'):
            self.log.error('Expecting mesos master URL for mesos executor')
            raise AirflowException('mesos.master not provided for mesos executor')
        else:
            master = configuration.conf.get('mesos', 'MASTER')
            framework.name = get_framework_name()
            if not configuration.conf.get('mesos', 'TASK_CPU'):
                task_cpu = 1
            else:
                task_cpu = configuration.conf.getint('mesos', 'TASK_CPU')
            if not configuration.conf.get('mesos', 'TASK_MEMORY'):
                task_memory = 256
            else:
                task_memory = configuration.conf.getint('mesos', 'TASK_MEMORY')
            if configuration.conf.getboolean('mesos', 'CHECKPOINT'):
                framework.checkpoint = True
                if configuration.conf.get('mesos', 'FAILOVER_TIMEOUT'):
                    from airflow.models import Connection
                    conn_id = FRAMEWORK_CONNID_PREFIX + framework.name
                    session = Session()
                    connection = session.query(Connection).filter_by(conn_id=conn_id).first()
                    if connection is not None:
                        framework.id.value = connection.extra
                    framework.failover_timeout = configuration.conf.getint('mesos', 'FAILOVER_TIMEOUT')
            else:
                framework.checkpoint = False
            self.log.info('MesosFramework master : %s, name : %s, cpu : %s, mem : %s, checkpoint : %s', master, framework.name, str(task_cpu), str(task_memory), str(framework.checkpoint))
            implicit_acknowledgements = 1
            if configuration.conf.getboolean('mesos', 'AUTHENTICATE'):
                if not configuration.conf.get('mesos', 'DEFAULT_PRINCIPAL'):
                    self.log.error('Expecting authentication principal in the environment')
                    raise AirflowException('mesos.default_principal not provided in authenticated mode')
                if not configuration.conf.get('mesos', 'DEFAULT_SECRET'):
                    self.log.error('Expecting authentication secret in the environment')
                    raise AirflowException('mesos.default_secret not provided in authenticated mode')
                credential = mesos_pb2.Credential()
                credential.principal = configuration.conf.get('mesos', 'DEFAULT_PRINCIPAL')
                credential.secret = configuration.conf.get('mesos', 'DEFAULT_SECRET')
                framework.principal = credential.principal
                driver = mesos.native.MesosSchedulerDriver(AirflowMesosScheduler(self.task_queue, self.result_queue, task_cpu, task_memory), framework, master, implicit_acknowledgements, credential)
            else:
                framework.principal = 'Airflow'
            driver = mesos.native.MesosSchedulerDriver(AirflowMesosScheduler(self.task_queue, self.result_queue, task_cpu, task_memory), framework, master, implicit_acknowledgements)
        self.mesos_driver = driver
        self.mesos_driver.start()

    def execute_async(self, key, command, queue=None, executor_config=None):
        self.task_queue.put((key, command))

    def sync(self):
        while not self.result_queue.empty():
            results = self.result_queue.get()
            (self.change_state)(*results)

    def end(self):
        self.task_queue.join()
        self.mesos_driver.stop()