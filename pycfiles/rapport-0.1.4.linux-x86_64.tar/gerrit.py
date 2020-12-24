# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib/python2.7/site-packages/rapport/plugins/gerrit.py
# Compiled at: 2013-06-25 03:06:32
"""
Gerrit plugin.
"""
from __future__ import print_function
import json
from datetime import datetime
import paramiko, rapport.plugin

class GerritPlugin(rapport.plugin.Plugin):

    def __init__(self, *args, **kwargs):
        super(GerritPlugin, self).__init__(*args, **kwargs)
        self._client = paramiko.SSHClient()
        self._client.load_system_host_keys()

    def _ssh_cmd(self, *args):
        """Execute a gerrit command over SSH.
        """
        command = ('gerrit {0}').format((' ').join(args))
        _, stdout, stderr = self._client.exec_command(command)
        return (stdout.readlines(), stderr.readlines())

    def _ssh_query(self, *args):
        """Execute a gerrit query over SSH and returns JSON-formatted data.
        """
        return self._ssh_cmd('query', '--format=JSON', *args)

    def collect(self, timeframe):
        self._client.connect(self.url.hostname, self.url.port, self.login)
        stdout, stderr = self._ssh_query(('owner:{0}').format(self.login))
        self._client.close()
        changes = []
        if not stderr:
            for line in stdout[:-1]:
                change = json.loads(line)
                if 'lastUpdated' in change:
                    last_updated = datetime.utcfromtimestamp(change['lastUpdated'])
                    if timeframe.contains(last_updated):
                        changes.append(change)
                else:
                    print(('Change {0} is missing lastUpdated').format(change))

        return self._results({'changes': changes})


rapport.plugin.register('gerrit', GerritPlugin)