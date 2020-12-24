# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/asc/parser.py
# Compiled at: 2011-02-15 04:49:04
from datetime import datetime, timedelta
import json, os, re
from urllib import urlopen

class Parser(object):
    tracks = []

    def __init__(self, url):
        self.url = url
        self.parse()

    def parse_length(self, length):
        minutes = int(length[:2])
        seconds = int(length[3:5])
        return minutes * 60 + seconds

    def parse(self):
        print 'Querying %s' % self.url
        data = urlopen(self.url).read()
        data = data.split('\n')
        start_time = datetime.now()
        for line in data:
            match = re.match('(.{8})(.{8})(.{7})(.{51})(.{102})(.{8})', line)
            if match:
                length = self.parse_length(match.group(6))
                if match.group(3).startswith('Song'):
                    track = Track(title=match.group(5), artist=match.group(4), status=match.group(2), length=length, start_time=start_time)
                    self.tracks.append(track)
                    print 'Resolved %s' % track
                start_time += timedelta(seconds=length)

    def now_playing(self):
        for track in self.tracks:
            if track.status.startswith('Playing'):
                return track


class Track(object):

    def __init__(self, title, artist, status, length, start_time):
        self.title = self.sanitize(title)
        self.artist = self.sanitize(artist)
        self.status = self.sanitize(status).lower()
        self.length = length
        self.start_time = start_time

    def sanitize(self, text):
        text = re.sub(' +', ' ', text)
        return text.rstrip(' ').title().replace("'S", "'s").replace("'R", "'r")

    def __unicode__(self):
        return '%s - %s - %s - %s - %s' % (self.start_time, self.status, self.title, self.artist, self.length)

    def __str__(self):
        return self.__unicode__()