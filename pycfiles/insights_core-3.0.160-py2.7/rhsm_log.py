# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/insights/parsers/rhsm_log.py
# Compiled at: 2019-05-16 13:41:33
from .. import LogFileOutput, parser
from insights.specs import Specs

@parser(Specs.rhsm_log)
class RhsmLog(LogFileOutput):
    """
    Class for parsing the log file: ``/var/log/rhsm/rhsm.log``.

    .. note::
        Please refer to its super-class :class:`insights.core.LogFileOutput`
    """
    pass