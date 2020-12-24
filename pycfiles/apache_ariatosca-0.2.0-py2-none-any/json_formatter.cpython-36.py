# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/airflow/utils/log/json_formatter.py
# Compiled at: 2019-09-11 03:47:35
# Size of source mod 2**32: 1798 bytes
__doc__ = '\njson_formatter module stores all related to ElasticSearch specific logger classes\n'
import logging, json

def merge_dicts(d1, d2):
    """
    Merge two dicts
    """
    merged = d1.copy()
    merged.update(d2)
    return merged


class JSONFormatter(logging.Formatter):
    """JSONFormatter"""

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