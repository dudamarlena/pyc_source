# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ukcensusapi/utils.py
# Compiled at: 2018-07-05 11:46:47
# Size of source mod 2**32: 779 bytes
"""
Common utility/helpers
"""
import os
from pathlib import Path

def _expand_home(path):
    """
  pathlib doesn't interpret ~/ as $HOME
  This doesnt deal with other user's homes e.g. ~another/dir is not changed
  """
    return Path(path.replace('~/', str(Path.home()) + '/'))


def init_cache_dir(directory):
    """
  Checks path exists and is a writable directory
  Create if it doesnt exist
  Throw PermissionError if not
  """
    directory = _expand_home(directory)
    if not os.path.exists(str(directory)):
        os.makedirs(str(directory))
    if not os.path.isdir(str(directory)):
        raise PermissionError(str(directory) + ' is not a directory')
    if not os.access(str(directory), os.W_OK):
        raise PermissionError(str(directory) + ' is not writable')
    return directory