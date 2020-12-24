# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/mediagoblin/tools/processing.py
# Compiled at: 2016-02-04 13:34:40
# Size of source mod 2**32: 2545 bytes
import logging, json, traceback
from six.moves.urllib import request, parse
_log = logging.getLogger(__name__)
TESTS_CALLBACKS = {}

def create_post_request(url, data, **kw):
    """
    Issue a HTTP POST request.

    Args:
        url: The URL to which the POST request should be issued
        data: The data to be send in the body of the request
        **kw:
        data_parser: The parser function that is used to parse the `data`
            argument
    """
    data_parser = kw.get('data_parser', parse.urlencode)
    headers = kw.get('headers', {})
    return request.Request(url, data_parser(data), headers=headers)


def json_processing_callback(entry):
    """
    Send an HTTP post to the registered callback url, if any.
    """
    if not entry.processing_metadata:
        _log.debug('No processing callback URL for {0}'.format(entry))
        return
    url = entry.processing_metadata[0].callback_url
    _log.debug('Sending processing callback for {0} to {1}'.format(entry, url))
    headers = {'Content-Type': 'application/json'}
    data = {'id': entry.id, 
     'state': entry.state}
    if url.endswith('secrettestmediagoblinparam'):
        TESTS_CALLBACKS.update({url: data})
        return True
    request = create_post_request(url, data, headers=headers, data_parser=json.dumps)
    try:
        request.urlopen(request)
        _log.debug('Processing callback for {0} sent'.format(entry))
        return True
    except request.HTTPError:
        _log.error('Failed to send callback: {0}'.format(traceback.format_exc()))
        return False