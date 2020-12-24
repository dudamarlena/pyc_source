# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.5-i386/egg/fez/djangoskel/templates/django_buildout/bootstrap.py
# Compiled at: 2009-01-02 04:30:21
"""Bootstrap a buildout-based project

Simply run this script in a directory containing a buildout.cfg.
The script accepts buildout command-line options, so you can
use the -c option to specify an alternate configuration file.

$Id$
"""
import os, shutil, sys, tempfile, urllib2
tmpeggs = tempfile.mkdtemp()
is_jython = sys.platform.startswith('java')
try:
    import pkg_resources
except ImportError:
    ez = {}
    exec urllib2.urlopen('http://peak.telecommunity.com/dist/ez_setup.py').read() in ez
    ez['use_setuptools'](to_dir=tmpeggs, download_delay=0)
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
if is_jython:
    import subprocess
    assert subprocess.Popen([sys.executable] + ['-c', quote(cmd), '-mqNxd',
     quote(tmpeggs), 'zc.buildout'], env=dict(os.environ, PYTHONPATH=ws.find(pkg_resources.Requirement.parse('setuptools')).location)).wait() == 0
else:
    assert os.spawnle(os.P_WAIT, sys.executable, quote(sys.executable), '-c', quote(cmd), '-mqNxd', quote(tmpeggs), 'zc.buildout', dict(os.environ, PYTHONPATH=ws.find(pkg_resources.Requirement.parse('setuptools')).location)) == 0
ws.add_entry(tmpeggs)
ws.require('zc.buildout')
import zc.buildout.buildout
zc.buildout.buildout.main(sys.argv[1:] + ['bootstrap'])
shutil.rmtree(tmpeggs)