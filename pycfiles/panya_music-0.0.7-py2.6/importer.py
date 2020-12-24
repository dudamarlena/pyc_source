# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/music/importer.py
# Compiled at: 2011-09-19 04:01:13
from datetime import datetime, timedelta
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.utils.importlib import import_module
from music.models import MusicCreditOption, Track

class TrackImporter(object):

    def get_importer(self):
        """
        Resolve importer from TRACK_IMPORTER_CLASS setting.
        """
        try:
            importer_path = settings.TRACK_IMPORTER_CLASS
        except AttributeError:
            raise ImproperlyConfigured('No TRACK_IMPORTER_CLASS setting found.')

        try:
            dot = importer_path.rindex('.')
        except ValueError:
            raise ImproperlyConfigured("%s isn't a Track Importer module." % importer_path)

        module, classname = importer_path[:dot], importer_path[dot + 1:]
        try:
            mod = import_module(module)
        except ImportError, e:
            raise ImproperlyConfigured('Could not import Track Importer %s: "%s".' % (module, e))

        try:
            importer_class = getattr(mod, classname)
        except AttributeError:
            raise ImproperlyConfigured('Track Importer module "%s" does not define a "%s" class.' % (module, classname))

        importer_instance = importer_class()
        if not hasattr(importer_instance, 'run'):
            raise ImproperlyConfigured('Track Importer class "%s" does not define a run method. Implement the method to return a list of Track objects.' % classname)
        return importer_instance

    def lookup_track(self, track):
        """
        Looks up Django Track object for provided raw importing track object.
        """
        tracks = Track.objects.filter(title__iexact=track.title)
        for track_obj in tracks:
            for contributor in track_obj.get_primary_contributors(permitted=False):
                if contributor.title == track.artist:
                    return track_obj

        return

    def run(self):
        """
        Run import.
        """
        latest_track = Track.objects.all().order_by('-last_played')
        latest_track = latest_track[0] if latest_track else None
        importer = self.get_importer()
        tracks = importer.run()
        for track in tracks:
            if not latest_track or not latest_track.last_played or track.start_time > latest_track.last_played:
                obj = self.lookup_track(track)
                if latest_track:
                    if obj == latest_track:
                        print '[%s-%s]: Start time not updated as it is the latest track.' % (track.title, track.artist)
                        continue
                    print obj or '[%s-%s]: Created.' % (track.title, track.artist)
                    obj = Track.objects.create(title=track.title)
                    obj.length = track.length
                    roles = MusicCreditOption.objects.all().order_by('role_priority')
                    role = roles[0].role_priority if roles else 1
                    obj.create_credit(track.artist, role)
                else:
                    print '[%s-%s]: Not created as it already exists.' % (track.title, track.artist)
                obj.last_played = track.start_time
                obj.save()
                print '[%s-%s]: Start time updated to %s.' % (track.title, track.artist, track.start_time)
            else:
                print '[%s-%s]: Not created as it has a past start time of %s (latest %s). ' % (track.title, track.artist, track.start_time, latest_track.last_played)

        return