# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/fanart/movie.py
# Compiled at: 2019-03-12 04:24:44
# Size of source mod 2**32: 2586 bytes
import fanart
from fanart.items import LeafItem, Immutable, ResourceItem
__all__ = ('ArtItem', 'DiscItem', 'LogoItem', 'PosterItem', 'BackgroundItem', 'HdLogoItem',
           'HdArtItem', 'BannerItem', 'ThumbItem', 'Movie')

class MovieItem(LeafItem):

    @Immutable.mutablemethod
    def __init__(self, id, url, likes, lang):
        super(MovieItem, self).__init__(id, url, likes)
        self.lang = lang


class DiscItem(MovieItem):
    KEY = fanart.TYPE.MOVIE.DISC

    @Immutable.mutablemethod
    def __init__(self, id, url, likes, lang, disc, disc_type):
        super(DiscItem, self).__init__(id, url, likes, lang)
        self.disc = int(disc)
        self.disc_type = disc_type


class ArtItem(MovieItem):
    KEY = fanart.TYPE.MOVIE.ART


class LogoItem(MovieItem):
    KEY = fanart.TYPE.MOVIE.LOGO


class PosterItem(MovieItem):
    KEY = fanart.TYPE.MOVIE.POSTER


class BackgroundItem(MovieItem):
    KEY = fanart.TYPE.MOVIE.BACKGROUND


class HdLogoItem(MovieItem):
    KEY = fanart.TYPE.MOVIE.HDLOGO


class HdArtItem(MovieItem):
    KEY = fanart.TYPE.MOVIE.HDART


class BannerItem(MovieItem):
    KEY = fanart.TYPE.MOVIE.BANNER


class ThumbItem(MovieItem):
    KEY = fanart.TYPE.MOVIE.THUMB


class Movie(ResourceItem):
    WS = fanart.WS.MOVIE

    @Immutable.mutablemethod
    def __init__(self, name, imdbid, tmdbid, arts, logos, discs, posters, backgrounds, hdlogos, hdarts, banners, thumbs):
        self.name = name
        self.imdbid = imdbid
        self.tmdbid = tmdbid
        self.arts = arts
        self.posters = posters
        self.logos = logos
        self.discs = discs
        self.backgrounds = backgrounds
        self.hdlogos = hdlogos
        self.hdarts = hdarts
        self.banners = banners
        self.thumbs = thumbs

    @classmethod
    def from_dict(cls, resource):
        minimal_keys = {'name', 'imdb_id', 'tmdb_id'}
        assert all((k in resource for k in minimal_keys)), 'Bad Format Map'
        return cls(name=(resource['name']),
          imdbid=(resource['imdb_id']),
          tmdbid=(resource['tmdb_id']),
          arts=(ArtItem.extract(resource)),
          logos=(LogoItem.extract(resource)),
          discs=(DiscItem.extract(resource)),
          posters=(PosterItem.extract(resource)),
          backgrounds=(BackgroundItem.extract(resource)),
          hdlogos=(HdLogoItem.extract(resource)),
          hdarts=(HdArtItem.extract(resource)),
          banners=(BannerItem.extract(resource)),
          thumbs=(ThumbItem.extract(resource)))