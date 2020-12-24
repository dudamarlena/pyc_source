# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-build-ed191__6/pip/pip/_internal/req/req_tracker.py
# Compiled at: 2020-01-10 16:25:21
# Size of source mod 2**32: 3195 bytes
from __future__ import absolute_import
import contextlib, errno, hashlib, logging, os
from pip._internal.utils.temp_dir import TempDirectory
from pip._internal.utils.typing import MYPY_CHECK_RUNNING
if MYPY_CHECK_RUNNING:
    from types import TracebackType
    from typing import Iterator, Optional, Set, Type
    from pip._internal.req.req_install import InstallRequirement
    from pip._internal.models.link import Link
logger = logging.getLogger(__name__)

class RequirementTracker(object):

    def __init__(self):
        self._root = os.environ.get('PIP_REQ_TRACKER')
        if self._root is None:
            self._temp_dir = TempDirectory(delete=False, kind='req-tracker')
            self._root = os.environ['PIP_REQ_TRACKER'] = self._temp_dir.path
            logger.debug('Created requirements tracker %r', self._root)
        else:
            self._temp_dir = None
            logger.debug('Re-using requirements tracker %r', self._root)
        self._entries = set()

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
            elif not req not in self._entries:
                raise AssertionError
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

    @contextlib.contextmanager
    def track(self, req):
        self.add(req)
        yield
        self.remove(req)