# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ztfy/scheduler/task.py
# Compiled at: 2014-12-23 09:23:16
__docformat__ = 'restructuredtext'
import codecs, logging
logger = logging.getLogger('ztfy.scheduler')
import traceback, transaction, zmq
from apscheduler.triggers.cron import CronTrigger
from apscheduler.triggers.interval import IntervalTrigger
from apscheduler.triggers.simple import SimpleTrigger
from cStringIO import StringIO
from datetime import datetime, timedelta
from persistent import Persistent
from persistent.list import PersistentList
from transaction.interfaces import ITransactionManager
from zope.annotation.interfaces import IAnnotations
from zope.component.interfaces import ObjectEvent, ISite
from zope.dublincore.interfaces import IZopeDublinCore
from zope.intid.interfaces import IIntIds
from zope.sendmail.interfaces import IMailDelivery
from ztfy.scheduler.interfaces import ISchedulerTask, ISchedulerTaskSchedulingMode, ISchedulerCronTask, ISchedulerCronTaskInfo, ISchedulerDateTask, ISchedulerDateTaskInfo, ISchedulerLoopTask, ISchedulerLoopTaskInfo, ISchedulerTaskHistoryInfo, IBeforeJobRunEvent, IAfterJobRunEvent, IScheduler
from ztfy.utils.interfaces import IZEOConnection
from zope.app.publication.zopepublication import ZopePublication
from zope.component import queryUtility, getUtility, adapter
from zope.container.contained import Contained
from zope.event import notify
from zope.interface import implementer, implements, alsoProvides, noLongerProvides, Interface
from zope.location import locate, Location
from zope.schema.fieldproperty import FieldProperty
from zope.site import hooks
from zope.traversing import api as traversing_api
from ztfy.mail.message import TextMessage
from ztfy.utils.date import getDuration
from ztfy.utils.property import cached_property
from ztfy.utils.timezone import tztime
from ztfy.utils.traversing import getParent
from ztfy.utils.zodb import ZEOConnectionInfo
from ztfy.scheduler import _

class BeforeJobRunEvent(ObjectEvent):
    implements(IBeforeJobRunEvent)


class AfterJobRunEvent(ObjectEvent):
    implements(IAfterJobRunEvent)

    def __init__(self, object, status):
        self.object = object
        self.status = status


class TaskHistoryItem(Persistent, Contained):
    """Task history item"""
    implements(ISchedulerTaskHistoryInfo)
    date = FieldProperty(ISchedulerTaskHistoryInfo['date'])
    status = FieldProperty(ISchedulerTaskHistoryInfo['status'])
    report = FieldProperty(ISchedulerTaskHistoryInfo['report'])


class TaskHistoryContainer(PersistentList, Location):
    """Task history container"""
    pass


