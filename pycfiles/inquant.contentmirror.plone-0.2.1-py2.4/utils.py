# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/inquant/contentmirror/plone/utils.py
# Compiled at: 2008-01-17 05:11:55
__author__ = 'Stefan Eletzhofer <stefan.eletzhofer@inquant.de>'
__docformat__ = 'plaintext'
__revision__ = '$Revision: 57036 $'
__version__ = '$Revision: 57036 $'[11:-2]
import logging
from marshal import loads
from urllib import unquote
from zlib import decompress
from Acquisition import aq_base
from ZODB.POSException import ConflictError
from OFS import Moniker
from zope.app.component.hooks import getSite
info = logging.getLogger().info

def _cb_decode(s):
    return loads(decompress(unquote(s)))


def get_copy_objects(cb_copy_data=None, REQUEST=None):
    """ return a list of objects from the clipboard """
    cp = None
    if cb_copy_data is not None:
        cp = cb_copy_data
    elif REQUEST is not None and REQUEST.has_key('__cp'):
        cp = REQUEST['__cp']
    if cp is None:
        raise AttributeError('no copy data')
    try:
        (op, mdatas) = _cb_decode(cp)
    except:
        raise AttributeError('invalid copy data')

    oblist = []
    app = getSite().getPhysicalRoot()
    for mdata in mdatas:
        m = Moniker.loadMoniker(mdata)
        try:
            ob = m.bind(app)
        except ConflictError:
            raise
        except:
            raise AttributeError('object not found')

        oblist.append(ob)

    return oblist


def give_new_context(obj, context):
    obj = aq_base(obj)
    obj = obj.__of__(context)
    return obj