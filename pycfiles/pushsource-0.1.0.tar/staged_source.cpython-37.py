# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/rmcgover/src/pushsource/src/pushsource/_impl/backend/staged/staged_source.py
# Compiled at: 2020-02-03 23:31:33
# Size of source mod 2**32: 12645 bytes
import os, threading, logging, itertools, functools
from concurrent import futures
try:
    from os import scandir, walk
except ImportError:
    from scandir import scandir, walk

import yaml, json
from pushcollector import Collector
from more_executors import Executors
from more_executors.futures import f_map
from ...source import Source
from .staged_utils import StagingMetadata, StagingLeafDir
from ...helpers import list_argument
from .staged_files import StagedFilesMixin
LOG = logging.getLogger('pushsource')
METADATA_FILES = ['staged.yaml', 'staged.yml', 'staged.json', 'pub-mapfile.json']
CACHE_LOCK = threading.RLock()

class StagedSource(Source, StagedFilesMixin):
    __doc__ = 'Uses a directory with a predefined layout (a "staging directory") as\n    the source of push items.'
    _FILE_TYPES = {}

    def __init__(self, url, threads=4, timeout=3600):
        """Create a new source.

        Parameters:
            url (list[str])
                URL(s) of locally accessible staging directories, e.g.
                ``"/mnt/staging/my-content-for-push"``.

                These directories must follow the documented layout for staging areas.

            threads (int)
                Number of threads used for concurrent loading of files.

            timeout (int)
                Number of seconds after which an error is raised, if no progress is
                made during each step.

        """
        super(StagedSource, self).__init__()
        self._url = list_argument(url)
        self._threads = threads
        self._timeout = timeout
        self._executor = Executors.thread_pool(max_workers=threads).with_timeout(timeout).with_retry()

    def __iter__(self):
        """Iterate over push items."""
        return (itertools.chain)(*[self._push_items_for_topdir(x) for x in self._url]).__iter__()

    def _load_metadata(self, topdir):
        for candidate in METADATA_FILES:
            metadata_file = os.path.join(topdir, candidate)
            if os.path.exists(metadata_file):
                break
        else:
            return StagingMetadata()

        basename = os.path.basename(metadata_file)
        with open(metadata_file, 'rt') as (f):
            content = f.read()
            Collector.get().attach_file(basename, content).result()
            if metadata_file.endswith('.json'):
                metadata = json.loads(content)
            else:
                metadata = yaml.safe_load(content)
        return StagingMetadata.from_data(metadata, os.path.basename(metadata_file))

    def _push_items_for_leafdir(self, leafdir, metadata):
        return self._FILE_TYPES[leafdir.file_type](leafdir=leafdir, metadata=metadata)

    def _push_items_for_topdir(self, topdir):
        LOG.debug('Checking files in: %s', topdir)
        destdirs = []
        for entry in scandir(topdir):
            if entry.is_dir() and entry.name != 'logs':
                destdirs.append(entry.path)

        if not destdirs:
            LOG.warning('%s has no destination directories', topdir)
            return []
        metadata = self._load_metadata(topdir)
        all_leaf_dirs = []
        for destdir in destdirs:
            for file_type in self._FILE_TYPES:
                path = os.path.join(destdir, file_type)
                LOG.debug('Scanning %s', path)
                if os.path.exists(path):
                    all_leaf_dirs.append(StagingLeafDir(dest=(os.path.basename(destdir)),
                      file_type=file_type,
                      path=path))

        process_dir = functools.partial((self._push_items_for_leafdir), metadata=metadata)
        pushitems_fs = [self._executor.submit(process_dir, leafdir) for leafdir in all_leaf_dirs]
        completed_fs = futures.as_completed(pushitems_fs, timeout=(self._timeout))
        for f in completed_fs:
            for pushitem in f.result():
                yield pushitem

        return []


Source.register_backend('staged', StagedSource)