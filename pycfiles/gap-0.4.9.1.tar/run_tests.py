# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/robin/projects/gap/.venv/lib/python2.7/site-packages/gap/templates/tests/run_tests.py
# Compiled at: 2013-10-11 03:16:02
"""
simple shortcut for running nosetests via python
replacement for *.bat or *.sh wrappers
"""
import sys, os
from copy import copy
from os.path import dirname, realpath, join
import logging
extra_plugins = []
import re
from gap.utils.setup import fix_sys_path
app_path = join(dirname(dirname(realpath(__file__))), 'src')
fix_sys_path(app_path)
os.chdir(dirname(__file__))
sys.path.insert(0, realpath(dirname(__file__)))
argv = copy(sys.argv)
try:
    import nose, webtest
    from nosegae import NoseGAE
except ImportError:
    if sys.__stdin__.isatty():
        print 'Missing testing requirements. Shell I install them for you? [Yn] '
        resp = raw_input().strip().lower()
        if not resp or resp in ('y', 'a'):
            import pip
            pip.main(['install', '-r', 'requirements.pip'])
            import nose, webtest
            from nosegae import NoseGAE
        else:
            print 'Quitting'
            print 'You can install requirements by `pip install -r tests/requirements.pip`'
            print
            sys.exit(255)
    else:
        raise

from nose.config import Config
from nose.plugins import DefaultPluginManager
CONFIG = Config(files=[
 'nose.cfg'], plugins=DefaultPluginManager(plugins=[NoseGAE()]))
try:
    from rednose import RedNose
except ImportError:
    pass
else:
    extra_plugins.append(RedNose())
    argv.append('--rednose')

def run_all():
    logging.debug('Running tests with arguments: %r' % sys.argv)
    nose.run_exit(argv=argv, config=CONFIG, addplugins=extra_plugins)


class TestLoader(nose.loader.TestLoader):

    def __init__(self):
        super(self.__class__, self).__init__(config=CONFIG)


if __name__ == '__main__':
    run_all()