# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/mishmash/commands/mgmt.py
# Compiled at: 2020-03-01 00:28:25
# Size of source mod 2**32: 8984 bytes
import os
from eyed3.core import VARIOUS_TYPE
import eyed3.utils.prompt as prompt
from nicfit.console.ansi import Style, Fg
from ..orm import Artist, Library, Image, IMAGE_TABLES
from ..core import Command
from ..console import promptArtist, selectArtist
from ..util import normalizeCountry, commonDirectoryPrefix, mostCommonItem

@Command.register
class SplitArtists(Command):
    NAME = 'split-artists'
    HELP = 'Split a single artist name into N distinct artists.'
    _library_arg_nargs = 1

    def _initArgParser(self, parser):
        super()._initArgParser(parser)
        parser.add_argument('artist', help='The name of the artist to split.')

    def _displayArtistMusic(self, artist, albums, singles):
        if albums:
            print('%d albums by %s:' % (len(albums),
             Style.bright(Fg.blue(artist.name))))
            for alb in albums:
                print('%s %s' % (str(alb.getBestDate()).center(17),
                 alb.title))

        if singles:
            print('%d single tracks by %s' % (
             len(singles), Style.bright(Fg.blue(artist.name))))
            for s in singles:
                print('\t%s' % s.title)

    def _run(self):
        session = self.db_session
        lib = session.query(Library).filter(Library.name == self.args.lib).one()
        artists = session.query(Artist).filter(Artist.lib_id == lib.id).filter(Artist.name == self.args.artist).all()
        if not artists:
            print('Artist not found: %s' % self.args.artist)
            return 1
        elif len(artists) > 1:
            artist = selectArtist((Fg.blue("Select which '%s' to split...") % artists[0].name),
              choices=artists,
              allow_create=False)
        else:
            artist = artists[0]
        albums = list(artist.albums) + artist.getAlbumsByType(VARIOUS_TYPE)
        singles = artist.getTrackSingles()
        if len(albums) < 2:
            if len(singles) < 2:
                print("%d albums and %d singles found for '%s', nothing to do." % (
                 len(albums), len(singles), artist.name))
                return 0
        self._displayArtistMusic(artist, albums, singles)

        def _validN--- This code section failed: ---

 L.  69         0  SETUP_FINALLY        24  'to 24'

 L.  70         2  LOAD_FAST                '_n'
                4  LOAD_CONST               1
                6  COMPARE_OP               >
                8  JUMP_IF_FALSE_OR_POP    20  'to 20'
               10  LOAD_FAST                '_n'
               12  LOAD_GLOBAL              len
               14  LOAD_DEREF               'albums'
               16  CALL_FUNCTION_1       1  ''
               18  COMPARE_OP               <=
             20_0  COME_FROM             8  '8'
               20  POP_BLOCK        
               22  RETURN_VALUE     
             24_0  COME_FROM_FINALLY     0  '0'

 L.  71        24  DUP_TOP          
               26  LOAD_GLOBAL              Exception
               28  COMPARE_OP               exception-match
               30  POP_JUMP_IF_FALSE    44  'to 44'
               32  POP_TOP          
               34  POP_TOP          
               36  POP_TOP          

 L.  72        38  POP_EXCEPT       
               40  LOAD_CONST               False
               42  RETURN_VALUE     
             44_0  COME_FROM            30  '30'
               44  END_FINALLY      

