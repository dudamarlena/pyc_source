# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\derek_2\Google Drive\nvda-addon-exploded\notepad++\scons-local-2.5.0\SCons\SConf.py
# Compiled at: 2016-07-07 03:21:31
"""SCons.SConf

Autoconf-like configuration support.

In other words, SConf allows to run tests on the build machine to detect
capabilities of system and do some things based on result: generate config
files, header files for C/C++, update variables in environment.

Tests on the build system can detect if compiler sees header files, if
libraries are installed, if some command line options are supported etc.

"""
__revision__ = 'src/engine/SCons/SConf.py rel_2.5.0:3543:937e55cd78f7 2016/04/09 11:29:54 bdbaddog'
import SCons.compat, io, os, re, sys, traceback, SCons.Action, SCons.Builder, SCons.Errors, SCons.Job, SCons.Node.FS, SCons.Taskmaster, SCons.Util, SCons.Warnings, SCons.Conftest
from SCons.Debug import Trace
SCons.Conftest.LogInputFiles = 0
SCons.Conftest.LogErrorMessages = 0
build_type = None
build_types = ['clean', 'help']

def SetBuildType(type):
    global build_type
    build_type = type


dryrun = 0
AUTO = 0
FORCE = 1
CACHE = 2
cache_mode = AUTO

def SetCacheMode(mode):
    """Set the Configure cache mode. mode must be one of "auto", "force",
    or "cache"."""
    global cache_mode
    if mode == 'auto':
        cache_mode = AUTO
    elif mode == 'force':
        cache_mode = FORCE
    elif mode == 'cache':
        cache_mode = CACHE
    else:
        raise ValueError('SCons.SConf.SetCacheMode: Unknown mode ' + mode)


progress_display = SCons.Util.display

def SetProgressDisplay(display):
    """Set the progress display to use (called from SCons.Script)"""
    global progress_display
    progress_display = display


SConfFS = None
_ac_build_counter = 0
_ac_config_logs = {}
_ac_config_hs = {}
sconf_global = None

def _createConfigH(target, source, env):
    t = open(str(target[0]), 'w')
    defname = re.sub('[^A-Za-z0-9_]', '_', str(target[0]).upper())
    t.write('#ifndef %(DEFNAME)s_SEEN\n#define %(DEFNAME)s_SEEN\n\n' % {'DEFNAME': defname})
    t.write(source[0].get_contents())
    t.write('\n#endif /* %(DEFNAME)s_SEEN */\n' % {'DEFNAME': defname})
    t.close()


def _stringConfigH(target, source, env):
    return 'scons: Configure: creating ' + str(target[0])


def NeedConfigHBuilder():
    global _ac_config_hs
    if len(_ac_config_hs) == 0:
        return False
    else:
        return True


def CreateConfigHBuilder(env):
    """Called if necessary just before the building targets phase begins."""
    action = SCons.Action.Action(_createConfigH, _stringConfigH)
    sconfigHBld = SCons.Builder.Builder(action=action)
    env.Append(BUILDERS={'SConfigHBuilder': sconfigHBld})
    for k in _ac_config_hs.keys():
        env.SConfigHBuilder(k, env.Value(_ac_config_hs[k]))


class SConfWarning(SCons.Warnings.Warning):
    pass


SCons.Warnings.enableWarningClass(SConfWarning)

class SConfError(SCons.Errors.UserError):

    def __init__(self, msg):
        SCons.Errors.UserError.__init__(self, msg)


class ConfigureDryRunError(SConfError):
    """Raised when a file or directory needs to be updated during a Configure
    process, but the user requested a dry-run"""

    def __init__(self, target):
        if not isinstance(target, SCons.Node.FS.File):
            msg = 'Cannot create configure directory "%s" within a dry-run.' % str(target)
        else:
            msg = 'Cannot update configure test "%s" within a dry-run.' % str(target)
        SConfError.__init__(self, msg)


class ConfigureCacheError(SConfError):
    """Raised when a use explicitely requested the cache feature, but the test
    is run the first time."""

    def __init__(self, target):
        SConfError.__init__(self, '"%s" is not yet built and cache is forced.' % str(target))


def _createSource(target, source, env):
    fd = open(str(target[0]), 'w')
    fd.write(source[0].get_contents())
    fd.close()


