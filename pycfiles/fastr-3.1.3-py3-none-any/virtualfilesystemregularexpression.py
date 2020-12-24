# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/hachterberg/dev/fastr/fastr/fastr/resources/plugins/ioplugins/virtualfilesystemregularexpression.py
# Compiled at: 2019-06-04 03:03:06
"""
This module contains the VirtualFileSystemRegularExpression plugin for fastr
"""
import os, re, urlparse, fastr, fastr.exceptions as exceptions
from fastr.core.ioplugin import IOPlugin

class VirtualFileSystemRegularExpression(IOPlugin):
    r"""
    The VirtualFileSystemValueList an expand-only type of IOPlugin. No URLs
    can actually be fetched, but it can expand a single URL into a larger
    amount of URLs.

    A ``vfsregex://`` URL is a vfs URL that can contain regular expressions
    on every level of the path. The regular expressions follow the
    :mod:`re module <re>` definitions.

    An example of a valid URLs would be::

        vfsregex://tmp/network_dir/.*/.*/__fastr_result__.pickle.gz
        vfsregex://tmp/network_dir/nodeX/(?P<id>.*)/__fastr_result__.pickle.gz

    The first URL would result in all the ``__fastr_result__.pickle.gz`` in
    the working directory of a Network. The second URL would only result in
    the file for a specific node (nodeX), but by adding the named group
    ``id`` using ``(?P<id>.*)`` the sample id of the data is automatically
    set to that group (see :ref:`python:re-syntax` under the special
    characters for more info on named groups in regular expression).

    Concretely if we would have a directory ``vfs://mount/somedir`` containing::

        image_1/Image.nii
        image_2/image.nii
        image_3/anotherimage.nii
        image_5/inconsistentnamingftw.nii

    we could match these files using ``vfsregex://mount/somedir/(?P<id>image_\d+)/.*\.nii``
    which would result in the following source data after expanding the URL::

        {'image_1': 'vfs://mount/somedir/image_1/Image.nii',
         'image_2': 'vfs://mount/somedir/image_2/image.nii',
         'image_3': 'vfs://mount/somedir/image_3/anotherimage.nii',
         'image_5': 'vfs://mount/somedir/image_5/inconsistentnamingftw.nii'}

    Showing the power of this regular expression filtering. Also it shows how
    the ID group from the URL can be used to have sensible sample ids.

    .. warning:: due to the nature of regexp on multiple levels, this method
                 can be slow when having many matches on the lower level of
                 the path (because the tree of potential matches grows) or
                 when directories that are parts of the path are very large.
    """
    scheme = 'vfsregex'

    def __init__(self):
        super(VirtualFileSystemRegularExpression, self).__init__()

    def expand_url(self, url):
        if fastr.data.url.get_url_scheme(url) != 'vfsregex':
            raise exceptions.FastrValueError('URL not of vfsregex type!')
        parsed = urlparse.urlparse(url)
        baseurl = urlparse.urlunparse(urlparse.ParseResult(scheme='vfs', netloc=parsed.netloc, path='', params='', query='', fragment=''))
        basepath = fastr.ioplugins.url_to_path(baseurl)
        if parsed.query != '':
            path = parsed.path + '?' + parsed.query
        else:
            path = parsed.path
        subpaths = fastr.data.url.full_split(path)
        if subpaths[0] != '/':
            return ValueError('vfs url should always contain a valid path')
        else:
            pathlist = [
             (
              None, basepath)]
            fastr.log.debug(('Basepath: {}, Subpaths {}').format(basepath, subpaths))
            for subpath in subpaths[1:]:
                subpath = ('^{}$').format(subpath)
                try:
                    re.compile(subpath)
                except Exception as detail:
                    raise exceptions.FastrValueError(('Error parsing regexp "{}": {}').format(subpath, detail))

                newpathlist = []
                for id_, curpath in pathlist:
                    contents = os.listdir(curpath)
                    for option in contents:
                        match = re.match(subpath, option)
                        if match is not None:
                            try:
                                id_ = match.group('id')
                            except IndexError:
                                pass

                            newpathlist.append((id_, os.path.join(curpath, option)))

                pathlist = newpathlist

            pathlist = tuple((id_, re.sub(basepath, baseurl + '/', x)) for id_, x in sorted(pathlist))
            return pathlist