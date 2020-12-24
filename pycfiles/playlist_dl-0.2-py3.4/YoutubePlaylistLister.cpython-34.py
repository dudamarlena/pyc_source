# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\playlist_dl\YoutubePlaylistLister.py
# Compiled at: 2015-10-31 14:03:48
# Size of source mod 2**32: 616 bytes
import youtube_dl
ydl = youtube_dl.YoutubeDL()
url = input('Enter URL of playlist (any url will do) : \n')
res = ydl.extract_info(url, download=False)
if 'entries' in res:
    res = res['entries']
s = ''
for i in res:
    print(len(i['requested_formats']))
    s = s + str(i['playlist_index']) + '\n' + i['title'] + '\n' + i['webpage_url'] + '\n'
    print(i['playlist_index'])
    print(i['title'])
    print(i['webpage_url'])

fp = open('output.txt', 'w')
fp.write(s)
fp.close()