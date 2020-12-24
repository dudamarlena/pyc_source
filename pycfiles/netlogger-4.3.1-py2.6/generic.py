# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-x86_64/egg/netlogger/parsers/modules/generic.py
# Compiled at: 2010-04-29 00:14:32
"""
Generic parser that uses a fixed event name and puts all the
information in a single string-valued attribute.
"""
__author__ = 'Dan Gunter dkgunter@lbl.gov'
__rcsid__ = '$Id: generic.py 24753 2010-04-29 04:14:31Z dang $'
from logging import DEBUG
import time
from netlogger.parsers.base import BaseParser

class Parser(BaseParser):
    """Generic parser that uses a fixed event name and puts all the
    information in a single string-valued attribute.

    Parameters:
        - attribute_name {STRING,'msg'*}: Output name for the attribute containing 
                                          the input line.
        - event_name {STRING,'event'*}: Output event name
    """

    def __init__(self, f, attribute_name='msg', event_name='event', **kwargs):
        BaseParser.__init__(self, f, fullname=__name__, **kwargs)
        self.event = event_name
        self.attr = attribute_name

    def process(self, line):
        self.log.debug('process.start')
        now = time.time()
        result = ({'ts': now, 'event': self.event, self.attr: line},)
        self.log.debug('process.end', status=0, n=len(result))
        return result