class BaseTask(Persistent, Location):
    """Scheduler base management task"""
    implements(ISchedulerTask)
    _title = FieldProperty(ISchedulerTask['title'])
    _schedule_mode = FieldProperty(ISchedulerTask['schedule_mode'])
    report_source = FieldProperty(ISchedulerTask['report_source'])
    report_target = FieldProperty(ISchedulerTask['report_target'])
    report_mailer = FieldProperty(ISchedulerTask['report_mailer'])
    report_errors_only = FieldProperty(ISchedulerTask['report_errors_only'])
    send_empty_reports = FieldProperty(ISchedulerTask['send_empty_reports'])
    keep_empty_reports = FieldProperty(ISchedulerTask['keep_empty_reports'])
    _history_length = FieldProperty(ISchedulerTask['history_length'])

    def __init__(self):
        history = self.history = TaskHistoryContainer()
        locate(history, self, '++history++')

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, value):
        self._title = value
        IZopeDublinCore(self).title = value

    @property
    def schedule_mode(self):
        return self._schedule_mode

    @schedule_mode.setter
    def schedule_mode(self, value):
        if self._schedule_mode is not None:
            mode = queryUtility(ISchedulerTaskSchedulingMode, self._schedule_mode)
            if mode is not None and mode.marker_interface.providedBy(self):
                noLongerProvides(self, mode.marker_interface)
        self._schedule_mode = value
        if value:
            mode = getUtility(ISchedulerTaskSchedulingMode, value)
            alsoProvides(self, mode.marker_interface)
            mode.schema(self).active = False
            self.reset()
        return

    @property
    def history_length(self):
        return self._history_length

    @history_length.setter
    def history_length(self, value):
        self._history_length = value
        if value < len(self.history):
            history = self.history
            while value < len(history):
                del history[0]

            self.history = history

    @cached_property
    def internal_id(self):
        intids = queryUtility(IIntIds, context=self)
        if intids is not None:
            return intids.register(self)
        else:
            return

    def getTrigger(self):
        mode = queryUtility(ISchedulerTaskSchedulingMode, self.schedule_mode)
        if mode is None:
            return
        else:
            return mode.getTrigger(self)

    def getSchedulingInfo(self):
        mode = queryUtility(ISchedulerTaskSchedulingMode, self.schedule_mode)
        if mode is None:
            return
        else:
            return mode.schema(self, None)

    def getNextRun(self):
        trigger = self.getTrigger()
        if trigger is not None:
            now = datetime.utcnow()
            return trigger.get_next_fire_time(now)
        else:
            return

    def reset(self, delete_only=False):
        scheduler = getParent(self, IScheduler)
        transaction.get().addAfterCommitHook(self._resetAction, kws={'scheduler': scheduler})

    def _resetAction(self, status, *args, **kw):
        if not status:
            return
        else:
            scheduler = kw.get('scheduler')
            if scheduler is None:
                scheduler = getParent(self, IScheduler)
            if scheduler is not None:
                zeo = getUtility(IZEOConnection, scheduler.zeo_connection)
                context = zmq.Context()
                socket = context.socket(zmq.REQ)
                socket.connect('tcp://' + scheduler.zmq_address)
                socket.send_json(['reset_task',
                 {'zeo': zeo.getSettings(), 'task_name': traversing_api.getName(self), 
                    'job_id': self.internal_id}])
                socket.recv_json()
            return

    def launch(self):
        scheduler = getParent(self, IScheduler)
        transaction.get().addAfterCommitHook(self._launchAction, kws={'scheduler': scheduler})

    def _launchAction(self, status, *args, **kw):
        if not status:
            return
        else:
            scheduler = kw.get('scheduler')
            if scheduler is None:
                scheduler = getParent(self, IScheduler)
            if scheduler is not None:
                zeo = getUtility(IZEOConnection, scheduler.zeo_connection)
                context = zmq.Context()
                socket = context.socket(zmq.REQ)
                socket.connect('tcp://' + scheduler.zmq_address)
                socket.send_json(['run_task',
                 {'zeo': zeo.getSettings(), 'task_name': traversing_api.getName(self), 
                    'job_id': self.internal_id}])
                socket.recv_json()
            return

    def __call__(self, *args, **kw):
        report = codecs.getwriter('utf-8')(StringIO())
        self._run(report, **kw)

    @property
    def runnable(self):
        mode = queryUtility(ISchedulerTaskSchedulingMode, self.schedule_mode)
        if mode is None:
            return False
        else:
            info = mode.schema(self, None)
            if info is None:
                return False
            return info.active

    def _run(self, report, **kw):
        """Execute task"""
        zeo_connection = ZEOConnectionInfo()
        zeo_connection.update(kw.get('zeo_settings'))
        with zeo_connection as (root):
            manager = None
            try:
                root_folder = root.get(ZopePublication.root_name, None)
                task = traversing_api.traverse(root_folder, traversing_api.getPath(self))
                if not (kw.get('run_immediate') or task.runnable):
                    return
                manager = ITransactionManager(task)
                for attempt in manager.attempts():
                    with attempt as (t):
                        start = datetime.utcnow()
                        try:
                            site = getParent(task, ISite)
                            hooks.setSite(site)
                            notify(BeforeJobRunEvent(task))
                            task.run(report)
                            if report.getvalue():
                                status = 'OK'
                            else:
                                status = 'Empty'
                            report.write('\n\nTask duration: ' + getDuration(start) + '\n')
                        except:
                            status = 'Error'
                            task._logException(report, 'An error occured during execution of task %s' % task.title)

                        notify(AfterJobRunEvent(task, status))
                        task.storeReport(report, status)
                        task.sendReport(report, status)
                    if t.status == 'Committed':
                        break

            except:
                self._logException(None, "Can't execute scheduled job %s" % self.title)

        ITransactionManager(self).abort()
        return

    def run(self, report):
        raise NotImplementedError, _("The 'run' method must be implemented by BaseTask subclasses")

    def _logReport(self, report, message, add_timestamp=True, level=logging.INFO):
        if add_timestamp:
            message = '%s - %s' % (tztime(datetime.utcnow()).strftime('%c'), message)
        if report is not None:
            report.write(message + '\n')
        logger.log(level, message)
        return

    def _logException(self, report, message=None):
        message = '%s - %s' % (tztime(datetime.utcnow()).strftime('%c'), message or 'An error occurred')
        if report is not None:
            report.write(message + '\n\n')
            report.write(traceback.format_exc() + '\n')
        logger.exception(message)
        return

    def storeReport(self, report, status):
        """Store execution report in task's history and send it by mail"""
        if status == 'Empty' and not self.keep_empty_reports:
            return
        item = TaskHistoryItem()
        item.date = tztime(datetime.utcnow())
        item.status = status
        item.report = unicode(codecs.decode(report.getvalue(), 'utf-8'))
        if len(self.history) >= self.history_length:
            history = self.history
            while len(history) >= self.history_length:
                del history[0]

            self.history = history
        if self.history_length:
            self.history.append(item)
            locate(item, self.history)

    def sendReport(self, report, status):
        if self.report_target and (status in ('Error', 'Warning') or status == 'Empty' and self.send_empty_reports or status == 'OK' and not self.report_errors_only):
            mailer = queryUtility(IMailDelivery, self.report_mailer)
            if mailer is not None:
                if status == 'Error':
                    subject = '[SCHEDULER ERROR] ' + self.title
                else:
                    subject = '[scheduler] ' + self.title
                for target in self.report_target.split(';'):
                    message = TextMessage(subject=subject, fromaddr=self.report_source, toaddr=(
                     target,), text=report.getvalue())
                    mailer.send(self.report_source, (target,), message.as_string())

        return


