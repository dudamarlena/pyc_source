# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\derek_2\Google Drive\nvda-addon-exploded\notepad++\scons-local-2.5.0\SCons\Tool\swig.py
# Compiled at: 2016-07-07 03:21:33
"""SCons.Tool.swig

Tool-specific initialization for swig.

There normally shouldn't be any need to import this module directly.
It will usually be imported through the generic SCons.Tool.Tool()
selection method.

"""
__revision__ = 'src/engine/SCons/Tool/swig.py rel_2.5.0:3543:937e55cd78f7 2016/04/09 11:29:54 bdbaddog'
import os.path, re, subprocess, SCons.Action, SCons.Defaults, SCons.Tool, SCons.Util, SCons.Node
verbose = False
swigs = [
 'swig', 'swig3.0', 'swig2.0']
SwigAction = SCons.Action.Action('$SWIGCOM', '$SWIGCOMSTR')

def swigSuffixEmitter(env, source):
    if '-c++' in SCons.Util.CLVar(env.subst('$SWIGFLAGS', source=source)):
        return '$SWIGCXXFILESUFFIX'
    else:
        return '$SWIGCFILESUFFIX'


_reModule = re.compile('%module(\\s*\\(.*\\))?\\s+("?)(\\S+)\\2')

def _find_modules(src):
    """Find all modules referenced by %module lines in `src`, a SWIG .i file.
       Returns a list of all modules, and a flag set if SWIG directors have
       been requested (SWIG will generate an additional header file in this
       case.)"""
    directors = 0
    mnames = []
    try:
        matches = _reModule.findall(open(src).read())
    except IOError:
        matches = []
        mnames.append(os.path.splitext(os.path.basename(src))[0])

    for m in matches:
        mnames.append(m[2])
        directors = directors or m[0].find('directors') >= 0

    return (
     mnames, directors)


def _add_director_header_targets(target, env):
    suffix = env.subst(env['SWIGCXXFILESUFFIX'])
    for x in target[:]:
        n = x.name
        d = x.dir
        if n[-len(suffix):] == suffix:
            target.append(d.File(n[:-len(suffix)] + env['SWIGDIRECTORSUFFIX']))


def _swigEmitter(target, source, env):
    swigflags = env.subst('$SWIGFLAGS', target=target, source=source)
    flags = SCons.Util.CLVar(swigflags)
    for src in source:
        src = str(src.rfile())
        mnames = None
        if '-python' in flags and '-noproxy' not in flags:
            if mnames is None:
                mnames, directors = _find_modules(src)
            if directors:
                _add_director_header_targets(target, env)
            python_files = [ m + '.py' for m in mnames ]
            outdir = env.subst('$SWIGOUTDIR', target=target, source=source)
            if outdir:
                python_files = [ env.fs.File(os.path.join(outdir, j)) for j in python_files ]
            else:
                python_files = [ target[0].dir.File(m) for m in python_files ]
            target.extend(python_files)
        if '-java' in flags:
            if mnames is None:
                mnames, directors = _find_modules(src)
            if directors:
                _add_director_header_targets(target, env)
            java_files = [ [m + '.java', m + 'JNI.java'] for m in mnames ]
            java_files = SCons.Util.flatten(java_files)
            outdir = env.subst('$SWIGOUTDIR', target=target, source=source)
            if outdir:
                java_files = [ os.path.join(outdir, j) for j in java_files ]
            java_files = list(map(env.fs.File, java_files))

            def t_from_s(t, p, s, x):
                return t.dir

            tsm = SCons.Node._target_from_source_map
            tkey = len(tsm)
            tsm[tkey] = t_from_s
            for jf in java_files:
                jf._func_target_from_source = tkey

            target.extend(java_files)

    return (
     target, source)


def _get_swig_version(env, swig):
    """Run the SWIG command line tool to get and return the version number"""
    swig = env.subst(swig)
    pipe = SCons.Action._subproc(env, SCons.Util.CLVar(swig) + ['-version'], stdin='devnull', stderr='devnull', stdout=subprocess.PIPE)
    if pipe.wait() != 0:
        return
    out = pipe.stdout.read()
    match = re.search('SWIG Version\\s+(\\S+).*', out, re.MULTILINE)
    if match:
        if verbose:
            print 'Version is:%s' % match.group(1)
        return match.group(1)
    if verbose:
        print 'Unable to detect version: [%s]' % out


def generate(env):
    """Add Builders and construction variables for swig to an Environment."""
    c_file, cxx_file = SCons.Tool.createCFileBuilders(env)
    c_file.suffix['.i'] = swigSuffixEmitter
    cxx_file.suffix['.i'] = swigSuffixEmitter
    c_file.add_action('.i', SwigAction)
    c_file.add_emitter('.i', _swigEmitter)
    cxx_file.add_action('.i', SwigAction)
    cxx_file.add_emitter('.i', _swigEmitter)
    java_file = SCons.Tool.CreateJavaFileBuilder(env)
    java_file.suffix['.i'] = swigSuffixEmitter
    java_file.add_action('.i', SwigAction)
    java_file.add_emitter('.i', _swigEmitter)
    if 'SWIG' not in env:
        env['SWIG'] = env.Detect(swigs) or swigs[0]
    env['SWIGVERSION'] = _get_swig_version(env, env['SWIG'])
    env['SWIGFLAGS'] = SCons.Util.CLVar('')
    env['SWIGDIRECTORSUFFIX'] = '_wrap.h'
    env['SWIGCFILESUFFIX'] = '_wrap$CFILESUFFIX'
    env['SWIGCXXFILESUFFIX'] = '_wrap$CXXFILESUFFIX'
    env['_SWIGOUTDIR'] = '${"-outdir \\"%s\\"" % SWIGOUTDIR}'
    env['SWIGPATH'] = []
    env['SWIGINCPREFIX'] = '-I'
    env['SWIGINCSUFFIX'] = ''
    env['_SWIGINCFLAGS'] = '$( ${_concat(SWIGINCPREFIX, SWIGPATH, SWIGINCSUFFIX, __env__, RDirs, TARGET, SOURCE)} $)'
    env['SWIGCOM'] = '$SWIG -o $TARGET ${_SWIGOUTDIR} ${_SWIGINCFLAGS} $SWIGFLAGS $SOURCES'


def exists(env):
    swig = env.get('SWIG') or env.Detect(['swig'])
    return swig