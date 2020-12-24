# uncompyle6 version 3.6.7
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-i686/egg/pyrun.py
# Compiled at: 2008-05-12 06:47:45
__doc__ = "%prog  [-nidDpP] [BASEPATH(s)][-m mod.name | '--'] [TARGET-OPTIONS]\n\nDiscover python packages and modules under BASEPATH(s). Run the first module\nfile named in `BASEPATH(s)` *OR* explicitly nominated using the `-m` option.\n\nIn most cases the solo '--' is not required. It tends to be useful when you\nimplicitly select the module to run AND you want to pass a non option argument\nas the first value in the command line for that module. It can also be\nnecessary when the target module has short options, without long-name\nalternatives, which collide with those defined for pyrun.\n\nNOTE: Any option that is marked [NYI] is Not Yet Implemented."
import os, sys, types, re, traceback, inspect, imp, compiler
from os.path import join, dirname, basename, isfile, isdir, exists, splitext, abspath, normpath, isabs, expandvars, expanduser
from textwrap import dedent
import logging
log = logging.getLogger(__name__)
have_runpy = False
try:
    import runpy
    have_runpy = True
except ImportError:
    pass

OPTIONS_runex = [
 (
  '--log-level',
  dict(default='WARNING', metavar='LEVEL', help='[default:%default] set the logging level, any string which names\na log level which is defined by the logging package is allowed.\nFor example any of CRITICAL, WARNING, INFO and DEBUG (in\nincreasing order of verbosity)')),
 (
  '-q',
  dict(default=False, action='store_true', metavar='QUIET', help='Suppress all warnings about missing paths etc. Useful when you are\nusing speculative paths and are using -p or -P to print the discoverd\npath.')),
 (
  '-p',
  dict(default=False, action='store_true', metavar='PRINTPATH', help='Print the discovered path')),
 (
  '-P',
  dict(default=False, action='store_true', metavar='PRINTPATH', help='Print the discovered path in a PYTHONPATH compatible format')),
 (
  '-n',
  dict(default=False, action='store_true', metavar='NORUN', help="NORUN. Don't run any of the modules implied by module file references in\n the discovery path.")),
 (
  '-C',
  dict(default=None, type='string', metavar='SCRIPT', help='Identify a *python* SCRIPT to execute. The script need not have file\nextension but it must contain leagal python code. This option trumps -m. This\noption should only be necessary when the launcher for the python program you\nwish to run contains significant functionality. No additions are made to the\ndiscovery path or sys.path as a result of using this option. If the target\nscript imports a related package you will need to include additional non option\narguments to discover its path.')),
 (
  '-m',
  dict(default='', metavar='MODULE', help='Explicitly select a module to run. (trumped by -S)')),
 (
  '-d',
  dict(default=False, action='store_true', metavar='DEBUG', help='DEBUG session. Use `pdb.runeval` on the module code in order to enter\nan interactive debug session at the first python statement of the\ntarget module')),
 (
  '-D',
  dict(default=False, action='store_true', metavar='DEBUG', help='POSTMORTEM debugging. If the target raises an exception, start a\n    postmortem pdb debugging session.')),
 (
  '-i',
  dict(default=False, action='store_true', metavar='INTERACTIVE', help='INTERACTIVE session with prepared sys.argv and sys.path.')),
 (
  '-c',
  dict(default=False, metavar='STATEMENT', help='Update sys.argv and sys.path then execute the statement in a new, clean,\nmodule context.')),
 (
  '-x',
  dict(default='', metavar='EXCLUDE', help='Exclude one or more directories, separated by "%s", from the discovery\npath.' % os.pathsep)),
 (
  '-X',
  dict(default=[], metavar='PRUNE', action='append', type='string', help='Prune all paths which contain this value from the set of paths which *were*\ndiscovered. Specify multiple -X options if you wish too prune based on\nmore than one string.'))]

