# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.12-x86_64/egg/cmislib/model.py
# Compiled at: 2016-12-29 18:00:54
"""
The model module contains the CmisClient object, which is responsible for
keeping track of connection information. The name 'model' is no longer
really appropriate, but it is kept for backwards compatibility.
"""
import logging
from cmislib.atompub.binding import AtomPubBinding
from cmislib.cmis_services import Binding
moduleLogger = logging.getLogger('cmislib.model')

class CmisClient(object):
    """
    Handles all communication with the CMIS provider.
    """

    def __init__(self, repositoryUrl, username, password, **kwargs):
        """
        This is the entry point to the API. You need to know the
        :param repositoryUrl: The service URL of the CMIS provider
        :param username: Username
        :param password: Password

        >>> client = CmisClient('http://localhost:8080/alfresco/s/cmis', 'admin', 'admin')
        """
        self.repositoryUrl = repositoryUrl
        self.username = username
        self.password = password
        self.extArgs = kwargs
        if kwargs.has_key('binding') and isinstance(kwargs['binding'], Binding):
            self.binding = kwargs['binding']
        else:
            self.binding = AtomPubBinding(**kwargs)
        self.logger = logging.getLogger('cmislib.model.CmisClient')
        self.logger.debug('Creating an instance of CmisClient')

    def __str__(self):
        """To string"""
        return 'CMIS client connection to %s' % self.repositoryUrl

    def getRepositories(self):
        """
        Returns a dict of high-level info about the repositories available at
        this service. The dict contains entries for 'repositoryId' and
        'repositoryName'.

        >>> client.getRepositories()
        [{'repositoryName': u'Main Repository', 'repositoryId': u'83beb297-a6fa-4ac5-844b-98c871c0eea9'}]
        """
        return self.binding.getRepositoryService().getRepositories(self)

    def getRepository(self, repositoryId):
        """
        Returns the repository identified by the specified repositoryId.

        >>> repo = client.getRepository('83beb297-a6fa-4ac5-844b-98c871c0eea9')
        >>> repo.getRepositoryName()
        u'Main Repository'
        """
        return self.binding.getRepositoryService().getRepository(self, repositoryId)

    def getDefaultRepository(self):
        """
        There does not appear to be anything in the spec that identifies
        a repository as being the default, so we'll define it to be the
        first one in the list.

        >>> repo = client.getDefaultRepository()
        >>> repo.getRepositoryId()
        u'83beb297-a6fa-4ac5-844b-98c871c0eea9'
        """
        return self.binding.getRepositoryService().getDefaultRepository(self)

    defaultRepository = property(getDefaultRepository)
    repositories = property(getRepositories)