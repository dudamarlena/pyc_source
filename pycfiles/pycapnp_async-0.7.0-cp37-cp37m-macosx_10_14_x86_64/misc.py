# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/cfl/ternaris/marv/pycapnp/buildutils/misc.py
__doc__ = 'misc build utility functions'
import os, sys, logging
from distutils import ccompiler
from distutils.sysconfig import customize_compiler
from pipes import quote
from subprocess import Popen, PIPE
pjoin = os.path.join
if sys.version_info[0] >= 3:
    u = lambda x: x
else:
    u = lambda x: x.decode('utf8', 'replace')

def customize_mingw(cc):
    for cmd in [cc.compiler, cc.compiler_cxx, cc.compiler_so, cc.linker_exe, cc.linker_so]:
        if '-mno-cygwin' in cmd:
            cmd.remove('-mno-cygwin')

    if 'msvcr90' in cc.dll_libraries:
        cc.dll_libraries.remove('msvcr90')


def get_compiler(compiler, **compiler_attrs):
    """get and customize a compiler"""
    if compiler is None or isinstance(compiler, str):
        cc = ccompiler.new_compiler(compiler=compiler)
        customize_compiler(cc)
        if cc.compiler_type == 'mingw32':
            customize_mingw(cc)
    else:
        cc = compiler
    for name, val in compiler_attrs.items():
        setattr(cc, name, val)

    return cc


def get_output_error(cmd):
    """Return the exit status, stdout, stderr of a command"""
    if not isinstance(cmd, list):
        cmd = [
         cmd]
    logging.debug('Running: %s', (' ').join(map(quote, cmd)))
    try:
        result = Popen(cmd, stdout=PIPE, stderr=PIPE)
    except IOError as e:
        return (
         -1, u(''), u('Failed to run %r: %r' % (cmd, e)))

    so, se = result.communicate()
    so = so.decode('utf8', 'replace')
    se = se.decode('utf8', 'replace')
    return (
     result.returncode, so, se)