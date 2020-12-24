# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-x86_64/egg/collective/flowplayercaptions/events.py
# Compiled at: 2011-01-02 19:02:46
from zope.interface import alsoProvides, noLongerProvides
from collective.flowplayercaptions.interfaces import ICaptionsSource

def toggleCaptions(object, event):
    """Mark the video as ICaptionsSource, or remove it; it depends on "captions" data"""
    data = object.getField('captions').get(object)
    if data:
        if not ICaptionsSource.providedBy(object):
            alsoProvides(object, ICaptionsSource)
            object.reindexObject(idxs=['object_provides'])
    elif ICaptionsSource.providedBy(object):
        noLongerProvides(object, ICaptionsSource)
        object.reindexObject(idxs=['object_provides'])