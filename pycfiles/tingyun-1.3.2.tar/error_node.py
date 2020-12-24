# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/nb/publish/btw/tingyun/tingyun/logistics/warehouse/error_node.py
# Compiled at: 2016-06-30 06:13:10
from collections import namedtuple
_ErrorNode = namedtuple('_ErrorNode', ['error_time', 'http_status', 'error_class_name', 'uri', 'thread_name',
 'message', 'stack_trace', 'request_params', 'tracker_type', 'referer'])
_ExternalNode = namedtuple('_ExternalNode', ['error_time', 'status_code', 'url', 'thread_name', 'tracker_type',
 'error_class_name', 'stack_trace', 'request_params',
 'http_status'])

class ErrorNode(_ErrorNode):
    """

    """
    pass


class ExternalErrorNode(_ExternalNode):
    """
    """
    pass