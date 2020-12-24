# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/reg/src/youtube/youtube2zim/youtube.py
# Compiled at: 2020-03-04 05:21:48
# Size of source mod 2**32: 9679 bytes
import requests
from dateutil import parser as dt_parser
from zimscraperlib.download import save_file
from zimscraperlib.imaging import resize_image
from .constants import logger, YOUTUBE
from .utils import save_json, load_json, get_slug
YOUTUBE_API = 'https://www.googleapis.com/youtube/v3'
PLAYLIST_API = f"{YOUTUBE_API}/playlists"
PLAYLIST_ITEMS_API = f"{YOUTUBE_API}/playlistItems"
CHANNEL_SECTIONS_API = f"{YOUTUBE_API}/channelSections"
CHANNELS_API = f"{YOUTUBE_API}/channels"
SEARCH_API = f"{YOUTUBE_API}/search"
VIDEOS_API = f"{YOUTUBE_API}/videos"
MAX_VIDEOS_PER_REQUEST = 50
RESULTS_PER_PAGE = 50

class Playlist(object):

    def __init__(self, playlist_id, title, description, creator_id, creator_name):
        self.playlist_id = playlist_id
        self.title = title
        self.description = description
        self.creator_id = creator_id
        self.creator_name = creator_name
        self.slug = get_slug(title, js_safe=True)

    @classmethod
    def from_id(cls, playlist_id):
        playlist_json = get_playlist_json(playlist_id)
        return Playlist(playlist_id=playlist_id,
          title=(playlist_json['snippet']['title']),
          description=(playlist_json['snippet']['description']),
          creator_id=(playlist_json['snippet']['channelId']),
          creator_name=(playlist_json['snippet']['channelTitle']))


def credentials_ok--- This code section failed: ---

 L.  48         0  LOAD_GLOBAL              requests
                2  LOAD_ATTR                get

 L.  49         4  LOAD_GLOBAL              SEARCH_API

 L.  49         6  LOAD_STR                 'snippet'
                8  LOAD_CONST               1
               10  LOAD_GLOBAL              YOUTUBE
               12  LOAD_ATTR                api_key
               14  LOAD_CONST               ('part', 'maxResults', 'key')
               16  BUILD_CONST_KEY_MAP_3     3 

 L.  48        18  LOAD_CONST               ('params',)
               20  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
               22  STORE_FAST               'req'

 L.  51        24  LOAD_FAST                'req'
               26  LOAD_ATTR                status_code
               28  LOAD_CONST               400
               30  COMPARE_OP               >
               32  POP_JUMP_IF_FALSE    60  'to 60'

 L.  52        34  LOAD_GLOBAL              logger
               36  LOAD_METHOD              error
               38  LOAD_STR                 'HTTP '
               40  LOAD_FAST                'req'
               42  LOAD_ATTR                status_code
               44  FORMAT_VALUE          0  ''
               46  LOAD_STR                 ' Error response: '
               48  LOAD_FAST                'req'
               50  LOAD_ATTR                text
               52  FORMAT_VALUE          0  ''
               54  BUILD_STRING_4        4 
               56  CALL_METHOD_1         1  ''
               58  POP_TOP          
             60_0  COME_FROM            32  '32'

 L.  53        60  SETUP_FINALLY        88  'to 88'

 L.  54        62  LOAD_FAST                'req'
               64  LOAD_METHOD              raise_for_status
               66  CALL_METHOD_0         0  ''
               68  POP_TOP          

 L.  55        70  LOAD_GLOBAL              bool
               72  LOAD_FAST                'req'
               74  LOAD_METHOD              json
               76  CALL_METHOD_0         0  ''
               78  LOAD_STR                 'items'
               80  BINARY_SUBSCR    
               82  CALL_FUNCTION_1       1  ''
               84  POP_BLOCK        
               86  RETURN_VALUE     
             88_0  COME_FROM_FINALLY    60  '60'

 L.  56        88  DUP_TOP          
               90  LOAD_GLOBAL              Exception
               92  COMPARE_OP               exception-match
               94  POP_JUMP_IF_FALSE   108  'to 108'
               96  POP_TOP          
               98  POP_TOP          
              100  POP_TOP          

 L.  57       102  POP_EXCEPT       
              104  LOAD_CONST               False
              106  RETURN_VALUE     
            108_0  COME_FROM            94  '94'
              108  END_FINALLY      