def exc_string(einfo=None):
    """Attempt to collapse a trace back into a single line.

    See the exc_string.py module for an implementation that works harder to
    deal with encoding issues.

    """
    try:
        try:
            (t, v, tb) = einfo or sys.exc_info()
            if t is None:
                return 'no exception'
            e = str(t)
            if v is not None:
                e = str(v)
            t = getattr(t, '__name__', type(t).__name__)
            tracestr = (' <- ').join([ '%s() (%s:%s)' % (m, os.path.split(f)[1], n) for (f, n, m, u) in reversed(traceback.extract_tb(tb))
                                     ])
            return '[%s:"%s"] in %s' % (t, e, tracestr)
        except:
            return '** failed to extract traceback **'

    finally:
        t = v = tb = einfo = None

    return


def path_moduleinfo(path, allowmtypes=(
 imp.PY_SOURCE, imp.PY_COMPILED)):
    """Get extended module info for `path`

    If path identifies a legitemate python file (as determined by
    inspect.getmoduleinfo) then return a 4 element tuple:

    (dirname(path), modname, ext, mode, mtype)

    modname, ext, mode and mtype are obtained using `inspect.getmoduleinfo`
    Note that for a legitemate path::

        path_moduleinfo(path)[1:] == inspect.moduleinfo(path)

    """
    v = inspect.getmoduleinfo(path)
    if not v:
        return
    (modname, ext, mode, mtype) = v
    if mtype not in allowmtypes:
        return
    return (dirname(path), modname, ext, mode, mtype)


def path_pkg_moduleinfo(path, allowmtypes=(
 imp.PY_SOURCE, imp.PY_COMPILED)):
    """Get extended module info for `path`

    `path` must be the location of a real file on disk.

    If path identifies a legitemate python file (as determined by
    inspect.getmoduleinfo) then return a 4 element tuple:

    (pkg_path, modname, ext, mode, mtype)

    ext, mode and mtype are obtained using `inspect.getmoduleinfo`

    `modname` is the fully qualified module name.
    `path` is the directory containing the top most package.

    `modname` and `pkg_path` are found by testing succesive directories above
    `path`. The upward walk terminates when it encounters a directory whose
    basename is not a legal python module name OR which does not contain a
    suitable __init__.py (The search allows for __init__.py, __init__.pyc,
    and __init__.pyo).

    """
    if not isfile(path):
        return
    v = inspect.getmoduleinfo(path)
    if not v:
        return
    (modname, ext, mode, mtype) = v
    if mtype not in allowmtypes:
        return
    p = dirname(path)
    packagedirs = []
    packages = []
    m = basename(p)
    while p and '.' not in m and (isfile(join(p, '__init__.py')) or isfile(join(p, '__init__.pyc'))):
        packagedirs.append(p)
        packages.append(m)
        p = dirname(p)
        m = basename(p)

    packagedirs.reverse()
    packages.reverse()
    packages.append(modname)
    return (
     p, ('.').join(packages), ext, mode, mtype)


def convert_path(pathname):
    """Return 'pathname' as a name that will work on the native filesystem,
    i.e. split it on '/' and put it back together again using the current
    directory separator.  Needed because filenames in the setup script are
    always supplied in Unix style, and have to be converted to the local
    convention before we can actually use them in the filesystem.  Raises
    ValueError on non-Unix-ish systems if 'pathname' either starts or
    ends with a slash.
    """
    if os.sep == '/':
        return pathname
    if not pathname:
        return pathname
    if pathname[0] == '/':
        raise ValueError, "path '%s' cannot be absolute" % pathname
    if pathname[(-1)] == '/':
        raise ValueError, "path '%s' cannot end with '/'" % pathname
    paths = pathname.split('/')
    while '.' in paths:
        paths.remove('.')

    if not paths:
        return os.curdir
    return apply(os.path.join, paths)


pkg_resources_EGG_NAME = re.compile('(?P<name>[^-]+)( -(?P<ver>[^-]+) (-py(?P<pyver>[^-]+) (-(?P<plat>.+))? )? )?', re.VERBOSE | re.IGNORECASE).match
pkg_resources_component_re = re.compile('(\\d+ | [a-z]+ | \\.| -)', re.VERBOSE)
pkg_resources_ver_replace = {'pre': 'c', 'preview': 'c', '-': 'final-', 'rc': 'c', 'dev': '@'}.get

