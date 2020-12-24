# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/local/lib/python2.7/site-packages/pycrunchbase/resource/degree.py
# Compiled at: 2017-01-13 23:45:16
import six
from .node import Node
from .utils import parse_date

@six.python_2_unicode_compatible
class Degree(Node):
    """Represents a Degree on CrunchBase"""
    KNOWN_PROPERTIES = [
     'started_on',
     'started_on_trust_code',
     'is_completed',
     'completed_on',
     'completed_on_trust_code',
     'degree_type_name',
     'degree_subject',
     'created_at',
     'updated_at']
    KNOWN_RELATIONSHIPS = [
     'school',
     'person']

    def _coerce_values(self):
        for attr in ['started_on', 'completed_on']:
            if getattr(self, attr, None):
                setattr(self, attr, parse_date(getattr(self, attr)))

        return

    def __str__(self):
        return ('{name} {subject}').format(name=self.degree_type_name, subject=self.degree_subject)

    def __repr__(self):
        return self.__str__()