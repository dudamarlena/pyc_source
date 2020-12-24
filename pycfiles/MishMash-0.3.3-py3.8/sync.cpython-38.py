# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/mishmash/commands/sync/sync.py
# Compiled at: 2020-02-22 17:47:39
# Size of source mod 2**32: 20725 bytes
import os, platform, time, collections
from pathlib import Path
from os.path import getctime
from datetime import datetime
from nicfit import getLogger
from sqlalchemy.orm.exc import NoResultFound
import eyed3, eyed3.main
from eyed3.utils import art
from eyed3.plugins import LoaderPlugin
from eyed3.utils.prompt import PromptExit
import eyed3.main as eyed3_main
from eyed3.core import TXXX_ALBUM_TYPE, VARIOUS_TYPE, LP_TYPE, SINGLE_TYPE, EP_TYPE
from nicfit.console.ansi import Fg
from nicfit.console import pout, perr
from ...util import normalizeCountry
from ...orm import Track, Artist, Album, Meta, Image, Library, VARIOUS_ARTISTS_ID, VARIOUS_ARTISTS_NAME, MAIN_LIB_NAME, NULL_LIB_ID
from ... import console
from ... import database as db
from ...core import Command, EP_MAX_SIZE_HINT
from ...config import MusicLibrary
from .utils import syncImage, deleteOrphans
log = getLogger(__name__)
IMAGE_TYPES = {'artist':(Image.LOGO_TYPE, Image.ARTIST_TYPE, Image.LIVE_TYPE),  'album':(
  Image.FRONT_COVER_TYPE, Image.BACK_COVER_TYPE,
  Image.MISC_COVER_TYPE)}

