# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/collective/gacontext/utilities.py
# Compiled at: 2008-05-20 05:21:26
__author__ = 'Stefan Eletzhofer <stefan.eletzhofer@inquant.de>'
__docformat__ = 'plaintext'
__revision__ = '$Revision: 60982 $'
__version__ = '$Revision: 60982 $'[11:-2]
from Acquisition import aq_inner, aq_parent
from collective.gacontext.interfaces import *

def _chain(object):
    """Generator to walk the acquistion chain of object, considering that it
    could be a function.
    """
    context = aq_inner(object)
    while context is not None:
        yield context
        func_object = getattr(context, 'im_self', None)
        if func_object is not None:
            context = aq_inner(func_object)
        else:
            context = aq_parent(context)

    return


def gafinder(context):
    """ find the ga snippet responsible for the context
    """
    for obj in _chain(context):
        if IGAContextMarker.providedBy(obj):
            return IGACode(obj).ga_code

    return