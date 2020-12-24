# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/sutekh/base/gui/PkgIcon.py
# Compiled at: 2019-12-11 16:37:48
"""Provide a base class for handling the application icon"""
from pkg_resources import resource_stream
import gtk

class PkgIcon(object):
    """Load a gtk Pixbuf object from a package resource file."""

    def __init__(self, sPkg, sResource):
        oLoader = gtk.gdk.PixbufLoader()
        oFile = resource_stream(sPkg, sResource)
        oLoader.write(oFile.read())
        oFile.close()
        oLoader.close()
        self._oIcon = oLoader.get_pixbuf()

    def get_pixbuf(self):
        """Return the actual icon"""
        return self._oIcon