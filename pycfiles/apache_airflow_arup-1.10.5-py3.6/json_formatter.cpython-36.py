# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/utils/log/json_formatter.py
# Compiled at: 2019-09-11 03:47:35
# Size of source mod 2**32: 1798 bytes
"""
json_formatter module stores all related to ElasticSearch specific logger classes
"""
import logging, json

def merge_dicts(d1, d2):
    """
    Merge two dicts
    """
    merged = d1.copy()
    merged.update(d2)
    return merged


class JSONFormatter(logging.Formatter):
    __doc__ = '\n    JSONFormatter instances are used to convert a log record to json.\n    '

    def __init__(self, fmt=None, datefmt=None, json_fields=None, extras=None):
        super(JSONFormatter, self).__init__(fmt, datefmt)
        if extras is None:
            extras = {}
        if json_fields is None:
            json_fields = []
        self.json_fields = json_fields
        self.extras = extras

    def format(self, record):
        super(JSONFormatter, self).format(record)
        record_dict = {label:getattr(record, label, None) for label in self.json_fields}
        merged_record = merge_dicts(record_dict, self.extras)
        return json.dumps(merged_record)