# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-i686/egg/collective/synchro/buildout/plone_30/bootstrap.py
# Compiled at: 2008-12-16 18:21:20
__doc__ = 'Bootstrap a buildout-based project\n\nSimply run this script in a directory containing a buildout.cfg.\nThe script accepts buildout command-line options, so you can\nuse the -c option to specify an alternate configuration file.\n\n$Id$\n'
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