def pkg_resources_parse_version_parts(s):
    for part in pkg_resources_component_re.split(s):
        part = pkg_resources_ver_replace(part, part)
        if not part or part == '.':
            continue
        if part[:1] in '0123456789':
            yield part.zfill(8)
        else:
            yield '*' + part

    yield '*final'


def filter_best_eggs(source, remove_ifnoteggmatch=False):
    eggs = {}
    keep = []
    prune_2ndpass = []
    for s in source:
        mo = pkg_resources_EGG_NAME(basename(s))
        if not mo:
            if not remove_ifnoteggmatch:
                keep.append(s)
            continue
        pkgname, ver, pyver = mo.group('name'), mo.group('ver'), mo.group('pyver')
        if not (pkgname and ver and pyver):
            if pkgname:
                if not remove_ifnoteggmatch:
                    keep.append(s)
                continue
            if not pyver.startswith(sys.version[:3]):
                continue
            ver = tuple(pkg_resources_parse_version_parts(ver))
        elif pkgname not in eggs:
            eggs[pkgname] = (
             pkgname, ver, s)
            keep.append(s)
        elif ver >= eggs[pkgname][1]:
            prune_2ndpass.append(eggs[pkgname][2])
            keep.append(s)
        elif ver < eggs[pkgname][1]:
            prune_2ndpass.append(s)

    prune_2ndpass = frozenset(prune_2ndpass)
    return [ s for s in keep if s not in prune_2ndpass ]


def evaluate_packagepath(path, name='', allow_egglinks=False):
    if isegg_path(path, allow_links=True):
        if not isegg_path(path, allow_links=False):
            if not allow_egglinks:
                return False
            egg_pth = file(path, 'r').read().strip()
            egg_pth = egg_pth.split('\n')[0].strip()
            return name or normpath(abspath(join(dirname(path), egg_pth)))
        else:
            return name or path
    if isdir(path) and '.' not in name and (isfile(join(path, '__init__.py')) or isfile(join(path, '__init__.pyc')) or isfile(join(path, '__init__.pyo'))):
        return name or dirname(path)
    return False


def isegg_path(path, allow_links=False):
    bn = basename(path)
    if not pkg_resources_EGG_NAME(bn):
        return False
    if path.endswith('.egg'):
        return True
    if path.endswith('.egg-link'):
        if not allow_links:
            return False
        return True
    return False


def find_top_packages(where='.', evaluate_packagelocation=evaluate_packagepath, allow_descent=lambda path: isdir(path) and not isegg_path(path)):
    """Find all top level package directories under `where`

    If `where` is a relative path then, by default all resulting paths will
    also be relative. If `where` is an absoloute path then the result paths
    will also be absoloute. This behaviour can be modified by providing a
    custom `evaluate_packagelocation` function.

    Note that by default, egg directories and egg archive files are found as
    top level package paths but the find process will not decends below the
    level of an egg directory. This behaviour can be modified by judicious use
    of `evaluate_packagelocation` and `allow_descent`.

    """
    tops = {}
    stack = [
     convert_path(where)]
    while stack:
        where = stack.pop(0)
        for name in os.listdir(where):
            fn = join(where, name)
            result = evaluate_packagelocation(fn, name=name)
            if result:
                tops.setdefault(where, []).append(result)
            if allow_descent(fn) and not result:
                stack.append(fn)

    return sorted(tops.items())


def find_package_paths(*rootpaths, **kw):
    pthset = set(kw.pop('pth', []))
    exclude = kw.pop('exclude', [])
    pth = []
    evpp = lambda p, name='': evaluate_packagepath(p)

    def allow_descent(path):
        for e in exclude:
            if path.startswith(e) or not isabs(e) and path.startswith(join('.', e)):
                log.info('Excluding: "%s" as it startswith "%s"' % (
                 path, e))
                return False

        return isdir(path) and not isegg_path(path)

    for rp in rootpaths:
        ep = evpp(rp)
        if ep and ep not in pthset:
            pthset.add(ep)
            pth.append(ep)
            continue
        if not isdir(rp):
            continue
        for top in find_top_packages(rp, evaluate_packagelocation=evpp, allow_descent=allow_descent):
            for p in top[1]:
                if p not in pthset:
                    pth.append(p)
                    pthset.add(p)

    return filter_best_eggs(pth)