Parse error at or near `POP_TOP' instruction at offset 98


def get_channel_json(channel_id, for_username=False):
    """ fetch or retieve-save and return the Youtube ChannelResult JSON """
    fname = f"channel_{channel_id}"
    channel_json = load_json(YOUTUBE.cache_dir, fname)
    if channel_json is None:
        logger.debugf"query youtube-api for Channel #{channel_id}"
        req = requests.get(CHANNELS_API,
          params={'forUsername' if for_username else 'id': channel_id, 
         'part': 'brandingSettings,snippet,contentDetails', 
         'key': YOUTUBE.api_key})
        if req.status_code > 400:
            logger.errorf"HTTP {req.status_code} Error response: {req.text}"
        req.raise_for_status
        try:
            channel_json = req.json['items'][0]
        except IndexError:
            if for_username:
                logger.errorf"Invalid username `{channel_id}`: Not Found"
            else:
                logger.errorf"Invalid channelId `{channel_id}`: Not Found"
            raise
        else:
            save_json(YOUTUBE.cache_dir, fname, channel_json)
    return channel_json


def get_channel_playlists_json(channel_id):
    """ fetch or retieve-save and return the Youtube Playlists JSON for a channel"""
    fname = f"channel_{channel_id}_playlists"
    channel_playlists_json = load_json(YOUTUBE.cache_dir, fname)
    items = load_json(YOUTUBE.cache_dir, fname)
    if items is not None:
        return items
    else:
        logger.debugf"query youtube-api for Playlists of channel #{channel_id}"
        items = []
        page_token = None
    req = requests.get(PLAYLIST_API,
      params={'channelId':channel_id, 
     'part':'id', 
     'key':YOUTUBE.api_key, 
     'maxResults':RESULTS_PER_PAGE, 
     'pageToken':page_token})
    if req.status_code > 400:
        logger.errorf"HTTP {req.status_code} Error response: {req.text}"
    req.raise_for_status
    channel_playlists_json = req.json
    items += channel_playlists_json['items']
    save_json(YOUTUBE.cache_dir, fname, items)
    page_token = channel_playlists_json.get'nextPageToken'
    if not page_token:
        break
    return items


def get_playlist_json(playlist_id):
    """ fetch or retieve-save and return the Youtube PlaylistResult JSON """
    fname = f"playlist_{playlist_id}"
    playlist_json = load_json(YOUTUBE.cache_dir, fname)
    if playlist_json is None:
        logger.debugf"query youtube-api for Playlist #{playlist_id}"
        req = requests.get(PLAYLIST_API,
          params={'id':playlist_id, 
         'part':'snippet',  'key':YOUTUBE.api_key})
        if req.status_code > 400:
            logger.errorf"HTTP {req.status_code} Error response: {req.text}"
        req.raise_for_status
        try:
            playlist_json = req.json['items'][0]
        except IndexError:
            logger.errorf"Invalid playlistId `{playlist_id}`: Not Found"
            raise
        else:
            save_json(YOUTUBE.cache_dir, fname, playlist_json)
    return playlist_json


def get_videos_json(playlist_id):
    """ retrieve a list of youtube PlaylistItem dict

        same request for both channel and playlist
        channel mode uses `uploads` playlist from channel """
    fname = f"playlist_{playlist_id}_videos"
    items = load_json(YOUTUBE.cache_dir, fname)
    if items is not None:
        return items
    else:
        logger.debugf"query youtube-api for PlaylistItems of playlist #{playlist_id}"
        items = []
        page_token = None
    req = requests.get(PLAYLIST_ITEMS_API,
      params={'playlistId':playlist_id, 
     'part':'snippet,contentDetails', 
     'key':YOUTUBE.api_key, 
     'maxResults':RESULTS_PER_PAGE, 
     'pageToken':page_token})
    if req.status_code > 400:
        logger.errorf"HTTP {req.status_code} Error response: {req.text}"
    req.raise_for_status
    videos_json = req.json
    items += videos_json['items']
    page_token = videos_json.get'nextPageToken'
    if not page_token:
        break
    save_json(YOUTUBE.cache_dir, fname, items)
    return items


def get_videos_authors_info(videos_ids):
    """ query authors' info for each video from their relative channel """
    items = load_json(YOUTUBE.cache_dir, 'videos_channels')
    if items is not None:
        return items
    logger.debug'query youtube-api for Video details of {} videos'.formatlen(videos_ids)
    items = {}

    def retrieve_videos_for(videos_ids):
        """ {videoId: {channelId: channelTitle}} for all videos_ids """
        req_items = {}
        page_token = None
        while True:
            req = requests.get(VIDEOS_API,
              params={'id':','.joinvideos_ids, 
             'part':'snippet', 
             'key':YOUTUBE.api_key, 
             'maxResults':RESULTS_PER_PAGE, 
             'pageToken':page_token})
            if req.status_code > 400:
                logger.errorf"HTTP {req.status_code} Error response: {req.text}"
            req.raise_for_status
            videos_json = req.json
            for item in videos_json['items']:
                req_items.update{item['id']: {'channelId':item['snippet']['channelId'], 
                              'channelTitle':item['snippet']['channelTitle']}}
            else:
                page_token = videos_json.get'nextPageToken'

            if not page_token:
                break

        return req_items

    for interv in range(0, len(videos_ids), MAX_VIDEOS_PER_REQUEST):
        items.updateretrieve_videos_for(videos_ids[interv:interv + MAX_VIDEOS_PER_REQUEST])
    else:
        save_json(YOUTUBE.cache_dir, 'videos_channels', items)
        return items


def save_channel_branding(channels_dir, channel_id, save_banner=False):
    """ download, save and resize profile [and banner] of a channel """
    channel_json = get_channel_json(channel_id)
    thumbnails = channel_json['snippet']['thumbnails']
    for quality in ('medium', 'default'):
        if quality in thumbnails.keys:
            thumnbail = thumbnails[quality]['url']
            break
        profile_path = channels_dir.joinpath(channel_id, 'profile.jpg')
        if not profile_path.exists:
            save_file(thumnbail, profile_path)
            resize_image(profile_path, width=100, height=100)
        if save_banner:
            banner = channel_json['brandingSettings']['image']['bannerImageUrl']
            banner_path = channels_dir.joinpath(channel_id, 'banner.jpg')
            if not banner_path.exists:
                save_file(banner, banner_path)


def skip_deleted_videos(item):
    """ filter func to filter-out deleted videos from list """
    return item['snippet']['title'] != 'Deleted video' and item['snippet']['description'] != 'This video is unavailable.'


def skip_outofrange_videos(date_range, item):
    """ filter func to filter-out videos that are not within specified date range"""
    return dt_parser.parseitem['snippet']['publishedAt'].date in date_range


# NOTE: have internal decompilation grammar errors.
# Use -t option to show full context.
# not in loop:
#	break
#      L. 121       192  BREAK_LOOP          196  'to 196'
# not in loop:
#	break
#      L. 180       166  BREAK_LOOP          170  'to 170'