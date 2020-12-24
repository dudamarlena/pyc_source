# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/insights/parsers/cron_daily_rhsmd.py
# Compiled at: 2020-04-23 14:49:03
"""
CronDailyRhsmd - file ``/etc/cron.daily/rhsmd``
===============================================
"""
from insights.core import Scannable
from insights.core.plugins import parser
from insights.specs import Specs

@parser(Specs.cron_daily_rhsmd)
class CronDailyRhsmd(Scannable):
    """
    Parse the ``/etc/cron.daily/rhsmd`` file.

    Sample input::

        config=$(grep -E "^processTimeout" /etc/rhsm/rhsm.conf | grep -Po "[0-9]+")
        rhsmd_timeout=$config
        abc=$config

    .. note::
        Please refer to its super-class :py:class:`insights.core.Scannable`
        for full usage.

    Examples:

        >>> # CronDailyRhsmd.collect('config_lines', lambda n: n if "$config" in n else "")
        >>> # CronDailyRhsmd.any('one_config_line', lambda n: n if "$config" in n else "")
        >>> rhsmd.config_lines
        ['rhsmd_timeout=$config', 'abc=$config']
        >>> rhsmd.one_config_line
        'rhsmd_timeout=$config'
    """
    pass