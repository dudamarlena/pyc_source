# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\derek_2\Google Drive\nvda-addon-exploded\notepad++\scons-local-2.5.0\SCons\Environment.py
# Compiled at: 2016-07-07 03:21:32
"""SCons.Environment

Base class for construction Environments.  These are
the primary objects used to communicate dependency and
construction information to the build engine.

Keyword arguments supplied when the construction Environment
is created are construction variables used to initialize the
Environment
"""
__revision__ = 'src/engine/SCons/Environment.py rel_2.5.0:3543:937e55cd78f7 2016/04/09 11:29:54 bdbaddog'
import copy, os, sys, re, shlex
from collections import UserDict
import SCons.Action, SCons.Builder, SCons.Debug
from SCons.Debug import logInstanceCreation
import SCons.Defaults, SCons.Errors, SCons.Memoize, SCons.Node, SCons.Node.Alias, SCons.Node.FS, SCons.Node.Python, SCons.Platform, SCons.SConf, SCons.SConsign, SCons.Subst, SCons.Tool, SCons.Util, SCons.Warnings

class _Null(object):
    pass


_null = _Null
_warn_copy_deprecated = True
_warn_source_signatures_deprecated = True
_warn_target_signatures_deprecated = True
CleanTargets = {}
CalculatorArgs = {}
semi_deepcopy = SCons.Util.semi_deepcopy
semi_deepcopy_dict = SCons.Util.semi_deepcopy_dict
UserError = SCons.Errors.UserError

def alias_builder(env, target, source):
    pass


AliasBuilder = SCons.Builder.Builder(action=alias_builder, target_factory=SCons.Node.Alias.default_ans.Alias, source_factory=SCons.Node.FS.Entry, multi=1, is_explicit=None, name='AliasBuilder')

def apply_tools(env, tools, toolpath):
    if toolpath is not None:
        env['toolpath'] = toolpath
    if not tools:
        return
    else:
        for tool in [ _f for _f in tools if _f ]:
            if SCons.Util.is_List(tool) or isinstance(tool, tuple):
                toolname = tool[0]
                toolargs = tool[1]
                tool = env.Tool(toolname, **toolargs)
            else:
                env.Tool(tool)

        return


reserved_construction_var_names = [
 'CHANGED_SOURCES',
 'CHANGED_TARGETS',
 'SOURCE',
 'SOURCES',
 'TARGET',
 'TARGETS',
 'UNCHANGED_SOURCES',
 'UNCHANGED_TARGETS']
future_reserved_construction_var_names = []

def copy_non_reserved_keywords(dict):
    result = semi_deepcopy(dict)
    for k in result.keys():
        if k in reserved_construction_var_names:
            msg = "Ignoring attempt to set reserved variable `$%s'"
            SCons.Warnings.warn(SCons.Warnings.ReservedVariableWarning, msg % k)
            del result[k]

    return result


def _set_reserved(env, key, value):
    msg = "Ignoring attempt to set reserved variable `$%s'"
    SCons.Warnings.warn(SCons.Warnings.ReservedVariableWarning, msg % key)


def _set_future_reserved(env, key, value):
    env._dict[key] = value
    msg = "`$%s' will be reserved in a future release and setting it will become ignored"
    SCons.Warnings.warn(SCons.Warnings.FutureReservedVariableWarning, msg % key)


def _set_BUILDERS(env, key, value):
    try:
        bd = env._dict[key]
        for k in bd.keys():
            del bd[k]

    except KeyError:
        bd = BuilderDict(kwbd, env)
        env._dict[key] = bd

    for k, v in value.items():
        if not SCons.Builder.is_a_Builder(v):
            raise SCons.Errors.UserError('%s is not a Builder.' % repr(v))

    bd.update(value)


def _del_SCANNERS(env, key):
    del env._dict[key]
    env.scanner_map_delete()


def _set_SCANNERS(env, key, value):
    env._dict[key] = value
    env.scanner_map_delete()


def _delete_duplicates(l, keep_last):
    """Delete duplicates from a sequence, keeping the first or last."""
    seen = {}
    result = []
    if keep_last:
        l.reverse()
    for i in l:
        try:
            if i not in seen:
                result.append(i)
                seen[i] = 1
        except TypeError:
            result.append(i)

    if keep_last:
        result.reverse()
    return result


class MethodWrapper(object):
    """
    A generic Wrapper class that associates a method (which can
    actually be any callable) with an object.  As part of creating this
    MethodWrapper object an attribute with the specified (by default,
    the name of the supplied method) is added to the underlying object.
    When that new "method" is called, our __call__() method adds the
    object as the first argument, simulating the Python behavior of
    supplying "self" on method calls.

    We hang on to the name by which the method was added to the underlying
    base class so that we can provide a method to "clone" ourselves onto
    a new underlying object being copied (without which we wouldn't need
    to save that info).
    """

    def __init__(self, object, method, name=None):
        if name is None:
            name = method.__name__
        self.object = object
        self.method = method
        self.name = name
        setattr(self.object, name, self)
        return

    def __call__(self, *args, **kwargs):
        nargs = (self.object,) + args
        return self.method(*nargs, **kwargs)

    def clone(self, new_object):
        """
        Returns an object that re-binds the underlying "method" to
        the specified new object.
        """
        return self.__class__(new_object, self.method, self.name)


class BuilderWrapper(MethodWrapper):
    """
    A MethodWrapper subclass that that associates an environment with
    a Builder.

    This mainly exists to wrap the __call__() function so that all calls
    to Builders can have their argument lists massaged in the same way
    (treat a lone argument as the source, treat two arguments as target
    then source, make sure both target and source are lists) without
    having to have cut-and-paste code to do it.

    As a bit of obsessive backwards compatibility, we also intercept
    attempts to get or set the "env" or "builder" attributes, which were
    the names we used before we put the common functionality into the
    MethodWrapper base class.  We'll keep this around for a while in case
    people shipped Tool modules that reached into the wrapper (like the
    Tool/qt.py module does, or did).  There shouldn't be a lot attribute
    fetching or setting on these, so a little extra work shouldn't hurt.
    """

    def __call__(self, target=None, source=_null, *args, **kw):
        if source is _null:
            source = target
            target = None
        if target is not None and not SCons.Util.is_List(target):
            target = [
             target]
        if source is not None and not SCons.Util.is_List(source):
            source = [
             source]
        return MethodWrapper.__call__(self, target, source, *args, **kw)

    def __repr__(self):
        return '<BuilderWrapper %s>' % repr(self.name)

    def __str__(self):
        return self.__repr__()

    def __getattr__(self, name):
        if name == 'env':
            return self.object
        if name == 'builder':
            return self.method
        raise AttributeError(name)

    def __setattr__(self, name, value):
        if name == 'env':
            self.object = value
        elif name == 'builder':
            self.method = value
        else:
            self.__dict__[name] = value


class BuilderDict(UserDict):
    """This is a dictionary-like class used by an Environment to hold
    the Builders.  We need to do this because every time someone changes
    the Builders in the Environment's BUILDERS dictionary, we must
    update the Environment's attributes."""

    def __init__(self, dict, env):
        self.env = env
        UserDict.__init__(self, dict)

    def __semi_deepcopy__(self):
        raise TypeError('cannot semi_deepcopy a BuilderDict')

    def __setitem__(self, item, val):
        try:
            method = getattr(self.env, item).method
        except AttributeError:
            pass
        else:
            self.env.RemoveMethod(method)

        UserDict.__setitem__(self, item, val)
        BuilderWrapper(self.env, val, item)

    def __delitem__(self, item):
        UserDict.__delitem__(self, item)
        delattr(self.env, item)

    def update(self, dict):
        for i, v in dict.items():
            self.__setitem__(i, v)


_is_valid_var = re.compile('[_a-zA-Z]\\w*$')

def is_valid_construction_var(varstr):
    """Return if the specified string is a legitimate construction
    variable.
    """
    return _is_valid_var.match(varstr)


