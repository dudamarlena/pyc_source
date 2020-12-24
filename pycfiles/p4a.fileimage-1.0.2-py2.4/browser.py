# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/p4a/fileimage/browser.py
# Compiled at: 2007-11-30 08:40:44
import os
from p4a.fileimage import utils

class DownloadFile(object):
    """A view for downloading file content.
    """
    __module__ = __name__

    def __init__(self, context, request):
        self.context = context
        self.request = request

    def __call__(self):
        (ifpackagename, ifname, fieldname) = self.request.form.get('field', ':').split(':')
        ifpackage = __import__(ifpackagename, {}, {}, ifpackagename)
        iface = getattr(ifpackage, ifname)
        adapted = iface(self.context)
        value = getattr(adapted, fieldname)
        return value.index_html(self.request, self.request.response)


class ViewImage(DownloadFile):
    """A view for streaming image content.
    """
    __module__ = __name__