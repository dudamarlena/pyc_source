# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/kyle/projects/top30/pyenv/lib/python3.7/site-packages/top30/chart.py
# Compiled at: 2019-04-09 15:18:15
# Size of source mod 2**32: 5495 bytes
"""
Manages the Top30 chart and related functions
"""
from __future__ import unicode_literals
import mutagen, os, youtube_dl, top30

class Chart:
    __doc__ = '\n    A Top 30 chart is what is sent detailing the top 30 songs of the week.\n    '

    def __init__(self, chart_file, prefix=''):
        self.prefix = prefix
        self.songs = parse_chart(chart_file)
        for i in range(0, len(self.songs)):
            self.find_song(i)

    def get(self, position, attribute):
        """
        Returns a property from the song at a position in the chart
        """
        return self.songs[(position - 1)][attribute]

    def get_prefix(self):
        return self.prefix

    def find_song(self, position):
        """
        Finds a song in the download directory. If it is not found
        it attempts to download it.
        """
        song = self.songs[position]
        artist = sanitize(song['artist'])
        title = sanitize(song['title'])
        song_filename = artist + '-' + title
        for filename in os.listdir(top30.SETTINGS.song_directory()):
            if filename.endswith(song_filename + '.ogg') or song_filename in filename:
                self.songs[position]['path'] = os.path.join(top30.SETTINGS.song_directory(), filename)
                return

        print(song['title'] + ' by ' + song['artist'] + ' cannot be found')
        url = input('Enter the youtube URL of the song or file location: ')
        if 'http://' in url or 'https://' in url:
            download_song(url, song_filename)
            self.songs[position]['path'] = os.path.join(top30.SETTINGS.song_directory(), song_filename + '.ogg')
            start = input('Enter the start time (mm:ss): ')
            set_start(self.songs[position]['path'], start)
            return
        url = os.path.expanduser(url)
        if os.path.isfile(url):
            os.symlink(url, os.path.join(top30.SETTINGS.song_directory(), song_filename + '.ogg'))
        else:
            while not os.path.isfile(url):
                if 'http://' not in url and 'https://' not in url:
                    print('Unable to find file')
                    print(song['title'] + ' by ' + song['artist'] + ' cannot be found')
                    url = input('Enter the youtube URL of the song or file location: ')
                    if 'http://' not in url and 'https://' not in url:
                        url = os.path.expanduser(url)

            if 'http://' in url or 'https://' in url:
                download_song(url, song_filename)
                start = input('Enter the start time (mm:ss): ')
                set_start(os.path.join(top30.SETTINGS.song_directory(), song_filename + '.ogg'), start)
            else:
                os.symlink(url, os.path.join(top30.SETTINGS.song_directory(), song_filename + '.ogg'))
        self.songs[position]['path'] = os.path.join(top30.SETTINGS.song_directory(), song_filename + '.ogg')


def sanitize(string):
    """
    Sanitizes a string so that it can be used as part of a filename
    """
    string = string.strip().lower()
    string = string.replace(' ', '_').replace('feat.', 'feat').replace('ft.', 'ft')
    string = string.replace('/', '').replace(',', '').replace('’', '')
    string = string.replace("'", '').replace('&', '').replace('__', '_')
    return string


def parse_chart(filename):
    """
    Parses a chart textfile at filename

    The text file has the format:
    Position | Artist | Title | Loc/Int
    """
    text = open(filename).read()
    chart_list = text.split('\n')
    chart = []
    for song in chart_list:
        song = [i.trim() for i in song.split('|')]
        chart.append({'artist':chart_list[1],  'title':chart_list[2]})

    return chart


def download_song(url, filename):
    """
    Downloads a song at url and converts it into a useable format
    """
    ydl_opts = {'outtmpl':os.path.join(top30.SETTINGS.song_directory(), filename + '.%(ext)s'), 
     'format':'bestaudio', 
     'postprocessors':[
      {'key':'FFmpegExtractAudio', 
       'preferredcodec':'vorbis'}]}
    with youtube_dl.YoutubeDL(ydl_opts) as (ydl):
        ydl.download([url])


def set_start(filename, start_time):
    """
    Writes the start of the song section to file
    """
    song_meta = mutagen.File(filename, easy=True)
    song_meta[top30.SETTINGS.song_start_tag()] = start_time
    song_meta.save()