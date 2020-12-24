# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/dist-packages/vsmclient/v1/monitors.py
# Compiled at: 2016-06-13 14:11:03
"""
Monitors interface.
"""
import urllib
from vsmclient import base

class Monitor(base.Resource):
    """
    A monitor maintain maps of the cluster state, including the
    monitor map, the OSD map, the PG map, and the CRUSH map.
    """

    def __repr__(self):
        return '<Monitor: %s>' % self.id


class MonitorsManager(base.ManagerWithFind):
    """
    Manage :class:`Monitor` resources.
    """
    resource_class = Monitor

    def get(self, monitor_id):
        """
        Get a monitor.

        :param monitor_id: The ID of the monitor.
        :rtype: :class:`Monitor`
        """
        return self._get('/monitors/%s' % monitor_id, 'monitor')

    def list(self, detailed=False, search_opts=None):
        """
        Get a list of all monitors.

        :rtype: list of :class:`Monitor`
        """
        if search_opts is None:
            search_opts = {}
        qparams = {}
        for opt, val in search_opts.iteritems():
            if val:
                qparams[opt] = val

        query_string = '?%s' % urllib.urlencode(qparams) if qparams else ''
        detail = ''
        if detailed:
            detail = '/detail'
        ret = self._list('/monitors%s%s' % (detail, query_string), 'monitors')
        return ret

    def summary(self):
        """
        summary
        """
        url = '/monitors/summary'
        return self._get(url, 'monitor-summary')

    def restart(self, mon):
        self._action('restart', mon)

    def _action(self, action, monitor, info=None, **kwargs):
        """
        Perform a monitor "action."
        """
        body = {action: info}
        self.run_hooks('modify_body_for_action', body, **kwargs)
        url = '/monitors/%s/action' % base.getid(monitor)
        return self.api.client.post(url, body=body)