class SubstitutionEnvironment(object):
    """Base class for different flavors of construction environments.

    This class contains a minimal set of methods that handle contruction
    variable expansion and conversion of strings to Nodes, which may or
    may not be actually useful as a stand-alone class.  Which methods
    ended up in this class is pretty arbitrary right now.  They're
    basically the ones which we've empirically determined are common to
    the different construction environment subclasses, and most of the
    others that use or touch the underlying dictionary of construction
    variables.

    Eventually, this class should contain all the methods that we
    determine are necessary for a "minimal" interface to the build engine.
    A full "native Python" SCons environment has gotten pretty heavyweight
    with all of the methods and Tools and construction variables we've
    jammed in there, so it would be nice to have a lighter weight
    alternative for interfaces that don't need all of the bells and
    whistles.  (At some point, we'll also probably rename this class
    "Base," since that more reflects what we want this class to become,
    but because we've released comments that tell people to subclass
    Environment.Base to create their own flavors of construction
    environment, we'll save that for a future refactoring when this
    class actually becomes useful.)
    """

    def __init__(self, **kw):
        """Initialization of an underlying SubstitutionEnvironment class.
        """
        if SCons.Debug.track_instances:
            logInstanceCreation(self, 'Environment.SubstitutionEnvironment')
        self.fs = SCons.Node.FS.get_default_fs()
        self.ans = SCons.Node.Alias.default_ans
        self.lookup_list = SCons.Node.arg2nodes_lookups
        self._dict = kw.copy()
        self._init_special()
        self.added_methods = []

    def _init_special(self):
        """Initial the dispatch tables for special handling of
        special construction variables."""
        self._special_del = {}
        self._special_del['SCANNERS'] = _del_SCANNERS
        self._special_set = {}
        for key in reserved_construction_var_names:
            self._special_set[key] = _set_reserved

        for key in future_reserved_construction_var_names:
            self._special_set[key] = _set_future_reserved

        self._special_set['BUILDERS'] = _set_BUILDERS
        self._special_set['SCANNERS'] = _set_SCANNERS
        self._special_set_keys = list(self._special_set.keys())

    def __cmp__(self, other):
        return cmp(self._dict, other._dict)

    def __delitem__(self, key):
        special = self._special_del.get(key)
        if special:
            special(self, key)
        else:
            del self._dict[key]

    def __getitem__(self, key):
        return self._dict[key]

    def __setitem__(self, key, value):
        if key in self._special_set_keys:
            self._special_set[key](self, key, value)
        else:
            if key not in self._dict and not _is_valid_var.match(key):
                raise SCons.Errors.UserError("Illegal construction variable `%s'" % key)
            self._dict[key] = value

    def get(self, key, default=None):
        """Emulates the get() method of dictionaries."""
        return self._dict.get(key, default)

    def has_key(self, key):
        return key in self._dict

    def __contains__(self, key):
        return self._dict.__contains__(key)

    def items(self):
        return list(self._dict.items())

    def arg2nodes(self, args, node_factory=_null, lookup_list=_null, **kw):
        if node_factory is _null:
            node_factory = self.fs.File
        if lookup_list is _null:
            lookup_list = self.lookup_list
        if not args:
            return []
        else:
            args = SCons.Util.flatten(args)
            nodes = []
            for v in args:
                if SCons.Util.is_String(v):
                    n = None
                    for l in lookup_list:
                        n = l(v)
                        if n is not None:
                            break

                    if n is not None:
                        if SCons.Util.is_String(n):
                            kw['raw'] = 1
                            n = self.subst(n, **kw)
                            if node_factory:
                                n = node_factory(n)
                        if SCons.Util.is_List(n):
                            nodes.extend(n)
                        else:
                            nodes.append(n)
                    elif node_factory:
                        kw['raw'] = 1
                        v = node_factory(self.subst(v, **kw))
                        if SCons.Util.is_List(v):
                            nodes.extend(v)
                        else:
                            nodes.append(v)
                else:
                    nodes.append(v)

            return nodes

    def gvars(self):
        return self._dict

    def lvars(self):
        return {}

    def subst(self, string, raw=0, target=None, source=None, conv=None, executor=None):
        """Recursively interpolates construction variables from the
        Environment into the specified string, returning the expanded
        result.  Construction variables are specified by a $ prefix
        in the string and begin with an initial underscore or
        alphabetic character followed by any number of underscores
        or alphanumeric characters.  The construction variable names
        may be surrounded by curly braces to separate the name from
        trailing characters.
        """
        gvars = self.gvars()
        lvars = self.lvars()
        lvars['__env__'] = self
        if executor:
            lvars.update(executor.get_lvars())
        return SCons.Subst.scons_subst(string, self, raw, target, source, gvars, lvars, conv)

    def subst_kw(self, kw, raw=0, target=None, source=None):
        nkw = {}
        for k, v in kw.items():
            k = self.subst(k, raw, target, source)
            if SCons.Util.is_String(v):
                v = self.subst(v, raw, target, source)
            nkw[k] = v

        return nkw

    def subst_list(self, string, raw=0, target=None, source=None, conv=None, executor=None):
        """Calls through to SCons.Subst.scons_subst_list().  See
        the documentation for that function."""
        gvars = self.gvars()
        lvars = self.lvars()
        lvars['__env__'] = self
        if executor:
            lvars.update(executor.get_lvars())
        return SCons.Subst.scons_subst_list(string, self, raw, target, source, gvars, lvars, conv)

    def subst_path(self, path, target=None, source=None):
        """Substitute a path list, turning EntryProxies into Nodes
        and leaving Nodes (and other objects) as-is."""
        if not SCons.Util.is_List(path):
            path = [
             path]

        def s(obj):
            """This is the "string conversion" routine that we have our
            substitutions use to return Nodes, not strings.  This relies
            on the fact that an EntryProxy object has a get() method that
            returns the underlying Node that it wraps, which is a bit of
            architectural dependence that we might need to break or modify
            in the future in response to additional requirements."""
            try:
                get = obj.get
            except AttributeError:
                obj = SCons.Util.to_String_for_subst(obj)
            else:
                obj = get()

            return obj

        r = []
        for p in path:
            if SCons.Util.is_String(p):
                p = self.subst(p, target=target, source=source, conv=s)
                if SCons.Util.is_List(p):
                    if len(p) == 1:
                        p = p[0]
                    else:
                        p = ('').join(map(SCons.Util.to_String_for_subst, p))
            else:
                p = s(p)
            r.append(p)

        return r

    subst_target_source = subst

    def backtick(self, command):
        import subprocess
        kw = {'stdin': 'devnull', 'stdout': subprocess.PIPE, 
           'stderr': subprocess.PIPE, 
           'universal_newlines': True}
        if not SCons.Util.is_List(command):
            kw['shell'] = True
        p = SCons.Action._subproc(self, command, **kw)
        out, err = p.communicate()
        status = p.wait()
        if err:
            sys.stderr.write(unicode(err))
        if status:
            raise OSError("'%s' exited %d" % (command, status))
        return out

    def AddMethod(self, function, name=None):
        """
        Adds the specified function as a method of this construction
        environment with the specified name.  If the name is omitted,
        the default name is the name of the function itself.
        """
        method = MethodWrapper(self, function, name)
        self.added_methods.append(method)

    def RemoveMethod(self, function):
        """
        Removes the specified function's MethodWrapper from the
        added_methods list, so we don't re-bind it when making a clone.
        """
        self.added_methods = [ dm for dm in self.added_methods if dm.method is not function ]

    def Override(self, overrides):
        """
        Produce a modified environment whose variables are overridden by
        the overrides dictionaries.  "overrides" is a dictionary that
        will override the variables of this environment.

        This function is much more efficient than Clone() or creating
        a new Environment because it doesn't copy the construction
        environment dictionary, it just wraps the underlying construction
        environment, and doesn't even create a wrapper object if there
        are no overrides.
        """
        if not overrides:
            return self
        else:
            o = copy_non_reserved_keywords(overrides)
            if not o:
                return self
            overrides = {}
            merges = None
            for key, value in o.items():
                if key == 'parse_flags':
                    merges = value
                else:
                    overrides[key] = SCons.Subst.scons_subst_once(value, self, key)

            env = OverrideEnvironment(self, overrides)
            if merges:
                env.MergeFlags(merges)
            return env

    def ParseFlags(self, *flags):
        """
        Parse the set of flags and return a dict with the flags placed
        in the appropriate entry.  The flags are treated as a typical
        set of command-line flags for a GNU-like toolchain and used to
        populate the entries in the dict immediately below.  If one of
        the flag strings begins with a bang (exclamation mark), it is
        assumed to be a command and the rest of the string is executed;
        the result of that evaluation is then added to the dict.
        """
        dict = {'ASFLAGS': SCons.Util.CLVar(''), 
           'CFLAGS': SCons.Util.CLVar(''), 
           'CCFLAGS': SCons.Util.CLVar(''), 
           'CXXFLAGS': SCons.Util.CLVar(''), 
           'CPPDEFINES': [], 'CPPFLAGS': SCons.Util.CLVar(''), 
           'CPPPATH': [], 'FRAMEWORKPATH': SCons.Util.CLVar(''), 
           'FRAMEWORKS': SCons.Util.CLVar(''), 
           'LIBPATH': [], 'LIBS': [], 'LINKFLAGS': SCons.Util.CLVar(''), 
           'RPATH': []}

        def do_parse(arg):
            if not arg:
                return
            else:
                if not SCons.Util.is_String(arg):
                    for t in arg:
                        do_parse(t)

                    return
                if arg[0] == '!':
                    arg = self.backtick(arg[1:])

                def append_define(name, dict=dict):
                    t = name.split('=')
                    if len(t) == 1:
                        dict['CPPDEFINES'].append(name)
                    else:
                        dict['CPPDEFINES'].append([t[0], ('=').join(t[1:])])

                params = shlex.split(arg)
                append_next_arg_to = None
                for arg in params:
                    if append_next_arg_to:
                        if append_next_arg_to == 'CPPDEFINES':
                            append_define(arg)
                        elif append_next_arg_to == '-include':
                            t = (
                             '-include', self.fs.File(arg))
                            dict['CCFLAGS'].append(t)
                        elif append_next_arg_to == '-isysroot':
                            t = (
                             '-isysroot', arg)
                            dict['CCFLAGS'].append(t)
                            dict['LINKFLAGS'].append(t)
                        elif append_next_arg_to == '-isystem':
                            t = (
                             '-isystem', arg)
                            dict['CCFLAGS'].append(t)
                        elif append_next_arg_to == '-arch':
                            t = (
                             '-arch', arg)
                            dict['CCFLAGS'].append(t)
                            dict['LINKFLAGS'].append(t)
                        else:
                            dict[append_next_arg_to].append(arg)
                        append_next_arg_to = None
                    elif arg[0] not in ('-', '+'):
                        dict['LIBS'].append(self.fs.File(arg))
                    elif arg == '-dylib_file':
                        dict['LINKFLAGS'].append(arg)
                        append_next_arg_to = 'LINKFLAGS'
                    elif arg[:2] == '-L':
                        if arg[2:]:
                            dict['LIBPATH'].append(arg[2:])
                        else:
                            append_next_arg_to = 'LIBPATH'
                    elif arg[:2] == '-l':
                        if arg[2:]:
                            dict['LIBS'].append(arg[2:])
                        else:
                            append_next_arg_to = 'LIBS'
                    elif arg[:2] == '-I':
                        if arg[2:]:
                            dict['CPPPATH'].append(arg[2:])
                        else:
                            append_next_arg_to = 'CPPPATH'
                    elif arg[:4] == '-Wa,':
                        dict['ASFLAGS'].append(arg[4:])
                        dict['CCFLAGS'].append(arg)
                    elif arg[:4] == '-Wl,':
                        if arg[:11] == '-Wl,-rpath=':
                            dict['RPATH'].append(arg[11:])
                        elif arg[:7] == '-Wl,-R,':
                            dict['RPATH'].append(arg[7:])
                        elif arg[:6] == '-Wl,-R':
                            dict['RPATH'].append(arg[6:])
                        else:
                            dict['LINKFLAGS'].append(arg)
                    elif arg[:4] == '-Wp,':
                        dict['CPPFLAGS'].append(arg)
                    elif arg[:2] == '-D':
                        if arg[2:]:
                            append_define(arg[2:])
                        else:
                            append_next_arg_to = 'CPPDEFINES'
                    elif arg == '-framework':
                        append_next_arg_to = 'FRAMEWORKS'
                    elif arg[:14] == '-frameworkdir=':
                        dict['FRAMEWORKPATH'].append(arg[14:])
                    elif arg[:2] == '-F':
                        if arg[2:]:
                            dict['FRAMEWORKPATH'].append(arg[2:])
                        else:
                            append_next_arg_to = 'FRAMEWORKPATH'
                    elif arg in ('-mno-cygwin', '-pthread', '-openmp', '-fopenmp'):
                        dict['CCFLAGS'].append(arg)
                        dict['LINKFLAGS'].append(arg)
                    elif arg == '-mwindows':
                        dict['LINKFLAGS'].append(arg)
                    elif arg[:5] == '-std=':
                        if arg[5:].find('++') != -1:
                            key = 'CXXFLAGS'
                        else:
                            key = 'CFLAGS'
                        dict[key].append(arg)
                    elif arg[0] == '+':
                        dict['CCFLAGS'].append(arg)
                        dict['LINKFLAGS'].append(arg)
                    elif arg in ('-include', '-isysroot', '-isystem', '-arch'):
                        append_next_arg_to = arg
                    else:
                        dict['CCFLAGS'].append(arg)

                return

        for arg in flags:
            do_parse(arg)

        return dict

    def MergeFlags(self, args, unique=1, dict=None):
        """
        Merge the dict in args into the construction variables of this
        env, or the passed-in dict.  If args is not a dict, it is
        converted into a dict using ParseFlags.  If unique is not set,
        the flags are appended rather than merged.
        """
        if dict is None:
            dict = self
        if not SCons.Util.is_Dict(args):
            args = self.ParseFlags(args)
        if not unique:
            self.Append(**args)
            return self
        else:
            for key, value in args.items():
                if not value:
                    continue
                try:
                    orig = self[key]
                except KeyError:
                    orig = value
                else:
                    if not orig:
                        orig = value
                    else:
                        if value:
                            try:
                                orig = orig + value
                            except (KeyError, TypeError):
                                try:
                                    add_to_orig = orig.append
                                except AttributeError:
                                    value.insert(0, orig)
                                    orig = value
                                else:
                                    add_to_orig(value)

                        t = []
                        if key[-4:] == 'PATH':
                            for v in orig:
                                if v not in t:
                                    t.append(v)

                        else:
                            orig.reverse()
                            for v in orig:
                                if v not in t:
                                    t.insert(0, v)

                    self[key] = t

            return self


