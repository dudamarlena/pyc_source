# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/david/source/lyrics/lyrics/fetcher.py
# Compiled at: 2013-02-03 10:36:13
import re, requests
from requests.exceptions import ConnectionError
from bs4 import BeautifulSoup, NavigableString
import database, settings, debug
from _compatibility import unicode

def fetch(artist, song, album):
    try:
        lyrics = Wikia.fetch(artist, song, album)
        if lyrics or settings.save_not_found_lyrics:
            database.save(artist, song, album, lyrics)
    except ConnectionError as e:
        lyrics = 'Could not fetch lyrics. Connection failed.'
        debug.debug('Connection error: %r' % e)

    return lyrics


class Wikia(object):

    def __init__(self):
        self.url = 'http://lyrics.wikia.com/api.php?artist=%s&song=%s&fmt=json'

    def fetch(self, artist, song, album):
        if not artist or not song:
            return
        r = requests.get(self.url % (artist, song))
        if r.status_code != 200:
            return
        else:
            match = re.search("'url':'([^']+)'", r.text)
            if match is None:
                return
            html_url = match.group(1)
            debug.debug('fetch url', html_url)
            if 'action=edit' in html_url:
                return
            r = requests.get(html_url)
            gracenote = False
            if r.status_code != 200:
                html_url = html_url[:9] + html_url[9:].replace('/', '/Gracenote:', 1)
                debug.debug('fetch url', html_url)
                r = requests.get(html_url)
                gracenote = True
                if r.status_code != 200:
                    return
            match = re.search("<div class='lyricbox'>", r.text)
            if match is None:
                debug.debug('src not found in url', html_url)
                return
            soup = BeautifulSoup(r.text)
            lyricbox = soup.find('div', 'lyricbox')
            if lyricbox is None:
                debug.debug("BeautifulSoup doesn't find content", html_url)
                return
            if gracenote:
                lyricbox = lyricbox.find('p')
            lyrics = ''
            for c in lyricbox.contents:
                text = unicode(c).strip()
                if type(c) == NavigableString:
                    lyrics += text.strip()
                elif text.startswith('<br'):
                    lyrics += '\n'

            return lyrics.strip()


Wikia = Wikia()