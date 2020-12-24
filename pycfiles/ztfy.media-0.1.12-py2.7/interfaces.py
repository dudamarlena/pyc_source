# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ztfy/media/interfaces.py
# Compiled at: 2016-12-26 08:50:19
from zope.interface import Interface, Attribute
from zope.schema import TextLine, Choice, List, Bool
from ztfy.media import _
CUSTOM_AUDIO_TYPES = ('application/ogg', )
CUSTOM_VIDEO_TYPES = ()

class IMediaInfo(Interface):
    """Media file info interface"""
    vtype = Attribute(_('Media type'))
    audio_codec_name = Attribute(_('Media audio codec name'))
    video_codec_name = Attribute(_('Media video codec name'))
    duration = Attribute(_('Media duration, in seconds'))
    bitrate = Attribute(_('Media audio bitrate'))
    frame_rate = Attribute(_('Media video frames rate'))
    frame_size = Attribute(_('Media frame size, if available'))
    frame_mode = Attribute(_('Media frame mode, if available'))
    infos = Attribute(_('Complete media infos dictionary'))


class IMediaConverter(Interface):
    """Media converter interface"""
    label = Attribute(_('Media converter label'))
    format = Attribute(_('Media converter target format'))

    def convert(self, media):
        """Convert media to format handled by given converter"""
        pass


class IMediaVideoConverter(IMediaConverter):
    """Media video converter"""
    pass


class IMediaAudioConverter(IMediaConverter):
    """Media audio converter"""
    pass


MEDIA_CONVERSIONS_KEY = 'ztfy.media.conversions'
MEDIA_CONVERSION_CMDLINE_KEY = 'ztfy.media.conversion.cmdline'

class IMediaConversionsInfo(Interface):
    """Media conversions info interface"""

    def hasConversion(self, formats):
        """Check if one of given formats if available in conversions"""
        pass

    def getConversion(self, format):
        """Get converted media for given format and width"""
        pass

    def getConversions(self):
        """Get current list of media conversions"""
        pass


class IMediaConversionsWriter(Interface):
    """Media conversions writer interface"""

    def addConversion(self, conversion, format, extension=None, width=None):
        """Add given conversion to media"""
        pass


class IMediaConversions(IMediaConversionsInfo, IMediaConversionsWriter):
    """Media file conversions storage interface"""
    pass


class IMediaConversionUtility(Interface):
    """Media conversion client interface"""
    converter_address = TextLine(title=_('Medias converter process address'), description=_("Address of media converter listener, in the 'IPv4:port' format.Keep empty to disable it."), required=False, default='127.0.0.1:5555')
    video_formats = List(title=_('Video formats conversions'), description=_('Published video files will be automatically converted to this format'), value_type=Choice(vocabulary='ZTFY media video converters'))
    force_video_conversion = Bool(title=_('Force video conversion?'), description=_('Convert video even when source file has same target content type'), required=True, default=False)
    audio_formats = List(title=_('Audio formats conversions'), description=_('Published audio files will be automatically converted to this format'), value_type=Choice(vocabulary='ZTFY media audio converters'))
    force_audio_conversion = Bool(title=_('Force audio conversion?'), description=_('Convert audio file even when source file has same target content type'), required=True, default=True)
    zeo_connection = Choice(title=_('ZEO connection name'), description=_('Name of ZEO connection utility defining converter connection'), required=True, vocabulary='ZEO connections')

    def checkMediaConversion(self, media):
        """Check if conversion is needed for given media"""
        pass

    def convert(self, media, format):
        """Convert given media to requested format"""
        pass