class SyncPlugin(LoaderPlugin):
    __doc__ = 'An eyeD3 file scanner/loader plugin.'
    NAMES = [
     'mishmash-sync']
    SUMMARY = 'Synchronize files/directories with a Mishmash database.'
    DESCRIPTION = ''

    def __init__(self, arg_parser):
        super().__init__(arg_parser, cache_files=True, track_images=True)
        eyed3.main.setFileScannerOpts(arg_parser,
          default_recursive=True, paths_metavar='PATH_OR_LIB', paths_help='Files/directory paths, or individual music libraries. No arguments will sync all configured libraries.')
        arg_parser.add_argument('--monitor',
          action='store_true', dest='monitor', help="Monitor sync'd dirs for changes.")
        arg_parser.add_argument('-f',
          '--force', action='store_true', dest='force', help='Force sync a library when sync=False.')
        arg_parser.add_argument('--no-purge',
          action='store_true', dest='no_purge', help='Do not purge orphaned data (tracks, artists, albums, etc.). This will make for a faster sync, and useful when files were only added to a library.')
        arg_parser.add_argument('--no-prompt',
          action='store_true', dest='no_prompt', help='Skip files that require user input.')
        arg_parser.add_argument('--speed',
          default='fast', choices=('fast', 'normal'), help="Sync speed. 'fast' will skips files whose timestamps have not changed, while 'normal' scans all files all the time.")
        self.monitor_proc = None
        self._num_added = 0
        self._num_modified = 0
        self._num_deleted = 0
        self._db_session = None
        self._lib = None
        self.start_time = None

    def start(self, args, config):
        import eyed3.utils.prompt
        self._num_loaded = 0
        eyed3.utils.prompt.DISABLE_PROMPT = 'raise' if args.no_prompt else None
        super().start(args, config)
        self.start_time = time.time()
        self._db_session = args.db_session
        try:
            lib = self._db_session.query(Library).filter_by(name=(args._library.name)).one()
        except NoResultFound:
            lib = Library(name=(args._library.name))
            self._db_session.add(lib)
            self._db_session.flush()
        else:
            self._lib = lib
            if self.args.monitor:
                from ._inotify import Monitor
                if self.monitor_proc is None:
                    self.monitor_proc = Monitor()
                for p in self.args.paths:
                    self._watchDir(p)

    def _getArtist(self, session, name, origin, resolved_artist):
        origin_dict = {'origin_city':origin.city if origin else None, 
         'origin_state':origin.state if origin else None, 
         'origin_country':normalizeCountry(origin.country) if origin else None}
        if name == VARIOUS_ARTISTS_NAME:
            artist_rows = [session.query(Artist).filter_by(name=VARIOUS_ARTISTS_NAME, lib_id=NULL_LIB_ID).one()]
        else:
            artist_rows = (session.query(Artist).filter_by)(name=name, 
             lib_id=self._lib.id, **origin_dict).all()
        if artist_rows:
            if len(artist_rows) > 1 and resolved_artist:
                artist = resolved_artist
            else:
                if len(artist_rows) > 1:
                    try:
                        heading = "Multiple artists names '%s'" % artist_rows[0].name
                        artist = console.selectArtist((Fg.blue(heading)), choices=artist_rows,
                          allow_create=True)
                    except PromptExit:
                        log.warning('Duplicate artist requires user intervention to resolve.')
                        artist = None
                    else:
                        if artist not in artist_rows:
                            session.add(artist)
                            session.flush()
                            pout(Fg.blue('Updating artist') + ': ' + name)
                        resolved_artist = artist
                else:
                    assert len(artist_rows) == 1
                    artist = artist_rows[0]
        else:
            artist = Artist(name=name, lib_id=self._lib.id, **origin_dict)
            session.add(artist)
            session.flush()
            pout(Fg.green('Adding artist') + ': ' + name)
        return (artist, resolved_artist)

    def _syncAudioFile(self, audio_file, album_type, d_datetime, session):
        path = audio_file.path
        info = audio_file.info
        tag = audio_file.tag
        album = None
        is_various = album_type == VARIOUS_TYPE
        if not (info and tag):
            log.warning(f"File missing {'audio' if not info else 'tag/metadata'}, skipping: {path}")
            return (None, None)
        if None in (tag.title, tag.artist):
            log.warning('File missing required artist and/or title metadata, skipping: %s' % path)
            return (None, None)
        resolved_artist = None
        resolved_album_artist = None
        try:
            track = session.query(Track).filter_by(path=path,
              lib_id=(self._lib.id)).one()
        except NoResultFound:
            track = None
        else:
            if self.args.speed == 'fast':
                if datetime.fromtimestamp(getctime(path)) == track.ctime:
                    return (
                     track, track.album)
                else:
                    artist, resolved_artist = self._getArtist(session, tag.artist, tag.artist_origin, resolved_artist)
                    if album_type != SINGLE_TYPE:
                        if tag.album_artist:
                            if tag.artist != tag.album_artist:
                                album_artist, resolved_album_artist = self._getArtist(session, tag.album_artist, tag.artist_origin, resolved_album_artist)
                            else:
                                album_artist = artist
                            if artist is None:
                                return (None, None)
                            album_artist_id = album_artist.id if not is_various else VARIOUS_ARTISTS_ID
                            rel_date = tag.release_date
                            rec_date = tag.recording_date
                            or_date = tag.original_release_date
                            if or_date:
                                album = session.query(Album).filter_by(lib_id=(self._lib.id), artist_id=album_artist_id,
                                  title=(tag.album),
                                  original_release_date=or_date).one_or_none()
                            if not album:
                                if rel_date:
                                    album = session.query(Album).filter_by(lib_id=(self._lib.id), artist_id=album_artist_id,
                                      title=(tag.album),
                                      release_date=rel_date).one_or_none()
                            if not album:
                                if rec_date:
                                    album = session.query(Album).filter_by(lib_id=(self._lib.id), artist_id=album_artist_id,
                                      title=(tag.album),
                                      release_date=rel_date,
                                      recording_date=rec_date).one_or_none()
                            if album is None:
                                album = Album(title=(tag.album), lib_id=(self._lib.id), artist_id=album_artist_id,
                                  type=album_type,
                                  release_date=rel_date,
                                  original_release_date=or_date,
                                  recording_date=rec_date,
                                  date_added=d_datetime)
                                pout(f"{Fg.green('Adding album')}: {album.title}")
                                session.add(album)
                        elif album.type != album_type:
                            pout(Fg.yellow('Updating album') + ': ' + album.title)
                            album.type = album_type
                        session.flush()
                    if not track:
                        track = Track(audio_file=audio_file, lib_id=(self._lib.id))
                        self._num_added += 1
                        pout(Fg.green('Adding track') + ': ' + path)
                    else:
                        track.update(audio_file)
                    self._num_modified += 1
                    pout(Fg.yellow('Updating track') + ': ' + path)
                track.artist_id = artist.id
                track.album_id = album.id if album else None
                if tag.genre:
                    for genre in tag.genre.name.split('\x00'):
                        genre_tag = db.getTag(genre, session, (self._lib.id), add=True)
                        track.tags.append(genre_tag)

                else:
                    session.add(track)
                    if album:
                        img_type = None
                        for img in tag.images:
                            for img_type in art.TO_ID3_ART_TYPES:
                                if img.picture_type in art.TO_ID3_ART_TYPES[img_type]:
                                    break
                                img_type = None

                            if img_type is None:
                                log.warning(f"Skipping unsupported image type: {img.picture_type}")

            else:
                new_img = Image.fromTagFrame(img, img_type)
                if new_img:
                    syncImage(new_img, album if img_type in IMAGE_TYPES['album'] else album.artist, session)
                else:
                    log.warning('Invalid image in tag')
                return (track, album)

    @staticmethod
    def _albumTypeHint--- This code section failed: ---

 L. 294         0  LOAD_GLOBAL              collections
                2  LOAD_METHOD              Counter
                4  CALL_METHOD_0         0  ''
                6  STORE_FAST               'types'

 L. 302         8  LOAD_LISTCOMP            '<code_object <listcomp>>'
               10  LOAD_STR                 'SyncPlugin._albumTypeHint.<locals>.<listcomp>'
               12  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
               14  LOAD_FAST                'audio_files'
               16  GET_ITER         
               18  CALL_FUNCTION_1       1  ''
               20  GET_ITER         
             22_0  COME_FROM            40  '40'
               22  FOR_ITER             62  'to 62'
               24  STORE_FAST               'tag'

 L. 303        26  LOAD_FAST                'tag'
               28  LOAD_ATTR                user_text_frames
               30  LOAD_METHOD              get
               32  LOAD_GLOBAL              TXXX_ALBUM_TYPE
               34  CALL_METHOD_1         1  ''
               36  STORE_FAST               'album_type'

 L. 304        38  LOAD_FAST                'album_type'
               40  POP_JUMP_IF_FALSE    22  'to 22'

 L. 305        42  LOAD_FAST                'types'
               44  LOAD_FAST                'album_type'
               46  LOAD_ATTR                text
               48  DUP_TOP_TWO      
               50  BINARY_SUBSCR    
               52  LOAD_CONST               1
               54  INPLACE_ADD      
               56  ROT_THREE        
               58  STORE_SUBSCR     
               60  JUMP_BACK            22  'to 22'

 L. 307        62  LOAD_GLOBAL              len
               64  LOAD_FAST                'types'
               66  CALL_FUNCTION_1       1  ''
               68  LOAD_CONST               1
               70  COMPARE_OP               ==
               72  POP_JUMP_IF_FALSE    90  'to 90'

 L. 308        74  LOAD_FAST                'types'
               76  LOAD_METHOD              most_common
               78  CALL_METHOD_0         0  ''
               80  LOAD_CONST               0
               82  BINARY_SUBSCR    
               84  LOAD_CONST               0
               86  BINARY_SUBSCR    
               88  RETURN_VALUE     
             90_0  COME_FROM            72  '72'

 L. 310        90  LOAD_GLOBAL              len
               92  LOAD_FAST                'types'
               94  CALL_FUNCTION_1       1  ''
               96  LOAD_CONST               0
               98  COMPARE_OP               ==
          100_102  POP_JUMP_IF_FALSE   300  'to 300'

 L. 311       104  LOAD_GLOBAL              set
              106  CALL_FUNCTION_0       0  ''
              108  STORE_FAST               'artist_set'

 L. 312       110  LOAD_GLOBAL              set
              112  CALL_FUNCTION_0       0  ''
              114  STORE_FAST               'album_artist_set'

 L. 313       116  LOAD_GLOBAL              list
              118  CALL_FUNCTION_0       0  ''
              120  STORE_FAST               'albums'

 L. 314       122  LOAD_LISTCOMP            '<code_object <listcomp>>'
              124  LOAD_STR                 'SyncPlugin._albumTypeHint.<locals>.<listcomp>'
              126  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
              128  LOAD_FAST                'audio_files'
              130  GET_ITER         
              132  CALL_FUNCTION_1       1  ''
              134  GET_ITER         
            136_0  COME_FROM           180  '180'
              136  FOR_ITER            196  'to 196'
              138  STORE_FAST               'tag'

 L. 315       140  LOAD_FAST                'tag'
              142  LOAD_ATTR                artist
              144  POP_JUMP_IF_FALSE   158  'to 158'

 L. 316       146  LOAD_FAST                'artist_set'
              148  LOAD_METHOD              add
              150  LOAD_FAST                'tag'
              152  LOAD_ATTR                artist
              154  CALL_METHOD_1         1  ''
              156  POP_TOP          
            158_0  COME_FROM           144  '144'

 L. 318       158  LOAD_FAST                'tag'
              160  LOAD_ATTR                album_artist
              162  POP_JUMP_IF_FALSE   176  'to 176'

 L. 319       164  LOAD_FAST                'album_artist_set'
              166  LOAD_METHOD              add
              168  LOAD_FAST                'tag'
              170  LOAD_ATTR                album_artist
              172  CALL_METHOD_1         1  ''
              174  POP_TOP          
            176_0  COME_FROM           162  '162'

 L. 321       176  LOAD_FAST                'tag'
              178  LOAD_ATTR                album
              180  POP_JUMP_IF_FALSE   136  'to 136'

 L. 322       182  LOAD_FAST                'albums'
              184  LOAD_METHOD              append
              186  LOAD_FAST                'tag'
              188  LOAD_ATTR                album
              190  CALL_METHOD_1         1  ''
              192  POP_TOP          
              194  JUMP_BACK           136  'to 136'

 L. 325       196  LOAD_GLOBAL              len
              198  LOAD_FAST                'artist_set'
              200  CALL_FUNCTION_1       1  ''
              202  LOAD_CONST               1
              204  COMPARE_OP               >
              206  JUMP_IF_FALSE_OR_POP   244  'to 244'

 L. 326       208  LOAD_GLOBAL              len
              210  LOAD_FAST                'album_artist_set'
              212  CALL_FUNCTION_1       1  ''
              214  LOAD_CONST               0
              216  COMPARE_OP               ==
              218  POP_JUMP_IF_TRUE    230  'to 230'
              220  LOAD_FAST                'album_artist_set'
              222  LOAD_GLOBAL              VARIOUS_ARTISTS_NAME
              224  BUILD_SET_1           1 
              226  COMPARE_OP               ==

 L. 325       228  JUMP_IF_FALSE_OR_POP   244  'to 244'
            230_0  COME_FROM           218  '218'

 L. 327       230  LOAD_GLOBAL              len
              232  LOAD_FAST                'albums'
              234  CALL_FUNCTION_1       1  ''
              236  LOAD_GLOBAL              len
              238  LOAD_FAST                'audio_files'
              240  CALL_FUNCTION_1       1  ''
              242  COMPARE_OP               ==
            244_0  COME_FROM           228  '228'
            244_1  COME_FROM           206  '206'

 L. 324       244  STORE_FAST               'is_various'

 L. 330       246  LOAD_FAST                'is_various'
          248_250  POP_JUMP_IF_FALSE   256  'to 256'

 L. 331       252  LOAD_GLOBAL              VARIOUS_TYPE
              254  RETURN_VALUE     
            256_0  COME_FROM           248  '248'

 L. 332       256  LOAD_GLOBAL              len
              258  LOAD_FAST                'albums'
              260  CALL_FUNCTION_1       1  ''
              262  LOAD_GLOBAL              len
              264  LOAD_FAST                'audio_files'
              266  CALL_FUNCTION_1       1  ''
              268  COMPARE_OP               ==
          270_272  POP_JUMP_IF_FALSE   296  'to 296'

 L. 333       274  LOAD_GLOBAL              len
              276  LOAD_FAST                'audio_files'
              278  CALL_FUNCTION_1       1  ''
              280  LOAD_GLOBAL              EP_MAX_SIZE_HINT
              282  COMPARE_OP               >
          284_286  POP_JUMP_IF_FALSE   292  'to 292'
              288  LOAD_GLOBAL              LP_TYPE
              290  RETURN_VALUE     
            292_0  COME_FROM           284  '284'
              292  LOAD_GLOBAL              EP_TYPE
              294  RETURN_VALUE     
            296_0  COME_FROM           270  '270'

 L. 335       296  LOAD_GLOBAL              SINGLE_TYPE
              298  RETURN_VALUE     
            300_0  COME_FROM           100  '100'

 L. 337       300  LOAD_GLOBAL              len
              302  LOAD_FAST                'types'
              304  CALL_FUNCTION_1       1  ''
              306  LOAD_CONST               1
              308  COMPARE_OP               >
          310_312  POP_JUMP_IF_FALSE   340  'to 340'

 L. 338       314  LOAD_GLOBAL              log
              316  LOAD_METHOD              warning
              318  LOAD_STR                 'Inconsistent type hints: %s'
              320  LOAD_GLOBAL              str
              322  LOAD_FAST                'types'
              324  LOAD_METHOD              keys
              326  CALL_METHOD_0         0  ''
              328  CALL_FUNCTION_1       1  ''
              330  BINARY_MODULO    
              332  CALL_METHOD_1         1  ''
              334  POP_TOP          

 L. 339       336  LOAD_CONST               None
              338  RETURN_VALUE     
            340_0  COME_FROM           310  '310'

