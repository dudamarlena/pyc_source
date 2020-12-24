# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /net/orion/data/home/tack/projects/kaa/metadata/build/lib.linux-x86_64-2.6/kaa/metadata/audio/webradio.py
# Compiled at: 2007-05-07 17:47:54
__all__ = [
 'Parser']
import urlparse, string, urllib, core
ICY = {'icy-name': 'title', 'icy-genre': 'genre', 
   'icy-br': 'bitrate', 
   'icy-url': 'caption'}

class WebRadio(core.Music):
    table_mapping = {'ICY': ICY}

    def __init__(self, url):
        core.Music.__init__(self)
        tup = urlparse.urlsplit(url)
        scheme, location, path, query, fragment = tup
        if scheme != 'http':
            raise core.ParseError()
        fi = urllib.urlopen(url)
        self.statusline = fi.readline()
        try:
            statuslist = string.split(self.statusline)
        except ValueError:
            statuslist = [
             'ICY', '200']

        if statuslist[1] != '200':
            if fi:
                fi.close()
            raise core.ParseError()
        self.type = 'audio'
        self.subtype = 'mp3'
        linecnt = 0
        tab = {}
        lines = fi.readlines(512)
        for linecnt in range(0, 11):
            icyline = lines[linecnt]
            icyline = icyline.rstrip('\r\n')
            if len(icyline) < 4:
                break
            cidx = icyline.find(':')
            if cidx != -1:
                tab[icyline[:cidx].strip()] = icyline[cidx + 2:].strip()

        if fi:
            fi.close()
        self._appendtable('ICY', tab)

    def _finalize(self):
        core.Music._finalize(self)
        self.bitrate = string.atoi(self.bitrate) * 1000


Parser = WebRadio