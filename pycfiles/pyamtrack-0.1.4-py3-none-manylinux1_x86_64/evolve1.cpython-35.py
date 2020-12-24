# uncompyle6 version 3.6.7
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/pyams_file/generations/evolve1.py
# Compiled at: 2019-12-20 07:23:03
# Size of source mod 2**32: 2082 bytes
__doc__ = 'PyAMS_file.generations.evolve1 module\n\nThis generation module is looking for existing thumbnails and remove them from the database\nto avois a bug in previous release which was leading to blob files never being correctly deleted\non database packing.\n'
import logging
from zope.intid import IIntIds
from pyams_file.interfaces import IMediaFile
from pyams_file.interfaces.thumbnail import IThumbnails
from pyams_utils.registry import get_local_registry, get_utility, set_local_registry
__docformat__ = 'restructuredtext'
LOGGER = logging.getLogger('PyAMS (file)')

def evolve(site):
    """Evolve 1: remove all images thumbnails to free blobs"""
    registry = get_local_registry()
    try:
        medias = set()
        set_local_registry(site.getSiteManager())
        LOGGER.warning('Removing all thumbnails from database to free unused blobs...')
        intids = get_utility(IIntIds)
        for ref in list(intids.refs.keys()):
            obj = intids.queryObject(ref)
            if IMediaFile.providedBy(obj):
                LOGGER.debug('>>> removing thumbnails for image {!r}'.format(obj))
                thumbnails = IThumbnails(obj, None)
                if thumbnails is not None:
                    medias.add(obj)
                    thumbnails.clear_thumbnails()

        LOGGER.warning('Thumbnails cleanup is finished. Launch *zeopack* (for ZEO storage) or *zodbpack* (for Relstorage) command to remove all unused blobs.')
        LOGGER.warning('{} images updated'.format(len(medias)))
    finally:
        set_local_registry(registry)