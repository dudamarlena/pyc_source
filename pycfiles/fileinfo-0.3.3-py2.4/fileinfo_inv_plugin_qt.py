# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.5-i386/egg/fileinfo/plugins/fileinfo_inv_plugin_qt.py
# Compiled at: 2008-06-17 03:18:50
"""A fileinfo plug-in for Quicktime files.

This is very bare bones and will run only on Mac OS X.
The Quicktime access via NSMovie seems to be very shaky.
"""
import sys, os.path, compiler, tokenize, cStringIO, keyword
try:
    from AppKit import NSMovie
    from Foundation import NSURL
    HAVE_PYOBJC = True
except ImportError:
    HAVE_PYOBJC = False

from fileinfo.investigator import BaseInvestigator

class QTInvestigator(BaseInvestigator):
    """A class for determining attributes of Quicktime files."""
    __module__ = __name__
    attrMap = {'duration': 'getDuration', 'ntracks': 'getNtracks', 'datasize': 'getDataSize', 'box': 'getBox'}
    totals = ('duration', 'ntracks', 'datasize')

    def activate(self):
        """Try activating self, setting 'active' variable."""
        if not HAVE_PYOBJC:
            self.active = False
            return self.active
        self.qtmov = None
        try:
            self.u = NSURL.URLWithString_('file://%s' % self.path)
            self.mov = NSMovie.alloc().initWithURL_byReference_(self.u, True)
            self.qtmov = self.mov.QTMovie()
            self.active = True
        except:
            self.active = False

        return self.active

    def getDuration(self):
        """Return movie duration (in frames)."""
        return self.qtmov.GetMovieDuration()

    def getNtracks(self):
        """Return number of movie tracks."""
        return self.qtmov.GetMovieTrackCount()

    def getDataSize(self):
        """Return movie data size."""
        return self.qtmov.GetMovieDataSize()

    def getBox(self):
        """Return movie box."""
        res = '%dx%d' % self.qtmov.GetMovieBox()[2:]
        return res