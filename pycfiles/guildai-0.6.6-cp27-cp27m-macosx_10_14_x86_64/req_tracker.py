# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: ./guild/external/pip/_internal/req/req_tracker.py
# Compiled at: 2019-09-10 15:18:29
from __future__ import absolute_import
import contextlib, errno, hashlib, logging, os
from pip._internal.utils.temp_dir import TempDirectory
logger = logging.getLogger(__name__)

class RequirementTracker(object):

    def __init__(self):
        self._root = os.environ.get('PIP_REQ_TRACKER')
        if self._root is None:
            self._temp_dir = TempDirectory(delete=False, kind='req-tracker')
            self._temp_dir.create()
            self._root = os.environ['PIP_REQ_TRACKER'] = self._temp_dir.path
            logger.debug('Created requirements tracker %r', self._root)
        else:
            self._temp_dir = None
            logger.debug('Re-using requirements tracker %r', self._root)
        self._entries = set()
        return

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.cleanup()

    def _entry_path(self, link):
        hashed = hashlib.sha224(link.url_without_fragment.encode()).hexdigest()
        return os.path.join(self._root, hashed)

    def add(self, req):
        link = req.link
        info = str(req)
        entry_path = self._entry_path(link)
        try:
            with open(entry_path) as (fp):
                raise LookupError('%s is already being built: %s' % (
                 link, fp.read()))
        except IOError as e:
            if e.errno != errno.ENOENT:
                raise
            assert req not in self._entries
            with open(entry_path, 'w') as (fp):
                fp.write(info)
            self._entries.add(req)
            logger.debug('Added %s to build tracker %r', req, self._root)

    def remove(self, req):
        link = req.link
        self._entries.remove(req)
        os.unlink(self._entry_path(link))
        logger.debug('Removed %s from build tracker %r', req, self._root)

    def cleanup(self):
        for req in set(self._entries):
            self.remove(req)

        remove = self._temp_dir is not None
        if remove:
            self._temp_dir.cleanup()
        logger.debug('%s build tracker %r', 'Removed' if remove else 'Cleaned', self._root)
        return

    @contextlib.contextmanager
    def track(self, req):
        self.add(req)
        yield
        self.remove(req)