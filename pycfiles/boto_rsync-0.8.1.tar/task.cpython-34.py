# uncompyle6 version 3.6.7
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.10-x86_64/egg/boto/manage/task.py
# Compiled at: 2015-11-24 05:02:18
# Size of source mod 2**32: 6781 bytes
import boto
from boto.sdb.db.property import StringProperty, DateTimeProperty, IntegerProperty
from boto.sdb.db.model import Model
import datetime, subprocess, time
from boto.compat import StringIO

def check_hour(val):
    if val == '*':
        return
    if int(val) < 0 or int(val) > 23:
        raise ValueError


class Task(Model):
    """Task"""
    name = StringProperty()
    hour = StringProperty(required=True, validator=check_hour, default='*')
    command = StringProperty(required=True)
    last_executed = DateTimeProperty()
    last_status = IntegerProperty()
    last_output = StringProperty()
    message_id = StringProperty()

    @classmethod
    def start_all(cls, queue_name):
        for task in cls.all():
            task.start(queue_name)

    def __init__(self, id=None, **kw):
        super(Task, self).__init__(id, **kw)
        self.hourly = self.hour == '*'
        self.daily = self.hour != '*'
        self.now = datetime.datetime.utcnow()

    def check(self):
        """
        Determine how long until the next scheduled time for a Task.
        Returns the number of seconds until the next scheduled time or zero
        if the task needs to be run immediately.
        If it's an hourly task and it's never been run, run it now.
        If it's a daily task and it's never been run and the hour is right, run it now.
        """
        boto.log.info('checking Task[%s]-now=%s, last=%s' % (self.name, self.now, self.last_executed))
        if self.hourly and not self.last_executed:
            return 0
        if self.daily and not self.last_executed:
            if int(self.hour) == self.now.hour:
                return 0
            else:
                return max(int(self.hour) - self.now.hour, self.now.hour - int(self.hour)) * 60 * 60
        delta = self.now - self.last_executed
        if self.hourly:
            if delta.seconds >= 3600:
                return 0
            else:
                return 3600 - delta.seconds
        else:
            if int(self.hour) == self.now.hour:
                if delta.days >= 1:
                    return 0
                else:
                    return 82800
            else:
                return max(int(self.hour) - self.now.hour, self.now.hour - int(self.hour)) * 60 * 60

    def _run(self, msg, vtimeout):
        boto.log.info('Task[%s] - running:%s' % (self.name, self.command))
        log_fp = StringIO()
        process = subprocess.Popen(self.command, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        nsecs = 5
        current_timeout = vtimeout
        while process.poll() is None:
            boto.log.info('nsecs=%s, timeout=%s' % (nsecs, current_timeout))
            if nsecs >= current_timeout:
                current_timeout += vtimeout
                boto.log.info('Task[%s] - setting timeout to %d seconds' % (self.name, current_timeout))
                if msg:
                    msg.change_visibility(current_timeout)
                time.sleep(5)
                nsecs += 5

        t = process.communicate()
        log_fp.write(t[0])
        log_fp.write(t[1])
        boto.log.info('Task[%s] - output: %s' % (self.name, log_fp.getvalue()))
        self.last_executed = self.now
        self.last_status = process.returncode
        self.last_output = log_fp.getvalue()[0:1023]

    def run(self, msg, vtimeout=60):
        delay = self.check()
        boto.log.info('Task[%s] - delay=%s seconds' % (self.name, delay))
        if delay == 0:
            self._run(msg, vtimeout)
            queue = msg.queue
            new_msg = queue.new_message(self.id)
            new_msg = queue.write(new_msg)
            self.message_id = new_msg.id
            self.put()
            boto.log.info('Task[%s] - new message id=%s' % (self.name, new_msg.id))
            msg.delete()
            boto.log.info('Task[%s] - deleted message %s' % (self.name, msg.id))
        else:
            boto.log.info('new_vtimeout: %d' % delay)
            msg.change_visibility(delay)

    def start(self, queue_name):
        boto.log.info('Task[%s] - starting with queue: %s' % (self.name, queue_name))
        queue = boto.lookup('sqs', queue_name)
        msg = queue.new_message(self.id)
        msg = queue.write(msg)
        self.message_id = msg.id
        self.put()
        boto.log.info('Task[%s] - start successful' % self.name)


class TaskPoller(object):

    def __init__(self, queue_name):
        self.sqs = boto.connect_sqs()
        self.queue = self.sqs.lookup(queue_name)

    def poll(self, wait=60, vtimeout=60):
        while True:
            m = self.queue.read(vtimeout)
            if m:
                task = Task.get_by_id(m.get_body())
                if task:
                    if not task.message_id or m.id == task.message_id:
                        boto.log.info('Task[%s] - read message %s' % (task.name, m.id))
                        task.run(m, vtimeout)
                    else:
                        boto.log.info('Task[%s] - found extraneous message, ignoring' % task.name)
            else:
                time.sleep(wait)