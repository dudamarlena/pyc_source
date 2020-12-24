# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /opt/hostedtoolcache/Python/3.8.2/x64/lib/python3.8/site-packages/musicbot/music/file.py
# Compiled at: 2020-04-15 22:39:47
# Size of source mod 2**32: 6941 bytes
import logging, json, copy, os, click, taglib
logger = logging.getLogger(__name__)
options = [
 click.option('--keywords', help='Keywords', default=None),
 click.option('--artist', help='Artist', default=None),
 click.option('--album', help='Album', default=None),
 click.option('--title', help='Title', default=None),
 click.option('--genre', help='Genre', default=None),
 click.option('--number', help='Track number', default=None),
 click.option('--rating', help='Rating', default=None)]
supported_formats = [
 'mp3', 'flac']

def mysplit(s, delim=','):
    if isinstance(s, list):
        return s
    if s is None:
        return []
    if isinstance(s, str):
        return [x for x in s.split(delim) if x]
    raise ValueError(s)


class File:

    def __init__(self, filename, _folder=''):
        self._folder = _folder
        self.handle = taglib.File(filename)
        self.youtube_link = ''
        self.spotify_link = ''

    def __repr__(self):
        return self.path

    def close(self):
        self.handle.close()

    def ordered_dict(self):
        from collections import OrderedDict
        return OrderedDict([('title', self.title),
         (
          'album', self.album),
         (
          'genre', self.genre),
         (
          'artist', self.artist),
         (
          'folder', self._folder),
         (
          'youtube', self.youtube),
         (
          'spotify', self.spotify),
         (
          'number', self.number),
         (
          'path', self.path),
         (
          'rating', self.rating),
         (
          'duration', self.duration),
         (
          'size', self.size),
         (
          'keywords', mysplit(self.keywords, ' '))])

    def __iter__(self):
        (yield from self.ordered_dict().items())
        if False:
            yield None

    def to_dict(self):
        return dict(self.ordered_dict())

    def to_graphql(self):
        return ', '.join([f"{k}: {json.dumps(v)}" for k, v in self.ordered_dict().items()])

    def to_json(self):
        return json.dumps(self.ordered_dict())

    @property
    def path(self):
        return self.handle.path

    @property
    def folder(self):
        return self._folder

    def __get_first(self, tag, default=''):
        if tag not in self.handle.tags:
            return default
        for item in self.handle.tags[tag]:
            return str(item)
            return default

    def __set_first(self, tag, value, force=False):
        if value is None:
            return
        if tag not in self.handle.tags:
            if force:
                self.handle.tags[tag] = [
                 value]
            return
        del self.handle.tags[tag][0]
        self.handle.tags[tag].insert(0, value)

    @property
    def title(self):
        return self._File__get_first('TITLE')

    @title.setter
    def title(self, title):
        self._File__set_first('TITLE', title)

    @property
    def album(self):
        return self._File__get_first('ALBUM')

    @album.setter
    def album(self, album):
        self._File__set_first('ALBUM', album)

    @property
    def artist(self):
        return self._File__get_first('ARTIST')

    @artist.setter
    def artist(self, artist):
        self._File__set_first('ARTIST', artist)

    @property
    def rating--- This code section failed: ---

 L. 128         0  LOAD_FAST                'self'
                2  LOAD_METHOD              _File__get_first
                4  LOAD_STR                 'FMPS_RATING'
                6  CALL_METHOD_1         1  ''
                8  STORE_FAST               's'

 L. 129        10  SETUP_FINALLY        44  'to 44'

 L. 130        12  LOAD_GLOBAL              float
               14  LOAD_FAST                's'
               16  CALL_FUNCTION_1       1  ''
               18  STORE_FAST               'n'

 L. 131        20  LOAD_FAST                'n'
               22  LOAD_CONST               0.0
               24  COMPARE_OP               <
               26  POP_JUMP_IF_FALSE    34  'to 34'

 L. 132        28  POP_BLOCK        
               30  LOAD_CONST               0.0
               32  RETURN_VALUE     
             34_0  COME_FROM            26  '26'

 L. 133        34  LOAD_FAST                'n'
               36  LOAD_CONST               5.0
               38  BINARY_MULTIPLY  
               40  POP_BLOCK        
               42  RETURN_VALUE     
             44_0  COME_FROM_FINALLY    10  '10'

 L. 134        44  DUP_TOP          
               46  LOAD_GLOBAL              ValueError
               48  COMPARE_OP               exception-match
               50  POP_JUMP_IF_FALSE    64  'to 64'
               52  POP_TOP          
               54  POP_TOP          
               56  POP_TOP          

 L. 135        58  POP_EXCEPT       
               60  LOAD_CONST               0.0
               62  RETURN_VALUE     
             64_0  COME_FROM            50  '50'
               64  END_FINALLY      

