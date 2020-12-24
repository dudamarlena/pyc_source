# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pyrana/Pyrana.py
# Compiled at: 2011-07-09 22:57:16
__doc__ = " Pyrana -- a minimalist music player.\n\nThis program was written out of frustration with larger music players. Pretty\nmuch all I've ever wanted out of a music player was one that played random\nalbums by picking a random artist, then picking a random album, then playing\nthat album, then picking another random artist.\n\nFor some reason, I've never run into a music player that played random albums\nthat way, which led to me often ending up having to skip past multiple albums\nby a particular artist, especially when the artist has a large discography.\n\nWhile I call this player minimalist, that's not set in stone -- I'll probably\nadd last.fm scrobbling capability and other various features. These features\nwill, however, be ones that I find useful. I highly doubt this app will ever be\nincredibly bloated.\n\n"
from pkg_resources import resource_filename
from hashlib import md5
import ConfigParser, os, random, shutil, ConfigParser
from pkg_resources import resource_filename
from feather import Application
from pyrana.uis import GTK2
from pyrana.players import PyGSTPlayer, PyGamePlayer, PygletPlayer
from pyrana.playlists import SaneRandomAlbums
from pyrana.plugins import Notify, PidginStatus
Pyrana = Application(['play', 'pause', 'skipsong', 'skipalbum'])

def main():
    """Entry point for Pyrana.py.
    Start rockin'
    """
    root = os.path.expanduser(path)
    artists = [ [ os.path.join(artist, album) for album in os.listdir(artist) if os.path.isdir(os.path.join(artist, album)) ] for artist in [ os.path.join(root, artistname) for artistname in os.listdir(root) if os.path.isdir(os.path.join(root, artistname))
                                                                                                                                            ]
              ]
    return [ a for a in artists if a ]


class Pyrana(object):
    """ Our player, sending sweet, sweet sounds to our speakers.  """
    home = os.path.expanduser('~')
    confdir = os.path.join(home, '.config', 'pyrana')
    if not os.path.isdir(confdir):
        os.mkdir(confdir)
    conffile = os.path.join(confdir, 'options.ini')
    if not os.path.isfile(conffile):
        conftmpl = resource_filename('pyrana', 'resources/options.ini')
        shutil.copy(conftmpl, conffile)
    config = ConfigParser.ConfigParser()
    config.read(conffile)
    musicdir = os.path.expanduser(config.get('playlist', 'music_directory'))
    seenfile = os.path.expanduser(config.get('playlist', 'seen_file'))
    Pyrana.register(GTK2())
    Pyrana.register(PyGSTPlayer())
    Pyrana.register(SaneRandomAlbums(musicdir, seenfile))
    Pyrana.register(Notify())
    Pyrana.register(PidginStatus())
    Pyrana.start()


if __name__ == '__main__':
    main()