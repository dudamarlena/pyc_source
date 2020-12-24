# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.9-intel/egg/push-roulette.py
# Compiled at: 2014-05-31 16:55:00
import soundcloud, urllib, os, sys
from subprocess import call
from pydub import AudioSegment
from random import randrange
client = soundcloud.Client(client_id='cdbefc208d1db7a07c5af0e27e10b403')
while True:
    tracks = client.get('/tracks', q='downloadable', limit=50, offset=randrange(0, 8001))
    for track in tracks:
        if track.original_content_size < 10000000 and hasattr(track, 'download_url'):
            f = track.title + '.' + track.original_format
            urllib.urlretrieve(track.download_url + '?client_id=cdbefc208d1db7a07c5af0e27e10b403', f)
            audio = AudioSegment.from_file(f, os.path.splitext(f)[1][1:])
            os.remove(f)
            start = randrange(0, int(audio.duration_seconds) - 4) * 1000
            slicedAudio = audio[start:start + 5000]
            clip = os.path.splitext(f)[0] + '.mp3'
            slicedAudio.export(clip, format='mp3')
            print '\nThis clip provided by push-roulette and brought to you by SoundCloud'
            print '\tTitle: ' + track.title
            print '\tArtist: ' + track.user['username']
            print '\tGenre: ' + track.genre + '\n'
            call(['afplay', clip])
            os.remove(clip)
            sys.exit()