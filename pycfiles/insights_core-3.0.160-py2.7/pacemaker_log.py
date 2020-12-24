# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/insights/parsers/pacemaker_log.py
# Compiled at: 2019-05-16 13:41:33
"""
PacemakerLog - file ``/var/log/pacemaker.log``
==============================================
"""
from .. import LogFileOutput, parser
from insights.specs import Specs

@parser(Specs.pacemaker_log)
class PacemakerLog(LogFileOutput):
    """
    Read the pacemaker log file.  Uses the ``LogFileOutput`` class parser
    functionality.

    .. note::
        Please refer to its super-class :class:`insights.core.LogFileOutput`

    Sample pacemaker.log::

        Aug 21 12:58:40 [11656] example.redhat.com        cib:     info: crm_client_destroy:    Destroying 0 events
        Aug 21 12:59:53 [11655] example.redhat.com pacemakerd:     info: pcmk_quorum_notification:      Membership 12: quorum retained (3)
        Aug 21 12:59:53 [11661] example.redhat.com       crmd:     info: pcmk_quorum_notification:      Membership 12: quorum retained (3)
        Aug 21 12:59:53 [11655] example.redhat.com pacemakerd:     info: pcmk_quorum_notification:      Membership 12: quorum retained (3)

    .. note::
        Because pacemaker timestamps by default have no year, the
        year of the logs will be inferred from the year in your timestamp.
        This will also work around December/January crossovers.

    Examples:
        >>> pm = shared(PacemakerLog)
        >>> pm.get('crmd')[0]['raw_message']
        'Aug 21 12:59:53 [11661] example.redhat.comm       crmd:     info: pcmk_quorum_notification:    Membership 12: quorum retained (3)'
        >>> from datetime import datetime
        >>> len(list(pm.get_after(datetime(21, 8, 2017, 12, 59, 50))))
        3
    """
    time_format = '%b %d %H:%M:%S'