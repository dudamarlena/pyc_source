# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/mkcode/collector.py
# Compiled at: 2007-05-28 18:11:20
"""
Routines for collecting all of the tasks floating around the system in
places like setuptools, files, command-line args, etc.
"""
from mkcode import pathing, registry
import sys, imp, pkg_resources

class DistutilsTask(registry.Task):
    __module__ = __name__

    def __init__(self, command):
        super(DistutilsTask, self).__init__(command, None, self.run_command)
        self.distutils_command = command
        return

    def run_command(self, *args, **kwargs):
        run_setupcommand(self.distutils_command, *args, **kwargs)


def collect_from_distutils():
    """
    Return all of the tasks defined in the `distutils.commands' entry
    point.  Returns the tasks as part of the 'setup' namespace.
    """
    pts = pkg_resources.iter_entry_points('distutils.commands')
    ns = registry.namespace('setup')
    for pt in pts:
        t = DistutilsTask(pt.name)
        ns.add_task(t)

    return ns


def run_setupcommand(command, *args):
    """
    Run the specified distutils command with the supplied arguments
    list, `args'.
    
    There must be a setup.py file in the current working directory for
    this function to work.
    """
    setup_py = pathing.path('setup.py')
    if not setup_py.exists():
        raise IOError, 'A setup.py file could not be found in the current directory'
    sys.argv = [
     'setup.py', command] + list(args)
    execfile(setup_py)


def collect_from_file(mkfile):
    """
    Collect all of the tasks and variables defined in the specified
    Python mkfile.  Takes a `pathing.path()' object as it's only argument.
    """
    mdir = mkfile.abspath().dirname()
    name = mkfile.splitext()[0].basename()
    (fp, fullpath, desc) = imp.find_module(name, [mdir])
    try:
        imp.load_module(name, fp, fullpath, desc)
    finally:
        if fp:
            fp.close()


def collect_from_hooks():
    """
    Collect all tasks published by the setuptools entry point,
    `mkcode.collector'.
    """
    for pt in pkg_resources.iter_entry_points('mkcode.collector'):
        try:
            collector = pt.load()
            collector()
        except Exception, err:
            import traceback
            traceback.print_exc()


def collect_all(mkfile=None):
    """
    Collect all available tasks from all known sources.
    """
    collect_from_distutils()
    collect_from_hooks()
    if not mkfile:
        mkfile = 'mkfile.py'
    mkfp = pathing.path(mkfile)
    if mkfp.exists():
        collect_from_file(mkfp)