def enumerate_argv_args(argv, startpos=0):
    for i in range(len(argv) - startpos):
        ia = i + startpos
        a = argv[ia]
        if a[:2] == '--' or a[:1] == '-':
            return
        else:
            yield (
             ia, a)


def get_inferior_argv(opts, default_opts, flag_opts, argv, ia, short_opts=None):
    if short_opts is None:
        short_opts = {}
    assert ia <= len(argv) + 1, 'ia=%s, argv="%s"' % (
     ia, str(argv))
    if ia >= len(argv):
        return []
    if argv[ia] == '--' or argv[ia] == '-':
        del argv[ia]
    else:
        if argv[ia].startswith('--'):
            nextopt = argv[ia][2:]
        else:
            nextopt = argv[ia][1:]
        if nextopt in default_opts and getattr(opts, nextopt) == default_opts[nextopt]:
            if nextopt in flag_opts:
                setattr(opts, nextopt, not default_opts[nextopt])
                del argv[ia]
            elif len(argv) >= ia + 1:
                setattr(opts, nextopt, argv[(ia + 1)])
                del argv[ia:ia + 2]
            else:
                log.warning('The `-%s` option requires an argument', nextopt)
    return argv[ia:]


def discover_path(exclude, offset, *args):
    """Discover a python path.

    Discovers additional package paths by considering each item in args. args
    should typically be a sys.argv style argument list. Discovery terminates
    with the first argument that looks like an option. "Looks like an option"
    means is exactly ``--`` or startswith either '--' or '-'. The non option
    arguments should identify either: directories under which you want to
    discover package paths OR legitemate python module files.

    The results are returned as a 4 element tuple: The first element is the
    discovered path; The second is a list containing the result of
    `path_pkg_moduleinfo` for any explicit references to python module files;
    The third is the index of the first non option argument with your
    supplied offset added to it; and the last is a list of each item in args
    which does not exist on the file system:

        ``(pathextension, moduleinfos, inonoption, doesnotexist)``

    See the implementation of `discover_and_run` for a typical usage example.

    Note that the path implied by an explicit module reference is included in
    pathextension. The moduleinfos element of the return is a convenience to
    asist cases where you want to imediately `run` one or more of the
    discovered modules.

    Discovery is egg aware: it takes care to include only the *best* version of
    each egg and only those eggs that match the python interpreters version.

    The extension path discovered by this api consists of unique paths in order
    of discovery. Where egg directories or archive files are encountered care
    is taken to ensure that eggs which are incompatible with the current
    `sys.executable` are *excluded* and only the *best* available version for
    each project is *included*. The measure of "best available" is the same as
    used by pkg_resources.py from the setuptools project.

    """
    if exclude is None:
        exclude = frozenset([])
    doesnotexist = []
    minfos = []
    pthextend = []
    findpaths = []
    pthset = set([])
    ia = offset
    for (ia, a) in enumerate_argv_args(args, offset):
        if not exists(a):
            doesnotexist.append(a)
        elif isfile(a) and splitext(a)[1] == '.pth':
            if findpaths:
                newpaths = find_package_paths(pth=pthset, exclude=exclude, *findpaths)
                pthextend.extend(newpaths)
                findpaths[:] = []
            basedir = dirname(normpath(abspath(a)))
            for pth in file(a):
                pth = pth.strip()
                if not pth:
                    continue
                pth = expanduser(expandvars(pth))
                pth = normpath(abspath(join(basedir, pth)))
                if not exists(pth):
                    doesnotexist.append(pth)
                    continue
                pthextend.append(pth)

            continue
        minfo = path_pkg_moduleinfo(a)
        if minfo:
            minfos.append(minfo)
            a = minfo[0]
            if a not in pthset:
                pthextend.append(a)
                pthset.add(a)
        else:
            findpaths.append(a)

    newpaths = find_package_paths(pth=pthset, exclude=exclude, *findpaths)
    pthextend.extend(newpaths)
    return (
     pthextend, minfos, ia + 1, doesnotexist)


