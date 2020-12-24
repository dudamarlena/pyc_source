# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.8-x86_64/egg/vas/gemfire/PendingApplicationCodes.py
# Compiled at: 2012-11-01 11:35:36
from vas.gemfire.ApplicationCode import ApplicationCode
from vas.shared.Deletable import Deletable
from vas.shared.MutableCollection import MutableCollection

class PendingApplicationCodes(MutableCollection):
    """Used to enumerate, create, and delete a cache server's pending application code

    :ivar `vas.shared.Security.Security`    security:   The resource's security
    """

    def __init__(self, client, location):
        super(PendingApplicationCodes, self).__init__(client, location, 'pending-application-code', PendingApplicationCode)

    def create(self, image):
        """Creates a new pending application code

        :param `vas.gemfire.ApplicationCodeImages.ApplicationCodeImage` image:  The image to create the application code
                                                                                from
        :rtype:     :class:`vas.gemfire.PendingApplicationCodes.PendingApplicationCode`
        :return:    The new application code
        """
        return self._create({'image': image._location})


class PendingApplicationCode(ApplicationCode, Deletable):
    """An application code that is pending

    :ivar `vas.gemfire.ApplicationCodeImages.ApplicationCodeImage`  application_code_image: The image that was used to
                                                                                            create the application code
    :ivar `vas.gemfire.CacheServerInstances.CacheServerInstance`    instance:               The cache server instance
                                                                                            that contains the
                                                                                            application code
    :ivar str                                                       name:                   The name of the application
                                                                                            code
    :ivar `vas.shared.Security.Security`                            security:               The resource's security
    :ivar str                                                       version:                The version of the
                                                                                            application code
    """
    pass