# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.12-x86_64/egg/cmislib/cmis_services.py
# Compiled at: 2016-12-29 16:44:56
__doc__ = '\nThis module contains the base Binding class and other service objects.\n'
from cmislib.exceptions import CmisException, RuntimeException, ObjectNotFoundException, InvalidArgumentException, PermissionDeniedException, NotSupportedException, UpdateConflictException

class Binding(object):
    """
    Represents the binding used to communicate with the CMIS server.
    """

    def getRepositoryService(self):
        """
        Returns the repository service specific to this binding.
        """
        pass

    def _processCommonErrors(self, error, url):
        """
        Maps HTTPErrors that are common to all to exceptions. Only errors
        that are truly global, like 401 not authorized, should be handled
        here. Callers should handle the rest.
        """
        if error['status'] == '401':
            raise PermissionDeniedException(error['status'], url)
        elif error['status'] == '400':
            raise InvalidArgumentException(error['status'], url)
        elif error['status'] == '404':
            raise ObjectNotFoundException(error['status'], url)
        elif error['status'] == '403':
            raise PermissionDeniedException(error['status'], url)
        elif error['status'] == '405':
            raise NotSupportedException(error['status'], url)
        elif error['status'] == '409':
            raise UpdateConflictException(error['status'], url)
        elif error['status'] == '500':
            raise RuntimeException(error['status'], url)
        else:
            raise CmisException(error['status'], url)


class RepositoryServiceIfc(object):
    """
    Defines the interface for the repository service.
    """

    def getRepositories(self, client):
        """
        Returns a list of repositories for this server.
        """
        pass

    def getRepositoryInfo(self):
        """
        Returns the repository information for this server.
        """
        pass