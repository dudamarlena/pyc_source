# uncompyle6 version 3.6.7
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/jpopelka/git/user-cont/colin/colin/utils/cont.py
# Compiled at: 2018-09-17 04:16:15
# Size of source mod 2**32: 2590 bytes
__doc__ = '\nThis is a temporary module to support unpriv way of interacting with container images.\n\nIt will be migrated to conu sooner or later.\n'
import logging
logger = logging.getLogger(__name__)

class ImageName(object):
    """ImageName"""

    def __init__(self, registry=None, namespace=None, repository=None, tag=None, digest=None):
        self.registry = registry
        self.namespace = namespace
        self.repository = repository
        self.digest = digest
        self.tag = tag

    @classmethod
    def parse(cls, image_name):
        """
        Get the instance of ImageName from the string representation.

        :param image_name: str (any possible form of image name)
        :return: ImageName instance
        """
        result = cls()
        s = image_name.split('/', 2)
        if len(s) == 2:
            if '.' in s[0] or ':' in s[0]:
                result.registry = s[0]
            else:
                result.namespace = s[0]
        else:
            if len(s) == 3:
                result.registry = s[0]
                result.namespace = s[1]
        result.repository = s[(-1)]
        try:
            result.repository, result.digest = result.repository.rsplit('@', 1)
        except ValueError:
            try:
                result.repository, result.tag = result.repository.rsplit(':', 1)
            except ValueError:
                result.tag = 'latest'

        return result

    def __str__(self):
        return "Image: registry='{}' namespace='{}' repository='{}' tag='{}' digest='{}'".format(self.registry, self.namespace, self.repository, self.tag, self.digest)

    @property
    def name(self):
        """
        Get the string representation of the image
        (registry, namespace, repository and digest together).

        :return: str
        """
        name_parts = []
        if self.registry:
            name_parts.append(self.registry)
        if self.namespace:
            name_parts.append(self.namespace)
        if self.repository:
            name_parts.append(self.repository)
        name = '/'.join(name_parts)
        if self.digest:
            name += '@{}'.format(self.digest)
        else:
            if self.tag:
                name += ':{}'.format(self.tag)
        return name