# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-uunam8sj/pip/pip/_internal/utils/pkg_resources.py
# Compiled at: 2020-03-25 22:23:37
# Size of source mod 2**32: 1254 bytes
from pip._vendor.pkg_resources import yield_lines
from pip._vendor.six import ensure_str
from pip._internal.utils.typing import MYPY_CHECK_RUNNING
if MYPY_CHECK_RUNNING:
    from typing import Dict, Iterable, List

class DictMetadata(object):
    __doc__ = 'IMetadataProvider that reads metadata files from a dictionary.\n    '

    def __init__(self, metadata):
        self._metadata = metadata

    def has_metadata(self, name):
        return name in self._metadata

    def get_metadata(self, name):
        try:
            return ensure_str(self._metadata[name])
        except UnicodeDecodeError as e:
            e.reason += ' in {} file'.format(name)
            raise

    def get_metadata_lines(self, name):
        return yield_lines(self.get_metadata(name))

    def metadata_isdir(self, name):
        return False

    def metadata_listdir(self, name):
        return []

    def run_script(self, script_name, namespace):
        pass