# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/icnews/core/browser/admin.py
# Compiled at: 2008-10-06 10:31:17
"""Main admin screen
"""
import os
from Products.Five.browser import BrowserView
from icnews.core import pkg_home

class Overview(BrowserView):
    """ icNews config overview
    """
    __module__ = __name__

    def getVersion(self):
        fh = open(os.path.join(pkg_home, 'version.txt'))
        version_string = fh.read()
        fh.close()
        return version_string