def _stringSource(target, source, env):
    return str(target[0]) + ' <-\n  |' + source[0].get_contents().replace('\n', '\n  |')


class SConfBuildInfo(SCons.Node.FS.FileBuildInfo):
    """
    Special build info for targets of configure tests. Additional members
    are result (did the builder succeed last time?) and string, which
    contains messages of the original build phase.
    """
    __slots__ = ('result', 'string')

    def __init__(self):
        self.result = None
        self.string = None
        return

    def set_build_result(self, result, string):
        self.result = result
        self.string = string


class Streamer(object):
    """
    'Sniffer' for a file-like writable object. Similar to the unix tool tee.
    """

    def __init__(self, orig):
        self.orig = orig
        self.s = io.StringIO()

    def write(self, str):
        if self.orig:
            self.orig.write(str)
        try:
            self.s.write(str)
        except TypeError as e:
            self.s.write(str.decode())

    def writelines(self, lines):
        for l in lines:
            self.write(l + '\n')

    def getvalue(self):
        """
        Return everything written to orig since the Streamer was created.
        """
        return self.s.getvalue()

    def flush(self):
        if self.orig:
            self.orig.flush()
        self.s.flush()


class SConfBuildTask(SCons.Taskmaster.AlwaysTask):
    """
    This is almost the same as SCons.Script.BuildTask. Handles SConfErrors
    correctly and knows about the current cache_mode.
    """

    def display(self, message):
        global sconf_global
        if sconf_global.logstream:
            sconf_global.logstream.write('scons: Configure: ' + message + '\n')

    def display_cached_string(self, bi):
        """
        Logs the original builder messages, given the SConfBuildInfo instance
        bi.
        """
        if not isinstance(bi, SConfBuildInfo):
            SCons.Warnings.warn(SConfWarning, 'The stored build information has an unexpected class: %s' % bi.__class__)
        else:
            self.display('The original builder output was:\n' + ('  |' + str(bi.string)).replace('\n', '\n  |'))

    def failed(self):
        exc_type = self.exc_info()[0]
        if issubclass(exc_type, SConfError):
            raise
        elif issubclass(exc_type, SCons.Errors.BuildError):
            self.exc_clear()
        else:
            self.display('Caught exception while building "%s":\n' % self.targets[0])
            sys.excepthook(*self.exc_info())
        return SCons.Taskmaster.Task.failed(self)

    def collect_node_states(self):
        T = 0
        changed = False
        cached_error = False
        cachable = True
        for t in self.targets:
            if T:
                Trace('%s' % t)
            bi = t.get_stored_info().binfo
            if isinstance(bi, SConfBuildInfo):
                if T:
                    Trace(': SConfBuildInfo')
                if cache_mode == CACHE:
                    t.set_state(SCons.Node.up_to_date)
                    if T:
                        Trace(': set_state(up_to-date)')
                else:
                    if T:
                        Trace(': get_state() %s' % t.get_state())
                    if T:
                        Trace(': changed() %s' % t.changed())
                    if t.get_state() != SCons.Node.up_to_date and t.changed():
                        changed = True
                    if T:
                        Trace(': changed %s' % changed)
                cached_error = cached_error or bi.result
            else:
                if T:
                    Trace(': else')
                cachable = False
                changed = t.get_state() != SCons.Node.up_to_date
                if T:
                    Trace(': changed %s' % changed)

        if T:
            Trace('\n')
        return (
         not changed, cached_error, cachable)

    def execute(self):
        if not self.targets[0].has_builder():
            return
        sconf = sconf_global
        is_up_to_date, cached_error, cachable = self.collect_node_states()
        if cache_mode == CACHE and not cachable:
            raise ConfigureCacheError(self.targets[0])
        else:
            if cache_mode == FORCE:
                is_up_to_date = 0
            if cached_error and is_up_to_date:
                self.display('Building "%s" failed in a previous run and all its sources are up to date.' % str(self.targets[0]))
                binfo = self.targets[0].get_stored_info().binfo
                self.display_cached_string(binfo)
                raise SCons.Errors.BuildError
            elif is_up_to_date:
                self.display('"%s" is up to date.' % str(self.targets[0]))
                binfo = self.targets[0].get_stored_info().binfo
                self.display_cached_string(binfo)
            elif dryrun:
                raise ConfigureDryRunError(self.targets[0])
            else:
                s = sys.stdout = sys.stderr = Streamer(sys.stdout)
                try:
                    env = self.targets[0].get_build_env()
                    if cache_mode == FORCE:

                        def force_build(dependency, target, prev_ni, env_decider=env.decide_source):
                            env_decider(dependency, target, prev_ni)
                            return True

                        if env.decide_source.func_code is not force_build.func_code:
                            env.Decider(force_build)
                    env['PSTDOUT'] = env['PSTDERR'] = s
                    try:
                        sconf.cached = 0
                        self.targets[0].build()
                    finally:
                        sys.stdout = sys.stderr = env['PSTDOUT'] = env['PSTDERR'] = sconf.logstream

                except KeyboardInterrupt:
                    raise
                except SystemExit:
                    exc_value = sys.exc_info()[1]
                    raise SCons.Errors.ExplicitExit(self.targets[0], exc_value.code)
                except Exception as e:
                    for t in self.targets:
                        binfo = SConfBuildInfo()
                        binfo.merge(t.get_binfo())
                        binfo.set_build_result(1, s.getvalue())
                        sconsign_entry = SCons.SConsign.SConsignEntry()
                        sconsign_entry.binfo = binfo
                        sconsign = t.dir.sconsign()
                        sconsign.set_entry(t.name, sconsign_entry)
                        sconsign.merge()

                    raise e

                for t in self.targets:
                    binfo = SConfBuildInfo()
                    binfo.merge(t.get_binfo())
                    binfo.set_build_result(0, s.getvalue())
                    sconsign_entry = SCons.SConsign.SConsignEntry()
                    sconsign_entry.binfo = binfo
                    sconsign = t.dir.sconsign()
                    sconsign.set_entry(t.name, sconsign_entry)
                    sconsign.merge()


