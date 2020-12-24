# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/hachterberg/dev/fastr/fastr/fastr/resources/plugins/ioplugins/virtualfilesystemregularexpression.py
# Compiled at: 2019-06-04 03:32:43
# Size of source mod 2**32: 5262 bytes
"""
This module contains the VirtualFileSystemRegularExpression plugin for fastr
"""
import os, re, urllib.parse, fastr
from fastr import exceptions, resources
from fastr.core.ioplugin import IOPlugin

class VirtualFileSystemRegularExpression(IOPlugin):
    __doc__ = "\n    The VirtualFileSystemValueList an expand-only type of IOPlugin. No URLs\n    can actually be fetched, but it can expand a single URL into a larger\n    amount of URLs.\n\n    A ``vfsregex://`` URL is a vfs URL that can contain regular expressions\n    on every level of the path. The regular expressions follow the\n    :mod:`re module <re>` definitions.\n\n    An example of a valid URLs would be::\n\n        vfsregex://tmp/network_dir/.*/.*/__fastr_result__.pickle.gz\n        vfsregex://tmp/network_dir/nodeX/(?P<id>.*)/__fastr_result__.pickle.gz\n\n    The first URL would result in all the ``__fastr_result__.pickle.gz`` in\n    the working directory of a Network. The second URL would only result in\n    the file for a specific node (nodeX), but by adding the named group\n    ``id`` using ``(?P<id>.*)`` the sample id of the data is automatically\n    set to that group (see :ref:`python:re-syntax` under the special\n    characters for more info on named groups in regular expression).\n\n    Concretely if we would have a directory ``vfs://mount/somedir`` containing::\n\n        image_1/Image.nii\n        image_2/image.nii\n        image_3/anotherimage.nii\n        image_5/inconsistentnamingftw.nii\n\n    we could match these files using ``vfsregex://mount/somedir/(?P<id>image_\\d+)/.*\\.nii``\n    which would result in the following source data after expanding the URL::\n\n        {'image_1': 'vfs://mount/somedir/image_1/Image.nii',\n         'image_2': 'vfs://mount/somedir/image_2/image.nii',\n         'image_3': 'vfs://mount/somedir/image_3/anotherimage.nii',\n         'image_5': 'vfs://mount/somedir/image_5/inconsistentnamingftw.nii'}\n\n    Showing the power of this regular expression filtering. Also it shows how\n    the ID group from the URL can be used to have sensible sample ids.\n\n    .. warning:: due to the nature of regexp on multiple levels, this method\n                 can be slow when having many matches on the lower level of\n                 the path (because the tree of potential matches grows) or\n                 when directories that are parts of the path are very large.\n    "
    scheme = 'vfsregex'

    def __init__(self):
        super(VirtualFileSystemRegularExpression, self).__init__()

    def expand_url(self, url):
        if fastr.data.url.get_url_scheme(url) != 'vfsregex':
            raise exceptions.FastrValueError('URL not of vfsregex type!')
        else:
            parsed = urllib.parse.urlparse(url)
            baseurl = urllib.parse.urlunparse(urllib.parse.ParseResult(scheme='vfs', netloc=(parsed.netloc), path='', params='', query='', fragment=''))
            basepath = resources.ioplugins.url_to_path(baseurl)
            if parsed.query != '':
                path = parsed.path + '?' + parsed.query
            else:
                path = parsed.path
        subpaths = fastr.data.url.full_split(path)
        if subpaths[0] != '/':
            return ValueError('vfs url should always contain a valid path')
        pathlist = [(None, basepath)]
        fastr.log.debug('Basepath: {}, Subpaths {}'.format(basepath, subpaths))
        for subpath in subpaths[1:]:
            subpath = '^{}$'.format(subpath)
            try:
                re.compile(subpath)
            except Exception as detail:
                try:
                    raise exceptions.FastrValueError('Error parsing regexp "{}": {}'.format(subpath, detail))
                finally:
                    detail = None
                    del detail

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

        pathlist = tuple(((id_, re.sub(basepath, baseurl + '/', x)) for id_, x in sorted(pathlist)))
        return pathlist