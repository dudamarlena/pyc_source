# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/lib/python2.7/site-packages/rapport/plugins/bugzilla.py
# Compiled at: 2013-07-29 07:43:11
"""
Bugzilla plugin.
"""
from __future__ import absolute_import
import bugzilla, rapport.plugin

class BugzillaPlugin(rapport.plugin.Plugin):

    def __init__(self, email, *args, **kwargs):
        super(BugzillaPlugin, self).__init__(*args, **kwargs)
        self.email = email
        self.url = ('{0}/xmlrpc.cgi').format(self.url.geturl())

    def collect(self, timeframe):
        bz = bugzilla.Bugzilla(url=self.url)
        bz.login(user=self.login, password=self.password)
        open_bugs = bz.query({'assigned_to': self.email, 'bug_status': [
                        'NEW', 'ASSIGNED']})
        closed_bugs = bz.query({'assigned_to': self.email, 'bug_status': [
                        'CLOSED', 'RESOLVED'], 
           'last_change_time': timeframe.start})
        return self._results({'email': self.email, 'open_bugs': open_bugs, 'closed_bugs': closed_bugs})


rapport.plugin.register('bugzilla', BugzillaPlugin)