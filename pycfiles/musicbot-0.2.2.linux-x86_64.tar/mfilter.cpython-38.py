# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /opt/hostedtoolcache/Python/3.8.2/x64/lib/python3.8/site-packages/musicbot/music/mfilter.py
# Compiled at: 2020-04-15 22:39:47
# Size of source mod 2**32: 8797 bytes
import logging, json, attr, click
logger = logging.getLogger(__name__)
rating_choices = [x * 0.5 for x in range(0, 11)]

def sane_rating(ctx, param, value):
    if value is not None:
        if value in rating_choices:
            ctx.params[param.name] = value
            return ctx.params[param.name]


min_int = 0
max_int = 2147483647
default_name = None
default_filter = None
default_relative = False
default_shuffle = False
default_youtubes = []
default_no_youtubes = []
default_spotifys = []
default_no_spotifys = []
default_formats = []
default_no_formats = []
default_genres = []
default_no_genres = []
default_limit = max_int
default_min_duration = min_int
default_max_duration = max_int
default_min_size = min_int
default_max_size = max_int
default_min_rating = min(rating_choices)
default_max_rating = max(rating_choices)
default_keywords = []
default_no_keywords = []
default_artists = []
default_no_artists = []
default_titles = []
default_no_titles = []
default_albums = []
default_no_albums = []

@attr.s(frozen=True)
class Filter:
    name = attr.ib(default=default_name)
    relative = attr.ib(default=default_relative)
    shuffle = attr.ib(default=default_shuffle)
    youtubes = attr.ib(default=default_youtubes)
    no_youtubes = attr.ib(default=default_no_youtubes)
    spotifys = attr.ib(default=default_spotifys)
    no_spotifys = attr.ib(default=default_no_spotifys)
    formats = attr.ib(default=default_formats)
    no_formats = attr.ib(default=default_no_formats)
    limit = attr.ib(default=default_limit)
    genres = attr.ib(default=default_genres)
    no_genres = attr.ib(default=default_no_genres)
    genres = attr.ib(default=default_genres)
    no_genres = attr.ib(default=default_no_genres)
    min_duration = attr.ib(default=default_min_duration)
    max_duration = attr.ib(default=default_max_duration)
    min_size = attr.ib(default=default_min_size)
    max_size = attr.ib(default=default_max_size)
    min_rating = attr.ib(default=default_min_rating, validator=(attr.validators.in_(rating_choices)))
    max_rating = attr.ib(default=default_max_rating, validator=(attr.validators.in_(rating_choices)))
    keywords = attr.ib(default=default_keywords)
    no_keywords = attr.ib(default=default_no_keywords)
    artists = attr.ib(default=default_artists)
    no_artists = attr.ib(default=default_no_artists)
    titles = attr.ib(default=default_titles)
    no_titles = attr.ib(default=default_no_titles)
    albums = attr.ib(default=default_albums)
    no_albums = attr.ib(default=default_no_albums)

    def __attrs_post_init__(self):
        if self.min_size > self.max_size:
            raise ValueError(f"Invalid minimum ({self.min_rating}) or maximum ({self.max_rating}) size")
        if self.min_rating > self.max_rating:
            raise ValueError(f"Invalid minimum ({self.min_rating}) or maximum ({self.max_rating}) rating")
        if self.min_duration > self.max_duration:
            raise ValueError(f"Invalid minimum ({self.min_duration}) or maximum ({self.max_duration}) duration")
        is_bad_formats = set(self.formats).intersection(self.no_formats)
        is_bad_artists = set(self.artists).intersection(self.no_artists)
        is_bad_genres = set(self.genres).intersection(self.no_genres)
        is_bad_albums = set(self.albums).intersection(self.no_albums)
        is_bad_titles = set(self.titles).intersection(self.no_titles)
        is_bad_keywords = set(self.keywords).intersection(self.no_keywords)
        not_empty_set = is_bad_formats or is_bad_artists or is_bad_genres or is_bad_albums or is_bad_titles or is_bad_keywords
        if not_empty_set:
            raise ValueError(f"You can't have duplicates value in filters {self}")
        logger.debug('Filter: %s', self)

    def __repr__(self):
        return self.ordered_dict()

    def diff--- This code section failed: ---

 L. 108         0  LOAD_GLOBAL              vars
                2  LOAD_FAST                'self'
                4  CALL_FUNCTION_1       1  ''
                6  STORE_DEREF              'myself'

 L. 109         8  LOAD_GLOBAL              vars
               10  LOAD_GLOBAL              Filter
               12  CALL_FUNCTION_0       0  ''
               14  CALL_FUNCTION_1       1  ''
               16  STORE_DEREF              'default'

 L. 110        18  LOAD_CLOSURE             'default'
               20  LOAD_CLOSURE             'myself'
               22  BUILD_TUPLE_2         2 
               24  LOAD_DICTCOMP            '<code_object <dictcomp>>'
               26  LOAD_STR                 'Filter.diff.<locals>.<dictcomp>'
               28  MAKE_FUNCTION_8          'closure'
               30  LOAD_DEREF               'myself'
               32  GET_ITER         
               34  CALL_FUNCTION_1       1  ''
               36  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `LOAD_DICTCOMP' instruction at offset 24

    def common--- This code section failed: ---

 L. 114         0  LOAD_GLOBAL              vars
                2  LOAD_FAST                'self'
                4  CALL_FUNCTION_1       1  ''
                6  STORE_DEREF              'myself'

 L. 115         8  LOAD_GLOBAL              vars
               10  LOAD_GLOBAL              Filter
               12  CALL_FUNCTION_0       0  ''
               14  CALL_FUNCTION_1       1  ''
               16  STORE_DEREF              'default'

 L. 116        18  LOAD_CLOSURE             'default'
               20  LOAD_CLOSURE             'myself'
               22  BUILD_TUPLE_2         2 
               24  LOAD_DICTCOMP            '<code_object <dictcomp>>'
               26  LOAD_STR                 'Filter.common.<locals>.<dictcomp>'
               28  MAKE_FUNCTION_8          'closure'
               30  LOAD_DEREF               'myself'
               32  GET_ITER         
               34  CALL_FUNCTION_1       1  ''
               36  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `LOAD_DICTCOMP' instruction at offset 24

    def ordered_dict(self):
        from collections import OrderedDict
        return OrderedDict([('minDuration', self.min_duration),
         (
          'maxDuration', self.max_duration),
         (
          'minSize', self.min_size),
         (
          'maxSize', self.max_size),
         (
          'minRating', self.min_rating),
         (
          'maxRating', self.max_rating),
         (
          'artists', self.artists),
         (
          'noArtists', self.no_artists),
         (
          'albums', self.albums),
         (
          'noAlbums', self.no_albums),
         (
          'titles', self.titles),
         (
          'noTitles', self.no_titles),
         (
          'genres', self.genres),
         (
          'noGenres', self.no_genres),
         (
          'formats', self.formats),
         (
          'noFormats', self.no_formats),
         (
          'keywords', self.keywords),
         (
          'noKeywords', self.no_keywords),
         (
          'shuffle', self.shuffle),
         (
          'relative', self.relative),
         (
          'limit', self.limit),
         (
          'youtubes', self.youtubes),
         (
          'noYoutubes', self.no_youtubes),
         (
          'spotifys', self.spotifys),
         (
          'noSpotifys', self.no_spotifys)])

    def to_graphql(self):
        return ', '.join([f"{k}: {json.dumps(v)}" for k, v in self.ordered_dict().items()])