def discover_and_run(argv=None, run_module=True, modify_sys=True, exclude=frozenset([])):
    """Discover package paths and run the last module listed in argv.

    Uses `discover_path` to perform the path discovery and identify any
    module files listed on the command line.

    Uses runpy.run_module to run the module as though it was '__main__'.

    :Paramaters:
        run_module
            If False the module will *not* be executed. Otherwise it should
            be the either: The explicit name of the module to run or any
            value that evalutes True. If its true and its *not* a string
            then the module name corresponding to the *first* module file
            referenced in `argv` is implied.
        modify_sys
            If False sys.argv and sys.path will *not* be changed. Otherwise
            sys.argv and sys.path will be updated appropriately only if
            run_module is not False.

    :Returns:
        If a module is run the return value is the result of
        `runpy.run_module` otherwise it is a 3 element tuple:

        (pthextend, minfos, ia)

        * `pthextend` is a list of the paths that were discovered.
        * `minfos` is a list of tuples describing the results of examining
          any module files.
        * `ia` is index of the first option argument encountered after the
          discovery paths.

    """
    global runpy
    argv = argv or sys.argv[:]
    (pthextend, minfos, ia, doesnotexist) = discover_path(exclude, 1, *argv)
    if ia < len(argv) and argv[ia] == '--':
        del argv[ia]
    if run_module and not isinstance(run_module, types.StringTypes):
        run_module = minfos[0][1]
    if modify_sys:
        sys.path[0:0] = pthextend[:]
        sys.argv[:] = []
        sys.argv.append(run_module)
        sys.argv.extend(argv[ia:])
    if run_module and have_runpy is not False:
        return runpy.run_module(run_module, run_name='__main__', alter_sys=True)
    return (
     pthextend, minfos, ia)


def get_module_code_and_filename(mod_name):
    """Get the code object and filename for the python module `mod_name`

    This is exactly like runpy.run_module but instead of running the code,
    it returns (code, filename)

    """
    global runpy
    if not have_runpy:
        runpy = __import__('runpy')
    loader = runpy.get_loader(mod_name)
    if loader is None:
        raise ImportError('No module named ' + mod_name)
    code = loader.get_code(mod_name)
    if code is None:
        raise ImportError('No code object available for ' + mod_name)
    filename = runpy._get_filename(loader, mod_name)
    return (
     code, filename)


def get_module_code(mod_name):
    """Get the code object for the python module `mod_name`"""
    return get_module_code_and_filename(mod_name)[0]


def get_module_filename(mod_name):
    """Get the filename for the python module `mod_name`"""
    return get_module_code_and_filename(mod_name)[1]


def dbg_run_code(code, run_globals, init_globals, mod_name, mod_fname, mod_loader):
    if init_globals is not None:
        run_globals.update(init_globals)
    run_globals.update(__name__=mod_name, __file__=mod_fname, __loader__=mod_loader)
    import pdb
    pdb.runeval(code, run_globals)
    return run_globals


def run_module_code(runner, code, init_globals=None, mod_name=None, mod_fname=None, mod_loader=None, alter_sys=False):
    """Variant of runpy._run_module_code with hook for _run_code

    `runner` must be None or be a suitable replacement for runpy._run_code

    (For example see dbg_run_code above)

    """
    if runner is None:
        assert have_runpy
        runner = runpy._run_code
    if alter_sys:
        temp_module = imp.new_module(mod_name)
        mod_globals = temp_module.__dict__
        saved_argv0 = sys.argv[0]
        restore_module = mod_name in sys.modules
        if restore_module:
            saved_module = sys.modules[mod_name]
        sys.argv[0] = mod_fname
        sys.modules[mod_name] = temp_module
        try:
            runner(code, mod_globals, init_globals, mod_name, mod_fname, mod_loader)
        finally:
            sys.argv[0] = saved_argv0

        if restore_module:
            sys.modules[mod_name] = saved_module
        else:
            del sys.modules[mod_name]
        return mod_globals.copy()
    else:
        return runner(code, {}, init_globals, mod_name, mod_fname, mod_loader)
    return


