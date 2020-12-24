# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-hbx1i2h0/pip/pip/_internal/req/req_tracker.py
# Compiled at: 2020-04-16 14:32:34
# Size of source mod 2**32: 4723 bytes
from __future__ import absolute_import
import contextlib, errno, hashlib, logging, os
from pip._vendor import contextlib2
from pip._internal.utils.temp_dir import TempDirectory
from pip._internal.utils.typing import MYPY_CHECK_RUNNING
if MYPY_CHECK_RUNNING:
    from types import TracebackType
    from typing import Dict, Iterator, Optional, Set, Type, Union
    from pip._internal.req.req_install import InstallRequirement
    from pip._internal.models.link import Link
logger = logging.getLogger(__name__)

@contextlib.contextmanager
def update_env_context_manager(**changes):
    target = os.environ
    non_existent_marker = object()
    saved_values = {}
    for name, new_value in changes.items():
        try:
            saved_values[name] = target[name]
        except KeyError:
            saved_values[name] = non_existent_marker

        target[name] = new_value

    try:
        yield
    finally:
        for name, original_value in saved_values.items():
            if original_value is non_existent_marker:
                del target[name]
            else:
                assert isinstance(original_value, str)
                target[name] = original_value


@contextlib.contextmanager
def get_requirement_tracker():
    root = os.environ.get('PIP_REQ_TRACKER')
    with contextlib2.ExitStack() as (ctx):
        if root is None:
            root = ctx.enter_context(TempDirectory(kind='req-tracker')).path
            ctx.enter_context(update_env_context_manager(PIP_REQ_TRACKER=root))
            logger.debug('Initialized build tracking at %s', root)
        with RequirementTracker(root) as (tracker):
            yield tracker


class RequirementTracker(object):

    def __init__(self, root):
        self._root = root
        self._entries = set()
        logger.debug('Created build tracker: %s', self._root)

    def __enter__(self):
        logger.debug('Entered build tracker: %s', self._root)
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.cleanup()

    def _entry_path(self, link):
        hashed = hashlib.sha224(link.url_without_fragment.encode()).hexdigest()
        return os.path.join(self._root, hashed)

    def add(self, req):
        """Add an InstallRequirement to build tracking.
        """
        entry_path = self._entry_path(req.link)
        try:
            with open(entry_path) as (fp):
                contents = fp.read()
        except IOError as e:
            try:
                if e.errno != errno.ENOENT:
                    raise
            finally:
                e = None
                del e

        else:
            message = '%s is already being built: %s' % (req.link, contents)
            raise LookupError(message)
        assert req not in self._entries
        with open(entry_path, 'w') as (fp):
            fp.write(str(req))
        self._entries.add(req)
        logger.debug('Added %s to build tracker %r', req, self._root)

    def remove(self, req):
        """Remove an InstallRequirement from build tracking.
        """
        os.unlink(self._entry_path(req.link))
        self._entries.remove(req)
        logger.debug('Removed %s from build tracker %r', req, self._root)

    def cleanup(self):
        for req in set(self._entries):
            self.remove(req)

        logger.debug('Removed build tracker: %r', self._root)

    @contextlib.contextmanager
    def track(self, req):
        self.add(req)
        yield
        self.remove(req)