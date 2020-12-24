# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/fanart/tv.py
# Compiled at: 2019-03-12 05:00:25
# Size of source mod 2**32: 3161 bytes
import fanart
from fanart.items import LeafItem, Immutable, ResourceItem
__all__ = ('CharacterItem', 'ArtItem', 'LogoItem', 'BackgroundItem', 'SeasonItem',
           'SeasonPosterItem', 'SeasonBannerItem', 'ThumbItem', 'HdLogoItem', 'HdArtItem',
           'PosterItem', 'BannerItem', 'TvShow')

class TvItem(LeafItem):

    @Immutable.mutablemethod
    def __init__(self, id, url, likes, lang):
        super(TvItem, self).__init__(id, url, likes)
        self.lang = lang


class SeasonedTvItem(TvItem):

    @Immutable.mutablemethod
    def __init__(self, id, url, likes, lang, season):
        super(SeasonedTvItem, self).__init__(id, url, likes, lang)
        self.season = 0 if season == 'all' else int(season or 0)


class CharacterItem(TvItem):
    KEY = fanart.TYPE.TV.CHARACTER


class ArtItem(TvItem):
    KEY = fanart.TYPE.TV.ART


class LogoItem(TvItem):
    KEY = fanart.TYPE.TV.LOGO


class BackgroundItem(SeasonedTvItem):
    KEY = fanart.TYPE.TV.BACKGROUND


class SeasonItem(SeasonedTvItem):
    KEY = fanart.TYPE.TV.SEASONTHUMB


class SeasonPosterItem(SeasonedTvItem):
    KEY = fanart.TYPE.TV.SEASONPOSTER


class SeasonBannerItem(SeasonedTvItem):
    KEY = fanart.TYPE.TV.SEASONBANNER


class ThumbItem(TvItem):
    KEY = fanart.TYPE.TV.THUMB


class HdLogoItem(TvItem):
    KEY = fanart.TYPE.TV.HDLOGO


class HdArtItem(TvItem):
    KEY = fanart.TYPE.TV.HDART


class PosterItem(TvItem):
    KEY = fanart.TYPE.TV.POSTER


class BannerItem(TvItem):
    KEY = fanart.TYPE.TV.BANNER


class TvShow(ResourceItem):
    WS = fanart.WS.TV

    @Immutable.mutablemethod
    def __init__(self, name, tvdbid, backgrounds, characters, arts, logos, seasons, thumbs, hdlogos, hdarts, posters, banners, season_posters, season_banners):
        self.name = name
        self.tvdbid = tvdbid
        self.backgrounds = backgrounds
        self.characters = characters
        self.arts = arts
        self.logos = logos
        self.seasons = seasons
        self.thumbs = thumbs
        self.hdlogos = hdlogos
        self.hdarts = hdarts
        self.posters = posters
        self.banners = banners
        self.season_posters = posters
        self.season_banners = banners

    @classmethod
    def from_dict(cls, resource):
        minimal_keys = {'name', 'thetvdb_id'}
        assert all((k in resource for k in minimal_keys)), 'Bad Format Map'
        return cls(name=(resource['name']),
          tvdbid=(resource['thetvdb_id']),
          backgrounds=(BackgroundItem.extract(resource)),
          characters=(CharacterItem.extract(resource)),
          arts=(ArtItem.extract(resource)),
          logos=(LogoItem.extract(resource)),
          seasons=(SeasonItem.extract(resource)),
          thumbs=(ThumbItem.extract(resource)),
          hdlogos=(HdLogoItem.extract(resource)),
          hdarts=(HdArtItem.extract(resource)),
          posters=(PosterItem.extract(resource)),
          banners=(BannerItem.extract(resource)),
          season_posters=(SeasonPosterItem.extract(resource)),
          season_banners=(SeasonBannerItem.extract(resource)))