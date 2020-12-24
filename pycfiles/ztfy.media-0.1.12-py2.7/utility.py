# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ztfy/media/utility.py
# Compiled at: 2016-12-26 09:57:06
import logging
logger = logging.getLogger('ztfy.media')
from multiprocessing.process import Process
from persistent import Persistent
from threading import Thread
import os
from transaction.interfaces import ITransactionManager
from zope.annotation.interfaces import IAnnotations
from zope.app.file.interfaces import IFile
from zope.component.interfaces import ISite
from zope.dublincore.interfaces import IZopeDublinCore
from ztfy.media.interfaces import IMediaConversionUtility, IMediaConversions, IMediaConverter, CUSTOM_AUDIO_TYPES, CUSTOM_VIDEO_TYPES, MEDIA_CONVERSION_CMDLINE_KEY
from ztfy.utils.interfaces import IZEOConnection
from zope.app.publication.zopepublication import ZopePublication
from zope.component import getUtility, queryUtility, hooks
from zope.container.contained import Contained
from zope.interface import implements
from zope.schema.fieldproperty import FieldProperty
from zope.traversing import api as traversing_api
from ztfy.utils.request import getRequest, newParticipation, endParticipation
from ztfy.utils.traversing import getParent
from ztfy.utils.zodb import ZEOConnectionInfo
from ztfy.zmq.handler import ZMQMessageHandler
from ztfy.zmq.process import ZMQProcess
from ztfy.zmq.socket import zmq_socket, zmq_response

class MediasConversionProcess(ZMQProcess):
    """Medias conversion process"""
    pass


class ConversionProcess(Process):
    """Conversion manager process"""

    def __init__(self, settings, group=None, target=None, name=None, *args, **kwargs):
        Process.__init__(self, group=group, target=target, name=name, args=args, kwargs=kwargs)
        self.settings = settings

    def run(self):
        os.nice(10)
        settings = self.settings
        zeo_settings = settings.get('zeo')
        media_path = settings.get('media')
        media_format = settings.get('format')
        if not (zeo_settings and media_path and media_format):
            logger.warning('Received bad conversion request: %s' % str(settings))
            return
        else:
            logger.info('Received media conversion request: %s => %s' % (media_path, media_format))
            converter = queryUtility(IMediaConverter, media_format)
            if converter is None:
                logger.warning('Missing media converter: %s' % media_format)
                return
            connection_info = ZEOConnectionInfo()
            connection_info.update(zeo_settings)
            newParticipation(settings.get('principal'))
            request = getRequest()
            manager = None
            logger.debug('Opening ZEO connection...')
            storage, db = connection_info.getConnection(get_storage=True)
            try:
                connection = db.open()
                root = connection.root()
                root_folder = root.get(ZopePublication.root_name, None)
                media = traversing_api.traverse(root_folder, media_path, default=None, request=request)
                if IFile.providedBy(media):
                    site = getParent(media, ISite)
                    hooks.setSite(site)
                    logger.debug('Starting conversion process for %s to %s' % (media_path, media_format))
                    conversion = converter.convert(media)
                    conversion_result = conversion.get('output', '')
                    if len(conversion_result) > 0:
                        manager = ITransactionManager(media)
                        for attempt in manager.attempts():
                            with attempt as (t):
                                converted = IMediaConversions(media).addConversion(conversion_result, media_format, '.%s' % converter.format)
                                IAnnotations(converted)[MEDIA_CONVERSION_CMDLINE_KEY] = conversion.get('cmdline')
                            if t.status == 'Committed':
                                break

                    else:
                        logger.warning("Finished FFmpeg conversion process to '%s' with **NO OUTPUT**!!!" % media_format)
                        logger.warning(conversion.get('errors'))
                else:
                    logger.warning("Can't find requested media: %s" % media_path)
            finally:
                endParticipation()
                if manager is not None:
                    manager.abort()
                connection.close()
                storage.close()

            return


class ConversionThread(Thread):

    def __init__(self, process):
        Thread.__init__(self)
        self.process = process

    def run(self):
        self.process.start()
        self.process.join()


class ConversionHandler(object):
    """Media conversion manager
    
    The conversion manager is launched by a ZMQ 'convert' JSON message, which
    should contain the following attributes:
     - zeo: dict of ZEO connection settings
     - principal: media creator's ID
     - media: complete path to the new media
     - format: requested conversion format
    """

    def convert(self, data):
        ConversionThread(ConversionProcess(data)).start()
        return [200, 'OK - Conversion process started']


class ConversionMessageHandler(ZMQMessageHandler):
    """Media conversion message handler"""
    handler = ConversionHandler


class MediaConversionUtility(Persistent, Contained):
    """Media conversion configuration utility"""
    implements(IMediaConversionUtility)
    converter_address = FieldProperty(IMediaConversionUtility['converter_address'])
    video_formats = FieldProperty(IMediaConversionUtility['video_formats'])
    force_video_conversion = FieldProperty(IMediaConversionUtility['force_video_conversion'])
    audio_formats = FieldProperty(IMediaConversionUtility['audio_formats'])
    force_audio_conversion = FieldProperty(IMediaConversionUtility['force_audio_conversion'])
    zeo_connection = FieldProperty(IMediaConversionUtility['zeo_connection'])

    def checkMediaConversion(self, media):
        """Request conversion of given media"""
        content_type = media.contentType
        if self.audio_formats and (content_type.startswith('audio/') or content_type in CUSTOM_AUDIO_TYPES):
            requested_formats = [ format for format in self.audio_formats if self.force_audio_conversion or format != content_type ]
        else:
            if self.video_formats and (content_type.startswith('video/') or content_type in CUSTOM_VIDEO_TYPES):
                requested_formats = [ format for format in self.video_formats if self.force_video_conversion or format != content_type ]
            else:
                requested_formats = ()
            for format in requested_formats:
                self.convert(media, format)

    def convert(self, media, format):
        """Send conversion request for given media"""
        if not self.zeo_connection:
            return
        socket = zmq_socket(self.converter_address)
        zeo = getUtility(IZEOConnection, self.zeo_connection)
        settings = {'zeo': zeo.getSettings(), 'principal': IZopeDublinCore(media).creators[0], 
           'media': traversing_api.getPath(media), 
           'format': format}
        socket.send_json(['convert', settings])
        return zmq_response(socket)