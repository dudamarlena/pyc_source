# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.8-x86_64/egg/vas/gemfire/CacheServerLogs.py
# Compiled at: 2012-11-01 11:35:36
from vas.shared.Logs import Logs, Log

class CacheServerLogs(Logs):
    """Used to enumerate a cache server node instance's logs

    :ivar `vas.shared.Security.Security`    security:   The resource's security
    """

    def __init__(self, client, location):
        super(CacheServerLogs, self).__init__(client, location, CacheServerLog)


class CacheServerLog(Log):
    """A log file in a cache server node instance

    :ivar `vas.gemfire.CacheServerNodeInstances.CacheServerNodeInstance`    instance:       The node instance that the
                                                                                            log belongs to
    :ivar `datetime.datetime`                                               last_modified:  The last modified stamp of
                                                                                            the log
    :ivar str                                                               name:           The name of the log
    :ivar `vas.shared.Security.Security`                                    security:       The resource's security
    :ivar int                                                               size:           The size of the log
    """

    def __init__(self, client, location):
        super(CacheServerLog, self).__init__(client, location, 'cache-server-node-instance', CacheServerNodeInstance)


from vas.gemfire.CacheServerNodeInstances import CacheServerNodeInstance