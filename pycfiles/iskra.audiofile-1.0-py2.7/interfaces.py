# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-intel/egg/iskra/audiofile/interfaces.py
# Compiled at: 2012-07-09 11:02:01
from zope.interface import Interface, Attribute
from zope import schema
from iskra.audiofile import _

class IMediaElementJSPlayable(Interface):
    """A file playable with mediaelementjs
    """
    audiofile = Attribute('Audio file')
    image = Attribute('Image file')


class IVideo(IMediaElementJSPlayable):
    """Marker interface for files that contain mp4 content
    """
    pass


class IMediaInfo(Interface):
    """Information about a video object
    """
    width = schema.Int(title=_('Width'), required=False)
    height = schema.Int(title=_('Height'), required=False)
    duration = schema.Timedelta(title=_('Duration'), required=False)