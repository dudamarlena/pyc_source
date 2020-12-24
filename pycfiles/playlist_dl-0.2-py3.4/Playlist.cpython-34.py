# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\playlist_dl\Playlist.py
# Compiled at: 2015-11-02 03:27:50
# Size of source mod 2**32: 1363 bytes
import json, youtube_dl
try:
    from .Video import Video
except SystemError:
    from Video import Video

class Playlist:
    __doc__ = '\n\tPlaylist class\n\t'

    def __init__(self, url):
        """
                Initialises the class
                url is the playlist url
                If url = playlist.json, then it loads from the local playlist data.
                """
        if url == 'playlist.json':
            ptr = open('playlist.json', 'r')
            self.res = json.loads(ptr.read())['entries']
            ptr.close()
        else:
            ydl = youtube_dl.YoutubeDL()
            res = ydl.extract_info(url, download=False)
            if 'entries' in res:
                self.res = res['entries']
            self.makeSimpleList()
            ptr = open('playlist.json', 'w')
            ptr.write(json.dumps(res, indent=4))
            ptr.close()

    def download(self, index, **kwargs):
        """
                Resumes the download of item at index 'index' from the playlist
                """
        vobj = self.res[(index - 1)]
        video = Video(vobj)
        return video.download(**kwargs)

    def makeSimpleList(self):
        """
                Saves a simple json file for users to see what they have in the playlist
                """
        ptr = open('videolist.json', 'w')
        dic = {}
        c = 1
        for i in self.res:
            dic[c] = {'title': i['title'],  'url': i['webpage_url']}
            c += 1

        ptr.write(json.dumps(dic, indent=4))
        ptr.close()