# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/vsm/openstack/common/periodic_task.py
# Compiled at: 2016-06-13 14:11:03
import datetime, time, random
from oslo.config import cfg
from vsm import flags
from vsm.openstack.common.gettextutils import _
from vsm.openstack.common import log as logging
from vsm.openstack.common import timeutils
from vsm import db
from vsm import utils
FLAGS = flags.FLAGS
periodic_opts = [
 cfg.BoolOpt('run_external_periodic_tasks', default=True, help='Some periodic tasks can be run in a separate process. Should we run them here?')]
CONF = cfg.CONF
CONF.register_opts(periodic_opts)
LOG = logging.getLogger(__name__)
DEFAULT_INTERVAL = 60.0

class InvalidPeriodicTaskArg(Exception):
    message = _('Unexpected argument for periodic task creation: %(arg)s.')


def periodic_task(*args, **kwargs):
    """Decorator to indicate that a method is a periodic task.

    This decorator can be used in two ways:

        1. Without arguments '@periodic_task', this will be run on every cycle
           of the periodic scheduler.

        2. With arguments:
           @periodic_task(spacing=N [, run_immediately=[True|False]])
           this will be run on approximately every N seconds. If this number is
           negative the periodic task will be disabled. If the run_immediately
           argument is provided and has a value of 'True', the first run of the
           task will be shortly after task scheduler starts.  If
           run_immediately is omitted or set to 'False', the first time the
           task runs will be approximately N seconds after the task scheduler
           starts.
    """

    def decorator(f):
        if 'ticks_between_runs' in kwargs:
            raise InvalidPeriodicTaskArg(arg='ticks_between_runs')
        f._periodic_task = True
        f._periodic_external_ok = kwargs.pop('external_process_ok', False)
        if f._periodic_external_ok and not CONF.run_external_periodic_tasks:
            f._periodic_enabled = False
        else:
            f._periodic_enabled = kwargs.pop('enabled', True)
        f._periodic_spacing = kwargs.pop('spacing', 0)
        f._periodic_immediate = kwargs.pop('run_immediately', False)
        f._service_topic = kwargs.pop('service_topic', None)
        if f._periodic_immediate:
            f._periodic_last_run = None
        else:
            f._periodic_last_run = timeutils.utcnow()
        return f

    if kwargs:
        return decorator
    else:
        return decorator(args[0])


class _PeriodicTasksMeta(type):

    def __init__(cls, names, bases, dict_):
        """Metaclass that allows us to collect decorated periodic tasks."""
        super(_PeriodicTasksMeta, cls).__init__(names, bases, dict_)
        try:
            cls._periodic_tasks = cls._periodic_tasks[:]
        except AttributeError:
            cls._periodic_tasks = []

        try:
            cls._periodic_last_run = cls._periodic_last_run.copy()
        except AttributeError:
            cls._periodic_last_run = {}

        try:
            cls._periodic_spacing = cls._periodic_spacing.copy()
        except AttributeError:
            cls._periodic_spacing = {}

        try:
            cls._service_topic = cls._service_topic.copy()
        except AttributeError:
            cls._service_topic = {}

        for value in cls.__dict__.values():
            if getattr(value, '_periodic_task', False):
                task = value
                name = task.__name__
                if task._periodic_spacing < 0:
                    continue
                if not task._periodic_enabled:
                    continue
                if task._periodic_spacing == 0:
                    task._periodic_spacing = None
                cls._periodic_tasks.append((name, task))
                cls._periodic_spacing[name] = task._periodic_spacing
                cls._periodic_last_run[name] = task._periodic_last_run
                cls._service_topic[name] = task._service_topic

        return


class PeriodicTasks(object):
    __metaclass__ = _PeriodicTasksMeta

    def run_periodic_tasks(self, context, raise_on_error=False):
        """Tasks to be run at a periodic interval."""
        idle_for = DEFAULT_INTERVAL
        for task_name, task in self._periodic_tasks:
            full_task_name = ('.').join([self.__class__.__name__, task_name])
            now = timeutils.utcnow()
            spacing = self._periodic_spacing[task_name]
            last_run = self._periodic_last_run[task_name]
            service_topic = self._service_topic[task_name]
            if service_topic is not None:
                if not self._running_on_this_host(context, service_topic):
                    continue
            if spacing is not None and last_run is not None:
                due = last_run + datetime.timedelta(seconds=spacing)
                if not timeutils.is_soon(due, 0.2):
                    idle_for = min(idle_for, timeutils.delta_seconds(now, due))
                    continue
            if spacing is not None:
                idle_for = min(idle_for, spacing)
            self._periodic_last_run[task_name] = timeutils.utcnow()
            try:
                task(self, context)
            except Exception as e:
                LOG.exception(_('Error during %(full_task_name)s: %(e)s'), locals())
                if raise_on_error:
                    raise

            time.sleep(0)

        return idle_for

    def _running_on_this_host(self, context, service_topic):
        running_on_this_host = False
        host_list = []
        sers = db.service_get_all_by_topic(context, service_topic)
        for ser in sers:
            init_node = db.init_node_get_by_host(context, ser['host'])
            if utils.service_is_up(ser) and init_node and init_node['status'] == 'Active':
                host_list.append(ser['host'])

        host_list.sort()
        if len(host_list) == 0:
            return False
        select_host = random.randint(0, len(host_list) - 1)
        if host_list[select_host] == FLAGS.host:
            running_on_this_host = True
        return running_on_this_host