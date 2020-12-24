# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/kaa/metadata/image/generic.py
# Compiled at: 2009-02-13 16:41:01
__all__ = [
 'Parser']
import time, core, exiv2
mapping = {'Image.Width': 'width', 
   'Image.Height': 'height', 
   'Image.Mimetype': 'mime', 
   'Image.Thumbnail': 'thumbnail', 
   'Image.Keywords': 'keywords', 
   'Exif.Image.Model': 'hardware', 
   'Exif.Image.Software': 'software', 
   'Exif.Canon.OwnerName': 'artist', 
   'Iptc.Application2.Byline': 'artist', 
   'Iptc.Application2.BylineTitle': 'title', 
   'Iptc.Application2.Headline': 'title', 
   'Iptc.Application2.Writer': 'author', 
   'Iptc.Application2.Credit': 'author', 
   'Iptc.Application2.Byline': 'author', 
   'Iptc.Application2.LocationName': 'country', 
   'Iptc.Application2.Caption': 'description', 
   'Iptc.Application2.City': 'city', 
   'Iptc.Application2.SubLocation': 'location'}

class Generic(core.Image):
    table_mapping = {'exiv2': mapping}

    def __init__(self, file):
        core.Image.__init__(self)
        self.type = 'image'
        metadata = exiv2.parse(file.name)
        self._appendtable('exiv2', metadata)
        t = metadata.get('Exif.Photo.DateTimeOriginal')
        if not t:
            t = metadata.get('Exif.Image.DateTime')
        if t:
            try:
                t = time.strptime(str(t), '%Y:%m:%d %H:%M:%S')
                self.timestamp = int(time.mktime(t))
            except ValueError:
                pass

        orientation = metadata.get('Exif.Image.Orientation')
        if orientation == 2:
            self.rotation = 180
        if orientation == 5:
            self.rotation = 270
        if orientation == 6:
            self.rotation = 90


Parser = Generic