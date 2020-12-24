# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/advancedcaching/openstreetmap.py
# Compiled at: 2011-04-23 08:43:29
from __future__ import with_statement
import logging
logger = logging.getLogger('openstreetmap')
from os import path, mkdir, extsep, remove
from threading import Semaphore
from urllib import urlretrieve
from socket import setdefaulttimeout
import connection
setdefaulttimeout(30)
CONCURRENT_THREADS = 10

def get_tile_loader(prefix, remote_url, max_zoom=18, reverse_zoom=False, file_type='png', size=256):

    class TileLoader:
        downloading = {}
        semaphore = Semaphore(CONCURRENT_THREADS)
        noimage_cantload = None
        noimage_loading = None
        base_dir = ''
        PREFIX = prefix
        MAX_ZOOM = max_zoom
        FILE_TYPE = file_type
        REMOTE_URL = remote_url
        TILE_SIZE = size
        TPL_LOCAL_PATH = path.join('%s', PREFIX, '%d', '%d')
        TPL_LOCAL_FILENAME = path.join('%s', '%%d%s%s' % (extsep, FILE_TYPE))

        def __init__(self, id_string, tile, zoom, undersample=False, x=0, y=0, callback_draw=None, callback_load=None):
            self.id_string = id_string
            self.undersample = undersample
            self.tile = tile
            self.download_tile = tile
            if not undersample:
                self.download_zoom = zoom
                self.display_zoom = zoom
            else:
                self.download_zoom = zoom - 1
                self.display_zoom = zoom
                self.download_tile = (int(self.download_tile[0] / 2), int(self.download_tile[1] / 2))
            self.pbuf = None
            self.callback_draw = callback_draw
            self.callback_load = callback_load
            self.my_noimage = None
            self.stop = False
            self.x = x
            self.y = y
            self.local_path = self.TPL_LOCAL_PATH % (self.base_dir, self.download_zoom, self.download_tile[0])
            self.local_filename = self.TPL_LOCAL_FILENAME % (self.local_path, self.download_tile[1])
            self.remote_filename = self.REMOTE_URL % {'zoom': self.download_zoom, 'x': self.download_tile[0], 'y': self.download_tile[1]}
            return

        def halt(self):
            self.stop = True

        @staticmethod
        def create_recursive(dpath):
            if dpath != '/':
                if not path.exists(dpath):
                    (head, tail) = path.split(dpath)
                    TileLoader.create_recursive(head)
                    try:
                        mkdir(dpath)
                    except Exception:
                        pass

        def run(self):
            answer = True
            if not path.isfile(self.local_filename):
                self.create_recursive(self.local_path)
                self.draw(self.get_no_image(self.noimage_loading))
                answer = self.__download(self.remote_filename, self.local_filename)
            if answer == True:
                self.load()
                self.draw(self.pbuf)
            elif answer == False:
                self.draw(self.get_no_image(self.noimage_cantload))

        def run_again(self):
            self.load()
            self.draw(self.pbuf)
            return False

        def get_no_image(self, default):
            return (
             default, None)

        def load(self, tryno=0):
            if self.stop:
                return True
            else:
                try:
                    size, tile = self.TILE_SIZE, self.tile
                    if self.undersample:
                        supertile_x = int(tile[0] / 2)
                        supertile_y = int(tile[1] / 2)
                        off_x = (tile[0] / 2.0 - supertile_x) * size
                        off_y = (tile[1] / 2.0 - supertile_y) * size
                        surface = self.callback_load(self.local_filename)
                        self.pbuf = (
                         surface, (off_x, off_y))
                    else:
                        surface = self.callback_load(self.local_filename)
                        self.pbuf = (surface, None)
                    return True
                except Exception, e:
                    if tryno == 0:
                        return self.recover()
                    else:
                        logger.exception('Exception while loading map tile: %s' % e)
                        self.pbuf = (self.noimage_cantload, None)
                        return True

                return

        def recover(self):
            try:
                remove(self.local_filename)
            except:
                pass

            self.__download(self.remote_filename, self.local_filename)
            return self.load(1)

        def draw(self, pbuf):
            if not self.stop:
                return self.callback_draw(self.id_string, pbuf[0], self.x, self.y, pbuf[1])
            return False

        def __download(self, remote, local):
            if path.exists(local):
                return True
            else:
                if connection.offline:
                    return False
                with TileLoader.semaphore:
                    try:
                        if self.stop:
                            return
                        else:
                            info = urlretrieve(remote, local)
                            if 'text/html' in info[1]['Content-Type']:
                                return False
                            return True
                    except Exception, e:
                        print 'Download Error', e
                        return False

                return

        def download_tile_only(self):
            if not path.isfile(self.local_filename):
                self.create_recursive(self.local_path)
            return self.__download(self.remote_filename, self.local_filename)

    return TileLoader