def default_decide_source(dependency, target, prev_ni):
    f = SCons.Defaults.DefaultEnvironment().decide_source
    return f(dependency, target, prev_ni)


def default_decide_target(dependency, target, prev_ni):
    f = SCons.Defaults.DefaultEnvironment().decide_target
    return f(dependency, target, prev_ni)


def default_copy_from_cache(src, dst):
    f = SCons.Defaults.DefaultEnvironment().copy_from_cache
    return f(src, dst)


class Base(SubstitutionEnvironment):
    """Base class for "real" construction Environments.  These are the
    primary objects used to communicate dependency and construction
    information to the build engine.

    Keyword arguments supplied when the construction Environment
    is created are construction variables used to initialize the
    Environment.
    """

    def __init__(self, platform=None, tools=None, toolpath=None, variables=None, parse_flags=None, **kw):
        """
        Initialization of a basic SCons construction environment,
        including setting up special construction variables like BUILDER,
        PLATFORM, etc., and searching for and applying available Tools.

        Note that we do *not* call the underlying base class
        (SubsitutionEnvironment) initialization, because we need to
        initialize things in a very specific order that doesn't work
        with the much simpler base class initialization.
        """
        if SCons.Debug.track_instances:
            logInstanceCreation(self, 'Environment.Base')
        self._memo = {}
        self.fs = SCons.Node.FS.get_default_fs()
        self.ans = SCons.Node.Alias.default_ans
        self.lookup_list = SCons.Node.arg2nodes_lookups
        self._dict = semi_deepcopy(SCons.Defaults.ConstructionEnvironment)
        self._init_special()
        self.added_methods = []
        self.decide_target = default_decide_target
        self.decide_source = default_decide_source
        self.copy_from_cache = default_copy_from_cache
        self._dict['BUILDERS'] = BuilderDict(self._dict['BUILDERS'], self)
        if platform is None:
            platform = self._dict.get('PLATFORM', None)
            if platform is None:
                platform = SCons.Platform.Platform()
        if SCons.Util.is_String(platform):
            platform = SCons.Platform.Platform(platform)
        self._dict['PLATFORM'] = str(platform)
        platform(self)
        self._dict['HOST_OS'] = self._dict.get('HOST_OS', None)
        self._dict['HOST_ARCH'] = self._dict.get('HOST_ARCH', None)
        self._dict['TARGET_OS'] = self._dict.get('TARGET_OS', None)
        self._dict['TARGET_ARCH'] = self._dict.get('TARGET_ARCH', None)
        if 'options' in kw:
            variables = kw['options']
            del kw['options']
        self.Replace(**kw)
        keys = list(kw.keys())
        if variables:
            keys = keys + list(variables.keys())
            variables.Update(self)
        save = {}
        for k in keys:
            try:
                save[k] = self._dict[k]
            except KeyError:
                pass

        SCons.Tool.Initializers(self)
        if tools is None:
            tools = self._dict.get('TOOLS', None)
            if tools is None:
                tools = [
                 'default']
        apply_tools(self, tools, toolpath)
        for key, val in save.items():
            self._dict[key] = val

        if parse_flags:
            self.MergeFlags(parse_flags)
        return

    def get_builder(self, name):
        """Fetch the builder with the specified name from the environment.
        """
        try:
            return self._dict['BUILDERS'][name]
        except KeyError:
            return

        return

    def get_CacheDir(self):
        try:
            path = self._CacheDir_path
        except AttributeError:
            path = SCons.Defaults.DefaultEnvironment()._CacheDir_path

        try:
            if path == self._last_CacheDir_path:
                return self._last_CacheDir
        except AttributeError:
            pass

        cd = SCons.CacheDir.CacheDir(path)
        self._last_CacheDir_path = path
        self._last_CacheDir = cd
        return cd

    def get_factory(self, factory, default='File'):
        """Return a factory function for creating Nodes for this
        construction environment.
        """
        name = default
        try:
            is_node = issubclass(factory, SCons.Node.FS.Base)
        except TypeError:
            pass

        if is_node:
            try:
                name = factory.__name__
            except AttributeError:
                pass
            else:
                factory = None

        if not factory:
            factory = getattr(self.fs, name)
        return factory

    @SCons.Memoize.CountMethodCall
    def _gsm(self):
        try:
            return self._memo['_gsm']
        except KeyError:
            pass

        result = {}
        try:
            scanners = self._dict['SCANNERS']
        except KeyError:
            pass

        if not SCons.Util.is_List(scanners):
            scanners = [
             scanners]
        else:
            scanners = scanners[:]
        scanners.reverse()
        for scanner in scanners:
            for k in scanner.get_skeys(self):
                if k and self['PLATFORM'] == 'win32':
                    k = k.lower()
                result[k] = scanner

        self._memo['_gsm'] = result
        return result

    def get_scanner(self, skey):
        """Find the appropriate scanner given a key (usually a file suffix).
        """
        if skey and self['PLATFORM'] == 'win32':
            skey = skey.lower()
        return self._gsm().get(skey)

    def scanner_map_delete(self, kw=None):
        """Delete the cached scanner map (if we need to).
        """
        try:
            del self._memo['_gsm']
        except KeyError:
            pass

    def _update(self, dict):
        """Update an environment's values directly, bypassing the normal
        checks that occur when users try to set items.
        """
        self._dict.update(dict)

    def get_src_sig_type(self):
        try:
            return self.src_sig_type
        except AttributeError:
            t = SCons.Defaults.DefaultEnvironment().src_sig_type
            self.src_sig_type = t
            return t

    def get_tgt_sig_type(self):
        try:
            return self.tgt_sig_type
        except AttributeError:
            t = SCons.Defaults.DefaultEnvironment().tgt_sig_type
            self.tgt_sig_type = t
            return t

    def Append(self, **kw):
        """Append values to existing construction variables
        in an Environment.
        """
        kw = copy_non_reserved_keywords(kw)
        for key, val in kw.items():
            try:
                if key == 'CPPDEFINES' and SCons.Util.is_String(self._dict[key]):
                    self._dict[key] = [
                     self._dict[key]]
                orig = self._dict[key]
            except KeyError:
                if key == 'CPPDEFINES' and SCons.Util.is_String(val):
                    self._dict[key] = [
                     val]
                else:
                    self._dict[key] = val
            else:
                try:
                    update_dict = orig.update
                except AttributeError:
                    try:
                        self._dict[key] = orig + val
                    except (KeyError, TypeError):
                        try:
                            add_to_orig = orig.append
                        except AttributeError:
                            if orig:
                                val.insert(0, orig)
                            self._dict[key] = val
                        else:
                            if val:
                                add_to_orig(val)

                else:
                    if SCons.Util.is_List(val):
                        if key == 'CPPDEFINES':
                            tmp = []
                            for k, v in orig.iteritems():
                                if v is not None:
                                    tmp.append((k, v))
                                else:
                                    tmp.append((k,))

                            orig = tmp
                            orig += val
                            self._dict[key] = orig
                        else:
                            for v in val:
                                orig[v] = None

                    else:
                        try:
                            update_dict(val)
                        except (AttributeError, TypeError, ValueError):
                            if SCons.Util.is_Dict(val):
                                for k, v in val.items():
                                    orig[k] = v

                            else:
                                orig[val] = None

        self.scanner_map_delete(kw)
        return

    def _canonicalize(self, path):
        if not SCons.Util.is_String(path):
            path = str(path)
        if path and path[0] == '#':
            path = str(self.fs.Dir(path))
        return path

    def AppendENVPath(self, name, newpath, envname='ENV', sep=os.pathsep, delete_existing=1):
        """Append path elements to the path 'name' in the 'ENV'
        dictionary for this environment.  Will only add any particular
        path once, and will normpath and normcase all paths to help
        assure this.  This can also handle the case where the env
        variable is a list instead of a string.

        If delete_existing is 0, a newpath which is already in the path
        will not be moved to the end (it will be left where it is).
        """
        orig = ''
        if envname in self._dict and name in self._dict[envname]:
            orig = self._dict[envname][name]
        nv = SCons.Util.AppendPath(orig, newpath, sep, delete_existing, canonicalize=self._canonicalize)
        if envname not in self._dict:
            self._dict[envname] = {}
        self._dict[envname][name] = nv

    def AppendUnique(self, delete_existing=0, **kw):
        """Append values to existing construction variables
        in an Environment, if they're not already there.
        If delete_existing is 1, removes existing values first, so
        values move to end.
        """
        kw = copy_non_reserved_keywords(kw)
        for key, val in kw.items():
            if SCons.Util.is_List(val):
                val = _delete_duplicates(val, delete_existing)
            if key not in self._dict or self._dict[key] in ('', None):
                self._dict[key] = val
            elif SCons.Util.is_Dict(self._dict[key]) and SCons.Util.is_Dict(val):
                self._dict[key].update(val)
            elif SCons.Util.is_List(val):
                dk = self._dict[key]
                if key == 'CPPDEFINES':
                    tmp = []
                    for i in val:
                        if SCons.Util.is_List(i):
                            if len(i) >= 2:
                                tmp.append((i[0], i[1]))
                            else:
                                tmp.append((i[0],))
                        elif SCons.Util.is_Tuple(i):
                            tmp.append(i)
                        else:
                            tmp.append((i,))

                    val = tmp
                    if SCons.Util.is_Dict(dk):
                        tmp = []
                        for k, v in dk.iteritems():
                            if v is not None:
                                tmp.append((k, v))
                            else:
                                tmp.append((k,))

                        dk = tmp
                    elif SCons.Util.is_String(dk):
                        dk = [
                         (
                          dk,)]
                    else:
                        tmp = []
                        for i in dk:
                            if SCons.Util.is_List(i):
                                if len(i) >= 2:
                                    tmp.append((i[0], i[1]))
                                else:
                                    tmp.append((i[0],))
                            elif SCons.Util.is_Tuple(i):
                                tmp.append(i)
                            else:
                                tmp.append((i,))

                        dk = tmp
                elif not SCons.Util.is_List(dk):
                    dk = [
                     dk]
                if delete_existing:
                    dk = [ x for x in dk if x not in val ]
                else:
                    val = [ x for x in val if x not in dk ]
                self._dict[key] = dk + val
            else:
                dk = self._dict[key]
                if SCons.Util.is_List(dk):
                    if key == 'CPPDEFINES':
                        tmp = []
                        for i in dk:
                            if SCons.Util.is_List(i):
                                if len(i) >= 2:
                                    tmp.append((i[0], i[1]))
                                else:
                                    tmp.append((i[0],))
                            elif SCons.Util.is_Tuple(i):
                                tmp.append(i)
                            else:
                                tmp.append((i,))

                        dk = tmp
                        if SCons.Util.is_Dict(val):
                            tmp = []
                            for k, v in val.iteritems():
                                if v is not None:
                                    tmp.append((k, v))
                                else:
                                    tmp.append((k,))

                            val = tmp
                        elif SCons.Util.is_String(val):
                            val = [
                             (
                              val,)]
                        if delete_existing:
                            dk = filter(lambda x, val=val: x not in val, dk)
                            self._dict[key] = dk + val
                        else:
                            dk = [ x for x in dk if x not in val ]
                            self._dict[key] = dk + val
                    elif delete_existing:
                        dk = filter(lambda x, val=val: x not in val, dk)
                        self._dict[key] = dk + [val]
                    elif val not in dk:
                        self._dict[key] = dk + [val]
                else:
                    if key == 'CPPDEFINES':
                        if SCons.Util.is_String(dk):
                            dk = [
                             dk]
                        elif SCons.Util.is_Dict(dk):
                            tmp = []
                            for k, v in dk.iteritems():
                                if v is not None:
                                    tmp.append((k, v))
                                else:
                                    tmp.append((k,))

                            dk = tmp
                        if SCons.Util.is_String(val):
                            if val in dk:
                                val = []
                            else:
                                val = [
                                 val]
                        elif SCons.Util.is_Dict(val):
                            tmp = []
                            for i, j in val.iteritems():
                                if j is not None:
                                    tmp.append((i, j))
                                else:
                                    tmp.append(i)

                            val = tmp
                    if delete_existing:
                        dk = [ x for x in dk if x not in val ]
                    self._dict[key] = dk + val

        self.scanner_map_delete(kw)
        return

    def Clone(self, tools=[], toolpath=None, parse_flags=None, **kw):
        """Return a copy of a construction Environment.  The
        copy is like a Python "deep copy"--that is, independent
        copies are made recursively of each objects--except that
        a reference is copied when an object is not deep-copyable
        (like a function).  There are no references to any mutable
        objects in the original Environment.
        """
        builders = self._dict.get('BUILDERS', {})
        clone = copy.copy(self)
        clone._dict = semi_deepcopy_dict(self._dict, ['BUILDERS'])
        clone._dict['BUILDERS'] = BuilderDict(builders, clone)
        clone.added_methods = []
        for mw in self.added_methods:
            if mw == getattr(self, mw.name):
                clone.added_methods.append(mw.clone(clone))

        clone._memo = {}
        kw = copy_non_reserved_keywords(kw)
        new = {}
        for key, value in kw.items():
            new[key] = SCons.Subst.scons_subst_once(value, self, key)

        clone.Replace(**new)
        apply_tools(clone, tools, toolpath)
        clone.Replace(**new)
        if parse_flags:
            clone.MergeFlags(parse_flags)
        if SCons.Debug.track_instances:
            logInstanceCreation(self, 'Environment.EnvironmentClone')
        return clone

    def Copy(self, *args, **kw):
        global _warn_copy_deprecated
        if _warn_copy_deprecated:
            msg = 'The env.Copy() method is deprecated; use the env.Clone() method instead.'
            SCons.Warnings.warn(SCons.Warnings.DeprecatedCopyWarning, msg)
            _warn_copy_deprecated = False
        return self.Clone(*args, **kw)

    def _changed_build(self, dependency, target, prev_ni):
        if dependency.changed_state(target, prev_ni):
            return 1
        return self.decide_source(dependency, target, prev_ni)

    def _changed_content(self, dependency, target, prev_ni):
        return dependency.changed_content(target, prev_ni)

    def _changed_source(self, dependency, target, prev_ni):
        target_env = dependency.get_build_env()
        type = target_env.get_tgt_sig_type()
        if type == 'source':
            return target_env.decide_source(dependency, target, prev_ni)
        else:
            return target_env.decide_target(dependency, target, prev_ni)

    def _changed_timestamp_then_content(self, dependency, target, prev_ni):
        return dependency.changed_timestamp_then_content(target, prev_ni)

    def _changed_timestamp_newer(self, dependency, target, prev_ni):
        return dependency.changed_timestamp_newer(target, prev_ni)

    def _changed_timestamp_match(self, dependency, target, prev_ni):
        return dependency.changed_timestamp_match(target, prev_ni)

    def _copy_from_cache(self, src, dst):
        return self.fs.copy(src, dst)

    def _copy2_from_cache(self, src, dst):
        return self.fs.copy2(src, dst)

    def Decider(self, function):
        copy_function = self._copy2_from_cache
        if function in ('MD5', 'content'):
            if not SCons.Util.md5:
                raise UserError('MD5 signatures are not available in this version of Python.')
            function = self._changed_content
        elif function == 'MD5-timestamp':
            function = self._changed_timestamp_then_content
        elif function in ('timestamp-newer', 'make'):
            function = self._changed_timestamp_newer
            copy_function = self._copy_from_cache
        elif function == 'timestamp-match':
            function = self._changed_timestamp_match
        elif not callable(function):
            raise UserError('Unknown Decider value %s' % repr(function))
        self.decide_target = function
        self.decide_source = function
        self.copy_from_cache = copy_function

    def Detect(self, progs):
        """Return the first available program in progs.
        """
        if not SCons.Util.is_List(progs):
            progs = [
             progs]
        for prog in progs:
            path = self.WhereIs(prog)
            if path:
                return prog

        return

    def Dictionary(self, *args):
        if not args:
            return self._dict
        dlist = [ self._dict[x] for x in args ]
        if len(dlist) == 1:
            dlist = dlist[0]
        return dlist

    def Dump(self, key=None):
        """
        Using the standard Python pretty printer, return the contents of the
        scons build environment as a string.

        If the key passed in is anything other than None, then that will
        be used as an index into the build environment dictionary and
        whatever is found there will be fed into the pretty printer. Note
        that this key is case sensitive.
        """
        import pprint
        pp = pprint.PrettyPrinter(indent=2)
        if key:
            dict = self.Dictionary(key)
        else:
            dict = self.Dictionary()
        return pp.pformat(dict)

    def FindIxes(self, paths, prefix, suffix):
        """
        Search a list of paths for something that matches the prefix and suffix.

        paths - the list of paths or nodes.
        prefix - construction variable for the prefix.
        suffix - construction variable for the suffix.
        """
        suffix = self.subst('$' + suffix)
        prefix = self.subst('$' + prefix)
        for path in paths:
            dir, name = os.path.split(str(path))
            if name[:len(prefix)] == prefix and name[-len(suffix):] == suffix:
                return path

    def ParseConfig(self, command, function=None, unique=1):
        """
        Use the specified function to parse the output of the command
        in order to modify the current environment.  The 'command' can
        be a string or a list of strings representing a command and
        its arguments.  'Function' is an optional argument that takes
        the environment, the output of the command, and the unique flag.
        If no function is specified, MergeFlags, which treats the output
        as the result of a typical 'X-config' command (i.e. gtk-config),
        will merge the output into the appropriate variables.
        """
        if function is None:

            def parse_conf(env, cmd, unique=unique):
                return env.MergeFlags(cmd, unique)

            function = parse_conf
        if SCons.Util.is_List(command):
            command = (' ').join(command)
        command = self.subst(command)
        return function(self, self.backtick(command))

    def ParseDepends(self, filename, must_exist=None, only_one=0):
        """
        Parse a mkdep-style file for explicit dependencies.  This is
        completely abusable, and should be unnecessary in the "normal"
        case of proper SCons configuration, but it may help make
        the transition from a Make hierarchy easier for some people
        to swallow.  It can also be genuinely useful when using a tool
        that can write a .d file, but for which writing a scanner would
        be too complicated.
        """
        filename = self.subst(filename)
        try:
            fp = open(filename, 'r')
        except IOError:
            if must_exist:
                raise
            return

        lines = SCons.Util.LogicalLines(fp).readlines()
        lines = [ l for l in lines if l[0] != '#' ]
        tdlist = []
        for line in lines:
            try:
                target, depends = line.split(':', 1)
            except (AttributeError, ValueError):
                pass
            else:
                tdlist.append((target.split(), depends.split()))

        if only_one:
            targets = []
            for td in tdlist:
                targets.extend(td[0])

            if len(targets) > 1:
                raise SCons.Errors.UserError("More than one dependency target found in `%s':  %s" % (
                 filename, targets))
        for target, depends in tdlist:
            self.Depends(target, depends)

    def Platform(self, platform):
        platform = self.subst(platform)
        return SCons.Platform.Platform(platform)(self)

    def Prepend(self, **kw):
        """Prepend values to existing construction variables
        in an Environment.
        """
        kw = copy_non_reserved_keywords(kw)
        for key, val in kw.items():
            try:
                orig = self._dict[key]
            except KeyError:
                self._dict[key] = val
            else:
                try:
                    update_dict = orig.update
                except AttributeError:
                    try:
                        self._dict[key] = val + orig
                    except (KeyError, TypeError):
                        try:
                            add_to_val = val.append
                        except AttributeError:
                            if val:
                                orig.insert(0, val)
                        else:
                            if orig:
                                add_to_val(orig)
                            self._dict[key] = val

                else:
                    if SCons.Util.is_List(val):
                        for v in val:
                            orig[v] = None

                    else:
                        try:
                            update_dict(val)
                        except (AttributeError, TypeError, ValueError):
                            if SCons.Util.is_Dict(val):
                                for k, v in val.items():
                                    orig[k] = v

                            else:
                                orig[val] = None

        self.scanner_map_delete(kw)
        return

    def PrependENVPath(self, name, newpath, envname='ENV', sep=os.pathsep, delete_existing=1):
        """Prepend path elements to the path 'name' in the 'ENV'
        dictionary for this environment.  Will only add any particular
        path once, and will normpath and normcase all paths to help
        assure this.  This can also handle the case where the env
        variable is a list instead of a string.

        If delete_existing is 0, a newpath which is already in the path
        will not be moved to the front (it will be left where it is).
        """
        orig = ''
        if envname in self._dict and name in self._dict[envname]:
            orig = self._dict[envname][name]
        nv = SCons.Util.PrependPath(orig, newpath, sep, delete_existing, canonicalize=self._canonicalize)
        if envname not in self._dict:
            self._dict[envname] = {}
        self._dict[envname][name] = nv

    def PrependUnique(self, delete_existing=0, **kw):
        """Prepend values to existing construction variables
        in an Environment, if they're not already there.
        If delete_existing is 1, removes existing values first, so
        values move to front.
        """
        kw = copy_non_reserved_keywords(kw)
        for key, val in kw.items():
            if SCons.Util.is_List(val):
                val = _delete_duplicates(val, not delete_existing)
            if key not in self._dict or self._dict[key] in ('', None):
                self._dict[key] = val
            elif SCons.Util.is_Dict(self._dict[key]) and SCons.Util.is_Dict(val):
                self._dict[key].update(val)
            elif SCons.Util.is_List(val):
                dk = self._dict[key]
                if not SCons.Util.is_List(dk):
                    dk = [
                     dk]
                if delete_existing:
                    dk = [ x for x in dk if x not in val ]
                else:
                    val = [ x for x in val if x not in dk ]
                self._dict[key] = val + dk
            else:
                dk = self._dict[key]
                if SCons.Util.is_List(dk):
                    if delete_existing:
                        dk = [ x for x in dk if x not in val ]
                        self._dict[key] = [
                         val] + dk
                    elif val not in dk:
                        self._dict[key] = [
                         val] + dk
                else:
                    if delete_existing:
                        dk = [ x for x in dk if x not in val ]
                    self._dict[key] = val + dk

        self.scanner_map_delete(kw)
        return

    def Replace(self, **kw):
        """Replace existing construction variables in an Environment
        with new construction variables and/or values.
        """
        try:
            kwbd = kw['BUILDERS']
        except KeyError:
            pass
        else:
            kwbd = BuilderDict(kwbd, self)
            del kw['BUILDERS']
            self.__setitem__('BUILDERS', kwbd)

        kw = copy_non_reserved_keywords(kw)
        self._update(semi_deepcopy(kw))
        self.scanner_map_delete(kw)

    def ReplaceIxes(self, path, old_prefix, old_suffix, new_prefix, new_suffix):
        """
        Replace old_prefix with new_prefix and old_suffix with new_suffix.

        env - Environment used to interpolate variables.
        path - the path that will be modified.
        old_prefix - construction variable for the old prefix.
        old_suffix - construction variable for the old suffix.
        new_prefix - construction variable for the new prefix.
        new_suffix - construction variable for the new suffix.
        """
        old_prefix = self.subst('$' + old_prefix)
        old_suffix = self.subst('$' + old_suffix)
        new_prefix = self.subst('$' + new_prefix)
        new_suffix = self.subst('$' + new_suffix)
        dir, name = os.path.split(str(path))
        if name[:len(old_prefix)] == old_prefix:
            name = name[len(old_prefix):]
        if name[-len(old_suffix):] == old_suffix:
            name = name[:-len(old_suffix)]
        return os.path.join(dir, new_prefix + name + new_suffix)

    def SetDefault(self, **kw):
        for k in kw.keys():
            if k in self._dict:
                del kw[k]

        self.Replace(**kw)

    def _find_toolpath_dir(self, tp):
        return self.fs.Dir(self.subst(tp)).srcnode().get_abspath()

    def Tool(self, tool, toolpath=None, **kw):
        if SCons.Util.is_String(tool):
            tool = self.subst(tool)
            if toolpath is None:
                toolpath = self.get('toolpath', [])
            toolpath = list(map(self._find_toolpath_dir, toolpath))
            tool = SCons.Tool.Tool(tool, toolpath, **kw)
        tool(self)
        return

    def WhereIs(self, prog, path=None, pathext=None, reject=[]):
        """Find prog in the path.
        """
        if path is None:
            try:
                path = self['ENV']['PATH']
            except KeyError:
                pass

        elif SCons.Util.is_String(path):
            path = self.subst(path)
        if pathext is None:
            try:
                pathext = self['ENV']['PATHEXT']
            except KeyError:
                pass

        elif SCons.Util.is_String(pathext):
            pathext = self.subst(pathext)
        prog = SCons.Util.CLVar(self.subst(prog))
        path = SCons.Util.WhereIs(prog[0], path, pathext, reject)
        if path:
            return path
        else:
            return

    def Action(self, *args, **kw):

        def subst_string(a, self=self):
            if SCons.Util.is_String(a):
                a = self.subst(a)
            return a

        nargs = list(map(subst_string, args))
        nkw = self.subst_kw(kw)
        return SCons.Action.Action(*nargs, **nkw)

    def AddPreAction(self, files, action):
        nodes = self.arg2nodes(files, self.fs.Entry)
        action = SCons.Action.Action(action)
        uniq = {}
        for executor in [ n.get_executor() for n in nodes ]:
            uniq[executor] = 1

        for executor in uniq.keys():
            executor.add_pre_action(action)

        return nodes

    def AddPostAction(self, files, action):
        nodes = self.arg2nodes(files, self.fs.Entry)
        action = SCons.Action.Action(action)
        uniq = {}
        for executor in [ n.get_executor() for n in nodes ]:
            uniq[executor] = 1

        for executor in uniq.keys():
            executor.add_post_action(action)

        return nodes

    def Alias(self, target, source=[], action=None, **kw):
        tlist = self.arg2nodes(target, self.ans.Alias)
        if not SCons.Util.is_List(source):
            source = [
             source]
        source = [ _f for _f in source if _f ]
        if not action:
            if not source:
                return tlist
            result = []
            for t in tlist:
                bld = t.get_builder(AliasBuilder)
                result.extend(bld(self, t, source))

            return result
        nkw = self.subst_kw(kw)
        nkw.update({'action': SCons.Action.Action(action), 
           'source_factory': self.fs.Entry, 
           'multi': 1, 
           'is_explicit': None})
        bld = SCons.Builder.Builder(**nkw)
        result = []
        for t in tlist:
            b = t.get_builder()
            if b is None or b is AliasBuilder:
                b = bld
            else:
                nkw['action'] = b.action + action
                b = SCons.Builder.Builder(**nkw)
            t.convert()
            result.extend(b(self, t, t.sources + source))

        return result

    def AlwaysBuild(self, *targets):
        tlist = []
        for t in targets:
            tlist.extend(self.arg2nodes(t, self.fs.Entry))

        for t in tlist:
            t.set_always_build()

        return tlist

    def BuildDir(self, *args, **kw):
        msg = 'BuildDir() and the build_dir keyword have been deprecated;\n\tuse VariantDir() and the variant_dir keyword instead.'
        SCons.Warnings.warn(SCons.Warnings.DeprecatedBuildDirWarning, msg)
        if 'build_dir' in kw:
            kw['variant_dir'] = kw['build_dir']
            del kw['build_dir']
        return self.VariantDir(*args, **kw)

    def Builder(self, **kw):
        nkw = self.subst_kw(kw)
        return SCons.Builder.Builder(**nkw)

    def CacheDir(self, path):
        import SCons.CacheDir
        if path is not None:
            path = self.subst(path)
        self._CacheDir_path = path
        return

    def Clean(self, targets, files):
        global CleanTargets
        tlist = self.arg2nodes(targets, self.fs.Entry)
        flist = self.arg2nodes(files, self.fs.Entry)
        for t in tlist:
            try:
                CleanTargets[t].extend(flist)
            except KeyError:
                CleanTargets[t] = flist

    def Configure(self, *args, **kw):
        nargs = [
         self]
        if args:
            nargs = nargs + self.subst_list(args)[0]
        nkw = self.subst_kw(kw)
        nkw['_depth'] = kw.get('_depth', 0) + 1
        try:
            nkw['custom_tests'] = self.subst_kw(nkw['custom_tests'])
        except KeyError:
            pass

        return SCons.SConf.SConf(*nargs, **nkw)

    def Command(self, target, source, action, **kw):
        """Builds the supplied target files from the supplied
        source files using the supplied action.  Action may
        be any type that the Builder constructor will accept
        for an action."""
        bkw = {'action': action, 
           'target_factory': self.fs.Entry, 
           'source_factory': self.fs.Entry}
        try:
            bkw['source_scanner'] = kw['source_scanner']
        except KeyError:
            pass
        else:
            del kw['source_scanner']

        bld = SCons.Builder.Builder(**bkw)
        return bld(self, target, source, **kw)

    def Depends(self, target, dependency):
        """Explicity specify that 'target's depend on 'dependency'."""
        tlist = self.arg2nodes(target, self.fs.Entry)
        dlist = self.arg2nodes(dependency, self.fs.Entry)
        for t in tlist:
            t.add_dependency(dlist)

        return tlist

    def Dir(self, name, *args, **kw):
        """
        """
        s = self.subst(name)
        if SCons.Util.is_Sequence(s):
            result = []
            for e in s:
                result.append(self.fs.Dir(e, *args, **kw))

            return result
        return self.fs.Dir(s, *args, **kw)

    def NoClean(self, *targets):
        """Tags a target so that it will not be cleaned by -c"""
        tlist = []
        for t in targets:
            tlist.extend(self.arg2nodes(t, self.fs.Entry))

        for t in tlist:
            t.set_noclean()

        return tlist

    def NoCache(self, *targets):
        """Tags a target so that it will not be cached"""
        tlist = []
        for t in targets:
            tlist.extend(self.arg2nodes(t, self.fs.Entry))

        for t in tlist:
            t.set_nocache()

        return tlist

    def Entry(self, name, *args, **kw):
        """
        """
        s = self.subst(name)
        if SCons.Util.is_Sequence(s):
            result = []
            for e in s:
                result.append(self.fs.Entry(e, *args, **kw))

            return result
        return self.fs.Entry(s, *args, **kw)

    def Environment(self, **kw):
        return SCons.Environment.Environment(**self.subst_kw(kw))

    def Execute(self, action, *args, **kw):
        """Directly execute an action through an Environment
        """
        action = self.Action(action, *args, **kw)
        result = action([], [], self)
        if isinstance(result, SCons.Errors.BuildError):
            errstr = result.errstr
            if result.filename:
                errstr = result.filename + ': ' + errstr
            sys.stderr.write('scons: *** %s\n' % errstr)
            return result.status
        else:
            return result

    def File(self, name, *args, **kw):
        """
        """
        s = self.subst(name)
        if SCons.Util.is_Sequence(s):
            result = []
            for e in s:
                result.append(self.fs.File(e, *args, **kw))

            return result
        return self.fs.File(s, *args, **kw)

    def FindFile(self, file, dirs):
        file = self.subst(file)
        nodes = self.arg2nodes(dirs, self.fs.Dir)
        return SCons.Node.FS.find_file(file, tuple(nodes))

    def Flatten(self, sequence):
        return SCons.Util.flatten(sequence)

    def GetBuildPath(self, files):
        result = list(map(str, self.arg2nodes(files, self.fs.Entry)))
        if SCons.Util.is_List(files):
            return result
        else:
            return result[0]

    def Glob(self, pattern, ondisk=True, source=False, strings=False, exclude=None):
        return self.fs.Glob(self.subst(pattern), ondisk, source, strings, exclude)

    def Ignore(self, target, dependency):
        """Ignore a dependency."""
        tlist = self.arg2nodes(target, self.fs.Entry)
        dlist = self.arg2nodes(dependency, self.fs.Entry)
        for t in tlist:
            t.add_ignore(dlist)

        return tlist

    def Literal(self, string):
        return SCons.Subst.Literal(string)

    def Local(self, *targets):
        ret = []
        for targ in targets:
            if isinstance(targ, SCons.Node.Node):
                targ.set_local()
                ret.append(targ)
            else:
                for t in self.arg2nodes(targ, self.fs.Entry):
                    t.set_local()
                    ret.append(t)

        return ret

    def Precious(self, *targets):
        tlist = []
        for t in targets:
            tlist.extend(self.arg2nodes(t, self.fs.Entry))

        for t in tlist:
            t.set_precious()

        return tlist

    def Pseudo(self, *targets):
        tlist = []
        for t in targets:
            tlist.extend(self.arg2nodes(t, self.fs.Entry))

        for t in tlist:
            t.set_pseudo()

        return tlist

    def Repository(self, *dirs, **kw):
        dirs = self.arg2nodes(list(dirs), self.fs.Dir)
        self.fs.Repository(*dirs, **kw)

    def Requires(self, target, prerequisite):
        """Specify that 'prerequisite' must be built before 'target',
        (but 'target' does not actually depend on 'prerequisite'
        and need not be rebuilt if it changes)."""
        tlist = self.arg2nodes(target, self.fs.Entry)
        plist = self.arg2nodes(prerequisite, self.fs.Entry)
        for t in tlist:
            t.add_prerequisite(plist)

        return tlist

    def Scanner(self, *args, **kw):
        nargs = []
        for arg in args:
            if SCons.Util.is_String(arg):
                arg = self.subst(arg)
            nargs.append(arg)

        nkw = self.subst_kw(kw)
        return SCons.Scanner.Base(*nargs, **nkw)

    def SConsignFile(self, name='.sconsign', dbm_module=None):
        if name is not None:
            name = self.subst(name)
            if not os.path.isabs(name):
                name = os.path.join(str(self.fs.SConstruct_dir), name)
        if name:
            name = os.path.normpath(name)
            sconsign_dir = os.path.dirname(name)
            if sconsign_dir and not os.path.exists(sconsign_dir):
                self.Execute(SCons.Defaults.Mkdir(sconsign_dir))
        SCons.SConsign.File(name, dbm_module)
        return

    def SideEffect(self, side_effect, target):
        """Tell scons that side_effects are built as side
        effects of building targets."""
        side_effects = self.arg2nodes(side_effect, self.fs.Entry)
        targets = self.arg2nodes(target, self.fs.Entry)
        for side_effect in side_effects:
            if side_effect.multiple_side_effect_has_builder():
                raise SCons.Errors.UserError('Multiple ways to build the same target were specified for: %s' % str(side_effect))
            side_effect.add_source(targets)
            side_effect.side_effect = 1
            self.Precious(side_effect)
            for target in targets:
                target.side_effects.append(side_effect)

        return side_effects

    def SourceCode(self, entry, builder):
        """Arrange for a source code builder for (part of) a tree."""
        msg = 'SourceCode() has been deprecated and there is no replacement.\n\tIf you need this function, please contact scons-dev@scons.org'
        SCons.Warnings.warn(SCons.Warnings.DeprecatedSourceCodeWarning, msg)
        entries = self.arg2nodes(entry, self.fs.Entry)
        for entry in entries:
            entry.set_src_builder(builder)

        return entries

    def SourceSignatures(self, type):
        global _warn_source_signatures_deprecated
        if _warn_source_signatures_deprecated:
            msg = 'The env.SourceSignatures() method is deprecated;\n' + '\tconvert your build to use the env.Decider() method instead.'
            SCons.Warnings.warn(SCons.Warnings.DeprecatedSourceSignaturesWarning, msg)
            _warn_source_signatures_deprecated = False
        type = self.subst(type)
        self.src_sig_type = type
        if type == 'MD5':
            if not SCons.Util.md5:
                raise UserError('MD5 signatures are not available in this version of Python.')
            self.decide_source = self._changed_content
        elif type == 'timestamp':
            self.decide_source = self._changed_timestamp_match
        else:
            raise UserError("Unknown source signature type '%s'" % type)

    def Split(self, arg):
        """This function converts a string or list into a list of strings
        or Nodes.  This makes things easier for users by allowing files to
        be specified as a white-space separated list to be split.
        The input rules are:
            - A single string containing names separated by spaces. These will be
              split apart at the spaces.
            - A single Node instance
            - A list containing either strings or Node instances. Any strings
              in the list are not split at spaces.
        In all cases, the function returns a list of Nodes and strings."""
        if SCons.Util.is_List(arg):
            return list(map(self.subst, arg))
        else:
            if SCons.Util.is_String(arg):
                return self.subst(arg).split()
            return [self.subst(arg)]

    def TargetSignatures(self, type):
        global _warn_target_signatures_deprecated
        if _warn_target_signatures_deprecated:
            msg = 'The env.TargetSignatures() method is deprecated;\n' + '\tconvert your build to use the env.Decider() method instead.'
            SCons.Warnings.warn(SCons.Warnings.DeprecatedTargetSignaturesWarning, msg)
            _warn_target_signatures_deprecated = False
        type = self.subst(type)
        self.tgt_sig_type = type
        if type in ('MD5', 'content'):
            if not SCons.Util.md5:
                raise UserError('MD5 signatures are not available in this version of Python.')
            self.decide_target = self._changed_content
        elif type == 'timestamp':
            self.decide_target = self._changed_timestamp_match
        elif type == 'build':
            self.decide_target = self._changed_build
        elif type == 'source':
            self.decide_target = self._changed_source
        else:
            raise UserError("Unknown target signature type '%s'" % type)

    def Value(self, value, built_value=None):
        """
        """
        return SCons.Node.Python.Value(value, built_value)

    def VariantDir(self, variant_dir, src_dir, duplicate=1):
        variant_dir = self.arg2nodes(variant_dir, self.fs.Dir)[0]
        src_dir = self.arg2nodes(src_dir, self.fs.Dir)[0]
        self.fs.VariantDir(variant_dir, src_dir, duplicate)

    def FindSourceFiles(self, node='.'):
        """ returns a list of all source files.
        """
        node = self.arg2nodes(node, self.fs.Entry)[0]
        sources = []

        def build_source(ss):
            for s in ss:
                if isinstance(s, SCons.Node.FS.Dir):
                    build_source(s.all_children())
                elif s.has_builder():
                    build_source(s.sources)
                elif isinstance(s.disambiguate(), SCons.Node.FS.File):
                    sources.append(s)

        build_source(node.all_children())

        def final_source(node):
            while node != node.srcnode():
                node = node.srcnode()

            return node

        sources = map(final_source, sources)
        return list(set(sources))

    def FindInstalledFiles(self):
        """ returns the list of all targets of the Install and InstallAs Builder.
        """
        from SCons.Tool import install
        if install._UNIQUE_INSTALLED_FILES is None:
            install._UNIQUE_INSTALLED_FILES = SCons.Util.uniquer_hashables(install._INSTALLED_FILES)
        return install._UNIQUE_INSTALLED_FILES


