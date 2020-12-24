# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/webmpris/__init__.py
# Compiled at: 2013-11-15 16:44:18
__version__ = '1.1'
__description__ = 'REST API to control media players via MPRIS2 interfaces'
requires = [
 'pympris']
README = 'webmpris is a REST API\nto control media players via MPRIS2 interfaces.\n\nSupported intefaces:\norg.mpris.MediaPlayer2              via /players/<id>/Root\norg.mpris.MediaPlayer2.Player       via /players/<id>/Player\norg.mpris.MediaPlayer2.TrackList    via /players/<id>/TrackList\norg.mpris.MediaPlayer2.Playlists    via /players/<id>/Playlists\n\n'