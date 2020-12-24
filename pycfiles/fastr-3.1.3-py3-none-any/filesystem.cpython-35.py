# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3351)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/hachterberg/dev/fastr/fastr/fastr/resources/plugins/ioplugins/filesystem.py
# Compiled at: 2018-08-22 11:13:49
# Size of source mod 2**32: 5089 bytes
"""
This module contains the FileSystem plugin for fastr
"""
import os, shutil, urllib.parse, fastr
from fastr import exceptions
from fastr.core.ioplugin import IOPlugin

class FileSystem(IOPlugin):
    __doc__ = '\n    The FileSystem plugin is create to handle ``file://`` type or URLs. This is\n    generally not a good practice, as this is not portable over between\n    machines. However, for test purposes it might be useful.\n\n    The URL scheme is rather simple: ``file://host/path``\n    (see `wikipedia <http://en.wikipedia.org/wiki/File_URI_scheme>`_ for details)\n\n    We do not make use of the ``host`` part and at the moment only support\n    localhost (just leave the host empty) leading to ``file:///`` URLs.\n\n    .. warning:: This plugin ignores the hostname in the URL and does only\n                 accept driver letters on Windows in the form ``c:/``\n    '
    scheme = 'file'

    def __init__(self):
        super(FileSystem, self).__init__()

    def url_to_path(self, url):
        r""" Get the path to a file from a url.
        Currently supports the file:// scheme

        Examples:

        .. code-block:: python

          >>> 'file:///d:/data/project/file.ext'
          'd:\data\project\file.ext'

        .. warning::

          file:// will not function cross platform and is mainly for testing

        """
        parsed_url = up.urlparse(str(url))
        if parsed_url.scheme == self.scheme:
            if os.name == 'nt':
                path = parsed_url.path.lstrip('/')
            else:
                path = parsed_url.path
            return self._correct_separators(path)
        raise exceptions.FastrValueError('This parses the {} scheme and not the {} scheme!'.format(self.scheme, parsed_url.scheme))

    def path_to_url(self, path, mountpoint=None):
        """ Construct an url from a given mount point and a relative path to the mount point. """
        return '{scheme}:///{path}'.format(scheme=self.scheme, path=path)

    def fetch_url(self, inurl, outpath):
        """
        Fetch the files from the file.

        :param inurl: url to the item in the data store, starts with ``file://``
        :param outpath: path where to store the fetch data locally
        """
        inpath = self.url_to_path(inurl)
        if os.path.exists(outpath):
            fastr.log.info('Removing currently exists data at {}'.format(outpath))
            if os.path.islink(outpath):
                os.remove(outpath)
        else:
            if os.path.isdir(outpath):
                shutil.rmtree(outpath)
            else:
                os.remove(outpath)
        try:
            os.symlink(inpath, outpath)
            fastr.log.debug('Symlink successful')
        except OSError:
            fastr.log.debug('Cannot symlink, fallback to copy')
            if os.path.isdir(inpath):
                shutil.copytree(inpath, outpath)
            else:
                shutil.copy2(inpath, outpath)

        return outpath

    def fetch_value(self, inurl):
        """
        Fetch a value from an external file file.

        :param inurl: url of the value to read
        :return: the fetched value
        """
        path = self.url_to_path(inurl)
        with open(path, 'r') as (file_handle):
            data = file_handle.read()
        return data

    def put_url(self, inpath, outurl):
        """
        Put the files to the external data store.

        :param inpath: path of the local data
        :param outurl: url to where to store the data, starts with ``file://``
        """
        outpath = self.url_to_path(outurl)
        fastr.vfs.copy_file_dir(inpath, outpath)
        return os.path.exists(outpath)

    def put_value(self, value, outurl):
        """
        Put the value in the external data store.

        :param value: value to store
        :param outurl: url to where to store the data, starts with ``file://``
        """
        outpath = self.url_to_path(outurl)
        with open(outpath, 'w') as (file_handle):
            file_handle.write(str(value))
        return os.path.exists(outpath)