options = [
 click.option('--name', help='Filter name', default=default_name),
 click.option('--limit', help='Fetch a maximum limit of music', default=default_limit),
 click.option('--youtubes', help='Select musics with a youtube link', multiple=True, default=default_youtubes),
 click.option('--no-youtubes', help='Select musics without youtube link', multiple=True, default=default_no_youtubes),
 click.option('--spotifys', help='Select musics with a spotifys link', multiple=True, default=default_youtubes),
 click.option('--no-spotifys', help='Select musics without spotifys link', multiple=True, default=default_no_youtubes),
 click.option('--formats', help='Select musics with file format', multiple=True, default=default_formats),
 click.option('--no-formats', help='Filter musics without format', multiple=True, default=default_no_formats),
 click.option('--keywords', help='Select musics with keywords', multiple=True, default=default_keywords),
 click.option('--no-keywords', help='Filter musics without keywords', multiple=True, default=default_no_keywords),
 click.option('--artists', help='Select musics with artists', multiple=True, default=default_artists),
 click.option('--no-artists', help='Filter musics without artists', multiple=True, default=default_no_artists),
 click.option('--albums', help='Select musics with albums', multiple=True, default=default_albums),
 click.option('--no-albums', help='Filter musics without albums', multiple=True, default=default_no_albums),
 click.option('--titles', help='Select musics with titles', multiple=True, default=default_titles),
 click.option('--no-titles', help='Filter musics without titless', multiple=True, default=default_no_titles),
 click.option('--genres', help='Select musics with genres', multiple=True, default=default_genres),
 click.option('--no-genres', help='Filter musics without genres', multiple=True, default=default_no_genres),
 click.option('--min-duration', help='Minimum duration filter (hours:minutes:seconds)', default=default_min_duration),
 click.option('--max-duration', help='Maximum duration filter (hours:minutes:seconds))', default=default_max_duration),
 click.option('--min-size', help='Minimum file size filter (in bytes)', default=default_min_size),
 click.option('--max-size', help='Maximum file size filter (in bytes)', default=default_max_size),
 click.option('--min-rating', help='Minimum rating', default=default_min_rating, show_default=True, callback=sane_rating),
 click.option('--max-rating', help='Maximum rating', default=default_max_rating, show_default=True, callback=sane_rating),
 click.option('--relative', help='Generate relatives paths', default=default_relative, is_flag=True),
 click.option('--shuffle', help='Randomize selection', default=default_shuffle, is_flag=True)]