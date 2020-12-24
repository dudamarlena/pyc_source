# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.8-intel/egg/atomac/ldtpd/generic.py
# Compiled at: 2012-10-05 17:37:25
"""Generic class."""
import os, tempfile
from base64 import b64encode
from AppKit import *
from Quartz.CoreGraphics import *
from utils import Utils
from server_exception import LdtpServerException

class Generic(Utils):

    def imagecapture(self, window_name=None, x=0, y=0, width=None, height=None):
        """
        Captures screenshot of the whole desktop or given window
        
        @param window_name: Window name to look for, either full name,
        LDTP's name convention, or a Unix glob.
        @type window_name: string
        @param x: x co-ordinate value
        @type x: int
        @param y: y co-ordinate value
        @type y: int
        @param width: width co-ordinate value
        @type width: int
        @param height: height co-ordinate value
        @type height: int

        @return: screenshot with base64 encoded for the client
        @rtype: string
        """
        if x or y or width and width != -1 or height and height != -1:
            raise LdtpServerException('Not implemented')
        if window_name:
            handle, name, app = self._get_window_handle(window_name)
            try:
                self._grabfocus(handle)
            except:
                pass

            rect = self._getobjectsize(handle)
            screenshot = CGWindowListCreateImage(NSMakeRect(rect[0], rect[1], rect[2], rect[3]), 1, 0, 0)
        else:
            screenshot = CGWindowListCreateImage(CGRectInfinite, 1, 0, 0)
        image = CIImage.imageWithCGImage_(screenshot)
        bitmapRep = NSBitmapImageRep.alloc().initWithCIImage_(image)
        blob = bitmapRep.representationUsingType_properties_(NSPNGFileType, None)
        tmpFile = tempfile.mktemp('.png', 'ldtpd_')
        blob.writeToFile_atomically_(tmpFile, False)
        rv = b64encode(open(tmpFile).read())
        os.remove(tmpFile)
        return rv