class SConfBase(object):
    """This is simply a class to represent a configure context. After
    creating a SConf object, you can call any tests. After finished with your
    tests, be sure to call the Finish() method, which returns the modified
    environment.
    Some words about caching: In most cases, it is not necessary to cache
    Test results explicitly. Instead, we use the scons dependency checking
    mechanism. For example, if one wants to compile a test program
    (SConf.TryLink), the compiler is only called, if the program dependencies
    have changed. However, if the program could not be compiled in a former
    SConf run, we need to explicitly cache this error.
    """

    def __init__(self, env, custom_tests={}, conf_dir='$CONFIGUREDIR', log_file='$CONFIGURELOG', config_h=None, _depth=0):
        """Constructor. Pass additional tests in the custom_tests-dictionary,
        e.g. custom_tests={'CheckPrivate':MyPrivateTest}, where MyPrivateTest
        defines a custom test.
        Note also the conf_dir and log_file arguments (you may want to
        build tests in the VariantDir, not in the SourceDir)
        """
        global SConfFS
        if not SConfFS:
            SConfFS = SCons.Node.FS.default_fs or SCons.Node.FS.FS(env.fs.pathTop)
        if sconf_global is not None:
            raise SCons.Errors.UserError
        self.env = env
        if log_file is not None:
            log_file = SConfFS.File(env.subst(log_file))
        self.logfile = log_file
        self.logstream = None
        self.lastTarget = None
        self.depth = _depth
        self.cached = 0
        default_tests = {'CheckCC': CheckCC, 
           'CheckCXX': CheckCXX, 
           'CheckSHCC': CheckSHCC, 
           'CheckSHCXX': CheckSHCXX, 
           'CheckFunc': CheckFunc, 
           'CheckType': CheckType, 
           'CheckTypeSize': CheckTypeSize, 
           'CheckDeclaration': CheckDeclaration, 
           'CheckHeader': CheckHeader, 
           'CheckCHeader': CheckCHeader, 
           'CheckCXXHeader': CheckCXXHeader, 
           'CheckLib': CheckLib, 
           'CheckLibWithHeader': CheckLibWithHeader, 
           'CheckProg': CheckProg}
        self.AddTests(default_tests)
        self.AddTests(custom_tests)
        self.confdir = SConfFS.Dir(env.subst(conf_dir))
        if config_h is not None:
            config_h = SConfFS.File(config_h)
        self.config_h = config_h
        self._startup()
        return

    def Finish(self):
        """Call this method after finished with your tests:
                env = sconf.Finish()
        """
        self._shutdown()
        return self.env

    def Define(self, name, value=None, comment=None):
        """
        Define a pre processor symbol name, with the optional given value in the
        current config header.

        If value is None (default), then #define name is written. If value is not
        none, then #define name value is written.
        
        comment is a string which will be put as a C comment in the
        header, to explain the meaning of the value (appropriate C comments /* and
        */ will be put automatically."""
        lines = []
        if comment:
            comment_str = '/* %s */' % comment
            lines.append(comment_str)
        if value is not None:
            define_str = '#define %s %s' % (name, value)
        else:
            define_str = '#define %s' % name
        lines.append(define_str)
        lines.append('')
        self.config_h_text = self.config_h_text + ('\n').join(lines)
        return

    def BuildNodes(self, nodes):
        """
        Tries to build the given nodes immediately. Returns 1 on success,
        0 on error.
        """
        if self.logstream is not None:
            oldStdout = sys.stdout
            sys.stdout = self.logstream
            oldStderr = sys.stderr
            sys.stderr = self.logstream
        old_fs_dir = SConfFS.getcwd()
        old_os_dir = os.getcwd()
        SConfFS.chdir(SConfFS.Top, change_os_dir=1)
        for n in nodes:
            n.store_info = 0
            if not hasattr(n, 'attributes'):
                n.attributes = SCons.Node.Node.Attrs()
            n.attributes.keep_targetinfo = 1

        ret = 1
        try:
            save_max_drift = SConfFS.get_max_drift()
            SConfFS.set_max_drift(0)
            tm = SCons.Taskmaster.Taskmaster(nodes, SConfBuildTask)
            jobs = SCons.Job.Jobs(1, tm)
            jobs.run()
            for n in nodes:
                state = n.get_state()
                if state != SCons.Node.executed and state != SCons.Node.up_to_date:
                    ret = 0

        finally:
            SConfFS.set_max_drift(save_max_drift)
            os.chdir(old_os_dir)
            SConfFS.chdir(old_fs_dir, change_os_dir=0)
            if self.logstream is not None:
                sys.stdout = oldStdout
                sys.stderr = oldStderr

        return ret

    def pspawn_wrapper(self, sh, escape, cmd, args, env):
        """Wrapper function for handling piped spawns.

        This looks to the calling interface (in Action.py) like a "normal"
        spawn, but associates the call with the PSPAWN variable from
        the construction environment and with the streams to which we
        want the output logged.  This gets slid into the construction
        environment as the SPAWN variable so Action.py doesn't have to
        know or care whether it's spawning a piped command or not.
        """
        return self.pspawn(sh, escape, cmd, args, env, self.logstream, self.logstream)

    def TryBuild(self, builder, text=None, extension=''):
        """Low level TryBuild implementation. Normally you don't need to
        call that - you can use TryCompile / TryLink / TryRun instead
        """
        global _ac_build_counter
        try:
            self.pspawn = self.env['PSPAWN']
        except KeyError:
            raise SCons.Errors.UserError('Missing PSPAWN construction variable.')

        try:
            save_spawn = self.env['SPAWN']
        except KeyError:
            raise SCons.Errors.UserError('Missing SPAWN construction variable.')

        nodesToBeBuilt = []
        f = 'conftest_' + str(_ac_build_counter)
        pref = self.env.subst(builder.builder.prefix)
        suff = self.env.subst(builder.builder.suffix)
        target = self.confdir.File(pref + f + suff)
        try:
            self.env['SPAWN'] = self.pspawn_wrapper
            sourcetext = self.env.Value(text)
            if text is not None:
                textFile = self.confdir.File(f + extension)
                textFileNode = self.env.SConfSourceBuilder(target=textFile, source=sourcetext)
                nodesToBeBuilt.extend(textFileNode)
                source = textFileNode
            else:
                source = None
            nodes = builder(target=target, source=source)
            if not SCons.Util.is_List(nodes):
                nodes = [
                 nodes]
            nodesToBeBuilt.extend(nodes)
            result = self.BuildNodes(nodesToBeBuilt)
        finally:
            self.env['SPAWN'] = save_spawn

        _ac_build_counter = _ac_build_counter + 1
        if result:
            self.lastTarget = nodes[0]
        else:
            self.lastTarget = None
        return result

    def TryAction(self, action, text=None, extension=''):
        """Tries to execute the given action with optional source file
        contents <text> and optional source file extension <extension>,
        Returns the status (0 : failed, 1 : ok) and the contents of the
        output file.
        """
        builder = SCons.Builder.Builder(action=action)
        self.env.Append(BUILDERS={'SConfActionBuilder': builder})
        ok = self.TryBuild(self.env.SConfActionBuilder, text, extension)
        del self.env['BUILDERS']['SConfActionBuilder']
        if ok:
            outputStr = self.lastTarget.get_contents()
            return (
             1, outputStr)
        return (0, '')

    def TryCompile(self, text, extension):
        """Compiles the program given in text to an env.Object, using extension
        as file extension (e.g. '.c'). Returns 1, if compilation was
        successful, 0 otherwise. The target is saved in self.lastTarget (for
        further processing).
        """
        return self.TryBuild(self.env.Object, text, extension)

    def TryLink(self, text, extension):
        """Compiles the program given in text to an executable env.Program,
        using extension as file extension (e.g. '.c'). Returns 1, if
        compilation was successful, 0 otherwise. The target is saved in
        self.lastTarget (for further processing).
        """
        return self.TryBuild(self.env.Program, text, extension)

    def TryRun(self, text, extension):
        """Compiles and runs the program given in text, using extension
        as file extension (e.g. '.c'). Returns (1, outputStr) on success,
        (0, '') otherwise. The target (a file containing the program's stdout)
        is saved in self.lastTarget (for further processing).
        """
        ok = self.TryLink(text, extension)
        if ok:
            prog = self.lastTarget
            pname = prog.get_internal_path()
            output = self.confdir.File(os.path.basename(pname) + '.out')
            node = self.env.Command(output, prog, [[pname, '>', '${TARGET}']])
            ok = self.BuildNodes(node)
            if ok:
                outputStr = output.get_contents()
                return (
                 1, outputStr)
        return (0, '')

    class TestWrapper(object):
        """A wrapper around Tests (to ensure sanity)"""

        def __init__(self, test, sconf):
            self.test = test
            self.sconf = sconf

        def __call__(self, *args, **kw):
            if not self.sconf.active:
                raise SCons.Errors.UserError
            context = CheckContext(self.sconf)
            ret = self.test(context, *args, **kw)
            if self.sconf.config_h is not None:
                self.sconf.config_h_text = self.sconf.config_h_text + context.config_h
            context.Result('error: no result')
            return ret

    def AddTest(self, test_name, test_instance):
        """Adds test_class to this SConf instance. It can be called with
        self.test_name(...)"""
        setattr(self, test_name, SConfBase.TestWrapper(test_instance, self))

    def AddTests(self, tests):
        """Adds all the tests given in the tests dictionary to this SConf
        instance
        """
        for name in tests.keys():
            self.AddTest(name, tests[name])

    def _createDir(self, node):
        dirName = str(node)
        if dryrun:
            if not os.path.isdir(dirName):
                raise ConfigureDryRunError(dirName)
        elif not os.path.isdir(dirName):
            os.makedirs(dirName)

    def _startup(self):
        """Private method. Set up logstream, and set the environment
        variables necessary for a piped build
        """
        global _ac_config_logs
        global sconf_global
        self.lastEnvFs = self.env.fs
        self.env.fs = SConfFS
        self._createDir(self.confdir)
        self.confdir.up().add_ignore([self.confdir])
        if self.logfile is not None and not dryrun:
            if self.logfile in _ac_config_logs:
                log_mode = 'a'
            else:
                _ac_config_logs[self.logfile] = None
                log_mode = 'w'
            fp = open(str(self.logfile), log_mode)
            self.logstream = SCons.Util.Unbuffered(fp)
            self.logfile.dir.add_ignore([self.logfile])
            tb = traceback.extract_stack()[(-3 - self.depth)]
            old_fs_dir = SConfFS.getcwd()
            SConfFS.chdir(SConfFS.Top, change_os_dir=0)
            self.logstream.write('file %s,line %d:\n\tConfigure(confdir = %s)\n' % (
             tb[0], tb[1], str(self.confdir)))
            SConfFS.chdir(old_fs_dir)
        else:
            self.logstream = None
        action = SCons.Action.Action(_createSource, _stringSource)
        sconfSrcBld = SCons.Builder.Builder(action=action)
        self.env.Append(BUILDERS={'SConfSourceBuilder': sconfSrcBld})
        self.config_h_text = _ac_config_hs.get(self.config_h, '')
        self.active = 1
        sconf_global = self
        return

    def _shutdown(self):
        """Private method. Reset to non-piped spawn"""
        global sconf_global
        if not self.active:
            raise SCons.Errors.UserError('Finish may be called only once!')
        if self.logstream is not None and not dryrun:
            self.logstream.write('\n')
            self.logstream.close()
            self.logstream = None
        blds = self.env['BUILDERS']
        del blds['SConfSourceBuilder']
        self.env.Replace(BUILDERS=blds)
        self.active = 0
        sconf_global = None
        if self.config_h is not None:
            _ac_config_hs[self.config_h] = self.config_h_text
        self.env.fs = self.lastEnvFs
        return


