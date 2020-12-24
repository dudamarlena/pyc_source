# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/inquant/contentmirror/base/utils.py
# Compiled at: 2008-04-14 11:51:38
__author__ = 'Stefan Eletzhofer <stefan.eletzhofer@inquant.de>'
__docformat__ = 'plaintext'
__revision__ = '$Revision: 62284 $'
__version__ = '$Revision: 62284 $'[11:-2]
import logging
from Acquisition import aq_base
info = logging.getLogger('contentmirror').info
debug = logging.getLogger('contentmirror').debug
error = logging.getLogger('contentmirror').error

def give_new_context(obj, context):
    obj = aq_base(obj)
    obj = obj.__of__(context)
    return obj