Parse error at or near `LOAD_CONST' instruction at offset 30

    @rating.setter
    def rating(self, rating):
        self._File__set_first('FMPS_RATING', rating)

    @property
    def comment(self):
        return self._File__get_first('COMMENT')

    @comment.setter
    def comment(self, comment):
        self._File__set_first('COMMENT', comment)

    def fix_comment(self, comment):
        self._File__set_first('COMMENT', comment, force=True)

    @property
    def description(self):
        return self._File__get_first('DESCRIPTION')

    @description.setter
    def description(self, description):
        self._File__set_first('DESCRIPTION', description)

    def fix_description(self, description):
        self._File__set_first('DESCRIPTION', description, force=True)

    @property
    def genre(self):
        return self._File__get_first('GENRE')

    @genre.setter
    def genre(self, genre):
        self._File__set_first('GENRE', genre)

    @property
    def number--- This code section failed: ---

 L. 173         0  LOAD_FAST                'self'
                2  LOAD_METHOD              _File__get_first
                4  LOAD_STR                 'TRACKNUMBER'
                6  CALL_METHOD_1         1  ''
                8  STORE_FAST               's'

 L. 174        10  SETUP_FINALLY        68  'to 68'

 L. 175        12  LOAD_GLOBAL              int
               14  LOAD_FAST                's'
               16  CALL_FUNCTION_1       1  ''
               18  STORE_FAST               'n'

 L. 176        20  LOAD_FAST                'n'
               22  LOAD_CONST               0
               24  COMPARE_OP               <
               26  POP_JUMP_IF_FALSE    34  'to 34'

 L. 177        28  POP_BLOCK        
               30  LOAD_CONST               -1
               32  RETURN_VALUE     
             34_0  COME_FROM            26  '26'

 L. 178        34  LOAD_FAST                'n'
               36  LOAD_CONST               2147483647
               38  COMPARE_OP               >
               40  POP_JUMP_IF_FALSE    62  'to 62'

 L. 179        42  LOAD_GLOBAL              logger
               44  LOAD_METHOD              warning
               46  LOAD_STR                 '%s : invalid number %s'
               48  LOAD_FAST                'self'
               50  LOAD_FAST                'n'
               52  CALL_METHOD_3         3  ''
               54  POP_TOP          

 L. 180        56  POP_BLOCK        
               58  LOAD_CONST               0
               60  RETURN_VALUE     
             62_0  COME_FROM            40  '40'

 L. 181        62  LOAD_FAST                'n'
               64  POP_BLOCK        
               66  RETURN_VALUE     
             68_0  COME_FROM_FINALLY    10  '10'

 L. 182        68  DUP_TOP          
               70  LOAD_GLOBAL              ValueError
               72  COMPARE_OP               exception-match
               74  POP_JUMP_IF_FALSE    88  'to 88'
               76  POP_TOP          
               78  POP_TOP          
               80  POP_TOP          

 L. 183        82  POP_EXCEPT       
               84  LOAD_CONST               -1
               86  RETURN_VALUE     
             88_0  COME_FROM            74  '74'
               88  END_FINALLY      

Parse error at or near `LOAD_CONST' instruction at offset 30

    @number.setter
    def number(self, number):
        self._File__set_first('TRACKNUMBER', number)

    @property
    def keywords(self):
        if str(self.handle.path).endswith('.mp3'):
            return self.comment
        if str(self.handle.path).endswith('.flac'):
            if self.comment:
                if not self.description:
                    self.fix_description(self.comment)
            return self.description
        return ''

    @keywords.setter
    def keywords(self, keywords):
        if str(self.handle.path).endswith('.mp3'):
            self.comment = keywords
        else:
            if str(self.handle.path).endswith('.flac'):
                self.fix_description(keywords)

    def add_keywords(self, keywords):
        tags = copy.deepcopy(self.keywords)
        for k in keywords:
            if k not in tags:
                tags.append(k)
            if set(self.keywords) != set(tags):
                self.keywords = tags
                self.save()
                return True
            return False

    def delete_keywords(self, keywords):
        tags = copy.deepcopy(self.keywords)
        for k in keywords:
            if k in tags:
                tags.remove(k)
            if set(self.keywords) != set(tags):
                self.keywords = tags
                self.save()
                return True
            return False

    @property
    def duration(self):
        return self.handle.length

    @property
    def size(self):
        return os.path.getsize(self.handle.path)

    @property
    def youtube(self):
        return self.youtube_link

    @property
    def spotify(self):
        return self.spotify_link

    def fingerprint(self, api_key):
        import acoustid
        ids = acoustid.match(api_key, self.path)
        for score, recording_id, title, artist in ids:
            logger.info('score : %s | recording_id : %s | title : %s | artist : %s', score, recording_id, title, artist)
            return recording_id

    def save(self):
        self.handle.save()