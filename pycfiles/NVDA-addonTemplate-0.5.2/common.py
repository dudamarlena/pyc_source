# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\derek_2\Google Drive\nvda-addon-exploded\notepad++\scons-local-2.5.0\SCons\Tool\MSCommon\common.py
# Compiled at: 2016-07-07 03:21:35
__revision__ = 'src/engine/SCons/Tool/MSCommon/common.py rel_2.5.0:3543:937e55cd78f7 2016/04/09 11:29:54 bdbaddog'
__doc__ = '\nCommon helper functions for working with the Microsoft tool chain.\n'
import copy, os, subprocess, re, SCons.Util
logfile = os.environ.get('SCONS_MSCOMMON_DEBUG')
if logfile == '-':

    def debug(x):
        print x


elif logfile:
    try:
        import logging
    except ImportError:
        debug = lambda x: open(logfile, 'a').write(x + '\n')
    else:
        logging.basicConfig(filename=logfile, level=logging.DEBUG)
        debug = logging.debug

else:
    debug = lambda x: None
_is_win64 = None

def is_win64():
    """Return true if running on windows 64 bits.

    Works whether python itself runs in 64 bits or 32 bits."""
    global _is_win64
    if _is_win64 is None:
        _is_win64 = False
        if os.environ.get('PROCESSOR_ARCHITECTURE', 'x86') != 'x86':
            _is_win64 = True
        if os.environ.get('PROCESSOR_ARCHITEW6432'):
            _is_win64 = True
        if os.environ.get('ProgramW6432'):
            _is_win64 = True
    return _is_win64


def read_reg(value, hkroot=SCons.Util.HKEY_LOCAL_MACHINE):
    return SCons.Util.RegGetValue(hkroot, value)[0]


def has_reg(value):
    """Return True if the given key exists in HKEY_LOCAL_MACHINE, False
    otherwise."""
    try:
        SCons.Util.RegOpenKeyEx(SCons.Util.HKEY_LOCAL_MACHINE, value)
        ret = True
    except SCons.Util.WinError:
        ret = False

    return ret


def normalize_env(env, keys, force=False):
    """Given a dictionary representing a shell environment, add the variables
    from os.environ needed for the processing of .bat files; the keys are
    controlled by the keys argument.

    It also makes sure the environment values are correctly encoded.

    If force=True, then all of the key values that exist are copied
    into the returned dictionary.  If force=false, values are only
    copied if the key does not already exist in the copied dictionary.

    Note: the environment is copied."""
    normenv = {}
    if env:
        for k in env.keys():
            normenv[k] = copy.deepcopy(env[k]).encode('mbcs')

        for k in keys:
            if k in os.environ and (force or k not in normenv):
                normenv[k] = os.environ[k].encode('mbcs')

    sys32_dir = os.path.join(os.environ.get('SystemRoot', os.environ.get('windir', 'C:\\Windows\\system32')), 'System32')
    if sys32_dir not in normenv['PATH']:
        normenv['PATH'] = normenv['PATH'] + os.pathsep + sys32_dir
    debug('PATH: %s' % normenv['PATH'])
    return normenv


def get_output(vcbat, args=None, env=None):
    """Parse the output of given bat file, with given args."""
    if env is None:
        env = SCons.Environment.Environment(tools=[])
    vars = [
     'COMSPEC',
     'VS110COMNTOOLS',
     'VS100COMNTOOLS',
     'VS90COMNTOOLS',
     'VS80COMNTOOLS',
     'VS71COMNTOOLS',
     'VS70COMNTOOLS',
     'VS60COMNTOOLS']
    env['ENV'] = normalize_env(env['ENV'], vars, force=False)
    if args:
        debug("Calling '%s %s'" % (vcbat, args))
        popen = SCons.Action._subproc(env, '"%s" %s & set' % (vcbat, args), stdin='devnull', stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    else:
        debug("Calling '%s'" % vcbat)
        popen = SCons.Action._subproc(env, '"%s" & set' % vcbat, stdin='devnull', stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    stdout = popen.stdout.read()
    stderr = popen.stderr.read()
    if stderr:
        import sys
        sys.stderr.write(stderr)
    if popen.wait() != 0:
        raise IOError(stderr.decode('mbcs'))
    output = stdout.decode('mbcs')
    return output


def parse_output(output, keep=('INCLUDE', 'LIB', 'LIBPATH', 'PATH')):
    dkeep = dict([ (i, []) for i in keep ])
    rdk = {}
    for i in keep:
        rdk[i] = re.compile('%s=(.*)' % i, re.I)

    def add_env(rmatch, key, dkeep=dkeep):
        plist = rmatch.group(1).split(os.pathsep)
        for p in plist:
            if p:
                p = p.encode('mbcs')
                p = p.strip('"')
                dkeep[key].append(p)

    for line in output.splitlines():
        for k, v in rdk.items():
            m = v.match(line)
            if m:
                add_env(m, k)

    return dkeep