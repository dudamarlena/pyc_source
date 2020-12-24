# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/insights/parsers/secure.py
# Compiled at: 2019-05-16 13:41:33
"""
Secure -  file ``/var/log/secure``
==================================
"""
from .. import Syslog, parser
from insights.specs import Specs

@parser(Specs.secure)
class Secure(Syslog):
    """Class for parsing the ``/var/log/secure`` file.

    Sample log text::

        Aug 24 09:31:39 localhost polkitd[822]: Finished loading, compiling and executing 6 rules
        Aug 24 09:31:39 localhost polkitd[822]: Acquired the name org.freedesktop.PolicyKit1 on the system bus
        Aug 25 13:52:54 localhost sshd[23085]: pam_unix(sshd:session): session opened for user zjj by (uid=0)
        Aug 25 13:52:54 localhost sshd[23085]: error: openpty: No such file or directory

    .. note::
        Please refer to its super-class :class:`insights.core.Syslog`

    .. note::
        Because timestamps in the secure log by default have no year,
        the year of the logs will be inferred from the year in your
        timestamp. This will also work around December/January crossovers.

    Examples:
        >>> secure = shared[Secure]
        >>> secure.get('session opened')
        [{'timestamp':'Aug 25 13:52:54',
          'hostname':'localhost',
          'procname': 'sshd[23085]',
          'message': 'pam_unix(sshd:session): session opened for user zjj by (uid=0)',
          'raw_message': 'Aug 25 13:52:54 localhost sshd[23085]: pam_unix(sshd:session): session opened for user zjj by (uid=0)'
         }]
        >>> len(list(secure.get_after(datetime(2017, 8, 25, 0, 0, 0))))
        2
    """
    time_format = '%b %d %H:%M:%S'