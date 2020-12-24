# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/site-packages/pycrunchbase/resource/job.py
# Compiled at: 2017-01-13 23:45:16
import six
from .node import Node
from .utils import parse_date

@six.python_2_unicode_compatible
class Job(Node):
    """Represents a Job on CrunchBase"""
    KNOWN_PROPERTIES = [
     'title',
     'is_current',
     'started_on',
     'started_on_trust_code',
     'ended_on',
     'ended_on_trust_code',
     'created_at',
     'updated_at']
    KNOWN_RELATIONSHIPS = [
     'person',
     'organization']

    def _coerce_values(self):
        for attr in ['started_on', 'ended_on']:
            if getattr(self, attr, None):
                setattr(self, attr, parse_date(getattr(self, attr)))

        return

    def __str__(self):
        return ('{title}').format(title=self.title)

    def __repr__(self):
        return self.__str__()