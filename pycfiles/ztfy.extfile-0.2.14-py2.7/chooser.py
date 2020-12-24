# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ztfy/extfile/namechooser/chooser.py
# Compiled at: 2012-06-20 11:22:54
__docformat__ = 'restructuredtext'
import pytz
from datetime import datetime
from mimetypes import guess_extension
from ztfy.extfile.namechooser.interfaces import IExtFileNameChooser
from zope.interface import implements

class TimestampNameChooser(object):
    """A timestamp based file name chooser"""
    implements(IExtFileNameChooser)

    def getName(self, parent, extfile, name):
        d = datetime.now(pytz.UTC)
        ext = guess_extension(extfile.contentType.split(';')[0])
        return d.strftime('/%Y/%m/%d-%H%M%S-%%d%%s') % (d.microsecond, ext)