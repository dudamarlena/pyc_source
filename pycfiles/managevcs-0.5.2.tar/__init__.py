# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/dzhiltsov/Development/vcslib/managevcs/__init__.py
# Compiled at: 2015-06-08 07:05:57
VERSION = (0, 5, 2, 'dev')
__version__ = ('.').join(str(each) for each in VERSION[:4])
__all__ = [
 'get_version', 'get_repo', 'get_backend',
 'VCSError', 'RepositoryError', 'ChangesetError']
import sys
from managevcs.backends import get_repo, get_backend
from managevcs.exceptions import VCSError, RepositoryError, ChangesetError

def get_version():
    """
    Returns shorter version (digit parts only) as string.
    """
    return ('.').join(str(each) for each in VERSION[:3])


def main(argv=None):
    if argv is None:
        argv = sys.argv
    from managevcs.cli import ExecutionManager
    manager = ExecutionManager(argv)
    manager.execute()
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv))