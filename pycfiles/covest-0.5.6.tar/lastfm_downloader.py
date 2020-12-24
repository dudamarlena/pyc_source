# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /usr/lib/python2.7/site-packages/cover_grabber/lastfm_downloader.py
# Compiled at: 2012-07-03 20:53:30
import urllib
try:
    import xml.etree.cElementTree as ETree
except:
    import xml.etree.ElementTree as ETree

class LastFMDownloader(object):

    def __init__(self, album_name, artist_name):
        """ Initializes LastFM Downloader """
        self.LASTFM_API_KEY = 'a42ead6d2dcc2938bec2cda08a03b519'
        self.LASTFM_URL = 'http://ws.audioscrobbler.com/2.0/?method=album.search&album={album_name}&api_key=' + self.LASTFM_API_KEY
        self.album_name = album_name
        self.artist_name = artist_name
        self.url = self.format_url()

    def format_url(self):
        """ Sanitize and format URL for Last FM search """
        return self.LASTFM_URL.format(album_name=self.album_name.encode('utf8'))

    def search_for_image(self):
        """ Use LastFM's API to obtain a URL for the album cover art """
        print ('LastFM: Searching for "{artist_name} - {album_name}"').format(artist_name=self.artist_name, album_name=self.album_name)
        response = urllib.urlopen(self.url).read()
        xml_data = ETree.fromstring(response)
        for element in xml_data.getiterator('album'):
            if element.find('artist').text.lower() == self.artist_name.lower().encode('utf-8'):
                for elmnt in element.findall('image'):
                    if elmnt.attrib['size'] == 'extralarge':
                        url = elmnt.text
                        if url:
                            return url
                        return

        return