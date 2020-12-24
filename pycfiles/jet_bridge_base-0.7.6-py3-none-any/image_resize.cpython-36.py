# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/f1nal/Dropbox/python/jet-bridge/src/packages/jet_bridge_base/jet_bridge_base/views/image_resize.py
# Compiled at: 2019-10-30 05:24:12
# Size of source mod 2**32: 2223 bytes
import io
from six.moves import urllib
from PIL import Image
from jet_bridge_base.configuration import configuration
from jet_bridge_base.exceptions.not_found import NotFound
from jet_bridge_base.media_cache import cache
from jet_bridge_base.responses.redirect import RedirectResponse
from jet_bridge_base.views.base.api import APIView

class ImageResizeView(APIView):

    def create_thumbnail(self, file, thumbnail_path, max_width, max_height):
        img = Image.open(file)
        img.thumbnail((max_width, max_height), Image.ANTIALIAS)
        with io.BytesIO() as (memory_file):
            img.save(memory_file, format=(img.format), quality=85)
            memory_file.seek(0)
            configuration.media_save(thumbnail_path, memory_file.read())

    def get(self, *args, **kwargs):
        path = self.request.get_argument('path')
        max_width = self.request.get_argument('max_width', 320)
        max_height = self.request.get_argument('max_height', 240)
        external_path = path.startswith('http://') or path.startswith('https://')
        try:
            if not cache.exists(path):
                thumbnail_full_path = cache.full_path(path)
                if not external_path:
                    if not configuration.media_exists(path):
                        raise NotFound
                    file = configuration.media_open(path)
                else:
                    fd = urllib.request.urlopen(path)
                    file = io.BytesIO(fd.read())
                with file:
                    cache.clear_cache_if_needed()
                    self.create_thumbnail(file, thumbnail_full_path, max_width, max_height)
                    cache.add_file(path)
            return RedirectResponse(cache.url(path, self.request))
        except IOError as e:
            raise e