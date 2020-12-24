# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/pyams_file/generations/evolve2.py
# Compiled at: 2019-12-20 07:23:03
# Size of source mod 2**32: 1737 bytes
"""PyAMS_file.generations.evolve2 module

This module is doing a database scan of all registered blobs to add a reference to them
into blobs manager.
"""
import logging
from zope.intid import IIntIds
from pyams_file.interfaces import IBlobReferenceManager, IFile
from pyams_utils.registry import get_local_registry, get_utility, set_local_registry
__docformat__ = 'restructuredtext'
LOGGER = logging.getLogger('PyAMS (file)')

def evolve(site):
    """Evolve 2: create reference for all files blobs"""
    registry = get_local_registry()
    try:
        files = set()
        set_local_registry(site.getSiteManager())
        LOGGER.warning('Creating references to all blobs...')
        intids = get_utility(IIntIds)
        references = get_utility(IBlobReferenceManager)
        for ref in list(intids.refs.keys()):
            obj = intids.queryObject(ref)
            if IFile.providedBy(obj):
                blob = getattr(obj, '_blob', None)
                if blob is not None:
                    references.add_reference(blob, obj)
                LOGGER.debug('>>> updated blob reference for file {!r}'.format(obj))

        LOGGER.warning('{} files updated'.format(len(files)))
    finally:
        set_local_registry(registry)