class CheckContext(object):
    """Provides a context for configure tests. Defines how a test writes to the
    screen and log file.

    A typical test is just a callable with an instance of CheckContext as
    first argument:

        def CheckCustom(context, ...):
            context.Message('Checking my weird test ... ')
            ret = myWeirdTestFunction(...)
            context.Result(ret)

    Often, myWeirdTestFunction will be one of
    context.TryCompile/context.TryLink/context.TryRun. The results of
    those are cached, for they are only rebuild, if the dependencies have
    changed.
    """

    def __init__(self, sconf):
        """Constructor. Pass the corresponding SConf instance."""
        self.sconf = sconf
        self.did_show_result = 0
        self.vardict = {}
        self.havedict = {}
        self.headerfilename = None
        self.config_h = ''
        return

    def Message(self, text):
        """Inform about what we are doing right now, e.g.
        'Checking for SOMETHING ... '
        """
        self.Display(text)
        self.sconf.cached = 1
        self.did_show_result = 0

    def Result(self, res):
        """Inform about the result of the test. If res is not a string, displays
        'yes' or 'no' depending on whether res is evaluated as true or false.
        The result is only displayed when self.did_show_result is not set.
        """
        if isinstance(res, str):
            text = res
        elif res:
            text = 'yes'
        else:
            text = 'no'
        if self.did_show_result == 0:
            self.Display(text + '\n')
            self.did_show_result = 1

    def TryBuild(self, *args, **kw):
        return self.sconf.TryBuild(*args, **kw)

    def TryAction(self, *args, **kw):
        return self.sconf.TryAction(*args, **kw)

    def TryCompile(self, *args, **kw):
        return self.sconf.TryCompile(*args, **kw)

    def TryLink(self, *args, **kw):
        return self.sconf.TryLink(*args, **kw)

    def TryRun(self, *args, **kw):
        return self.sconf.TryRun(*args, **kw)

    def __getattr__(self, attr):
        if attr == 'env':
            return self.sconf.env
        if attr == 'lastTarget':
            return self.sconf.lastTarget
        raise AttributeError("CheckContext instance has no attribute '%s'" % attr)

    def BuildProg(self, text, ext):
        self.sconf.cached = 1
        return not self.TryBuild(self.env.Program, text, ext)

    def CompileProg(self, text, ext):
        self.sconf.cached = 1
        return not self.TryBuild(self.env.Object, text, ext)

    def CompileSharedObject(self, text, ext):
        self.sconf.cached = 1
        return not self.TryBuild(self.env.SharedObject, text, ext)

    def RunProg(self, text, ext):
        self.sconf.cached = 1
        st, out = self.TryRun(text, ext)
        return (not st, out)

    def AppendLIBS(self, lib_name_list):
        oldLIBS = self.env.get('LIBS', [])
        self.env.Append(LIBS=lib_name_list)
        return oldLIBS

    def PrependLIBS(self, lib_name_list):
        oldLIBS = self.env.get('LIBS', [])
        self.env.Prepend(LIBS=lib_name_list)
        return oldLIBS

    def SetLIBS(self, val):
        oldLIBS = self.env.get('LIBS', [])
        self.env.Replace(LIBS=val)
        return oldLIBS

    def Display(self, msg):
        if self.sconf.cached:
            msg = '(cached) ' + msg
            self.sconf.cached = 0
        progress_display(msg, append_newline=0)
        self.Log('scons: Configure: ' + msg + '\n')

    def Log(self, msg):
        if self.sconf.logstream is not None:
            self.sconf.logstream.write(msg)
        return


