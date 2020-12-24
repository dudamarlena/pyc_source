# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/panya_paste/templates/panya_project/bootstrap.py
# Compiled at: 2010-11-24 00:47:47
"""Bootstrap a buildout-based project

Simply run this script in a directory containing a buildout.cfg.
The script accepts buildout command-line options, so you can
use the -c option to specify an alternate configuration file.

$Id: bootstrap.py 105417 2009-11-01 15:15:20Z tarek $
"""
import os, shutil, sys, tempfile, urllib2
from optparse import OptionParser
tmpeggs = tempfile.mkdtemp()
is_jython = sys.platform.startswith('java')
parser = OptionParser()
parser.add_option('-v', '--version', dest='version', help='use a specific zc.buildout version')
parser.add_option('-d', '--distribute', action='store_true', dest='distribute', default=False, help='Use Disribute rather than Setuptools.')
parser.add_option('-c', None, action='store', dest='config_file', help='Specify the path to the buildout configuration file to be used.')
(options, args) = parser.parse_args()
if options.config_file is not None:
    args += ['-c', options.config_file]
if options.version is not None:
    VERSION = '==%s' % options.version
else:
    VERSION = ''
USE_DISTRIBUTE = options.distribute
args = args + ['bootstrap']
to_reload = False
try:
    import pkg_resources
    if not hasattr(pkg_resources, '_distribute'):
        to_reload = True
        raise ImportError
except ImportError:
    ez = {}
    if USE_DISTRIBUTE:
        exec urllib2.urlopen('http://python-distribute.org/distribute_setup.py').read() in ez
        ez['use_setuptools'](to_dir=tmpeggs, download_delay=0, no_fake=True)
    else:
        exec urllib2.urlopen('http://peak.telecommunity.com/dist/ez_setup.py').read() in ez
        ez['use_setuptools'](to_dir=tmpeggs, download_delay=0)
    if to_reload:
        reload(pkg_resources)
    else:
        import pkg_resources

if sys.platform == 'win32':

    def quote(c):
        if ' ' in c:
            return '"%s"' % c
        else:
            return c


else:

    def quote(c):
        return c


cmd = 'from setuptools.command.easy_install import main; main()'
ws = pkg_resources.working_set
if USE_DISTRIBUTE:
    requirement = 'distribute'
else:
    requirement = 'setuptools'
if is_jython:
    import subprocess
    assert subprocess.Popen([sys.executable] + ['-c', quote(cmd), '-mqNxd',
     quote(tmpeggs), 'zc.buildout' + VERSION], env=dict(os.environ, PYTHONPATH=ws.find(pkg_resources.Requirement.parse(requirement)).location)).wait() == 0
else:
    assert os.spawnle(os.P_WAIT, sys.executable, quote(sys.executable), '-c', quote(cmd), '-mqNxd', quote(tmpeggs), 'zc.buildout' + VERSION, dict(os.environ, PYTHONPATH=ws.find(pkg_resources.Requirement.parse(requirement)).location)) == 0
ws.add_entry(tmpeggs)
ws.require('zc.buildout' + VERSION)
import zc.buildout.buildout
zc.buildout.buildout.main(args)
shutil.rmtree(tmpeggs)