# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/dockermap/map/policy/cache.py
# Compiled at: 2019-10-19 14:38:08
# Size of source mod 2**32: 5320 bytes
from __future__ import unicode_literals

class CachedItems(object):
    __doc__ = '\n    Abstract implementation for a caching collection of client names or ids.\n\n    :param client: Client object.\n    :type client: docker.client.Client\n    '

    def __init__(self, client):
        self._client = client
        super(CachedItems, self).__init__()
        self.refresh()

    def refresh(self):
        """
        Forces a refresh of the cached items. Does not need to return anything.
        """
        raise NotImplementedError("Method 'refresh' is not implemented.")


class CachedImages(CachedItems, dict):
    __doc__ = '\n    Dictionary of image names and ids, which also keeps track of the client object to pull images if necessary.\n    '

    def _update(self, image_list):
        for image in image_list:
            tags = image.get('RepoTags')
            if tags:
                self.update({tag:image['Id'] for tag in tags})

    def refresh(self):
        """
        Fetches image and their ids from the client.
        """
        if not self._client:
            return
        current_images = self._client.images()
        self.clear()
        self._update(current_images)
        for image in current_images:
            tags = image.get('RepoTags')
            if tags:
                self.update({tag:image['Id'] for tag in tags})

    def refresh_repo(self, name):
        if not self._client:
            return
        self._update(self._client.images(name=name))


class CachedContainerNames(CachedItems, dict):

    def refresh(self):
        """
        Fetches all current container names from the client, along with their id.
        """
        if not self._client:
            return
        current_containers = self._client.containers(all=True)
        self.clear()
        for container in current_containers:
            container_names = container.get('Names')
            if container_names:
                c_id = container['Id']
                self.update(((name[1:], c_id) for name in container_names))


class CachedNetworkNames(CachedItems, dict):

    def refresh(self):
        """
        Fetches all current network names from the client, along with their id.
        """
        if not self._client:
            return
        current_networks = self._client.networks()
        self.clear()
        self.update(((net['Name'], net['Id']) for net in current_networks))


class CachedVolumeNames(CachedItems, set):

    def refresh(self):
        """
        Fetches all current network names from the client.
        """
        if not self._client:
            return
        current_volumes = self._client.volumes()['Volumes']
        self.clear()
        if current_volumes:
            self.update((vol['Name'] for vol in current_volumes))


class DockerHostItemCache(dict):
    __doc__ = '\n    Abstract class for implementing caches of items (containers, images) present on the Docker client, so that\n    their existence does not have to be checked separately for every action.\n\n    :param clients: Dictionary of clients with alias and client object.\n    :type clients: dict[unicode | str, dockermap.map.config.client.ClientConfiguration]\n    '
    item_class = None

    def __init__(self, clients, *args, **kwargs):
        self._clients = clients
        (super(DockerHostItemCache, self).__init__)(*args, **kwargs)

    def __getitem__(self, item):
        if item not in self:
            return self.refresh(item)
        return super(DockerHostItemCache, self).__getitem__(item)

    def refresh(self, item):
        """
        Forces a refresh of a cached item.

        :param item: Client name.
        :type item: unicode | str
        :return: Items in the cache.
        :rtype: DockerHostItemCache.item_class
        """
        client = self._clients[item].get_client()
        self[item] = val = self.item_class(client)
        return val


class ImageCache(DockerHostItemCache):
    __doc__ = '\n    Fetches and caches image names and ids from a Docker host.\n    '
    item_class = CachedImages


class ContainerCache(DockerHostItemCache):
    __doc__ = '\n    Fetches and caches container names from a Docker host.\n    '
    item_class = CachedContainerNames


class NetworkCache(DockerHostItemCache):
    __doc__ = '\n    Fetches and caches network names from a Docker host.\n    '
    item_class = CachedNetworkNames

    def refresh(self, item):
        client_config = self._clients[item]
        if client_config.features['networks']:
            return super(NetworkCache, self).refresh(item)
        raise ValueError('Client does not support network configuration.', item)


class VolumeCache(DockerHostItemCache):
    __doc__ = '\n    Fetches and caches volume names from a Docker host.\n    '
    item_class = CachedVolumeNames

    def refresh(self, item):
        client_config = self._clients[item]
        if client_config.features['volumes']:
            return super(VolumeCache, self).refresh(item)
        raise ValueError('Client does not support volume configuration.', item)