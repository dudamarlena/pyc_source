# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\playlist_dl\Video.py
# Compiled at: 2015-11-02 03:27:39
# Size of source mod 2**32: 3858 bytes
import json, youtube_dl
from platform import subprocess

class Video:
    __doc__ = '\n\tVideo class\n\tGet video info, parse them and download videos\n\t'

    def __init__(self, vobj):
        """
                Inits the Video class
                """
        self.vobj = vobj
        self.url = vobj['webpage_url']

    def getVStream(self, height, ext=''):
        """
                Gets the format id of the required video stream
                Searches only DASH video
                """
        retid = 0
        csize = 18446744073709551616
        for item in self.vobj['formats']:
            if item['format_note'] != 'DASH video':
                if item['format'].find('DASH video') == -1:
                    continue
            if ext:
                if item['ext'] != ext:
                    continue
                if item['height'] != height:
                    continue
                if item['filesize'] < csize:
                    retid = item['format_id']
                    csize = item['filesize']
                    continue

        return int(retid)

    def getAStream(self, abr, ext=''):
        """
                Gets the format id of the required audio stream
                Searches only in DASH audio
                """
        retid = 0
        csize = 18446744073709551616
        for item in self.vobj['formats']:
            if item['format_note'] != 'DASH audio':
                if item['format'].find('DASH audio') == -1:
                    continue
            if ext:
                if item['ext'] != ext:
                    continue
                if item['abr'] != abr:
                    continue
                if item['filesize'] < csize:
                    retid = item['format_id']
                    csize = item['filesize']
                    continue

        return int(retid)

    def getBestDL(self, res='', bitrate='', vext='', aext=''):
        """
                Gets the best possible download combination for you
                If return has one item in array, that means it is a complete video
                If 2 items, then video+audio stream. 0 in these values means let yt-dl choose automatic
                """
        v, a = res, bitrate
        if not res:
            v = 0
        else:
            v = 0
            for item in self.vobj['formats']:
                if item['format_note'].find('DASH') == -1 and item['format'].find('DASH') == -1 and item['height'] == res:
                    v = int(item['format_id'])
                    if item['ext'] == vext:
                        return [v]
                    continue

            v2 = self.getVStream(res, vext)
            if not vext and v:
                return [v]
            v = v2
        if vext:
            if v == 0:
                v = self.getVStream(res)
        if not bitrate:
            a = 0
        else:
            a = self.getAStream(bitrate, aext)
        if aext:
            if a == 0:
                a = self.getAStream(bitrate)
        return [
         v, a]

    def download(self, **kwargs):
        """
                Starts the video download in the specified format
                """
        o = self.getBestDL(kwargs['res'], kwargs['bitrate'], kwargs['vext'], kwargs['aext'])
        if len(o) == 1:
            if o[0] == 0:
                pstr = 'youtube-dl'
            else:
                pstr = 'youtube-dl -f ' + str(o[0])
        else:
            if o[0] == 0:
                o[0] = 'bestvideo'
            if o[1] == 0:
                o[1] = 'bestaudio'
            pstr = 'youtube-dl -f ' + str(o[0]) + '+' + str(o[1])
        if o[0] == 0:
            if o[1] == 0:
                pstr = 'youtube-dl'
        mconfigs = ''
        oext = kwargs['oext']
        if oext:
            mconfigs = ' ' + '--merge-output-format ' + oext
            mconfigs += ' --recode-video ' + oext
        if kwargs['more']:
            mconfigs += ' ' + kwargs['more']
        retcode = subprocess.call(pstr + ' ' + self.url + mconfigs)
        return retcode