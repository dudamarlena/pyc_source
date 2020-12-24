# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/narendra/.pyenv/versions/aws/lib/python3.6/site-packages/tvarit_api/resources/alerting.py
# Compiled at: 2019-07-26 06:37:31
# Size of source mod 2**32: 1871 bytes
from .base import Base

class Alerting(Base):

    def __init__(self, api):
        super(Alerting, self).__init__(api)
        self.api = api

    def get_alerts(self, dashboardId=None, panelId=None, query=None, limit=None, state=None, folderId=None, dashboardQuery=None, dashboardTag=None):
        """
        Method to get alerts on the basis of query parameters
        :return: response
        """
        path = '/alerts'
        params = []
        if dashboardId:
            params.extend(['dashboardId=%s' % id_ for id_ in dashboardId])
        if panelId:
            params.append('panelId=%s' % panelId)
        if query:
            params.append('query=%s' % query)
        if limit:
            params.append('limit=%s' % limit)
        if dashboardQuery:
            params.append('dashboardQuery=%s' % dashboardQuery)
        if state:
            params.extend(['state=%s' % v for v in state])
        if folderId:
            params.extend(['folderId=%s' % v for v in folderId])
        if dashboardTag:
            params.extend(['dashboardTag=%s' % v for v in dashboardTag])
        if params:
            path += '?'
            path += '&'.join(params)
        r = self.api.GET(path)
        return r

    def get_alert_by_id(self, alert_id):
        """
        Method to get alert by ID
        :param alert_id: alert ID
        :return: response
        """
        path = '/alerts/%s' % alert_id
        r = self.api.GET(path)
        return r

    def pause_alert(self, alert_id, json_dict):
        """
        Method to pause alert by its ID
        :param alert_id: alert ID
        :param json_dict: json dict with pause flag True or False
        :return: response
        """
        path = '/alerts/%s/pause' % alert_id
        r = self.api.POST(path, json=json_dict)
        return r