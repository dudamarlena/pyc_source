# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: pyfeld/didlInfo.py
# Compiled at: 2017-11-23 08:41:51
from __future__ import unicode_literals
from xml.dom import minidom

class DidlInfo:

    @staticmethod
    def getTagNameValue(root_item, tag):
        return root_item.getElementsByTagName(tag)[0].childNodes[0].nodeValue

    def __init__(self, didl_data, fill_all=False):
        xml_Root = minidom.parseString(didl_data.encode(b'utf-8'))
        try:
            elem = xml_Root.getElementsByTagName(b'item')[0]
        except:
            try:
                elem = xml_Root.getElementsByTagName(b'container')[0]
            except Exception as e:
                print (b'parsing didl is odd {0}').format(e)
                return

        self.items = self.extract_from_node(elem, fill_all)

    @staticmethod
    def extract_from_node(elem, fill_all):
        item_list = {b'id': b'id', 
           b'raumfeld:name': b'raumfeldname', 
           b'raumfeld:sourceID': b'rfsourceID', 
           b'dc:title': b'title', 
           b'dc:description': b'description', 
           b'dc:creator': b'creator', 
           b'dc:date': b'date', 
           b'upnp:album': b'album', 
           b'upnp:artist': b'artist', 
           b'upnp:genre': b'genre', 
           b'upnp:originalTrackNumber': b'tracknumber', 
           b'upnp:albumArtURI': b'albumarturi', 
           b'upnp:class': b'class', 
           b'res': b'res'}
        items = dict()
        try:
            items[b'parentID'] = elem.attributes[b'parentID'].value
        except:
            items[b'parentID'] = b''

        try:
            items[b'refID'] = elem.attributes[b'refID'].value
        except:
            items[b'refID'] = None

        try:
            items[b'idPath'] = elem.attributes[b'id'].value
        except:
            items[b'idPath'] = b''

        if fill_all:
            items[b'resSampleFrequency'] = b''
            items[b'resBitrate'] = b''
            items[b'resSourceType'] = b''
            items[b'resSourceName'] = b''
            items[b'resSourceID'] = b''
        try:
            resElem = elem.getElementsByTagName(b'res')[0]
            items[b'resSampleFrequency'] = resElem.attributes[b'sampleFrequency'].value
            items[b'resBitrate'] = resElem.attributes[b'bitrate'].value
            items[b'resSourceType'] = resElem.attributes[b'sourceType'].value
            items[b'resSourceName'] = resElem.attributes[b'sourceName'].value
            items[b'resSourceID'] = resElem.attributes[b'sourceID'].value
        except Exception as e:
            pass

        for item_tag, key in item_list.items():
            try:
                res = DidlInfo.getTagNameValue(elem, item_tag)
                items[key] = res
            except Exception as e:
                if fill_all:
                    items[key] = b''

        return items

    def get_items(self):
        return self.items

    def print_items(self):
        print self.items


if __name__ == b'__main__':
    didl = b'&lt;DIDL-Lite xmlns=&quot;urn:schemas-upnp-org:metadata-1-0/DIDL-Lite/&quot; xmlns:raumfeld=&quot;urn:schemas-raumfeld-com:meta-data/raumfeld&quot; xmlns:upnp=&quot;urn:schemas-upnp-org:metadata-1-0/upnp/&quot; xmlns:dc=&quot;http://purl.org/dc/elements/1.1/&quot; xmlns:dlna=&quot;urn:schemas-dlna-org:metadata-1-0/&quot; lang=&quot;en&quot;&gt;&lt;item parentID=&quot;0/My Music/Artists/Al%20Di%20Meola/Al%20Di%20Meola+Elegant%20Gypsy&quot; id=&quot;0/My Music/Artists/Al%20Di%20Meola/Al%20Di%20Meola+Elegant%20Gypsy/74b3a119cec2e26e1d3bd0c9d4740e51&quot; restricted=&quot;1&quot;&gt;&lt;raumfeld:name&gt;Track&lt;/raumfeld:name&gt;&lt;upnp:class&gt;object.item.audioItem.musicTrack&lt;/upnp:class&gt;&lt;raumfeld:section&gt;My Music&lt;/raumfeld:section&gt;&lt;dc:title&gt;Flight Over Rio&lt;/dc:title&gt;&lt;upnp:album&gt;Elegant Gypsy&lt;/upnp:album&gt;&lt;upnp:artist&gt;Al Di Meola&lt;/upnp:artist&gt;&lt;upnp:genre&gt;Fusion&lt;/upnp:genre&gt;&lt;dc:creator&gt;Al Di Meola&lt;/dc:creator&gt;&lt;upnp:originalTrackNumber&gt;1&lt;/upnp:originalTrackNumber&gt;&lt;dc:date&gt;1977-01-01&lt;/dc:date&gt;&lt;upnp:albumArtURI dlna:profileID=&quot;JPEG_TN&quot;&gt;http://192.168.2.100:47366/?artist=Al%20Di%20Meola&amp;amp;albumArtist=Al%20Di%20Meola&amp;amp;album=Elegant%20Gypsy&amp;amp;track=Flight%20Over%20Rio&lt;/upnp:albumArtURI&gt;&lt;res protocolInfo=&quot;http-get:*:audio/mpeg:DLNA.ORG_PN=MP3&quot; size=&quot;13957120&quot; duration=&quot;0:07:16.000&quot; bitrate=&quot;256000&quot; sampleFrequency=&quot;44100&quot; nrAudioChannels=&quot;2&quot; sourceName=&quot;KINGSTON&quot; sourceType=&quot;usb&quot; sourceID=&quot;E2CC-190B&quot;&gt;http://192.168.2.100:53918/redirect?uri=file%3A%2F%2F%2Fmedia%2FE2CC-190B%2FAl%2520Di%2520Meola%2520-%2520%255BElegant%2520Gypsy%255D%2FAl%2520Di%2520Meola%2520-%2520%255BElegant%2520Gypsy%255D%2520-%2520%252801%2529%2520-%2520Flight%2520Over%2520Rio.mp3&lt;/res&gt;&lt;/item&gt;&lt;/DIDL-Lite&gt;'
    d = DidlInfo(didl)
    d.print_items()