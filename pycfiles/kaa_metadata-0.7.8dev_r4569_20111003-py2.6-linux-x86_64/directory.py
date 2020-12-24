# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /net/orion/data/home/tack/projects/kaa/metadata/build/lib.linux-x86_64-2.6/kaa/metadata/misc/directory.py
# Compiled at: 2008-10-26 20:23:09
__all__ = [
 'Parser']
import os, logging, kaa, kaa.metadata.core as core
from kaa.metadata.image.core import BinsParser
log = logging.getLogger('metadata')

class Directory(core.Media):
    """
    Simple parser for reading a .directory file.
    """
    media = core.MEDIA_DIRECTORY

    def __init__(self, directory):
        core.Media.__init__(self)
        info = os.path.join(directory, '.directory')
        if os.path.isfile(info):
            f = open(info)
            for l in f.readlines():
                if l.startswith('Icon='):
                    image = l[5:].strip()
                    if not image.startswith('/'):
                        image = os.path.join(directory, image)
                    if os.path.isfile(image):
                        self._set('image', image)
                if l.startswith('Name='):
                    self.title = l[5:].strip()
                if l.startswith('Comment='):
                    self.comment = l[8:].strip()

            f.close()
        binsxml = os.path.join(directory, 'album.xml')
        if os.path.isfile(binsxml):
            bins = BinsParser(binsxml)
            for key, value in bins.items():
                if key == 'sampleimage':
                    image = os.path.join(directory, kaa.unicode_to_str(value))
                    if os.path.isfile(image):
                        self._set('image', image)
                    continue
                self._set(key, value)

        folderjpg = os.path.join(directory, 'folder.jpg')
        if os.path.isfile(folderjpg):
            self._set('image', folderjpg)
        self.mime = 'text/directory'


Parser = Directory