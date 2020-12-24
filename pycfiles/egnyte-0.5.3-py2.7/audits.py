# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/egnyte/audits.py
# Compiled at: 2017-02-28 06:43:12
from __future__ import unicode_literals
from egnyte import base, exc

class Audits(base.HasClient):
    """
    This resource is used to generated various kinds of audit reports.
    """
    _url_template = b'pubapi/v1/audit/%(type)s'

    def _job_id(self, response):
        json = exc.accepted.check_json_response(response)
        return json[b'id']

    def logins(self, format, date_start, date_end, events, access_points=None, users=None):
        """
        Generate login report.
        Parameters:

        * format: 'csv' or 'json'
        * date_start: string in 'YYYY-MM-DD' format or datetime.date - first day report should cover
        * date_end: string in 'YYYY-MM-DD' format or datetime.date - last day report should cover
        * events: list of events to report on, at least one must be specified, allowed values: logins, logouts, account_lockouts, password_resets, failed_attempts

        Returns an AuditReport object.
        """
        json = dict(format=format, date_start=base.date_format(date_start), date_end=base.date_format(date_end), events=list(events))
        if access_points:
            json[b'access_points'] = list(access_points)
        if users:
            json[b'users'] = list(users)
        url = self._client.get_url(self._url_template, type=b'logins')
        r = self._client.POST(url, json)
        return AuditReport(self._client, id=self._job_id(r), format=format, type=b'logins')

    def files(self, format, date_start, date_end, folders=None, file=None, users=None, transaction_type=None):
        """
        Generate files report.
        Parameters:

        * format: 'csv' or 'json'
        * date_start: string in 'YYYY-MM-DD' format or datetime.date - first day report should cover
        * date_end: string in 'YYYY-MM-DD' format or datetime.date - last day report should cover

        Returns an AuditReport object.
        """
        json = dict(format=format, date_start=base.date_format(date_start), date_end=base.date_format(date_end))
        if folders:
            json[b'folders'] = list(folders)
        if file:
            json[b'file'] = file
        if users:
            json[b'users'] = list(users)
        if transaction_type:
            json[b'transaction_type'] = list(transaction_type)
        url = self._client.get_url(self._url_template, type=b'files')
        r = self._client.POST(url, json)
        return AuditReport(self._client, id=self._job_id(r), format=format, type=b'files')

    def permissions(self, format, date_start, date_end, folders, assigners, assignee_users, assignee_groups):
        """
        Generate permissions report.
        Parameters:

        * format: 'csv' or 'json'
        * date_start: string in 'YYYY-MM-DD' format or datetime.date - first day report should cover
        * date_end: string in 'YYYY-MM-DD' format or datetime.date - last day report should cover

        Returns an AuditReport object.
        """
        json = dict(format=format, date_start=base.date_format(date_start), date_end=base.date_format(date_end), folders=list(folders), assigners=list(assigners), assignee_users=list(assignee_users), assignee_groups=list(assignee_groups))
        url = self._client.get_url(self._url_template, type=b'permissions')
        r = self._client.POST(url, json)
        return AuditReport(self._client, id=self._job_id(r), format=format, type=b'permissions')

    def get(self, id):
        """Get a previously generated report by its id"""
        return AuditReport(self._client, id=id)


class AuditReport(base.Resource):
    _url_template = b'pubapi/v1/audit/jobs/%(id)s'
    _url_template_completed = b'pubapi/v1/audit/%(type)s/%(id)s'
    status = b'running'

    def is_ready(self):
        """
        True if report is ready to be downloaded.
        Does a single API request.
        """
        r = self._client.GET(self._url)
        if r.status_code == 303:
            self.status == b'completed'
            return True
        exc.default.check_response(r)
        return False

    def wait(self, check_time=5.0):
        """
        Block until report is ready.
        Probably only useful for command line applications.
        """
        import time
        while not self.is_ready():
            time.sleep(check_time)

    def complete_url(self):
        url = self._client.get_url(self._url_template_completed, type=self.type, id=self.id)
        return url

    def download(self):
        r = self._client.GET(self.complete_url(), stream=True)
        exc.default.check_response(r)
        return base.FileDownload(r, None)

    def json(self):
        r = self._client.GET(self.complete_url())
        return exc.default.check_json_response(r)