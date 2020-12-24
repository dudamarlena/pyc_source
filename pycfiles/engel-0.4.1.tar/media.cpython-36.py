# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/wduss/src/github.com/dalloriam/engel/engel/widgets/media.py
# Compiled at: 2017-01-06 15:18:40
# Size of source mod 2**32: 1442 bytes
from .base import BaseElement, BaseContainer
from ..utils import html_property

class Image(BaseElement):
    __doc__ = '\n    A simple image widget.\n    '
    html_tag = 'img'
    source = html_property('src')

    def build(self, img_url):
        super(Image, self).build()
        self.source = img_url


class Video(BaseElement):
    __doc__ = '\n    A simple video widget, set via ``Video.loop`` to loop by default.\n    '
    html_tag = 'video'
    source = html_property('src')
    loop = html_property('loop')

    def build(self, vid_url):
        super(Video, self).build()
        self.source = vid_url
        self.loop = 'true'


class ImageLink(BaseContainer):
    __doc__ = '\n    An image widget, with the added feature of linking to an external URL.\n    '
    html_tag = 'a'
    target = html_property('href')

    def build(self, link, img_url):
        super(ImageLink, self).build()
        self.target = link
        self.add_child(Image((self.id + '-img'), img_url=img_url))


class Audio(BaseElement):
    __doc__ = '\n    A simple audio widget.\n    '
    html_tag = 'audio'
    source = html_property('src')

    def build(self, audio_path):
        super(Audio, self).build()
        self.source = audio_path