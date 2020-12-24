# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/nb/publish/btw/tingyun/tingyun/armoury/external_urllib2.py
# Compiled at: 2016-07-03 22:35:45
"""

"""
import sys
from tingyun.packages import six
from tingyun.armoury.ammunition.tracker import current_tracker
from tingyun.armoury.ammunition.external_tracker import wrap_external_trace, parse_parameters
from tingyun.armoury.ammunition.external_tracker import MALFORMED_URL_ERROR_CODE
from tingyun.armoury.ammunition.external_tracker import OTHER_ERROR_CODE
from urllib2 import URLError, HTTPError

def wrap_exception(wrapped, url, parameters, *args, **kwargs):
    """
    """
    tracker = current_tracker()
    if tracker is None:
        return wrapped(*args, **kwargs)
    else:
        url = url if not callable(url) else url(*args, **kwargs)
        params = parameters if not callable(parameters) else parameters(*args, **kwargs)
        http_status = 500
        error_code = 0
        params = parse_parameters(url, params)
        try:
            rtv = wrapped(*args, **kwargs)
        except URLError:
            error_code = MALFORMED_URL_ERROR_CODE
            tracker.record_external_error(url, error_code, http_status, sys.exc_info(), params)
            raise
        except HTTPError as err:
            http_status = getattr(err, 'code')
            error_code = OTHER_ERROR_CODE
            tracker.record_external_error(url, error_code, http_status, sys.exc_info(), params)
            raise
        except Exception:
            error_code = OTHER_ERROR_CODE
            tracker.record_external_error(url, error_code, http_status, sys.exc_info(), params)
            raise

        http_status = rtv.getcode()
        if http_status is not None and int(http_status) != 200:
            tracker.record_external_error(url, error_code, int(http_status), sys.exc_info(), params)
        return rtv


def detect(module):

    def url_opener_open(instance, fullurl, *args, **kwargs):
        """
        :param instance:
        :param fullurl:
        :param args:
        :param kwargs:
        :return:
        """
        if isinstance(fullurl, six.string_types):
            return fullurl
        else:
            return fullurl.get_full_url()

    wrap_external_trace(module, 'OpenerDirector.open', 'urllib2', url_opener_open, exception_wrapper=wrap_exception)