Parse error at or near `POP_TOP' instruction at offset 34

        n = prompt('\nEnter the number of distinct artists', type_=int, validate=_validN)
        new_artists = []
        for i in range(1, n + 1):
            print(Style.bright('\n%s #%d') % (Fg.blue(artist.name), i))
            a = artist if i == 1 else Artist(name=(artist.name), date_added=(artist.date_added),
              lib_id=(artist.lib_id))
            a.origin_city = prompt('   City', required=False)
            a.origin_state = prompt('   State', required=False)
            a.origin_country = prompt('   Country', required=False, type_=normalizeCountry)
            new_artists.append(a)
        else:
            if not Artist.checkUnique(new_artists):
                print(Fg.red('Artists must be unique.'))
                return 1

        for a in new_artists:
            session.add(a)
        else:
            session.flush()
            print(Style.bright('\nAssign albums to the correct artist.'))
            for i, a in enumerate(new_artists):
                print('Enter %s%d%s for %s from %s%s%s' % (
                 Style.BRIGHT, i + 1, Style.RESET_BRIGHT,
                 a.name,
                 Style.BRIGHT, a.origin(country_code='iso3c'),
                 Style.RESET_BRIGHT))
            else:

                def _promptForArtist(_text):
                    a = prompt(_text, type_=int, choices=(range(1, len(new_artists) + 1)))
                    return new_artists[(a - 1)]

                print('')
                for alb in albums:
                    path = commonDirectoryPrefix(*[t.path for t in alb.tracks])
                    path = (os.path.join)(*path.split(os.sep)[-2:])
                    a = _promptForArtist('%s (%s)' % (alb.title, path))
                    if alb.type != VARIOUS_TYPE:
                        alb.artist_id = a.id

                for track in alb.tracks:
                    if track.artist_id == artist.id:
                        track.artist_id = a.id
                else:
                    print('')
                    for track in singles:
                        a = _promptForArtist(track.title)
                        track.artist_id = a.id
                    else:
                        session.flush()


@Command.register
class MergeArtists(Command):
    NAME = 'merge-artists'
    HELP = 'Merge two or more artists into a single artist.'
    _library_arg_nargs = 1

    def _initArgParser(self, parser):
        super()._initArgParser(parser)
        parser.add_argument('artists', nargs='+', help='The artist names to merge.')

    def _run(self):
        session = self.db_session
        lib = session.query(Library).filter(Library.name == self.args.lib).one()
        merge_list = []
        for artist_arg in self.args.artists:
            artists = session.query(Artist).filter(Artist.name == artist_arg).filter(Artist.lib_id == lib.id).all()
            if len(artists) == 1:
                merge_list.append(artists[0])
        else:
            if len(artists) > 1:
                merge_list += selectArtist((Fg.blue('Select the artists to merge...')),
                  multiselect=True,
                  choices=artists)

        if len(merge_list) > 1:
            artist_ids = {a:a.id for a in merge_list}
            min_id = min(*artist_ids.keys())
            artist = artist_ids[min_id]
            mc = mostCommonItem
            new_artist = promptArtist(('Merging %d artists into new artist...' % len(merge_list)),
              default_name=(mc([a.name for a in merge_list])),
              default_city=(mc([a.origin_city for a in merge_list])),
              default_state=(mc([a.origin_state for a in merge_list])),
              default_country=(mc([a.origin_country for a in merge_list])),
              artist=artist)
            new_artist.lib_id = lib.id
        else:
            print('Nothing to do, %s' % ('artist not found' if not len(merge_list) else 'only one artist found'))
            return 1
            assert new_artist in merge_list
            for artist in merge_list:
                if artist is new_artist:
                    pass
                else:
                    with session.no_autoflush:
                        for alb in list(artist.albums):
                            if alb.type != VARIOUS_TYPE:
                                alb.artist_id = new_artist.id
                                artist.albums.remove(alb)
                                with session.no_autoflush:
                                    new_artist.albums.append(alb)
                            for track in alb.tracks:
                                if track.artist_id == artist.id:
                                    track.artist_id = new_artist.id

                        else:
                            for track in artist.getTrackSingles():
                                track.artist_id = new_artist.id

                    session.flush()
                    session.delete(artist)
                    session.flush()


@Command.register
class Images(Command):
    NAME = 'image'
    HELP = 'Image mgmt.'
    _library_arg_nargs = 1

    def _initArgParser(self, parser):
        super()._initArgParser(parser)
        parser.add_argument('ids', nargs='+', help='The image IDs operate on.')
        parser.add_argument('--remove', action='store_true', help='Remove images from the database.')

    def _run(self):
        for id_ in self.args.ids:
            image = self.db_session.query(Image).filter(Image.id == int(id_)).first()
            if not image:
                print(f"Image not found: {id_}")
            elif self.args.remove:
                for table in IMAGE_TABLES:
                    self.db_session.execute(f"DELETE FROM {table.name} where img_id={id_}")
                else:
                    self.db_session.delete(image)

            else:
                print(image)
        else:
            self.db_session.commit()