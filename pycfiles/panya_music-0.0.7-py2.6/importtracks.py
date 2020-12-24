# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/music/management/commands/importtracks.py
# Compiled at: 2011-09-19 04:01:13
from django.core.management.base import BaseCommand, CommandError
from music.importer import TrackImporter

class Command(BaseCommand):
    args = '<poll_id poll_id ...>'
    help = 'Closes the specified poll for voting'

    def handle(self, *args, **options):
        try:
            importer = TrackImporter()
            importer.run()
        except Exception, e:
            raise CommandError(e)