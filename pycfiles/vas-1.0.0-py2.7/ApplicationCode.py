# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.8-x86_64/egg/vas/gemfire/ApplicationCode.py
# Compiled at: 2012-11-01 11:37:44
from vas.shared.Resource import Resource
from vas.util.LinkUtils import LinkUtils

class ApplicationCode(Resource):
    """Application code in a cache server instance

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
    __application_code_image = None
    __instance = None

    @property
    def application_code_image(self):
        self.__application_code_image = self.__application_code_image or ApplicationCodeImage(self._client, self.__application_code_image_location)
        return self.__application_code_image

    @property
    def instance(self):
        self.__instance = self.__instance or CacheServerInstance(self._client, self.__instance_location)
        return self.__instance

    @property
    def name(self):
        return self.__name

    @property
    def version(self):
        return self.__version

    def __init__(self, client, location):
        super(ApplicationCode, self).__init__(client, location)
        self.__name = self._details['name']
        self.__version = self._details['version']
        self.__application_code_image_location = LinkUtils.get_link_href(self._details, 'application-code-image')
        self.__instance_location = LinkUtils.get_link_href(self._details, 'cache-server-group-instance')

    def __str__(self):
        return ('<{} name={} version={}>').format(self.__class__.__name__, self.__name, self.__version)


from vas.gemfire.ApplicationCodeImages import ApplicationCodeImage
from vas.gemfire.CacheServerInstances import CacheServerInstance