def striplines(s):
    return ('\n').join(map(('').__class__.strip, s.split('\n')))


interactive_BANNER_BOILERPLATE = 'handy locals() are:\n    The function run() (runs the discovered module or -c/-C/-S options)\n    The variables target_argv, pthextend\n\nUpdate target_argv *in place* before calling run() if you want to tweak\nthe sys.argv the module sees.'

def pyrun_opts(**kw):
    """Convert keyword arguments to opts instance for `pyrun'

    raises TypeError if any keyword is present which is not a long or short
    option defined for the command line tool. Default values are filled in
    based on those used for the command line tool.

    :Returns:
        opts
            An instance, synthesized using `type', whose attributes correspond
            to the provided keywords. The default value for any pyrun option
            which is not provided via `kw' is included.
        defaultset
            A list of those options (co-erced to legal attribute names) which
            took on default values.
        notset
            A list of those options (co-erced to legal attribute names) which
            where not provided and for which no default exists.

    """
    optdefs = dict(OPTIONS_runex)
    present = dict()

    def k_to_opt(k):
        if len(k) == 1:
            return '-' + k
        else:
            return '--' + k.replace('_', '-')

    def opt_to_k(opt):
        if opt.startswith('--'):
            return opt[2:].replace('-', '_')
        else:
            return opt[1]

    for (k, v) in kw.iteritems():
        opt = k_to_opt(k)
        if opt not in optdefs:
            raise TypeError('Option "%s" not supported.' % opt)
        else:
            print 'present', opt
            present[k] = v
            continue

    opts = present.copy()
    defaultset = []
    notset = []
    for absent in set(optdefs.keys()) - set(present.keys()):
        kabsent = opt_to_k(absent)
        if 'default' in optdefs[absent]:
            opts[kabsent] = optdefs[absent]['default']
            defaultset.append(kabsent)
        else:
            notset.append(kabsent)

    return (type('PyRunOptions', (), opts)(), defaultset, notset)


def pyrun(opts, discovery_args):
    default_opts = get_default_opts()
    argv = discovery_args[:]
    argv.insert(0, None)

    def filter_empty(sequence, warningmsg, reportmsg=log.warning):
        for e in sequence:
            if not e:
                reportmsg(warningmsg)
                continue
            yield e

    exclude, prune = [], []
    if opts.x:
        exclude = list(filter_empty(opts.x.split(os.pathsep), dedent('                    Warning: empty path found in (and removed from) your\n                    exclusion path (-x)')))
    prune = list(filter_empty(opts.X, dedent('                Warning: An empty string was specified using -X,\n                as this would prune *all* paths it will be ignored.')))
    try:
        source = False
        sourcefile = None
        if opts.c and opts.C and not opts.q:
            log.warning(striplines('\n            Warning: -c and -C can not be used together. Ignoring "-C %s"\n            ' % opts.C))
        if opts.C:
            source = file(opts.C).read()
            sourcefile = opts.C
        if opts.c:
            sourcefile = '<command-line>'
            source = opts.c
        (pthextend, minfos, ia, doesnotexist) = discover_path(exclude, 1, *argv)
        if not opts.q and doesnotexist:
            log.warning(striplines('            Warning: your discovery path arguments referenced the following\n            files or directories which do not exist on the file system:            '))
            log.warning('\t' + ('\n\t').join(doesnotexist) + '\n')
        inferior_argv = get_inferior_argv(opts, default_opts, _get_flag_opts(), argv, ia)
        if opts.c and opts.C and not opts.q:
            log.warning('Warning: -c and -C can not be used together. Ignoring "-C %s"' % opts.C)
        if opts.C:
            source = file(opts.C).read()
            sourcefile = opts.C
        if opts.c:
            sourcefile = '<command-line>'
            source = opts.c
        modname = not source and (opts.m or minfos and minfos[0][1] or '')
        for X in prune:
            pthextend[:] = [ p for p in pthextend if not p.startswith(X) ]

        sys.path[0:0] = pthextend[:]
        target_argv = []
        if modname or source:
            target_argv.append(modname or source)
            target_argv.extend(inferior_argv)

        def run():
            if opts.n:
                log.critical('execution of module disabled by user options')
                return 0
            if not target_argv:
                log.critical('argv is empty')
                return 0
            sys.argv[:] = target_argv[:]
            if runpy is not False:
                runner = None
                if opts.d:
                    runner = dbg_run_code
                if not source:
                    (code, filename) = get_module_code_and_filename(modname)
                else:
                    code = compiler.compile(source, sourcefile, 'exec')
                    filename = sourcefile
                return run_module_code(runner, code, init_globals=None, mod_name='__main__', mod_fname=filename, alter_sys=True)
            return

        if opts.i:
            banner = ''
            if opts.p:
                banner += 'Discovered paths:\n\t%s' % ('\n\t').join(pthextend)
            if opts.P:
                banner += '\n\nPYTHONPATH=%s' % os.pathsep.join(pthextend)
            if opts.p or opts.P:
                banner += '\n\n'
            banner += interactive_BANNER_BOILERPLATE
            import code
            code.interact(banner=banner, local=locals())
        if not opts.i:
            if pthextend and opts.p:
                for p in pthextend:
                    print p

            if pthextend and opts.P:
                print os.pathsep.join(pthextend)
        if not (opts.n or opts.i) and (modname or source):
            exitval = run()
            if not isinstance(exitval, int):
                return 0
            return exitval
        return 0
    except SystemExit:
        raise
    except:
        einfo = sys.exc_info()
        msg = exc_string(einfo=einfo)
        print msg
        if opts.D and not opts.d:
            import pdb
            pdb.post_mortem(einfo[2])
        return -1

    return