class CronTaskScheduler(object):
    """Cron-style task scheduler class"""
    implements(ISchedulerTaskSchedulingMode)
    marker_interface = ISchedulerCronTask
    schema = ISchedulerCronTaskInfo

    def getTrigger(self, task):
        if not self.marker_interface.providedBy(task):
            raise Exception(_('Task is not configured for cron-style scheduling !'))
        info = self.schema(task)
        return CronTrigger(year=info.year or '*', month=info.month or '*', day=info.day or '*', week=info.week or '*', day_of_week=info.day_of_week or '*', hour=info.hour or '*', minute=info.minute or '*', second=info.second or '0', start_date=info.start_date.replace(tzinfo=None) if info.start_date else None)


CronTaskScheduler = CronTaskScheduler()
SCHEDULER_TASK_CRON_KEY = 'ztfy.scheduler.mode.cron'

@adapter(ISchedulerCronTask)
@implementer(ISchedulerCronTaskInfo)
def SchedulerTaskCronInfoFactory(context):
    """Scheduler task cron info adapter factory"""
    annotations = IAnnotations(context)
    info = annotations.get(SCHEDULER_TASK_CRON_KEY)
    if info is None:
        info = annotations[SCHEDULER_TASK_CRON_KEY] = SchedulerTaskCronInfo()
    return info


class SchedulerTaskCronInfo(Persistent):
    """Scheduler task cron info"""
    implements(ISchedulerCronTaskInfo)
    active = FieldProperty(ISchedulerCronTaskInfo['active'])
    max_runs = FieldProperty(ISchedulerCronTaskInfo['max_runs'])
    start_date = FieldProperty(ISchedulerCronTaskInfo['start_date'])
    year = FieldProperty(ISchedulerCronTaskInfo['year'])
    month = FieldProperty(ISchedulerCronTaskInfo['month'])
    day = FieldProperty(ISchedulerCronTaskInfo['day'])
    week = FieldProperty(ISchedulerCronTaskInfo['week'])
    day_of_week = FieldProperty(ISchedulerCronTaskInfo['day_of_week'])
    hour = FieldProperty(ISchedulerCronTaskInfo['hour'])
    minute = FieldProperty(ISchedulerCronTaskInfo['minute'])
    second = FieldProperty(ISchedulerCronTaskInfo['second'])


