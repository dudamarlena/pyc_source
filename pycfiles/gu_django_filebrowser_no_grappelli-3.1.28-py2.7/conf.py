# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.11-intel/egg/filebrowser/conf.py
# Compiled at: 2014-11-22 02:35:13
from filebrowser import settings

class FileBrowserSettings(object):
    """
    Proxy for file browser settings defined at module level

    This class allows for the addition of properties to
    compute the correct setting, and makes accessing settings
    explicit in modules that use it:

    >>> from filebrowser.conf import fb_settings
    >>> fb_settings.MEDIA_ROOT # etc..
    """

    def __getattr__(self, name):
        return getattr(settings, name)


fb_settings = FileBrowserSettings()