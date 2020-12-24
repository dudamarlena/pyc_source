# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/hooks/zendesk_hook.py
# Compiled at: 2019-09-11 02:44:38
# Size of source mod 2**32: 4668 bytes
import time
from zdesk import Zendesk, RateLimitError, ZendeskError
from airflow.hooks.base_hook import BaseHook

class ZendeskHook(BaseHook):
    __doc__ = '\n    A hook to talk to Zendesk\n    '

    def __init__(self, zendesk_conn_id):
        self._ZendeskHook__zendesk_conn_id = zendesk_conn_id
        self._ZendeskHook__url = None

    def get_conn(self):
        conn = self.get_connection(self._ZendeskHook__zendesk_conn_id)
        self._ZendeskHook__url = 'https://' + conn.host
        return Zendesk(zdesk_url=(self._ZendeskHook__url), zdesk_email=(conn.login), zdesk_password=(conn.password), zdesk_token=True)

    def __handle_rate_limit_exception(self, rate_limit_exception):
        """
        Sleep for the time specified in the exception. If not specified, wait
        for 60 seconds.
        """
        retry_after = int(rate_limit_exception.response.headers.get('Retry-After', 60))
        self.log.info('Hit Zendesk API rate limit. Pausing for %s seconds', retry_after)
        time.sleep(retry_after)

    def call(self, path, query=None, get_all_pages=True, side_loading=False):
        """
        Call Zendesk API and return results

        :param path: The Zendesk API to call
        :param query: Query parameters
        :param get_all_pages: Accumulate results over all pages before
               returning. Due to strict rate limiting, this can often timeout.
               Waits for recommended period between tries after a timeout.
        :param side_loading: Retrieve related records as part of a single
               request. In order to enable side-loading, add an 'include'
               query parameter containing a comma-separated list of resources
               to load. For more information on side-loading see
               https://developer.zendesk.com/rest_api/docs/core/side_loading
        """
        zendesk = self.get_conn()
        first_request_successful = False
        while not first_request_successful:
            try:
                results = zendesk.call(path, query)
                first_request_successful = True
            except RateLimitError as rle:
                self._ZendeskHook__handle_rate_limit_exception(rle)

        keys = [path.split('/')[(-1)].split('.json')[0]]
        next_page = results['next_page']
        if side_loading:
            keys += query['include'].split(',')
        results = {key:results[key] for key in keys}
        if get_all_pages:
            while next_page is not None:
                try:
                    next_url = next_page.split(self._ZendeskHook__url)[1]
                    self.log.info('Calling %s', next_url)
                    more_res = zendesk.call(next_url)
                    for key in results:
                        results[key].extend(more_res[key])

                    if next_page == more_res['next_page']:
                        break
                    else:
                        next_page = more_res['next_page']
                except RateLimitError as rle:
                    self._ZendeskHook__handle_rate_limit_exception(rle)
                except ZendeskError as ze:
                    if b'Use a start_time older than 5 minutes' in ze.msg:
                        break
                    else:
                        raise ze

        return results