class DateTaskScheduler(object):
    """Date-style task scheduler class"""
    implements(ISchedulerTaskSchedulingMode)
    marker_interface = ISchedulerDateTask
    schema = ISchedulerDateTaskInfo

    def getTrigger(self, task):
        if not self.marker_interface.providedBy(task):
            raise Exception(_('Task is not configured for date-style scheduling !'))
        info = self.schema(task)
        return SimpleTrigger(run_date=info.start_date.replace(tzinfo=None))


DateTaskScheduler = DateTaskScheduler()
SCHEDULER_TASK_DATE_KEY = 'ztfy.scheduler.mode.date'

@adapter(ISchedulerDateTask)
@implementer(ISchedulerDateTaskInfo)
def SchedulerTaskDateInfoFactory(context):
    """Scheduler task date info adapter"""
    annotations = IAnnotations(context)
    info = annotations.get(SCHEDULER_TASK_DATE_KEY)
    if info is None:
        info = annotations[SCHEDULER_TASK_DATE_KEY] = SchedulerTaskDateInfo()
    return info


class SchedulerTaskDateInfo(Persistent):
    """Scheduler task date info"""
    implements(ISchedulerDateTaskInfo)
    active = FieldProperty(ISchedulerDateTaskInfo['active'])
    max_runs = FieldProperty(ISchedulerDateTaskInfo['max_runs'])
    start_date = FieldProperty(ISchedulerDateTaskInfo['start_date'])


def ImmediateTaskTrigger():
    """Immediate-style task scheduler class"""
    return SimpleTrigger(run_date=datetime.now().replace(tzinfo=None) + timedelta(seconds=5))


class LoopTaskScheduler(object):
    """Interval-based task scheduler class"""
    implements(ISchedulerTaskSchedulingMode)
    marker_interface = ISchedulerLoopTask
    schema = ISchedulerLoopTaskInfo

    def getTrigger(self, task):
        if not self.marker_interface.providedBy(task):
            raise Exception(_('Task is not configured for loop-style scheduling !'))
        info = self.schema(task)
        return IntervalTrigger(timedelta(weeks=info.weeks, days=info.days, hours=info.hours, minutes=info.minutes, seconds=info.seconds), start_date=info.start_date.replace(tzinfo=None) if info.start_date else None)


LoopTaskScheduler = LoopTaskScheduler()
SCHEDULER_TASK_LOOP_KEY = 'ztfy.scheduler.mode.loop'

@adapter(ISchedulerLoopTask)
@implementer(ISchedulerLoopTaskInfo)
def SchedulerTaskLoopInfoFactory(context):
    """Scheduler task loop info adapter"""
    annotations = IAnnotations(context)
    info = annotations.get(SCHEDULER_TASK_LOOP_KEY)
    if info is None:
        info = annotations[SCHEDULER_TASK_LOOP_KEY] = SchedulerTaskLoopInfo()
    return info


class SchedulerTaskLoopInfo(Persistent):
    """Scheduler task loop info"""
    implements(ISchedulerLoopTaskInfo)
    active = FieldProperty(ISchedulerLoopTaskInfo['active'])
    max_runs = FieldProperty(ISchedulerLoopTaskInfo['max_runs'])
    start_date = FieldProperty(ISchedulerLoopTaskInfo['start_date'])
    weeks = FieldProperty(ISchedulerLoopTaskInfo['weeks'])
    days = FieldProperty(ISchedulerLoopTaskInfo['days'])
    hours = FieldProperty(ISchedulerLoopTaskInfo['hours'])
    minutes = FieldProperty(ISchedulerLoopTaskInfo['minutes'])
    seconds = FieldProperty(ISchedulerLoopTaskInfo['seconds'])