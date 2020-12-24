# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ztfy/media/events.py
# Compiled at: 2013-06-20 08:39:38
__docformat__ = 'restructuredtext'
import atexit, logging
logger = logging.getLogger('ztfy.media')
import mimetypes, time, transaction, zmq
from zope.app.file.interfaces import IFile
from zope.component.interfaces import IRegistered, IUnregistered, ISite
from zope.container.interfaces import IObjectAddedEvent
from zope.processlifetime import IDatabaseOpenedWithRoot
from zope.app.publication.zopepublication import ZopePublication
from zope.traversing import api as traversing_api
from ztfy.media.interfaces import IMediaConversionUtility, IMediaInfo, CUSTOM_AUDIO_TYPES, CUSTOM_VIDEO_TYPES
from zope.component import adapter, queryUtility
from zope.site import hooks
from ztfy.media.ffdocument import FFDocument
from ztfy.media.utility import ConversionMessageHandler, MediasConversionProcess
from ztfy.zmq.process import processExitFunc
_processes = {}

@adapter(IMediaConversionUtility, IRegistered)
def handleRegisteredMediaConversionUtility(utility, event):
    if utility.converter_address:
        path = traversing_api.getPath(utility)
        if _processes.get(path) is None:
            process = MediasConversionProcess(utility.converter_address, ConversionMessageHandler)
            process.start()
            time.sleep(2)
            if process.is_alive():
                _processes[path] = process
                atexit.register(processExitFunc, process=process)
            logger.info('Starting ZMQ listener process %s with PID %d for handler %s' % (
             process.name, process.pid, str(process.handler)))
    return


@adapter(IMediaConversionUtility, IUnregistered)
def handleUnregisteredMediaConversionUtility(utility, event):
    path = traversing_api.getPath(utility)
    process = _processes.get(path)
    if process is not None:
        process.terminate()
        process.join()
        logger.info('Stopped ZMQ process %s' % process.name)
        del _processes[path]
    return


@adapter(IDatabaseOpenedWithRoot)
def handleOpenedDatabase(event):
    """Launch ZMQ conversion process"""
    db = event.database
    connection = db.open()
    root = connection.root()
    root_folder = root.get(ZopePublication.root_name, None)
    for site in root_folder.values():
        if ISite(site, None) is not None:
            hooks.setSite(site)
            utility = queryUtility(IMediaConversionUtility)
            if utility is not None and utility.converter_address:
                try:
                    path = traversing_api.getPath(utility)
                    if _processes.get(path) is None:
                        process = MediasConversionProcess(utility.converter_address, ConversionMessageHandler)
                        process.start()
                        time.sleep(2)
                        if process.is_alive():
                            _processes[path] = process
                            atexit.register(processExitFunc, process=process)
                        logger.info('Starting ZMQ process %s listening on %s with PID %d for handler %s' % (
                         process.name, utility.converter_address,
                         process.pid, str(process.handler)))
                except zmq.ZMQError as e:
                    logger.warning("Can't start medias conversion process: " + e.message)

    return


def checkMediaConversions(status, object):
    if not status:
        return
    else:
        utility = queryUtility(IMediaConversionUtility)
        if utility is not None:
            utility.checkMediaConversion(object)
        return


@adapter(IFile, IObjectAddedEvent)
def handleNewFile(object, event):
    """Check for conversion of new files"""
    content_type = object.contentType
    if content_type.startswith('image/'):
        return
    else:
        media_type = content_type.startswith('audio/') or content_type.startswith('video/') or content_type in CUSTOM_AUDIO_TYPES + CUSTOM_VIDEO_TYPES
        if not media_type:
            document = FFDocument(object)
            metadata = document.__metadata__
            media_type = metadata.get('vtype')
            if media_type:
                ext = media_type.split(',')[0]
                content_type = mimetypes.guess_type('media.%s' % ext)[0]
                if content_type is not None:
                    object.contentType = content_type
        if media_type:
            _infos = IMediaInfo(object, None)
            transaction.get().addAfterCommitHook(checkMediaConversions, kws={'object': object})
        return