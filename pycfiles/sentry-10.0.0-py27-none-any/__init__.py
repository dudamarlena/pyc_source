# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /usr/src/sentry/src/sentry/__init__.py
# Compiled at: 2019-11-01 16:39:51
from __future__ import absolute_import
import os, os.path
from subprocess import check_output
try:
    VERSION = __import__('pkg_resources').get_distribution('sentry').version
except Exception:
    VERSION = 'unknown'

def _get_git_revision(path):
    if not os.path.exists(os.path.join(path, '.git')):
        return
    else:
        try:
            revision = check_output(['git', 'rev-parse', 'HEAD'], cwd=path, env=os.environ)
        except Exception:
            return

        return revision.strip()


def get_revision():
    """
    :returns: Revision number of this branch/checkout, if available. None if
        no revision number can be determined.
    """
    if 'SENTRY_BUILD' in os.environ:
        return os.environ['SENTRY_BUILD']
    else:
        package_dir = os.path.dirname(__file__)
        checkout_dir = os.path.normpath(os.path.join(package_dir, os.pardir, os.pardir))
        path = os.path.join(checkout_dir)
        if os.path.exists(path):
            return _get_git_revision(path)
        return


def get_version():
    if __build__:
        return '%s.%s' % (__version__, __build__)
    return __version__


def is_docker():
    return 'SENTRY_VERSION' in os.environ or 'SENTRY_BUILD' in os.environ


__version__ = VERSION
__build__ = get_revision()
__docformat__ = 'restructuredtext en'
__import__('sentry.monkey')