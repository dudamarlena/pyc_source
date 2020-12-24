# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/contrib/hooks/jira_hook.py
# Compiled at: 2019-09-11 03:47:34
# Size of source mod 2**32: 3466 bytes
from jira import JIRA
from jira.exceptions import JIRAError
from airflow.exceptions import AirflowException
from airflow.hooks.base_hook import BaseHook

class JiraHook(BaseHook):
    """JiraHook"""

    def __init__(self, jira_conn_id='jira_default', proxies=None):
        super(JiraHook, self).__init__(jira_conn_id)
        self.jira_conn_id = jira_conn_id
        self.proxies = proxies
        self.client = None
        self.get_conn()

    def get_conn(self):
        if not self.client:
            self.log.debug('Creating Jira client for conn_id: %s', self.jira_conn_id)
            get_server_info = True
            validate = True
            extra_options = {}
            conn = None
            if self.jira_conn_id is not None:
                conn = self.get_connection(self.jira_conn_id)
                if conn.extra is not None:
                    extra_options = conn.extra_dejson
                    if 'verify' in extra_options:
                        if extra_options['verify'].lower() == 'false':
                            extra_options['verify'] = False
                    if 'validate' in extra_options:
                        if extra_options['validate'].lower() == 'false':
                            validate = False
                    if 'get_server_info' in extra_options:
                        if extra_options['get_server_info'].lower() == 'false':
                            get_server_info = False
                try:
                    self.client = JIRA((conn.host), options=extra_options,
                      basic_auth=(
                     conn.login, conn.password),
                      get_server_info=get_server_info,
                      validate=validate,
                      proxies=(self.proxies))
                except JIRAError as jira_error:
                    raise AirflowException('Failed to create jira client, jira error: %s' % str(jira_error))
                except Exception as e:
                    raise AirflowException('Failed to create jira client, error: %s' % str(e))

        return self.client