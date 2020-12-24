# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/taurus/core/util/report/report.py
# Compiled at: 2019-08-19 15:09:29
"""This module provides a panel to display taurus messages"""
from builtins import object
__all__ = [
 'TaurusMessageReportHandler']
__docformat__ = 'restructuredtext'

class TaurusMessageReportHandler(object):
    Label = 'Default report handler'

    def __init__(self, parent):
        self.parent = parent

    def report(self, message):
        pass