# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/templer/ztfy/templates/ztfy_package/bootstrap.py
# Compiled at: 2014-05-10 04:16:12
"""Bootstrap a buildout-based project

Simply run this script in a directory containing a buildout.cfg.
The script accepts buildout command-line options, so you can
use the -c option to specify an alternate configuration file.
"""
import os, shutil, sys, tempfile
from optparse import OptionParser
tmpeggs = tempfile.mkdtemp()
usage = '[DESIRED PYTHON FOR BUILDOUT] bootstrap.py [options]\n\nBootstraps a buildout-based project.\n\nSimply run this script in a directory containing a buildout.cfg, using the\nPython that you want bin/buildout to use.\n\nNote that by using --find-links to point to local resources, you can keep \nthis script from going over the network.\n'
parser = OptionParser(usage=usage)
parser.add_option('-v', '--version', help='use a specific zc.buildout version')
parser.add_option('-t', '--accept-buildout-test-releases', dest='accept_buildout_test_releases', action='store_true', default=False, help='Normally, if you do not specify a --version, the bootstrap script and buildout gets the newest *final* versions of zc.buildout and its recipes and extensions for you.  If you use this flag, bootstrap and buildout will get the newest releases even if they are alphas or betas.')
parser.add_option('-c', '--config-file', help='Specify the path to the buildout configuration file to be used.')
parser.add_option('-f', '--find-links', help='Specify a URL to search for buildout releases')
parser.add_option('--allow-site-packages', action='store_true', default=False, help='Let bootstrap.py use existing site packages')
options, args = parser.parse_args()
try:
    if options.allow_site_packages:
        import setuptools, pkg_resources
    from urllib.request import urlopen
except ImportError:
    from urllib2 import urlopen

ez = {}
exec (
 urlopen('https://bootstrap.pypa.io/ez_setup.py').read(), ez)
if not options.allow_site_packages:
    import site
    if hasattr(site, 'getsitepackages'):
        for sitepackage_path in site.getsitepackages():
            sys.path[:] = [ x for x in sys.path if sitepackage_path not in x ]

setup_args = dict(to_dir=tmpeggs, download_delay=0)
ez['use_setuptools'](**setup_args)
import setuptools, pkg_resources
for path in sys.path:
    if path not in pkg_resources.working_set.entries:
        pkg_resources.working_set.add_entry(path)

ws = pkg_resources.working_set
cmd = [
 sys.executable, '-c',
 'from setuptools.command.easy_install import main; main()',
 '-mZqNxd', tmpeggs]
find_links = os.environ.get('bootstrap-testing-find-links', options.find_links or ('http://downloads.buildout.org/' if options.accept_buildout_test_releases else None))
if find_links:
    cmd.extend(['-f', find_links])
setuptools_path = ws.find(pkg_resources.Requirement.parse('setuptools')).location
requirement = 'zc.buildout'
version = options.version
if version is None and not options.accept_buildout_test_releases:
    import setuptools.package_index
    _final_parts = ('*final-', '*final')

    def _final_version(parsed_version):
        for part in parsed_version:
            if part[:1] == '*' and part not in _final_parts:
                return False

        return True


    index = setuptools.package_index.PackageIndex(search_path=[
     setuptools_path])
    if find_links:
        index.add_find_links((find_links,))
    req = pkg_resources.Requirement.parse(requirement)
    if index.obtain(req) is not None:
        best = []
        bestv = None
        for dist in index[req.project_name]:
            distv = dist.parsed_version
            if _final_version(distv):
                if bestv is None or distv > bestv:
                    best = [
                     dist]
                    bestv = distv
                elif distv == bestv:
                    best.append(dist)

        if best:
            best.sort()
            version = best[(-1)].version
if version:
    requirement = ('==').join((requirement, version))
cmd.append(requirement)
import subprocess
if subprocess.call(cmd, env=dict(os.environ, PYTHONPATH=setuptools_path)) != 0:
    raise Exception('Failed to execute command:\n%s' % repr(cmd)[1:-1])
ws.add_entry(tmpeggs)
ws.require(requirement)
import zc.buildout.buildout
if not [ a for a in args if '=' not in a ]:
    args.append('bootstrap')
if options.config_file is not None:
    args[0:0] = [
     '-c', options.config_file]
zc.buildout.buildout.main(args)
shutil.rmtree(tmpeggs)