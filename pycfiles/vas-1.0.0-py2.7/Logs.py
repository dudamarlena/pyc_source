# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.8-x86_64/egg/vas/web_server/Logs.py
# Compiled at: 2012-11-01 11:36:39
import vas.shared.Logs

class Logs(vas.shared.Logs.Logs):
    """Used to enumerate a Web Server node instance's logs

    :ivar `vas.shared.Security.Security`    security:   The resource's security
    """

    def __init__(self, client, location):
        super(Logs, self).__init__(client, location, Log)


class Log(vas.shared.Logs.Log):
    """A log file in a Web Server node instance

    :ivar `vas.web_server.NodeInstances.NodeInstance`   instance:       The node instance that the log belongs to
    :ivar `datetime.datetime`                           last_modified:  The last modified stamp of the log
    :ivar str                                           name:           The name of the log
    :ivar `vas.shared.Security.Security`                security:       The resource's security
    :ivar int                                           size:           The size of the log
    """

    def __init__(self, client, location):
        super(Log, self).__init__(client, location, 'node-instance', NodeInstance)


from vas.web_server.NodeInstances import NodeInstance