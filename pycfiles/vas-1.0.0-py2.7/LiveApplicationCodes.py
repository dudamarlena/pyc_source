# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.8-x86_64/egg/vas/gemfire/LiveApplicationCodes.py
# Compiled at: 2012-11-01 11:35:36
from vas.shared.Collection import Collection

class LiveApplicationCodes(Collection):
    """Used to enumerate a cache server's live application code

    :ivar `vas.shared.Security.Security`    security:   The resource's security
    """

    def __init__(self, client, location):
        super(LiveApplicationCodes, self).__init__(client, location, 'live-application-code', ApplicationCode)


from vas.gemfire.ApplicationCode import ApplicationCode