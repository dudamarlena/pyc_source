# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.8-x86_64/egg/vas/rabbitmq/PluginImages.py
# Compiled at: 2012-11-01 11:37:44
from vas.shared.Deletable import Deletable
from vas.shared.MutableCollection import MutableCollection
from vas.shared.Resource import Resource

class PluginImages(MutableCollection):
    """Used to enumerate, create, and delete RabbitMQ plugin images

    :ivar `vas.shared.Security.Security`    security:   The resource's security
    """

    def __init__(self, client, location):
        super(PluginImages, self).__init__(client, location, 'plugin-images', PluginImage)

    def create(self, path):
        """Creates a new plugin image by uploading a file

        :param str  path:   The path of the plugin ``.ez`` file to upload
        :rtype:     :class:`vas.rabbitmq.PluginImages.PluginImage`
        :return:    The new plugin image
        """
        return self._create_multipart(path)


class PluginImage(Resource, Deletable):
    """A plugin image

    :ivar str                               name:       The plugin image's name
    :ivar `vas.rabbitmq.Plugins.Plugins`    plugins:    The plugins that have been created from this plugin image
    :ivar `vas.shared.Security.Security`    security:   The resource's security
    :ivar int                               size:       The plugin image's size
    :ivar str                               version:    The plugin image's version
    """

    @property
    def name(self):
        return self.__name

    @property
    def plugins(self):
        self.__plugins = self.__plugins or self._create_resources_from_links('plugin', Plugin)
        return self.__plugins

    @property
    def size(self):
        return self.__size

    @property
    def version(self):
        return self.__version

    def __init__(self, client, location):
        super(PluginImage, self).__init__(client, location)
        self.__name = self._details['name']
        self.__size = self._details['size']
        self.__version = self._details['version']

    def reload(self):
        """Reloads the plugin image's details from the server"""
        super(PluginImage, self).reload()
        self.__plugins = None
        return

    def __str__(self):
        return ('<{} name={} size={} version={}>').format(self.__class__.__name__, self.__name, self.__size, self.__version)


from vas.rabbitmq.Plugins import Plugin