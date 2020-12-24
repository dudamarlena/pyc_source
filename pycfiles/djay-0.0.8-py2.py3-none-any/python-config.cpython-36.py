# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/ant/.pyenv/versions/3.6.5/lib/python3.6/python-config.py
# Compiled at: 2019-02-06 16:34:23
# Size of source mod 2**32: 2063 bytes
import getopt, os, sys, sysconfig
valid_opts = [
 'prefix', 'exec-prefix', 'includes', 'libs', 'cflags',
 'ldflags', 'extension-suffix', 'help', 'abiflags', 'configdir']

def exit_with_usage(code=1):
    print(('Usage: {0} [{1}]'.format(sys.argv[0], '|'.join('--' + opt for opt in valid_opts))),
      file=(sys.stderr))
    sys.exit(code)


try:
    opts, args = getopt.getopt(sys.argv[1:], '', valid_opts)
except getopt.error:
    exit_with_usage()

if not opts:
    exit_with_usage()
pyver = sysconfig.get_config_var('VERSION')
getvar = sysconfig.get_config_var
opt_flags = [flag for flag, val in opts]
if '--help' in opt_flags:
    exit_with_usage(code=0)
for opt in opt_flags:
    if opt == '--prefix':
        print(sysconfig.get_config_var('prefix'))
    else:
        if opt == '--exec-prefix':
            print(sysconfig.get_config_var('exec_prefix'))
        else:
            if opt in ('--includes', '--cflags'):
                flags = [
                 '-I' + sysconfig.get_path('include'),
                 '-I' + sysconfig.get_path('platinclude')]
                if opt == '--cflags':
                    flags.extend(getvar('CFLAGS').split())
                print(' '.join(flags))
            else:
                if opt in ('--libs', '--ldflags'):
                    libs = [
                     '-lpython' + pyver + sys.abiflags]
                    libs += getvar('LIBS').split()
                    libs += getvar('SYSLIBS').split()
                    if opt == '--ldflags':
                        if not getvar('Py_ENABLE_SHARED'):
                            libs.insert(0, '-L' + getvar('LIBPL'))
                        if not getvar('PYTHONFRAMEWORK'):
                            libs.extend(getvar('LINKFORSHARED').split())
                    print(' '.join(libs))
                else:
                    if opt == '--extension-suffix':
                        print(sysconfig.get_config_var('EXT_SUFFIX'))
                    else:
                        if opt == '--abiflags':
                            print(sys.abiflags)
                        else:
                            if opt == '--configdir':
                                print(sysconfig.get_config_var('LIBPL'))