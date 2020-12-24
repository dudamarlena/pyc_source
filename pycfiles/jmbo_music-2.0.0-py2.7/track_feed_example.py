# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/music/management/commands/track_feed_example.py
# Compiled at: 2015-04-21 15:32:16
from music.management.commands.base_track_feed import BaseCommand

class Command(BaseCommand):

    @property
    def past_tracks(self):
        return [
         dict(track="Don't look back in anger", artist='Oasis'),
         dict(track='Genie', artist='Springbok Nude Girls'),
         dict(track='Sexy and I Know It', artist='LMFAO'),
         dict(track='Young, Wild & Free', artist=['Snoop Dogg', 'Wiz Khalifa', 'Bruno Mars']),
         dict(track='Take Care', artist=['Drake', 'Rihanna']),
         dict(track='Niggas in Paris', artist=['Jay-Z', 'Kanye West'])]

    @property
    def current_track(self):
        return dict(track='Devil n Pistol', artist='Taxi Violence')

    @property
    def future_tracks(self):
        return [
         dict(track='Six Underground', artist=['Marilyn Manson', 'Sneaker Pimps'])]