class OverrideEnvironment(Base):
    """A proxy that overrides variables in a wrapped construction
    environment by returning values from an overrides dictionary in
    preference to values from the underlying subject environment.

    This is a lightweight (I hope) proxy that passes through most use of
    attributes to the underlying Environment.Base class, but has just
    enough additional methods defined to act like a real construction
    environment with overridden values.  It can wrap either a Base
    construction environment, or another OverrideEnvironment, which
    can in turn nest arbitrary OverrideEnvironments...

    Note that we do *not* call the underlying base class
    (SubsitutionEnvironment) initialization, because we get most of those
    from proxying the attributes of the subject construction environment.
    But because we subclass SubstitutionEnvironment, this class also
    has inherited arg2nodes() and subst*() methods; those methods can't
    be proxied because they need *this* object's methods to fetch the
    values from the overrides dictionary.
    """

    def __init__(self, subject, overrides={}):
        if SCons.Debug.track_instances:
            logInstanceCreation(self, 'Environment.OverrideEnvironment')
        self.__dict__['__subject'] = subject
        self.__dict__['overrides'] = overrides

    def __getattr__(self, name):
        return getattr(self.__dict__['__subject'], name)

    def __setattr__(self, name, value):
        setattr(self.__dict__['__subject'], name, value)

    def __getitem__(self, key):
        try:
            return self.__dict__['overrides'][key]
        except KeyError:
            return self.__dict__['__subject'].__getitem__(key)

    def __setitem__(self, key, value):
        if not is_valid_construction_var(key):
            raise SCons.Errors.UserError("Illegal construction variable `%s'" % key)
        self.__dict__['overrides'][key] = value

    def __delitem__(self, key):
        try:
            del self.__dict__['overrides'][key]
        except KeyError:
            deleted = 0
        else:
            deleted = 1

        try:
            result = self.__dict__['__subject'].__delitem__(key)
        except KeyError:
            if not deleted:
                raise
            result = None

        return result

    def get(self, key, default=None):
        """Emulates the get() method of dictionaries."""
        try:
            return self.__dict__['overrides'][key]
        except KeyError:
            return self.__dict__['__subject'].get(key, default)

    def has_key(self, key):
        try:
            self.__dict__['overrides'][key]
            return 1
        except KeyError:
            return key in self.__dict__['__subject']

    def __contains__(self, key):
        if self.__dict__['overrides'].__contains__(key):
            return 1
        return self.__dict__['__subject'].__contains__(key)

    def Dictionary(self):
        """Emulates the items() method of dictionaries."""
        d = self.__dict__['__subject'].Dictionary().copy()
        d.update(self.__dict__['overrides'])
        return d

    def items(self):
        """Emulates the items() method of dictionaries."""
        return list(self.Dictionary().items())

    def _update(self, dict):
        """Update an environment's values directly, bypassing the normal
        checks that occur when users try to set items.
        """
        self.__dict__['overrides'].update(dict)

    def gvars(self):
        return self.__dict__['__subject'].gvars()

    def lvars(self):
        lvars = self.__dict__['__subject'].lvars()
        lvars.update(self.__dict__['overrides'])
        return lvars

    def Replace(self, **kw):
        kw = copy_non_reserved_keywords(kw)
        self.__dict__['overrides'].update(semi_deepcopy(kw))