Parse error at or near `COME_FROM' instruction at offset 244_1

    def handleDirectory(self, d, _):
        pout(Fg.blue('Syncing directory') + ': ' + str(d))
        audio_files = list(self._file_cache)
        self._file_cache = []
        image_files = self._dir_images
        self._dir_images = []
        if not audio_files:
            return
        d_datetime = datetime.fromtimestamp(getctime(d))
        album_type = self._albumTypeHint(audio_files) or LP_TYPE
        album = None
        session = self._db_session
        for audio_file in audio_files:
            try:
                track, album = self._syncAudioFile(audio_file, album_type, d_datetime, session)
            except Exception as ex:
                try:
                    log.error(f"{audio_file.path} sync error: {ex}")
                finally:
                    ex = None
                    del ex

        else:
            if album:
                for img_file in image_files:
                    img_type = art.matchArtFile(img_file)
                    if img_type is None:
                        log.warning(f"Skipping unrecognized image file: {img_file}")
                    else:
                        new_img = Image.fromFile(img_file, img_type)
                        if new_img:
                            new_img.description = os.path.basename(img_file)
                            syncImage(new_img, album if img_type in IMAGE_TYPES['album'] else album.artist, session)
                        else:
                            log.warning(f"Invalid image file: {img_file}")

            session.commit()
            if self.args.monitor:
                self._watchDir(d)

    def _watchDir--- This code section failed: ---

 L. 387         0  LOAD_CONST               False
                2  STORE_FAST               'valid_path'

 L. 388         4  LOAD_GLOBAL              Path
                6  LOAD_FAST                'd'
                8  CALL_FUNCTION_1       1  ''
               10  STORE_FAST               'dirpath'

 L. 389        12  LOAD_LISTCOMP            '<code_object <listcomp>>'
               14  LOAD_STR                 'SyncPlugin._watchDir.<locals>.<listcomp>'
               16  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
               18  LOAD_FAST                'self'
               20  LOAD_ATTR                args
               22  LOAD_ATTR                paths
               24  GET_ITER         
               26  CALL_FUNCTION_1       1  ''
               28  GET_ITER         
               30  FOR_ITER            186  'to 186'
               32  STORE_FAST               'root'

 L. 390        34  SETUP_FINALLY        50  'to 50'

 L. 391        36  LOAD_FAST                'dirpath'
               38  LOAD_METHOD              relative_to
               40  LOAD_FAST                'root'
               42  CALL_METHOD_1         1  ''
               44  POP_TOP          
               46  POP_BLOCK        
               48  JUMP_FORWARD         74  'to 74'
             50_0  COME_FROM_FINALLY    34  '34'

 L. 392        50  DUP_TOP          
               52  LOAD_GLOBAL              ValueError
               54  COMPARE_OP               exception-match
               56  POP_JUMP_IF_FALSE    72  'to 72'
               58  POP_TOP          
               60  POP_TOP          
               62  POP_TOP          

 L. 393        64  POP_EXCEPT       
               66  JUMP_BACK            30  'to 30'
               68  POP_EXCEPT       
               70  JUMP_BACK            30  'to 30'
             72_0  COME_FROM            56  '56'
               72  END_FINALLY      
             74_0  COME_FROM            48  '48'

 L. 395        74  LOAD_CONST               True
               76  STORE_FAST               'valid_path'

 L. 396        78  LOAD_FAST                'self'
               80  LOAD_ATTR                monitor_proc
               82  LOAD_ATTR                dir_queue
               84  LOAD_METHOD              put
               86  LOAD_FAST                'self'
               88  LOAD_ATTR                _lib
               90  LOAD_ATTR                name
               92  LOAD_FAST                'dirpath'
               94  BUILD_TUPLE_2         2 
               96  CALL_METHOD_1         1  ''
               98  POP_TOP          

 L. 399       100  LOAD_FAST                'dirpath'
              102  LOAD_ATTR                parent
              104  STORE_FAST               'parent'

 L. 400       106  SETUP_FINALLY       122  'to 122'

 L. 401       108  LOAD_FAST                'parent'
              110  LOAD_METHOD              relative_to
              112  LOAD_FAST                'root'
              114  CALL_METHOD_1         1  ''
              116  POP_TOP          
              118  POP_BLOCK        
              120  JUMP_FORWARD        142  'to 142'
            122_0  COME_FROM_FINALLY   106  '106'

 L. 402       122  DUP_TOP          
              124  LOAD_GLOBAL              ValueError
              126  COMPARE_OP               exception-match
              128  POP_JUMP_IF_FALSE   140  'to 140'
              130  POP_TOP          
              132  POP_TOP          
              134  POP_TOP          

 L. 404       136  POP_EXCEPT       
              138  JUMP_FORWARD        180  'to 180'
            140_0  COME_FROM           128  '128'
              140  END_FINALLY      
            142_0  COME_FROM           120  '120'

 L. 406       142  LOAD_FAST                'parent'
              144  LOAD_FAST                'root'
              146  COMPARE_OP               !=
              148  POP_JUMP_IF_FALSE   180  'to 180'

 L. 407       150  LOAD_FAST                'self'
              152  LOAD_ATTR                monitor_proc
              154  LOAD_ATTR                dir_queue
              156  LOAD_METHOD              put
              158  LOAD_FAST                'self'
              160  LOAD_ATTR                _lib
              162  LOAD_ATTR                name

 L. 408       164  LOAD_FAST                'parent'

 L. 407       166  BUILD_TUPLE_2         2 
              168  CALL_METHOD_1         1  ''
              170  POP_TOP          

 L. 409       172  LOAD_FAST                'parent'
              174  LOAD_ATTR                parent
              176  STORE_FAST               'parent'
              178  JUMP_BACK           142  'to 142'
            180_0  COME_FROM           148  '148'
            180_1  COME_FROM           138  '138'

 L. 410       180  POP_TOP          
              182  BREAK_LOOP          186  'to 186'
              184  JUMP_BACK            30  'to 30'

 L. 411       186  LOAD_FAST                'valid_path'
              188  POP_JUMP_IF_TRUE    194  'to 194'
              190  LOAD_ASSERT              AssertionError
              192  RAISE_VARARGS_1       1  'exception instance'
            194_0  COME_FROM           188  '188'

Parse error at or near `POP_EXCEPT' instruction at offset 68

    def handleDone(self):
        t = time.time() - self.start_time
        session = self._db_session
        session.query(Meta).one().last_sync = datetime.utcnow()
        self._lib.last_sync = datetime.utcnow()
        num_orphaned_artists = 0
        num_orphaned_albums = 0
        if not self.args.no_purge:
            log.debug('Purging orphans (tracks, artists, albums) from database')
            self._num_deleted, num_orphaned_artists, num_orphaned_albums = deleteOrphans(session)
        if self._num_loaded or self._num_deleted:
            pout('')
            pout("== Library '{}' sync'd [ {:.2f}s time ({:.1f} files/sec) ] ==".format(self._lib.name, t, self._num_loaded / t))
            pout("%d files sync'd" % self._num_loaded)
            pout('%d tracks added' % self._num_added)
            pout('%d tracks modified' % self._num_modified)
            if not self.args.no_purge:
                pout('%d orphaned tracks deleted' % self._num_deleted)
                pout('%d orphaned artists deleted' % num_orphaned_artists)
                pout('%d orphaned albums deleted' % num_orphaned_albums)
            pout('')


