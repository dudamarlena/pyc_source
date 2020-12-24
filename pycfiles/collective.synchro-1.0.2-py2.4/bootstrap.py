# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/collective/synchro/buildout/plone_30/bootstrap.py
# Compiled at: 2008-12-16 18:21:20
"""Bootstrap a buildout-based project

Simply run this script in a directory containing a buildout.cfg.
The script accepts buildout command-line options, so you can
use the -c option to specify an alternate configuration file.

$Id$
"""
import os, shutil, sys, tempfile, urllib2
tmpeggs = tempfile.mkdtemp()
try:
    import pkg_resources
except ImportError:
    ez = {}
    exec urllib2.urlopen('http://peak.telecommunity.com/dist/ez_setup.py').read() in ez
    ez['use_setuptools'](to_dir=tmpeggs, download_delay=0)
    import pkg_resources

cmd = 'from setuptools.command.easy_install import main; main()'
if sys.platform == 'win32':
    cmd = '"%s"' % cmd
ws = pkg_resources.working_set
assert os.spawnle(os.P_WAIT, sys.executable, sys.executable, '-c', cmd, '-mqNxd', tmpeggs, 'zc.buildout', dict(os.environ, PYTHONPATH=ws.find(pkg_resources.Requirement.parse('setuptools')).location)) == 0
ws.add_entry(tmpeggs)
ws.require('zc.buildout')
import zc.buildout.buildout
zc.buildout.buildout.main(sys.argv[1:] + ['bootstrap'])
shutil.rmtree(tmpeggs)