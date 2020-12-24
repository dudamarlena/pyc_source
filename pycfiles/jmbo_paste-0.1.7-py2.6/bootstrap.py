# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/jmbo_paste/templates/jmbo_project/bootstrap.py
# Compiled at: 2011-09-22 10:48:12
"""Bootstrap a buildout-based project

Simply run this script in a directory containing a buildout.cfg.
The script accepts buildout command-line options, so you can
use the -c option to specify an alternate configuration file.
"""
import os, shutil, sys, tempfile, textwrap, urllib, urllib2, subprocess
from optparse import OptionParser
if sys.platform == 'win32':

    def quote(c):
        if ' ' in c:
            return '"%s"' % c
        else:
            return c


else:
    quote = str
(stdout, stderr) = subprocess.Popen([
 sys.executable, '-Sc',
 'try:\n    import ConfigParser\nexcept ImportError:\n    print 1\nelse:\n    print 0\n'], stdout=subprocess.PIPE, stderr=subprocess.PIPE).communicate()
has_broken_dash_S = bool(int(stdout.strip()))
if not has_broken_dash_S and 'site' in sys.modules:
    args = sys.argv[:]
    args[0:0] = [sys.executable, '-S']
    args = map(quote, args)
    os.execv(sys.executable, args)
clean_path = sys.path[:]
import site
sys.path[:] = clean_path
for (k, v) in sys.modules.items():
    if k in ('setuptools', 'pkg_resources') or hasattr(v, '__path__') and len(v.__path__) == 1 and not os.path.exists(os.path.join(v.__path__[0], '__init__.py')):
        sys.modules.pop(k)

is_jython = sys.platform.startswith('java')
setuptools_source = 'http://peak.telecommunity.com/dist/ez_setup.py'
distribute_source = 'http://python-distribute.org/distribute_setup.py'

def normalize_to_url(option, opt_str, value, parser):
    if value:
        if '://' not in value:
            value = 'file://%s' % (
             urllib.pathname2url(os.path.abspath(os.path.expanduser(value))),)
        if opt_str == '--download-base' and not value.endswith('/'):
            value += '/'
    else:
        value = None
    name = opt_str[2:].replace('-', '_')
    setattr(parser.values, name, value)
    return


usage = '[DESIRED PYTHON FOR BUILDOUT] bootstrap.py [options]\n\nBootstraps a buildout-based project.\n\nSimply run this script in a directory containing a buildout.cfg, using the\nPython that you want bin/buildout to use.\n\nNote that by using --setup-source and --download-base to point to\nlocal resources, you can keep this script from going over the network.\n'
parser = OptionParser(usage=usage)
parser.add_option('-v', '--version', dest='version', help='use a specific zc.buildout version')
parser.add_option('-d', '--distribute', action='store_true', dest='use_distribute', default=False, help='Use Distribute rather than Setuptools.')
parser.add_option('--setup-source', action='callback', dest='setup_source', callback=normalize_to_url, nargs=1, type='string', help='Specify a URL or file location for the setup file. If you use Setuptools, this will default to ' + setuptools_source + '; if you use Distribute, this will default to ' + distribute_source + '.')
parser.add_option('--download-base', action='callback', dest='download_base', callback=normalize_to_url, nargs=1, type='string', help='Specify a URL or directory for downloading zc.buildout and either Setuptools or Distribute. Defaults to PyPI.')
parser.add_option('--eggs', help='Specify a directory for storing eggs.  Defaults to a temporary directory that is deleted when the bootstrap script completes.')
parser.add_option('-t', '--accept-buildout-test-releases', dest='accept_buildout_test_releases', action='store_true', default=False, help='Normally, if you do not specify a --version, the bootstrap script and buildout gets the newest *final* versions of zc.buildout and its recipes and extensions for you.  If you use this flag, bootstrap and buildout will get the newest releases even if they are alphas or betas.')
parser.add_option('-c', None, action='store', dest='config_file', help='Specify the path to the buildout configuration file to be used.')
(options, args) = parser.parse_args()
if options.config_file is not None:
    args += ['-c', options.config_file]
if options.eggs:
    eggs_dir = os.path.abspath(os.path.expanduser(options.eggs))
else:
    eggs_dir = tempfile.mkdtemp()
if options.setup_source is None:
    if options.use_distribute:
        options.setup_source = distribute_source
    else:
        options.setup_source = setuptools_source
if options.accept_buildout_test_releases:
    args.append('buildout:accept-buildout-test-releases=true')
args.append('bootstrap')
try:
    import pkg_resources, setuptools
    if not hasattr(pkg_resources, '_distribute'):
        raise ImportError
except ImportError:
    ez_code = urllib2.urlopen(options.setup_source).read().replace('\r\n', '\n')
    ez = {}
    exec ez_code in ez
    setup_args = dict(to_dir=eggs_dir, download_delay=0)
    if options.download_base:
        setup_args['download_base'] = options.download_base
    if options.use_distribute:
        setup_args['no_fake'] = True
    ez['use_setuptools'](**setup_args)
    if 'pkg_resources' in sys.modules:
        reload(sys.modules['pkg_resources'])
    import pkg_resources
    for path in sys.path:
        if path not in pkg_resources.working_set.entries:
            pkg_resources.working_set.add_entry(path)

cmd = [
 quote(sys.executable),
 '-c',
 quote('from setuptools.command.easy_install import main; main()'),
 '-mqNxd',
 quote(eggs_dir)]
if not has_broken_dash_S:
    cmd.insert(1, '-S')
find_links = options.download_base
if not find_links:
    find_links = os.environ.get('bootstrap-testing-find-links')
if find_links:
    cmd.extend(['-f', quote(find_links)])
if options.use_distribute:
    setup_requirement = 'distribute'
else:
    setup_requirement = 'setuptools'
ws = pkg_resources.working_set
setup_requirement_path = ws.find(pkg_resources.Requirement.parse(setup_requirement)).location
env = dict(os.environ, PYTHONPATH=setup_requirement_path)
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
     setup_requirement_path])
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
if is_jython:
    import subprocess
    exitcode = subprocess.Popen(cmd, env=env).wait()
else:
    exitcode = os.spawnle(*([os.P_WAIT, sys.executable] + cmd + [env]))
if exitcode != 0:
    sys.stdout.flush()
    sys.stderr.flush()
    print 'An error occurred when trying to install zc.buildout. Look above this message for any errors that were output by easy_install.'
    sys.exit(exitcode)
ws.add_entry(eggs_dir)
ws.require(requirement)
import zc.buildout.buildout
zc.buildout.buildout.main(args)
if not options.eggs:
    shutil.rmtree(eggs_dir)