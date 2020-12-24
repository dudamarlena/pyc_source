# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.8-x86_64/egg/vas/tc_server/TemplateImages.py
# Compiled at: 2012-11-01 11:37:44
from vas.shared.Deletable import Deletable
from vas.shared.MutableCollection import MutableCollection
from vas.shared.Resource import Resource

class TemplateImages(MutableCollection):
    """ Used to enumerate, create, and delete tc Server template images

    :ivar `vas.shared.Security.Security`    security:   The resource's security
    """

    def __init__(self, client, location):
        super(TemplateImages, self).__init__(client, location, 'template-images', TemplateImage)

    def create(self, path, name, version):
        """Creates a new template image by uploading a ``.zip`` file to the server

        :param str  path:       The path of the template image ``.zip`` file
        :param str  name:       The name of the template image
        :param str  version:    The version of the template image
        :rtype:     :class:`vas.tc_server.TemplateImages.TemplateImage`
        :return:    The new template image
        """
        return self._create_multipart(path, {'name': name, 'version': version})


class TemplateImage(Resource, Deletable):
    """A template image

    :ivar str                               name:       The template image's name
    :ivar `vas.shared.Security.Security`    security:   The resource's security
    :ivar int                               size:       The template image's size
    :ivar list                              templates:  The templates that have been created from the template image
    :ivar str                               version:    The template image's version
    """

    @property
    def name(self):
        return self.__name

    @property
    def size(self):
        return self.__size

    @property
    def templates(self):
        self.__templates = self.__templates or self._create_resources_from_links('template', Template)
        return self.__templates

    @property
    def version(self):
        return self.__version

    def __init__(self, client, location):
        super(TemplateImage, self).__init__(client, location)
        self.__name = self._details['name']
        self.__size = self._details['size']
        self.__version = self._details['version']

    def reload(self):
        """Reloads the template image's details from the server"""
        super(TemplateImage, self).reload()
        self.__templates = None
        return

    def __str__(self):
        return ('<{} name={} version={} size={}>').format(self.__class__.__name__, self.__name, self.__version, self.__size)


from vas.tc_server.Templates import Template