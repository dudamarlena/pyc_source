# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/setuptools_scm/utils.py
# Compiled at: 2020-02-13 15:05:29
"""
utils
"""
from __future__ import print_function, unicode_literals
import inspect, warnings, sys, shlex, subprocess, os, io, platform, traceback
DEBUG = bool(os.environ.get(b'SETUPTOOLS_SCM_DEBUG'))
IS_WINDOWS = platform.system() == b'Windows'
PY2 = sys.version_info < (3, )
PY3 = sys.version_info > (3, )
string_types = (str,) if PY3 else (str, unicode)

def no_git_env(env):
    for k, v in env.items():
        if k.startswith(b'GIT_'):
            trace(k, v)

    return {k:v for k, v in env.items() if not k.startswith(b'GIT_') or k in ('GIT_EXEC_PATH',
                                                                              'GIT_SSH',
                                                                              'GIT_SSH_COMMAND') if not k.startswith(b'GIT_') or k in ('GIT_EXEC_PATH',
                                                                                                                                       'GIT_SSH',
                                                                                                                                       'GIT_SSH_COMMAND')}


def trace(*k):
    if DEBUG:
        print(*k)
        sys.stdout.flush()


def trace_exception():
    DEBUG and traceback.print_exc()


def ensure_stripped_str(str_or_bytes):
    if isinstance(str_or_bytes, str):
        return str_or_bytes.strip()
    else:
        return str_or_bytes.decode(b'utf-8', b'surrogateescape').strip()


def _always_strings(env_dict):
    """
    On Windows and Python 2, environment dictionaries must be strings
    and not unicode.
    """
    if IS_WINDOWS or PY2:
        env_dict.update((key, str(value)) for key, value in env_dict.items())
    return env_dict


def _popen_pipes(cmd, cwd):
    return subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, cwd=str(cwd), env=_always_strings(dict(no_git_env(os.environ), LC_ALL=b'C', LANGUAGE=b'', HGPLAIN=b'1')))


def do_ex(cmd, cwd=b'.'):
    trace(b'cmd', repr(cmd))
    if os.name == b'posix' and not isinstance(cmd, (list, tuple)):
        cmd = shlex.split(cmd)
    p = _popen_pipes(cmd, cwd)
    out, err = p.communicate()
    if out:
        trace(b'out', repr(out))
    if err:
        trace(b'err', repr(err))
    if p.returncode:
        trace(b'ret', p.returncode)
    return (
     ensure_stripped_str(out), ensure_stripped_str(err), p.returncode)


def do(cmd, cwd=b'.'):
    out, err, ret = do_ex(cmd, cwd)
    if ret:
        print(err)
    return out


def data_from_mime(path):
    with io.open(path, encoding=b'utf-8') as (fp):
        content = fp.read()
    trace(b'content', repr(content))
    data = dict(x.split(b': ', 1) for x in content.splitlines() if b': ' in x)
    trace(b'data', data)
    return data


def function_has_arg(fn, argname):
    assert inspect.isfunction(fn)
    if PY2:
        argspec = inspect.getargspec(fn).args
    else:
        argspec = inspect.signature(fn).parameters
    return argname in argspec


def has_command(name):
    try:
        p = _popen_pipes([name, b'help'], b'.')
    except OSError:
        trace(*sys.exc_info())
        res = False
    else:
        p.communicate()
        res = not p.returncode

    if not res:
        warnings.warn(b'%r was not found' % name)
    return res