def SConf(*args, **kw):
    if kw.get(build_type, True):
        kw['_depth'] = kw.get('_depth', 0) + 1
        for bt in build_types:
            try:
                del kw[bt]
            except KeyError:
                pass

        return SConfBase(*args, **kw)
    else:
        return SCons.Util.Null()


def CheckFunc(context, function_name, header=None, language=None):
    res = SCons.Conftest.CheckFunc(context, function_name, header=header, language=language)
    context.did_show_result = 1
    return not res


def CheckType(context, type_name, includes='', language=None):
    res = SCons.Conftest.CheckType(context, type_name, header=includes, language=language)
    context.did_show_result = 1
    return not res


def CheckTypeSize(context, type_name, includes='', language=None, expect=None):
    res = SCons.Conftest.CheckTypeSize(context, type_name, header=includes, language=language, expect=expect)
    context.did_show_result = 1
    return res


def CheckDeclaration(context, declaration, includes='', language=None):
    res = SCons.Conftest.CheckDeclaration(context, declaration, includes=includes, language=language)
    context.did_show_result = 1
    return not res


def createIncludesFromHeaders(headers, leaveLast, include_quotes='""'):
    if not SCons.Util.is_List(headers):
        headers = [
         headers]
    l = []
    if leaveLast:
        lastHeader = headers[(-1)]
        headers = headers[:-1]
    else:
        lastHeader = None
    for s in headers:
        l.append('#include %s%s%s\n' % (
         include_quotes[0], s, include_quotes[1]))

    return (
     ('').join(l), lastHeader)