def int_log_level(level):
    """Coerce a log level to an integer.

    In a manner cognizant of run time configured level names."""
    try:
        return int(level)
    except ValueError:
        try:
            return getattr(logging, level)
        except AttributeError:
            level = logging.getLevelName(level)
            level = logging.getLevelName(level)
            assert isinstance(level, int)
            return level


def _pyrun_cl_parse_log_init(argv=None):
    """Command line argument parsing and logging intialisation.

    :Returns:
        opts
            optparse.OptionValues instance containing the pyrun options
            which preceded the discover path
        args
            In order, pyrun discovery path, pyrun terminating options, and the
            options and arguments for the inferior programs.

    """
    import optparse
    parser = optparse.OptionParser(usage=__doc__)
    for (shrt, kw) in OPTIONS_runex:
        parser.add_option(shrt, **kw)

    parser.disable_interspersed_args()
    (opts, args) = parser.parse_args(argv or sys.argv[1:])
    logging.basicConfig(level=int_log_level(getattr(opts, 'log_level', 'WARNING')), format='%(message)s')
    return (
     opts, args)


def get_default_opts():
    """Return a dictionary containing the default pyrun option values."""
    default_opts = {}
    for (shrt, kw) in OPTIONS_runex:
        default_opts[shrt[1]] = kw['default']

    return default_opts


def runex(argv=None):
    """Provides Extened `pyrun` features on the command line."""
    (opts, discovery_args) = _pyrun_cl_parse_log_init(argv)
    return pyrun(opts, discovery_args)


def run(argv=None):
    """Basic features for command line use,

    `--` may be used to artificially terminate the pyrun discovery
    path. All other options are passed to the *implicitly* selected
    target module.

    NOTE: Command line help is not provided by this entry point and all options
    are expected to be for the target module.

    """
    try:
        rval = discover_and_run(argv)
        if not isinstance(rval, int):
            if isinstance(rval, tuple) and isinstance(rval[0], list):
                for p in rval[0]:
                    print p

            rval = 0
    except SystemExit:
        raise
    except:
        rval = -1
        msg = exc_string()
        print msg

    return rval


def _get_flag_opts():
    return tuple([ o[1:] for (o, kw) in OPTIONS_runex if kw.get('action', None) in ('store_true',
                                                                                    'store_false')
                 ])


if __name__ == '__main__':
    sys.exit(runex())