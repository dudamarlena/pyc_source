# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/rmcgover/src/pushsource/src/pushsource/_impl/backend/staged/staged_files.py
# Compiled at: 2020-02-03 23:57:46
# Size of source mod 2**32: 1598 bytes
import logging, os
try:
    from os import scandir, walk
except ImportError:
    from scandir import scandir, walk

from ...model import FilePushItem
LOG = logging.getLogger('pushsource')

class StagedFilesMixin(object):
    _FILE_TYPES = {}

    def __init__(self, *args, **kwargs):
        (super(StagedFilesMixin, self).__init__)(*args, **kwargs)
        self._FILE_TYPES = self._FILE_TYPES.copy()
        self._FILE_TYPES['ISOS'] = self._StagedFilesMixin__file_push_items
        self._FILE_TYPES['FILES'] = self._FILE_TYPES['ISOS']

    def __file_push_items(self, leafdir, metadata):
        out = []
        LOG.debug('Looking for files in %s', leafdir)
        for entry in scandir(leafdir.path):
            if entry.is_file():
                out.append(self._StagedFilesMixin__make_push_item(leafdir, metadata, entry))

        return out

    def __make_push_item(self, leafdir, metadata, entry):
        relative_path = os.path.join(leafdir.dest, leafdir.file_type, entry.name)
        file_md = metadata.file_metadata.get(relative_path)
        if not file_md:
            msg = "%s doesn't contain data for %s" % (metadata.filename, relative_path)
            LOG.error(msg)
            raise ValueError(msg)
        return FilePushItem(name=(file_md.filename or entry.name),
          src=(entry.path),
          description=(file_md.attributes.get('description')),
          sha256sum=(file_md.sha256sum),
          origin='staged',
          dest=[
         leafdir.dest])