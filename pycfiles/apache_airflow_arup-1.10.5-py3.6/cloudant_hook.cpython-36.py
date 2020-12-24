# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/contrib/hooks/cloudant_hook.py
# Compiled at: 2019-09-11 03:47:34
# Size of source mod 2**32: 2954 bytes
from past.builtins import unicode
import cloudant
from airflow.exceptions import AirflowException
from airflow.hooks.base_hook import BaseHook
from airflow.utils.log.logging_mixin import LoggingMixin

class CloudantHook(BaseHook):
    __doc__ = 'Interact with Cloudant.\n\n    This class is a thin wrapper around the cloudant python library. See the\n    documentation `here <https://github.com/cloudant-labs/cloudant-python>`_.\n    '

    def __init__(self, cloudant_conn_id='cloudant_default'):
        super(CloudantHook, self).__init__('cloudant')
        self.cloudant_conn_id = cloudant_conn_id

    def get_conn(self):

        def _str(s):
            if isinstance(s, unicode):
                log = LoggingMixin().log
                log.debug('cloudant-python does not support unicode. Encoding %s as ascii using "ignore".', s)
                return s.encode('ascii', 'ignore')
            else:
                return s

        conn = self.get_connection(self.cloudant_conn_id)
        for conn_param in ('host', 'password', 'schema'):
            if not hasattr(conn, conn_param) or not getattr(conn, conn_param):
                raise AirflowException('missing connection parameter {0}'.format(conn_param))

        account = cloudant.Account(_str(conn.host))
        username = _str(conn.login or conn.host)
        account.login(username, _str(conn.password)).raise_for_status()
        return account.database(_str(conn.schema))

    def db(self):
        """Returns the Database object for this hook.

        See the documentation for cloudant-python here
        https://github.com/cloudant-labs/cloudant-python.
        """
        return self.get_conn()