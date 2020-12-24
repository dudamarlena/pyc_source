# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pyrana/playlists/sanerandalbums.py
# Compiled at: 2011-07-09 22:56:18
import os, random, pickle
from md5 import md5
from feather import Plugin

class SaneRandomAlbums(Plugin):
    listeners = set(['play', 'skipsong', 'skipalbum', 'albumstart', 'albumend', 'songend'])
    messengers = set(['songloaded', 'albumstart', 'albumend'])
    name = 'SaneRandomAlbums'
    audio_types = set(['.mp3', '.m4a', '.ogg'])

    def __init__(self, musicdir, seen_file):
        super(SaneRandomAlbums, self).__init__()
        root = os.path.expanduser(musicdir)
        artistdata = [ [ os.path.join(artist, album) for album in os.listdir(artist) if os.path.isdir(os.path.join(artist, album)) ] for artist in [ os.path.join(root, artistname) for artistname in os.listdir(root) if os.path.isdir(os.path.join(root, artistname))
                                                                                                                                                   ]
                     ]
        self.artistdata = filter(None, artistdata)
        self.last_artist = self.current_artist = None
        self.seen_file = seen_file
        self.__init_seen()
        return

    def __init_seen(self):
        self.seen_file = os.path.expanduser(self.seen_file)
        if os.path.exists(self.seen_file):
            self.seen = pickle.load(open(self.seen_file, 'r'))
        else:
            self.seen = {}
        self.current_album_hash = None
        return

    def next_album(self, payload):
        while self.current_artist == self.last_artist:
            self.current_artist = random.choice(self.artistdata)

        self.last_artist = self.current_artist
        albumpath = self.current_artist.pop(random.randrange(len(self.current_artist)))
        album_hash = md5(albumpath).hexdigest()
        while album_hash in self.seen:
            albumpath = self.current_artist.pop(random.randrange(len(self.current_artist)))
            album_hash = md5(albumpath).hexdigest()

        self.seen[self.current_album_hash] = True
        self.current_album_hash = album_hash
        self.current_album = sorted([ os.path.join(albumpath, song) for song in os.listdir(albumpath) if os.path.splitext(song)[(-1)] in self.audio_types
                                    ])
        self.send('albumstart', albumpath)

    play = next_album
    skipalbum = next_album
    albumend = next_album

    def next_song(self, payload):
        if len(self.current_album) == 0:
            pickle.dump(self.seen, open(self.seen_file, 'w'))
            self.send('albumend')
        else:
            song = self.current_album[0]
            self.current_album = self.current_album[1:]
            self.send('songloaded', song)

    skipsong = next_song
    albumstart = next_song
    songend = next_song