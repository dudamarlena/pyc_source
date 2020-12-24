# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ztfy/media/adapter.py
# Compiled at: 2016-12-26 09:50:54
__docformat__ = 'restructuredtext'
import mimetypes
from BTrees.OOBTree import OOBTree
from persistent.dict import PersistentDict
from zope.app.file.interfaces import IFile
from zope.annotation.interfaces import IAnnotations
from zope.traversing.interfaces import TraversalError
from ztfy.media.interfaces import IMediaInfo, IMediaConversions, IMediaConversionUtility, CUSTOM_AUDIO_TYPES, CUSTOM_VIDEO_TYPES, MEDIA_CONVERSIONS_KEY
from zope.component import adapts, getUtility
from zope.event import notify
from zope.interface import implements
from zope.lifecycleevent import ObjectCreatedEvent
from zope.location import locate
from zope.traversing import namespace
from ztfy.extfile.blob import BlobFile
from ztfy.media.ffbase import FFmpeg
MEDIA_INFOS_KEY = 'ztfy.media.infos'

class MediaInfosAdapter(object):
    """Media infos adapter"""
    adapts(IFile)
    implements(IMediaInfo)

    def __new__(self, context):
        if not (context.contentType.startswith('audio/') or context.contentType.startswith('video/') or context.contentType in CUSTOM_AUDIO_TYPES + CUSTOM_VIDEO_TYPES):
            return None
        else:
            return object.__new__(self, context)

    def __init__(self, context):
        self.context = context
        annotations = IAnnotations(context)
        infos = annotations.get(MEDIA_INFOS_KEY)
        if infos is None:
            infos = FFmpeg().info(self.context)
            if infos:
                infos = annotations[MEDIA_INFOS_KEY] = PersistentDict(infos[0])
            else:
                infos = annotations[MEDIA_INFOS_KEY] = {}
        self.infos = infos
        return


class MediaConversionsAdapter(object):
    """Media conversions adapter"""
    adapts(IFile)
    implements(IMediaConversions)

    def __new__(self, context):
        if not (context.contentType.startswith('audio/') or context.contentType.startswith('video/') or context.contentType in CUSTOM_AUDIO_TYPES + CUSTOM_VIDEO_TYPES):
            return None
        else:
            return object.__new__(self, context)

    def __init__(self, context):
        self.context = context
        annotations = IAnnotations(context)
        conversions = annotations.get(MEDIA_CONVERSIONS_KEY)
        if conversions is None:
            conversions = annotations[MEDIA_CONVERSIONS_KEY] = OOBTree()
        self.conversions = conversions
        return

    def addConversion(self, data, format, extension=None, width=None):
        target = BlobFile()
        notify(ObjectCreatedEvent(target))
        target.data = data
        target.contentType = format
        if extension is None:
            extension = mimetypes.guess_extension(format)
        target_name = '%s%s' % ('w%d' % width if width else 'media', extension)
        self.conversions[target_name] = target
        target_name = '++conversion++%s' % target_name
        locate(target, self.context, target_name)
        return target

    def hasConversion(self, formats):
        if self.context.contentType in formats:
            return True
        for conversion in self.getConversions():
            if conversion.contentType in formats:
                return True

        return False

    def getConversions(self):
        converter = getUtility(IMediaConversionUtility)
        result = list(self.conversions.values())
        if self.context.contentType.startswith('video/') and not converter.force_video_conversion or self.context.contentType.startswith('audio/') and not converter.force_audio_conversion:
            result.append(self.context)
        return result

    def getConversion(self, name):
        if '/' in name:
            for conversion in self.getConversions():
                if conversion.contentType == name:
                    return conversion

        return self.conversions.get(name)


class MediaConversionPathTraverser(namespace.view):
    """Media ++conversion++ traverse adapter"""

    def traverse(self, name, ignored):
        conversions = IMediaConversions(self.context, None)
        if conversions is not None:
            result = conversions.getConversion(name)
            if result is not None:
                return result
        raise TraversalError('++conversion++%s' % name)
        return