@Command.register
class Sync(Command):
    NAME = 'sync'
    HELP = 'Synchronize music directories with database.'

    def __init__(self, subparsers):
        super(Sync, self).__init__(subparsers)
        self.plugin = SyncPlugin(self.parser)
        self.args = None

    def _run--- This code section failed: ---

 L. 453         0  LOAD_DEREF               'args'
                2  JUMP_IF_TRUE_OR_POP     8  'to 8'
                4  LOAD_FAST                'self'
                6  LOAD_ATTR                args
              8_0  COME_FROM             2  '2'
                8  STORE_DEREF              'args'

 L. 454        10  LOAD_FAST                'self'
               12  LOAD_ATTR                plugin
               14  LOAD_DEREF               'args'
               16  STORE_ATTR               plugin

 L. 456        18  LOAD_DEREF               'args'
               20  LOAD_ATTR                monitor
               22  POP_JUMP_IF_FALSE    58  'to 58'
               24  LOAD_GLOBAL              platform
               26  LOAD_METHOD              system
               28  CALL_METHOD_0         0  ''
               30  LOAD_STR                 'Darwin'
               32  COMPARE_OP               ==
               34  POP_JUMP_IF_FALSE    58  'to 58'

 L. 457        36  LOAD_GLOBAL              perr
               38  LOAD_STR                 'Monitor mode is not supported on OS/X\n'
               40  CALL_FUNCTION_1       1  ''
               42  POP_TOP          

 L. 458        44  LOAD_FAST                'self'
               46  LOAD_ATTR                parser
               48  LOAD_METHOD              print_usage
               50  CALL_METHOD_0         0  ''
               52  POP_TOP          

 L. 459        54  LOAD_CONST               1
               56  RETURN_VALUE     
             58_0  COME_FROM            34  '34'
             58_1  COME_FROM            22  '22'

 L. 461        58  LOAD_DICTCOMP            '<code_object <dictcomp>>'
               60  LOAD_STR                 'Sync._run.<locals>.<dictcomp>'
               62  MAKE_FUNCTION_0          'Neither defaults, keyword-only args, annotations, nor closures'
               64  LOAD_DEREF               'args'
               66  LOAD_ATTR                config
               68  LOAD_ATTR                music_libs
               70  GET_ITER         
               72  CALL_FUNCTION_1       1  ''
               74  STORE_FAST               'libs'

 L. 462        76  LOAD_FAST                'libs'
               78  POP_JUMP_IF_TRUE    108  'to 108'
               80  LOAD_DEREF               'args'
               82  LOAD_ATTR                paths
               84  POP_JUMP_IF_TRUE    108  'to 108'

 L. 463        86  LOAD_GLOBAL              perr
               88  LOAD_STR                 '\nMissing at least one path/library in which to sync!\n'
               90  CALL_FUNCTION_1       1  ''
               92  POP_TOP          

 L. 464        94  LOAD_FAST                'self'
               96  LOAD_ATTR                parser
               98  LOAD_METHOD              print_usage
              100  CALL_METHOD_0         0  ''
              102  POP_TOP          

 L. 465       104  LOAD_CONST               1
              106  RETURN_VALUE     
            108_0  COME_FROM            84  '84'
            108_1  COME_FROM            78  '78'

 L. 467       108  BUILD_LIST_0          0 
              110  STORE_FAST               'sync_libs'

 L. 468       112  LOAD_DEREF               'args'
              114  LOAD_ATTR                paths
              116  POP_JUMP_IF_FALSE   192  'to 192'

 L. 469       118  BUILD_LIST_0          0 
              120  STORE_FAST               'file_paths'

 L. 470       122  LOAD_DEREF               'args'
              124  LOAD_ATTR                paths
              126  GET_ITER         
              128  FOR_ITER            168  'to 168'
              130  STORE_FAST               'arg'

 L. 471       132  LOAD_FAST                'arg'
              134  LOAD_FAST                'libs'
              136  COMPARE_OP               in
              138  POP_JUMP_IF_FALSE   156  'to 156'

 L. 473       140  LOAD_FAST                'sync_libs'
              142  LOAD_METHOD              append
              144  LOAD_FAST                'libs'
              146  LOAD_FAST                'arg'
              148  BINARY_SUBSCR    
              150  CALL_METHOD_1         1  ''
              152  POP_TOP          
              154  JUMP_BACK           128  'to 128'
            156_0  COME_FROM           138  '138'

 L. 476       156  LOAD_FAST                'file_paths'
              158  LOAD_METHOD              append
              160  LOAD_FAST                'arg'
              162  CALL_METHOD_1         1  ''
              164  POP_TOP          
              166  JUMP_BACK           128  'to 128'

 L. 477       168  LOAD_FAST                'file_paths'
              170  POP_JUMP_IF_FALSE   204  'to 204'

 L. 478       172  LOAD_FAST                'sync_libs'
              174  LOAD_METHOD              append
              176  LOAD_GLOBAL              MusicLibrary
              178  LOAD_GLOBAL              MAIN_LIB_NAME
              180  LOAD_FAST                'file_paths'
              182  LOAD_CONST               ('paths',)
              184  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              186  CALL_METHOD_1         1  ''
              188  POP_TOP          
              190  JUMP_FORWARD        204  'to 204'
            192_0  COME_FROM           116  '116'

 L. 480       192  LOAD_GLOBAL              list
              194  LOAD_FAST                'libs'
              196  LOAD_METHOD              values
              198  CALL_METHOD_0         0  ''
              200  CALL_FUNCTION_1       1  ''
              202  STORE_FAST               'sync_libs'
            204_0  COME_FROM           190  '190'
            204_1  COME_FROM           170  '170'

 L. 482       204  LOAD_FAST                'self'
              206  LOAD_ATTR                db_engine
              208  LOAD_FAST                'self'
              210  LOAD_ATTR                db_session
              212  ROT_TWO          
              214  LOAD_DEREF               'args'
              216  STORE_ATTR               db_engine
              218  LOAD_DEREF               'args'
              220  STORE_ATTR               db_session

 L. 484       222  LOAD_CLOSURE             'args'
              224  BUILD_TUPLE_1         1 
              226  LOAD_CODE                <code_object _syncLib>
              228  LOAD_STR                 'Sync._run.<locals>._syncLib'
              230  MAKE_FUNCTION_8          'closure'
              232  STORE_FAST               '_syncLib'

 L. 498       234  SETUP_FINALLY       314  'to 314'

 L. 499       236  LOAD_FAST                'sync_libs'
              238  GET_ITER         
            240_0  COME_FROM           296  '296'
              240  FOR_ITER            310  'to 310'
              242  STORE_FAST               'lib'

 L. 500       244  LOAD_FAST                'lib'
              246  LOAD_ATTR                sync
          248_250  POP_JUMP_IF_TRUE    282  'to 282'
              252  LOAD_DEREF               'args'
              254  LOAD_ATTR                force
          256_258  POP_JUMP_IF_TRUE    282  'to 282'

 L. 501       260  LOAD_GLOBAL              pout
              262  LOAD_STR                 '[{}] - sync=False'
              264  LOAD_METHOD              format
              266  LOAD_FAST                'lib'
              268  LOAD_ATTR                name
              270  CALL_METHOD_1         1  ''
              272  LOAD_GLOBAL              log
              274  LOAD_CONST               ('log',)
              276  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              278  POP_TOP          

 L. 502       280  JUMP_BACK           240  'to 240'
            282_0  COME_FROM           256  '256'
            282_1  COME_FROM           248  '248'

 L. 503       282  LOAD_FAST                '_syncLib'
              284  LOAD_FAST                'lib'
              286  CALL_FUNCTION_1       1  ''
              288  STORE_FAST               'result'

 L. 504       290  LOAD_FAST                'result'
              292  LOAD_CONST               0
              294  COMPARE_OP               !=
              296  POP_JUMP_IF_FALSE   240  'to 240'

 L. 505       298  LOAD_FAST                'result'
              300  ROT_TWO          
              302  POP_TOP          
              304  POP_BLOCK        
              306  RETURN_VALUE     
              308  JUMP_BACK           240  'to 240'
              310  POP_BLOCK        
              312  JUMP_FORWARD        368  'to 368'
            314_0  COME_FROM_FINALLY   234  '234'

 L. 506       314  DUP_TOP          
              316  LOAD_GLOBAL              IOError
              318  COMPARE_OP               exception-match
          320_322  POP_JUMP_IF_FALSE   366  'to 366'
              324  POP_TOP          
              326  STORE_FAST               'err'
              328  POP_TOP          
              330  SETUP_FINALLY       354  'to 354'

 L. 507       332  LOAD_GLOBAL              perr
              334  LOAD_GLOBAL              str
              336  LOAD_FAST                'err'
              338  CALL_FUNCTION_1       1  ''
              340  CALL_FUNCTION_1       1  ''
              342  POP_TOP          

 L. 508       344  POP_BLOCK        
              346  POP_EXCEPT       
              348  CALL_FINALLY        354  'to 354'
              350  LOAD_CONST               1
              352  RETURN_VALUE     
            354_0  COME_FROM           348  '348'
            354_1  COME_FROM_FINALLY   330  '330'
              354  LOAD_CONST               None
              356  STORE_FAST               'err'
              358  DELETE_FAST              'err'
              360  END_FINALLY      
              362  POP_EXCEPT       
              364  JUMP_FORWARD        368  'to 368'
            366_0  COME_FROM           320  '320'
              366  END_FINALLY      
            368_0  COME_FROM           364  '364'
            368_1  COME_FROM           312  '312'

 L. 510       368  LOAD_DEREF               'args'
              370  LOAD_ATTR                monitor
          372_374  POP_JUMP_IF_FALSE   606  'to 606'

 L. 511       376  LOAD_CONST               1
              378  LOAD_CONST               ('SYNC_INTERVAL',)
              380  IMPORT_NAME              _inotify
              382  IMPORT_FROM              SYNC_INTERVAL
              384  STORE_FAST               'SYNC_INTERVAL'
              386  POP_TOP          

 L. 512       388  LOAD_FAST                'self'
              390  LOAD_ATTR                plugin
              392  LOAD_ATTR                monitor_proc
              394  STORE_FAST               'monitor'

 L. 515       396  LOAD_FAST                'self'
              398  LOAD_ATTR                db_session
              400  LOAD_METHOD              commit
              402  CALL_METHOD_0         0  ''
              404  POP_TOP          

 L. 517       406  LOAD_FAST                'monitor'
              408  LOAD_METHOD              start
              410  CALL_METHOD_0         0  ''
              412  POP_TOP          

 L. 518       414  SETUP_FINALLY       596  'to 596'

 L. 520       416  LOAD_FAST                'monitor'
              418  LOAD_ATTR                sync_queue
              420  LOAD_METHOD              empty
              422  CALL_METHOD_0         0  ''
          424_426  POP_JUMP_IF_FALSE   446  'to 446'

 L. 521       428  LOAD_GLOBAL              time
              430  LOAD_METHOD              sleep
              432  LOAD_FAST                'SYNC_INTERVAL'
              434  LOAD_CONST               2
              436  BINARY_TRUE_DIVIDE
              438  CALL_METHOD_1         1  ''
              440  POP_TOP          

 L. 522   442_444  JUMP_BACK           416  'to 416'
            446_0  COME_FROM           424  '424'

 L. 524       446  BUILD_MAP_0           0 
              448  STORE_FAST               'sync_libs'

 L. 525       450  LOAD_GLOBAL              range
              452  LOAD_FAST                'monitor'
              454  LOAD_ATTR                sync_queue
              456  LOAD_METHOD              qsize
              458  CALL_METHOD_0         0  ''
              460  CALL_FUNCTION_1       1  ''
              462  GET_ITER         
              464  FOR_ITER            520  'to 520'
              466  STORE_FAST               'i'

 L. 526       468  LOAD_FAST                'monitor'
              470  LOAD_ATTR                sync_queue
              472  LOAD_METHOD              get_nowait
              474  CALL_METHOD_0         0  ''
              476  UNPACK_SEQUENCE_2     2 
              478  STORE_FAST               'lib'
              480  STORE_FAST               'path'

 L. 527       482  LOAD_FAST                'lib'
              484  LOAD_FAST                'sync_libs'
              486  COMPARE_OP               not-in
          488_490  POP_JUMP_IF_FALSE   502  'to 502'

 L. 528       492  LOAD_GLOBAL              set
              494  CALL_FUNCTION_0       0  ''
              496  LOAD_FAST                'sync_libs'
              498  LOAD_FAST                'lib'
              500  STORE_SUBSCR     
            502_0  COME_FROM           488  '488'

 L. 529       502  LOAD_FAST                'sync_libs'
              504  LOAD_FAST                'lib'
              506  BINARY_SUBSCR    
              508  LOAD_METHOD              add
              510  LOAD_FAST                'path'
              512  CALL_METHOD_1         1  ''
              514  POP_TOP          
          516_518  JUMP_BACK           464  'to 464'

 L. 531       520  LOAD_FAST                'sync_libs'
              522  LOAD_METHOD              items
              524  CALL_METHOD_0         0  ''
              526  GET_ITER         
              528  FOR_ITER            588  'to 588'
              530  UNPACK_SEQUENCE_2     2 
              532  STORE_FAST               'lib'
              534  STORE_FAST               'paths'

 L. 532       536  LOAD_FAST                '_syncLib'
              538  LOAD_GLOBAL              MusicLibrary
              540  LOAD_FAST                'lib'
              542  LOAD_FAST                'paths'
              544  LOAD_CONST               ('paths',)
              546  CALL_FUNCTION_KW_2     2  '2 total positional and keyword args'
              548  CALL_FUNCTION_1       1  ''
              550  STORE_FAST               'result'

 L. 533       552  LOAD_FAST                'result'
              554  LOAD_CONST               0
              556  COMPARE_OP               !=
          558_560  POP_JUMP_IF_FALSE   574  'to 574'

 L. 534       562  LOAD_FAST                'result'
              564  ROT_TWO          
              566  POP_TOP          
              568  POP_BLOCK        
              570  CALL_FINALLY        596  'to 596'
              572  RETURN_VALUE     
            574_0  COME_FROM           558  '558'

 L. 535       574  LOAD_FAST                'self'
              576  LOAD_ATTR                db_session
              578  LOAD_METHOD              commit
              580  CALL_METHOD_0         0  ''
              582  POP_TOP          
          584_586  JUMP_BACK           528  'to 528'
          588_590  JUMP_BACK           416  'to 416'
              592  POP_BLOCK        
              594  BEGIN_FINALLY    
            596_0  COME_FROM           570  '570'
            596_1  COME_FROM_FINALLY   414  '414'

 L. 537       596  LOAD_FAST                'monitor'
              598  LOAD_METHOD              join
              600  CALL_METHOD_0         0  ''
              602  POP_TOP          
              604  END_FINALLY      
            606_0  COME_FROM           372  '372'

Parse error at or near `POP_BLOCK' instruction at offset 304