# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /webapp/bulbs/poll/sodahead.py
# Compiled at: 2016-09-22 15:00:17
# Size of source mod 2**32: 909 bytes
from django.conf import settings
from rest_framework.exceptions import APIException
SODAHEAD_DATE_FORMAT = '%m/%d/%y %I:%M %p'
SODAHEAD_POLL_ENDPOINT = '{}/api/polls/{{}}/'.format(settings.SODAHEAD_BASE_URL)
SODAHEAD_POLLS_ENDPOINT = '{}/api/polls/'.format(settings.SODAHEAD_BASE_URL)
SODAHEAD_DELETE_POLL_ENDPOINT = '{}/api/polls/{{}}/?access_token={{}}'.format(settings.SODAHEAD_BASE_URL)
BLANK_ANSWER = 'Intentionally blank'
DEFAULT_ANSWER_1 = 'default answer 1'
DEFAULT_ANSWER_2 = 'default answer 2'

class SodaheadResponseError(APIException):
    status_code = 503
    default_detail = 'Third-party poll provider temporarily unavailable.'

    def __init__(self, detail):
        self.detail = detail


class SodaheadResponseFailure(APIException):
    status_code = 400
    default_detail = 'Error from third-party poll provider'

    def __init__(self, detail):
        self.detail = detail