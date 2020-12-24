# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-intel/egg/sorl/thumbnail/kvstores/base.py
# Compiled at: 2012-12-12 10:05:53
from sorl.thumbnail.conf import settings
from sorl.thumbnail.helpers import serialize, deserialize, ThumbnailError
from sorl.thumbnail.images import serialize_image_file, deserialize_image_file

def add_prefix(key, identity='image'):
    """
    Adds prefixes to the key
    """
    return ('||').join([settings.THUMBNAIL_KEY_PREFIX, identity, key])


def del_prefix(key):
    """
    Removes prefixes from the key
    """
    return key.split('||')[(-1)]


class KVStoreBase(object):

    def get(self, image_file):
        """
        Gets the ``image_file`` from store. Returns ``None`` if not found.
        """
        return self._get(image_file.key)

    def set(self, image_file, source=None):
        """
        Updates store for the `image_file`. Makes sure the `image_file` has a
        size set.
        """
        image_file.set_size()
        self._set(image_file.key, image_file)
        if source is not None:
            if not self.get(source):
                raise ThumbnailError('Cannot add thumbnails for source: `%s` that is not in kvstore.' % source.name)
            thumbnails = self._get(source.key, identity='thumbnails') or []
            thumbnails = set(thumbnails)
            thumbnails.add(image_file.key)
            self._set(source.key, list(thumbnails), identity='thumbnails')
        return

    def get_or_set(self, image_file):
        cached = self.get(image_file)
        if cached is not None:
            return cached
        else:
            self.set(image_file)
            return image_file

    def delete(self, image_file, delete_thumbnails=True):
        """
        Deletes the referense to the ``image_file`` and deletes the references
        to thumbnails as well as thumbnail files if ``delete_thumbnails`` is
        `True``. Does not delete the ``image_file`` is self.
        """
        if delete_thumbnails:
            self.delete_thumbnails(image_file)
        self._delete(image_file.key)

    def delete_thumbnails(self, image_file):
        """
        Deletes references to thumbnails as well as thumbnail ``image_files``.
        """
        thumbnail_keys = self._get(image_file.key, identity='thumbnails')
        if thumbnail_keys:
            for key in thumbnail_keys:
                thumbnail = self._get(key)
                if thumbnail:
                    self.delete(thumbnail)
                    thumbnail.delete()

            self._delete(image_file.key, identity='thumbnails')

    def cleanup(self):
        """
        Cleans up the key value store. In detail:
        1. Deletes all key store references for image_files that do not exist
           and all key references for its thumbnails *and* their image_files.
        2. Deletes or updates all invalid thumbnail keys
        """
        for key in self._find_keys(identity='image'):
            image_file = self._get(key)
            if image_file and not image_file.exists():
                self.delete(image_file)

        for key in self._find_keys(identity='thumbnails'):
            image_file = self._get(key)
            if image_file:
                thumbnail_keys = self._get(key, identity='thumbnails') or []
                thumbnail_keys_set = set(thumbnail_keys)
                for thumbnail_key in thumbnail_keys:
                    if not self._get(thumbnail_key):
                        thumbnail_keys_set.remove(thumbnail_key)

                thumbnail_keys = list(thumbnail_keys_set)
                if thumbnail_keys:
                    self._set(key, thumbnail_keys, identity='thumbnails')
                    return
            self._delete(key, identity='thumbnails')

    def clear(self):
        """
        Brutely clears the key value store for keys with THUMBNAIL_KEY_PREFIX
        prefix. Use this in emergency situations. Normally you would probably
        want to use the ``cleanup`` method instead.
        """
        all_keys = self._find_keys_raw(settings.THUMBNAIL_KEY_PREFIX)
        self._delete_raw(*all_keys)

    def _get(self, key, identity='image'):
        """
        Deserializing, prefix wrapper for _get_raw
        """
        value = self._get_raw(add_prefix(key, identity))
        if value is None:
            return
        else:
            if identity == 'image':
                return deserialize_image_file(value)
            return deserialize(value)

    def _set(self, key, value, identity='image'):
        """
        Serializing, prefix wrapper for _set_raw
        """
        if identity == 'image':
            s = serialize_image_file(value)
        else:
            s = serialize(value)
        self._set_raw(add_prefix(key, identity), s)

    def _delete(self, key, identity='image'):
        """
        Prefix wrapper for _delete_raw
        """
        self._delete_raw(add_prefix(key, identity))

    def _find_keys(self, identity='image'):
        """
        Finds and returns all keys for identity,
        """
        prefix = add_prefix('', identity)
        raw_keys = self._find_keys_raw(prefix) or []
        for raw_key in raw_keys:
            yield del_prefix(raw_key)

    def _get_raw(self, key):
        """
        Gets the value from keystore, returns `None` if not found.
        """
        raise NotImplemented()

    def _set_raw(self, key, value):
        """
        Sets value associated to key. Key is expected to be shorter than 200
        chars. Value is a ``unicode`` object with an unknown (reasonable)
        length.
        """
        raise NotImplemented()

    def _delete_raw(self, *keys):
        """
        Deletes the keys. Silent failure for missing keys.
        """
        raise NotImplemented()

    def _find_keys_raw(self, prefix):
        """
        Finds all keys with prefix
        """
        raise NotImplemented()