# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/lukasz/develop/workspace/vcs/vcs/__init__.py
# Compiled at: 2013-04-30 09:32:13
"""
    vcs
    ~~~

    Various version Control System (vcs) management abstraction layer for
    Python.

    :created_on: Apr 8, 2010
    :copyright: (c) 2010-2011 by Marcin Kuzminski, Lukasz Balcerzak.
"""
VERSION = (0, 4, 0)
__version__ = ('.').join(str(each) for each in VERSION[:4])
__all__ = [
 'get_version', 'get_repo', 'get_backend',
 'VCSError', 'RepositoryError', 'ChangesetError']
import sys
from vcs.backends import get_repo, get_backend
from vcs.exceptions import VCSError, RepositoryError, ChangesetError

def get_version():
    """
    Returns shorter version (digit parts only) as string.
    """
    return ('.').join(str(each) for each in VERSION[:3])


def main(argv=None):
    if argv is None:
        argv = sys.argv
    from vcs.cli import ExecutionManager
    manager = ExecutionManager(argv)
    manager.execute()
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv))