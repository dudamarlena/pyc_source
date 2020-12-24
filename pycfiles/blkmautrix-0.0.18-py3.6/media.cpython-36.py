# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/mautrix/client/api/types/media.py
# Compiled at: 2019-11-21 01:01:47
# Size of source mod 2**32: 2509 bytes
from attr import dataclass
import attr
from .primitive import ContentURI
from .util import SerializableAttrs

@dataclass
class MediaRepoConfig(SerializableAttrs['MediaRepoConfig']):
    __doc__ = '\n    Matrix media repo config. See `GET /_matrix/media/r0/config`_.\n\n    .. _GET /_matrix/media/r0/config:\n        https://matrix.org/docs/spec/client_server/r0.5.0#get-matrix-media-r0-config\n    '
    upload_size: int = attr.ib(metadata={'json': 'm.upload_size'})


@dataclass
class OpenGraphImage(SerializableAttrs['OpenGraphImage']):
    url: ContentURI = attr.ib(default=None, metadata={'json': 'og:image'})
    mimetype: str = attr.ib(default=None, metadata={'json': 'og:image:type'})
    height: int = attr.ib(default=None, metadata={'json': 'og:image:width'})
    width: int = attr.ib(default=None, metadata={'json': 'og:image:height'})
    size: int = attr.ib(default=None, metadata={'json': 'matrix:image:size'})


@dataclass
class OpenGraphVideo(SerializableAttrs['OpenGraphVideo']):
    url: ContentURI = attr.ib(default=None, metadata={'json': 'og:video'})
    mimetype: str = attr.ib(default=None, metadata={'json': 'og:video:type'})
    height: int = attr.ib(default=None, metadata={'json': 'og:video:width'})
    width: int = attr.ib(default=None, metadata={'json': 'og:video:height'})
    size: int = attr.ib(default=None, metadata={'json': 'matrix:video:size'})


@dataclass
class OpenGraphAudio(SerializableAttrs['OpenGraphAudio']):
    url: ContentURI = attr.ib(default=None, metadata={'json': 'og:audio'})
    mimetype: str = attr.ib(default=None, metadata={'json': 'og:audio:type'})


@dataclass
class MXOpenGraph(SerializableAttrs['MXOpenGraph']):
    __doc__ = '\n    Matrix URL preview response. See `GET /_matrix/media/r0/preview_url`_.\n\n    .. _GET /_matrix/media/r0/preview_url:\n        https://matrix.org/docs/spec/client_server/r0.5.0#get-matrix-media-r0-preview-url\n    '
    title: str = attr.ib(default=None, metadata={'json': 'og:title'})
    description: str = attr.ib(default=None, metadata={'json': 'og:description'})
    image: OpenGraphImage = attr.ib(default=None, metadata={'flatten': True})
    video: OpenGraphVideo = attr.ib(default=None, metadata={'flatten': True})
    audio: OpenGraphAudio = attr.ib(default=None, metadata={'flatten': True})