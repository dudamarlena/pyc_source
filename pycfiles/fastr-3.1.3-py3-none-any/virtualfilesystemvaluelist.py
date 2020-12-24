# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/hachterberg/dev/fastr/fastr/fastr/resources/plugins/ioplugins/virtualfilesystemvaluelist.py
# Compiled at: 2019-06-04 03:03:06
"""
This module contains the VirtualFileSystemValueList plugin for fastr
"""
import urlparse, fastr, fastr.exceptions as exceptions
from fastr.core.ioplugin import IOPlugin

class VirtualFileSystemValueList(IOPlugin):
    """
    The VirtualFileSystemValueList an expand-only type of IOPlugin. No URLs
    can actually be fetched, but it can expand a single URL into a larger
    amount of URLs. A ``vfslist://`` URL basically is a url that points to a
    file using vfs. This file then contains a number lines each containing
    another URL.

    If the contents of a file ``vfs://mount/some/path/contents`` would be::

        vfs://mount/some/path/file1.txt
        vfs://mount/some/path/file2.txt
        vfs://mount/some/path/file3.txt
        vfs://mount/some/path/file4.txt

    Then using the URL ``vfslist://mount/some/path/contents`` as source data
    would result in the four files being pulled.

    .. note:: The URLs in a vfslist file do not have to use the ``vfs`` scheme,
              but can use any scheme known to the Fastr system.
    """
    scheme = 'vfslist'

    def __init__(self):
        super(VirtualFileSystemValueList, self).__init__()

    def expand_url(self, url):
        if fastr.data.url.get_url_scheme(url) != 'vfslist':
            raise exceptions.FastrValueError('URL not of vfslist type!')
        parsed = urlparse.urlparse(url)
        listurl = urlparse.urlunparse(urlparse.ParseResult(scheme='vfs', netloc=parsed.netloc, path=parsed.path, params='', query='', fragment=''))
        listpath = fastr.ioplugins.url_to_path(listurl)
        with open(listpath, 'r') as (file_handle):
            data = file_handle.read()
        valuelist = tuple((None, x.strip()) for x in data.strip().split('\n'))
        return valuelist