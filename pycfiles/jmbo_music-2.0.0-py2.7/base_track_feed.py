# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/music/management/commands/base_track_feed.py
# Compiled at: 2015-04-21 15:32:16
from types import StringType
from django.core.management.base import BaseCommand as ManagementBaseCommand, CommandError
from django.db import transaction
from django.utils import timezone
from django.contrib.sites.models import Site
from django.conf import settings
from music.models import Track

def _do_create(di):
    """Function that interprets a dictionary and creates objects"""
    track = di['track'].strip()
    artists = di['artist']
    if isinstance(artists, StringType):
        artists = [
         artists]
    tracks = Track.objects.filter(title=track, state='published')
    if tracks:
        track = tracks[0]
        track_created = False
    else:
        track = Track.objects.create(title=track, state='published')
        track_created = True
    last_played = di.get('last_played', None)
    if last_played and track.last_played != last_played:
        track.last_played = last_played
        track.save()
    if track_created:
        track.length = di.get('length', 240)
        track.sites = Site.objects.all()
        track.save(set_image=False)
        for artist in artists:
            track.create_credit(artist.strip(), 'artist')

        track.set_image()
    return


class BaseCommand(ManagementBaseCommand):
    help = 'Process a track feed and create or update tracks. Do not call\nthis command directly. It is intended to be subclassed.'

    @transaction.commit_on_success
    def handle(self, *args, **options):
        for di in self.past_tracks:
            _do_create(di)

        di = self.current_track
        if di:
            if not di.has_key('last_played'):
                di['last_played'] = timezone.now()
            _do_create(di)
        for di in self.future_tracks:
            _do_create(di)

    @property
    def past_tracks(self):
        """Return a list of dictionaries. Subclasses must implement this."""
        raise NotImplementedError

    @property
    def current_track(self):
        """Return a dictionary or None. Subclasses must implement this."""
        raise NotImplementedError

    @property
    def future_tracks(self):
        """Return a list of dictionaries. Subclasses must implement this."""
        raise NotImplementedError