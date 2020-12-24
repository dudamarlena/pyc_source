# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/ztfy/webapp/webapp_base/webapp_template/bootstrap.py
# Compiled at: 2011-12-19 03:06:16
"""Bootstrap a buildout-based project

Simply run this script in a directory containing a buildout.cfg.
The script accepts buildout command-line options, so you can
use the -c option to specify an alternate configuration file.
"""
import os, shutil, sys, tempfile, urllib2
from optparse import OptionParser
tmpeggs = tempfile.mkdtemp()
is_jython = sys.platform.startswith('java')
parser = OptionParser()
parser.add_option('-v', '--version', dest='version', help='use a specific zc.buildout version')
parser.add_option('-d', '--distribute', action='store_true', dest='distribute', default=True, help='For backward compatibility. Distribute is used by default.')
parser.add_option('--setuptools', action='store_false', dest='distribute', default=True, help='Use Setuptools rather than Distribute.')
parser.add_option('-c', None, action='store', dest='config_file', help='Specify the path to the buildout configuration file to be used.')
options, args = parser.parse_args()
if options.config_file is not None:
    args += ['-c', options.config_file]
if options.version is not None:
    VERSION = '==%s' % options.version
else:
    VERSION = ''
USE_DISTRIBUTE = options.distribute
args = args + ['bootstrap']
try:
    import pkg_resources, setuptools
    if not hasattr(pkg_resources, '_distribute'):
        raise ImportError
except ImportError:
    ez = {}
    if USE_DISTRIBUTE:
        exec urllib2.urlopen('http://python-distribute.org/distribute_setup.py').read() in ez
        ez['use_setuptools'](to_dir=tmpeggs, download_delay=0, no_fake=True)
    else:
        exec urllib2.urlopen('http://peak.telecommunity.com/dist/ez_setup.py').read() in ez
        ez['use_setuptools'](to_dir=tmpeggs, download_delay=0)
    reload(sys.modules['pkg_resources'])
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