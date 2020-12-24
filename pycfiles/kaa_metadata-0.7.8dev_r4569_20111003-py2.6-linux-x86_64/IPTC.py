# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/kaa/metadata/image/IPTC.py
# Compiled at: 2008-10-19 10:01:09
from struct import unpack
import kaa
mapping = {'by-line title': 'title', 
   'headline': 'title', 
   'keywords': 'keywords', 
   'writer-editor': 'author', 
   'credit': 'author', 
   'by-line': 'author', 
   'country/primary location name': 'country', 
   'caption-abstract': 'description', 
   'city': 'city', 
   'sub-location': 'location'}
c_datasets = {5: 'object name', 
   7: 'edit status', 
   8: 'editorial update', 
   10: 'urgency', 
   12: 'subject reference', 
   15: 'category', 
   20: 'supplemental category', 
   22: 'fixture identifier', 
   25: 'keywords', 
   26: 'content location code', 
   27: 'content location name', 
   30: 'release date', 
   35: 'release time', 
   37: 'expiration date', 
   38: 'expiration time', 
   40: 'special instructions', 
   42: 'action advised', 
   45: 'reference service', 
   47: 'reference date', 
   50: 'reference number', 
   55: 'date created', 
   60: 'time created', 
   62: 'digital creation date', 
   63: 'digital creation time', 
   65: 'originating program', 
   70: 'program version', 
   75: 'object cycle', 
   80: 'by-line', 
   85: 'by-line title', 
   90: 'city', 
   92: 'sub-location', 
   95: 'province/state', 
   100: 'country/primary location code', 
   101: 'country/primary location name', 
   103: 'original transmission reference', 
   105: 'headline', 
   110: 'credit', 
   115: 'source', 
   116: 'copyright notice', 
   118: 'contact', 
   120: 'caption-abstract', 
   122: 'writer-editor', 
   130: 'image type', 
   131: 'image orientation', 
   135: 'language identifier', 
   200: 'custom1', 
   201: 'custom2', 
   202: 'custom3', 
   203: 'custom4', 
   204: 'custom5', 
   205: 'custom6', 
   206: 'custom7', 
   207: 'custom8', 
   208: 'custom9', 
   209: 'custom10', 
   210: 'custom11', 
   211: 'custom12', 
   212: 'custom13', 
   213: 'custom14', 
   214: 'custom15', 
   215: 'custom16', 
   216: 'custom17', 
   217: 'custom18', 
   218: 'custom19', 
   219: 'custom20'}

def flatten(list):
    try:
        for (i, val) in list.items()[:]:
            if len(val) == 0:
                del list[i]
            elif i == 'keywords':
                list[i] = [ x.strip(' \t\x00\n\r') for x in val ]
            else:
                list[i] = (' ').join(val).strip()

        return list
    except (ValueError, AttributeError, IndexError, KeyError):
        return []


def parseiptc(app):
    iptc = {}
    if app[:14] == 'Photoshop 3.0\x00':
        app = app[14:]
    offset = 0
    data = None
    while app[offset:offset + 4] == '8BIM':
        offset = offset + 4
        code = unpack('<H', app[offset:offset + 2])[0]
        offset = offset + 2
        name_len = ord(app[offset])
        name = app[offset + 1:offset + 1 + name_len]
        offset = 1 + offset + name_len
        if offset & 1:
            offset = offset + 1
        size = unpack('<L', app[offset:offset + 4])[0]
        offset = offset + 4
        if code == 1028:
            data = app[offset:offset + size]
            break
        offset = offset + size
        if offset & 1:
            offset = offset + 1

    if not data:
        return
    else:
        offset = 0
        iptc = {}
        while 1:
            try:
                intro = ord(data[offset])
            except (ValueError, KeyError, IndexError):
                return flatten(iptc)
            else:
                if intro != 28:
                    return flatten(iptc)
                (tag, record, dataset, length) = unpack('!BBBH', data[offset:offset + 5])
                val = kaa.str_to_unicode(data[offset + 5:offset + length + 5])
                offset += length + 5
                name = c_datasets.get(dataset)
                if not name:
                    continue
                if iptc.has_key(name):
                    iptc[name].append(val)
                else:
                    iptc[name] = [
                     val]

        return flatten(iptc)