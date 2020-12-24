# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/msimonin/workspace/repos/enos/enos/ansible/plugins/callback/influxdb_events.py
# Compiled at: 2019-03-06 08:20:32
# Size of source mod 2**32: 4979 bytes
from __future__ import absolute_import, division, print_function
__metaclass__ = type
from datetime import datetime
import pwd, os
from requests import exceptions
from ansible.plugins.callback import CallbackBase
from influxdb import InfluxDBClient
from influxdb.exceptions import InfluxDBServerError

class CallbackModule(CallbackBase):
    __doc__ = '\n    This callback module fills an InfluxDB with Ansible events:\n    1. Create an empty list at the beginning of playbooks;\n    2. Add an event to the list for each playbook/play/task;\n    3. Connect to InfluxDB at the end of playbooks if succeeded and commit\n    events.\n    '
    CALLBACK_VERSION = 2.0
    CALLBACK_TYPE = 'notification'
    CALLBACK_NAME = 'influxdb_events'
    CALLBACK_NEEDS_WHITELIST = True

    def __init__(self):
        super(CallbackModule, self).__init__()
        self.timer = None
        self.events = []
        self.host_vars = None
        self.timer = None
        self.username = pwd.getpwuid(os.getuid()).pw_name

    def report_event(self, fields):
        """Add a new event in the list"""
        current_time = datetime.utcnow().strftime('%Y-%m-%dT%H:%M:%S.%f')
        event = {'time':current_time, 
         'measurement':'events', 
         'fields':fields}
        self.events.append(event)

    def v2_playbook_on_start(self, playbook):
        """Log each starting playbook"""
        self.playbook_name = os.path.basename(playbook._file_name)
        fields = {'tags':'playbook %s' % self.username, 
         'text':self.playbook_name, 
         'type':'playbook', 
         'title':self.playbook_name}
        self.report_event(fields)

    def v2_playbook_on_play_start(self, play):
        """Log each starting play"""
        self.vm = play.get_variable_manager()
        self.play = play
        fields = {'tags':'play {} {}'.format(self.playbook_name, self.play.name), 
         'title':play.name, 
         'type':'play', 
         'text':play.name}
        self.report_event(fields)

    def v2_playbook_on_task_start(self, task, is_conditional):
        """Restart the timer when a task starts"""
        self.timer = datetime.now()
        fields = {'tags':'task {} {} {}'.format(self.playbook_name, self.play.name, task.get_name()), 
         'text':task.get_name(), 
         'type':'task', 
         'title':task.get_name()}
        self.report_event(fields)

    def v2_runner_on_ok(self, result):
        """Log each finished task marked as 'changed'"""
        pass

    def v2_playbook_on_stats(self, stats):
        """Connect to InfluxDB and commit events"""
        enos_tags = self.vm.get_vars().get('enos_tags', '')
        fields = {'tags':'playbook {} {}'.format(self.playbook_name, enos_tags), 
         'text':'playbook finished', 
         'type':'playbook', 
         'title':self.playbook_name}
        self.report_event(fields)
        _host = os.getenv('INFLUX_VIP') or self.vm.get_vars().get('influx_vip')
        if not _host:
            return
        _port = '8086'
        _user = 'None'
        _pass = 'None'
        _dbname = 'events'
        influxdb = InfluxDBClient(_host, _port, _user, _pass, _dbname)
        try:
            version = influxdb.ping()
        except (InfluxDBServerError, exceptions.HTTPError,
         exceptions.ConnectionError,
         exceptions.Timeout,
         exceptions.RequestException) as error:
            return

        try:
            influxdb.write_points((self.events), time_precision='u')
        except Exception:
            self.disabled = True
            self._display.warning('Cannot write to InfluxDB, check the service state on %s.' % _host)
            return