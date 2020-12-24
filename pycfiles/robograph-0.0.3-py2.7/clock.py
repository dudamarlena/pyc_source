# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/robograph/datamodel/nodes/lib/clock.py
# Compiled at: 2016-07-13 17:51:17
import datetime
from robograph.datamodel.base import node

class Date(node.Node):
    _reqs = []
    DEFAULT_DATE_FORMAT = '%Y-%m-%d'

    def output(self):
        return datetime.datetime.today().strftime(self.DEFAULT_DATE_FORMAT)


class FormattedDate(Date):
    _reqs = [
     'format']

    def output(self):
        if self._params['format'] is None:
            fmt = self.DEFAULT_DATE_FORMAT
        else:
            fmt = self._params['format']
        return datetime.datetime.today().strftime(fmt)


class Now(node.Node):
    _reqs = []
    DEFAULT_DATETIME_FORMAT = '%Y-%m-%dT%H:%M:%S%z'

    def output(self):
        return datetime.datetime.now().strftime(self.DEFAULT_DATETIME_FORMAT)


class UtcNow(Now):

    def output(self):
        return datetime.datetime.utcnow().strftime(self.DEFAULT_DATETIME_FORMAT)