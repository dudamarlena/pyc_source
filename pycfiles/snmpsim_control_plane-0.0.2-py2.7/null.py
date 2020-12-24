# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/snmpsim_control_plane/supervisor/reporting/formats/null.py
# Compiled at: 2020-01-30 12:14:23
from snmpsim_control_plane.supervisor.reporting.formats import base

class NullReporter(base.BaseReporter):
    """No-op activity metrics reporter.
    """
    pass