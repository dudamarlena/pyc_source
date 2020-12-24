# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/f1nal/Dropbox/python/jet-bridge/src/packages/jet_bridge_base/jet_bridge_base/media_cache.py
# Compiled at: 2019-10-30 05:24:12
# Size of source mod 2**32: 2163 bytes
import os, hashlib
from jet_bridge_base.configuration import configuration

class MediaCache(object):
    max_cache_size = 52428800
    files = []
    size = 0
    dir = '_jet_cache'

    def __init__(self):
        self.update_files()

    def get_files(self):
        result = []
        if configuration.media_exists(self.dir):
            directories, files = configuration.media_listdir(self.dir)
            for f in files:
                fp = os.path.join(self.dir, f)
                result.append({'path':fp, 
                 'size':configuration.media_size(fp)})

            self.sort_files(result)
        return result

    def sort_files(self, files):
        files.sort(key=(lambda x: configuration.media_get_modified_time(x['path'])))

    def get_files_size(self, files):
        total_size = 0
        for file in files:
            total_size += file['size']

        return total_size

    def update_files(self):
        self.files = self.get_files()
        self.size = self.get_files_size(self.files)

    def add_file(self, path):
        absolute_path = cache.full_path(path)
        size = configuration.media_size(absolute_path)
        self.files.append({'path':absolute_path, 
         'size':size})
        self.size += size
        self.sort_files(self.files)

    def clear_cache_if_needed(self):
        while self.size > self.max_cache_size:
            configuration.media_delete(self.files[0]['path'])
            self.size -= self.files[0]['size']
            self.files.remove(self.files[0])

    def filename(self, path):
        extension = os.path.splitext(path)[1]
        return '{}{}'.format(hashlib.sha256(path.encode('utf8')).hexdigest(), extension)

    def full_path(self, path):
        return os.path.join(self.dir, self.filename(path))

    def exists(self, path):
        thumbnail_full_path = self.full_path(path)
        return configuration.media_exists(thumbnail_full_path)

    def url(self, path, request):
        return configuration.media_url(os.path.join(self.dir, self.filename(path)), request)


cache = MediaCache()