def CheckHeader(context, header, include_quotes='<>', language=None):
    """
    A test for a C or C++ header file.
    """
    prog_prefix, hdr_to_check = createIncludesFromHeaders(header, 1, include_quotes)
    res = SCons.Conftest.CheckHeader(context, hdr_to_check, prog_prefix, language=language, include_quotes=include_quotes)
    context.did_show_result = 1
    return not res


def CheckCC(context):
    res = SCons.Conftest.CheckCC(context)
    context.did_show_result = 1
    return not res


def CheckCXX(context):
    res = SCons.Conftest.CheckCXX(context)
    context.did_show_result = 1
    return not res


def CheckSHCC(context):
    res = SCons.Conftest.CheckSHCC(context)
    context.did_show_result = 1
    return not res


def CheckSHCXX(context):
    res = SCons.Conftest.CheckSHCXX(context)
    context.did_show_result = 1
    return not res


def CheckCHeader(context, header, include_quotes='""'):
    """
    A test for a C header file.
    """
    return CheckHeader(context, header, include_quotes, language='C')


def CheckCXXHeader(context, header, include_quotes='""'):
    """
    A test for a C++ header file.
    """
    return CheckHeader(context, header, include_quotes, language='C++')


def CheckLib(context, library=None, symbol='main', header=None, language=None, autoadd=1):
    """
    A test for a library. See also CheckLibWithHeader.
    Note that library may also be None to test whether the given symbol
    compiles without flags.
    """
    if library == []:
        library = [
         None]
    if not SCons.Util.is_List(library):
        library = [
         library]
    res = SCons.Conftest.CheckLib(context, library, symbol, header=header, language=language, autoadd=autoadd)
    context.did_show_result = 1
    return not res


def CheckLibWithHeader(context, libs, header, language, call=None, autoadd=1):
    """
    Another (more sophisticated) test for a library.
    Checks, if library and header is available for language (may be 'C'
    or 'CXX'). Call maybe be a valid expression _with_ a trailing ';'.
    As in CheckLib, we support library=None, to test if the call compiles
    without extra link flags.
    """
    prog_prefix, dummy = createIncludesFromHeaders(header, 0)
    if libs == []:
        libs = [
         None]
    if not SCons.Util.is_List(libs):
        libs = [
         libs]
    res = SCons.Conftest.CheckLib(context, libs, None, prog_prefix, call=call, language=language, autoadd=autoadd)
    context.did_show_result = 1
    return not res


def CheckProg(context, prog_name):
    """Simple check if a program exists in the path.  Returns the path
    for the application, or None if not found.
    """
    res = SCons.Conftest.CheckProg(context, prog_name)
    context.did_show_result = 1
    return res