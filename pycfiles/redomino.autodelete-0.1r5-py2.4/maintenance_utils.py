# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/redomino/autodelete/Extensions/maintenance_utils.py
# Compiled at: 2008-03-07 11:59:56
__author__ = 'Davide Moro <davide.moro@redomino.com>'
__docformat__ = 'plaintext'
import logging
from StringIO import StringIO
from zope.component import queryUtility
from redomino.autodelete.utils.interfaces import IAutoDelete
from redomino.autodelete.config import PROJECTNAME

def runAutodelete(self):
    """ Delete expired contents """
    out = StringIO()
    logger = logging.getLogger(PROJECTNAME)
    auto_delete = queryUtility(IAutoDelete)
    if auto_delete:
        for item in auto_delete.run_autodelete():
            print >> out, item

    else:
        msg = 'AutoDelete utility not found'
        logger.exception(msg)
        print >> out, msg
    return out.getvalue()