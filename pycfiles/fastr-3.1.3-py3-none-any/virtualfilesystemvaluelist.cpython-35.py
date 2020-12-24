# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/hachterberg/dev/fastr/fastr/fastr/resources/plugins/ioplugins/virtualfilesystemvaluelist.py
# Compiled at: 2018-10-11 06:24:57
# Size of source mod 2**32: 2534 bytes
"""
This module contains the VirtualFileSystemValueList plugin for fastr
"""
import urllib.parse, fastr
from fastr import exceptions, resources
from fastr.core.ioplugin import IOPlugin

class VirtualFileSystemValueList(IOPlugin):
    __doc__ = '\n    The VirtualFileSystemValueList an expand-only type of IOPlugin. No URLs\n    can actually be fetched, but it can expand a single URL into a larger\n    amount of URLs. A ``vfslist://`` URL basically is a url that points to a\n    file using vfs. This file then contains a number lines each containing\n    another URL.\n\n    If the contents of a file ``vfs://mount/some/path/contents`` would be::\n\n        vfs://mount/some/path/file1.txt\n        vfs://mount/some/path/file2.txt\n        vfs://mount/some/path/file3.txt\n        vfs://mount/some/path/file4.txt\n\n    Then using the URL ``vfslist://mount/some/path/contents`` as source data\n    would result in the four files being pulled.\n\n    .. note:: The URLs in a vfslist file do not have to use the ``vfs`` scheme,\n              but can use any scheme known to the Fastr system.\n    '
    scheme = 'vfslist'

    def __init__(self):
        super(VirtualFileSystemValueList, self).__init__()

    def expand_url(self, url):
        if fastr.data.url.get_url_scheme(url) != 'vfslist':
            raise exceptions.FastrValueError('URL not of vfslist type!')
        parsed = urllib.parse.urlparse(url)
        listurl = urllib.parse.urlunparse(urllib.parse.ParseResult(scheme='vfs', netloc=parsed.netloc, path=parsed.path, params='', query='', fragment=''))
        listpath = resources.ioplugins.url_to_path(listurl)
        with open(listpath, 'r') as (file_handle):
            data = file_handle.read()
        valuelist = tuple((None, x.strip()) for x in data.strip().split('\n'))
        return valuelist