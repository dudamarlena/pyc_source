# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/ks/schema/smartbytes/smartbytes.py
# Compiled at: 2008-12-22 08:23:22
"""SmartBytes class for the Zope 3 based ks.schema.smartbytes package

$Id: smartbytes.py 23861 2007-11-25 00:13:00Z xen $
"""
__author__ = 'Anatoly Bubenkov'
__license__ = 'ZPL'
__version__ = '$Revision: 23861 $'
__date__ = '$Date: 2007-11-25 02:13:00 +0200 (Sun, 25 Nov 2007) $'
__credits__ = 'Based heavily on zope.app.form.browser.objectwidget.ObjectWidget'
from zope.schema import Bytes

class SmartBytes(Bytes):
    """Smart Bytes"""
    __module__ = __name__

    def set(self, object, value):
        if value is None or not value:
            return
        return super(SmartBytes, self).set(object, value)