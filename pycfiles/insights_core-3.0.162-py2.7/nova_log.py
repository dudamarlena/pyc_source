# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/insights/parsers/nova_log.py
# Compiled at: 2019-05-16 13:41:33
"""
nova_log - files ``/var/log/nova/*.log``
========================================
This module contains classes to parse logs under ``/var/log/nova/``
"""
from .. import LogFileOutput, parser
from insights.specs import Specs

@parser(Specs.nova_api_log)
class NovaApiLog(LogFileOutput):
    """Class for parsing the ``/var/log/nova/nova-api.log`` file.

    .. note::
        Please refer to its super-class :class:`insights.core.LogFileOutput`
    """
    pass


@parser(Specs.nova_compute_log)
class NovaComputeLog(LogFileOutput):
    """Class for parsing the ``/var/log/nova/nova-compute.log`` file.

    .. note::
        Please refer to its super-class :class:`insights.core.LogFileOutput`
    """
    pass