Environment = Base

def NoSubstitutionProxy(subject):

    class _NoSubstitutionProxy(Environment):

        def __init__(self, subject):
            self.__dict__['__subject'] = subject

        def __getattr__(self, name):
            return getattr(self.__dict__['__subject'], name)

        def __setattr__(self, name, value):
            return setattr(self.__dict__['__subject'], name, value)

        def executor_to_lvars(self, kwdict):
            if kwdict.has_key('executor'):
                kwdict['lvars'] = kwdict['executor'].get_lvars()
                del kwdict['executor']
            else:
                kwdict['lvars'] = {}

        def raw_to_mode(self, dict):
            try:
                raw = dict['raw']
            except KeyError:
                pass
            else:
                del dict['raw']
                dict['mode'] = raw

        def subst(self, string, *args, **kwargs):
            return string

        def subst_kw(self, kw, *args, **kwargs):
            return kw

        def subst_list(self, string, *args, **kwargs):
            nargs = (string, self) + args
            nkw = kwargs.copy()
            nkw['gvars'] = {}
            self.executor_to_lvars(nkw)
            self.raw_to_mode(nkw)
            return SCons.Subst.scons_subst_list(*nargs, **nkw)

        def subst_target_source(self, string, *args, **kwargs):
            nargs = (string, self) + args
            nkw = kwargs.copy()
            nkw['gvars'] = {}
            self.executor_to_lvars(nkw)
            self.raw_to_mode(nkw)
            return SCons.Subst.scons_subst(*nargs, **nkw)

    return _NoSubstitutionProxy(subject)