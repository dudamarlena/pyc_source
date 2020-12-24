# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Library/Python/2.7/site-packages/src/metrics/users.py
# Compiled at: 2013-01-30 13:44:04
"""
    This module handles exposing user types for metrics processing.
"""
__author__ = 'ryan faulkner'
__date__ = '01/28/2013'
__email__ = 'rfaulkner@wikimedia.org'
from src.etl.data_loader import Connector
from dateutil.parser import parse as date_parse
MEDIAWIKI_DB_INSTANCE = 'slave'
MEDIAWIKI_TIMESTAMP_FORMAT = '%Y%m%d%H%M%S'

class MediaWikiUserException(Exception):
    """ Basic exception class for UserMetric types """

    def __init__(self, message='Error obtaining user(s) from MediaWiki instance.'):
        Exception.__init__(self, message)


class MediaWikiUser(object):
    """
        Class to expose users from MediaWiki databases in a standard way.
        A class level attribute QUERY_TYPES handles the method in which
        the user is extracted from a MediaWiki DB.
    """
    USER_QUERY_LOG = "\n                    SELECT log_user\n                    FROM %(project)s.logging\n                    WHERE log_timestamp > %(date_start)s AND\n                     log_timestamp <= %(date_end)s AND\n                     log_action = 'create' AND log_type='newusers'\n                "
    USER_QUERY_USER = '\n                    SELECT user_id\n                    FROM %(project)s.user\n                    WHERE user_registration > %(date_start)s AND\n                     user_registration <= %(date_end)s\n                '
    QUERY_TYPES = {1: USER_QUERY_LOG, 
       2: USER_QUERY_USER}

    def __init__(self, query_type=1):
        self._query_type = query_type
        super(MediaWikiUser, self).__init__()

    def get_users(self, date_start, date_end, project='enwiki'):
        """
            Returns a Generator for MediaWiki user IDs.
        """
        param_dict = {'date_start': self._format_mediawiki_timestamp(date_start), 
           'date_end': self._format_mediawiki_timestamp(date_end), 
           'project': project}
        conn = Connector(instance=MEDIAWIKI_DB_INSTANCE)
        conn._cur_.execute(self.QUERY_TYPES[self._query_type] % param_dict)
        for row in conn._cur_:
            yield row[0]

    def _format_mediawiki_timestamp(self, timestamp_repr):
        """ Convert to mediawiki timestamps """
        if hasattr(timestamp_repr, 'strftime'):
            return timestamp_repr.strftime(MEDIAWIKI_TIMESTAMP_FORMAT)
        else:
            return date_parse(timestamp_repr).strftime(MEDIAWIKI_TIMESTAMP_FORMAT)