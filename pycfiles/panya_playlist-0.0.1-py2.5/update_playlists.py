# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/playlist/management/commands/update_playlists.py
# Compiled at: 2011-01-05 03:30:24
from django.core.management.base import BaseCommand
from playlist.models import Playlist
from dstv.epg import WebserviceResponseError

class Command(BaseCommand):

    def handle(self, **options):
        print 'Updating playlists, please wait...'
        for playlist in Playlist.objects.exclude(classname='ManualPlaylist'):
            print 'Updating %s' % playlist
            try:
                playlist.as_leaf_class().update()
            except WebserviceResponseError, e:
                print 'Update failed: %s' % e

        print 'Update complete.'