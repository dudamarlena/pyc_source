# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/travis/build/g-braeunlich/IPyOpt/setup_helpers/pkg_config.py
# Compiled at: 2019-08-07 10:42:15
# Size of source mod 2**32: 1039 bytes
import subprocess, warnings

def pkg_config(*packages, **kwargs):
    """Calls pkg-config returning a dict containing all arguments
    for Extension() needed to compile the extension
    """
    flag_map = {b'-I':'include_dirs', 
     b'-L':'library_dirs', 
     b'-l':'libraries', 
     b'-D':'define_macros'}
    res = subprocess.run((('pkg-config', '--libs', '--cflags') + packages),
      stdout=(subprocess.PIPE), stderr=(subprocess.PIPE))
    if res.stderr:
        raise RuntimeError(res.stderr.decode())
    for token in res.stdout.split():
        kwargs.setdefault(flag_map.get(token[:2]), []).append(token[2:].decode())

    define_macros = kwargs.get('define_macros')
    if define_macros:
        kwargs['define_macros'] = [tuple(d.split()) for d in define_macros]
    undefined_flags = kwargs.pop(None, None)
    if undefined_flags:
        warnings.warn('Ignoring flags {} from pkg-config'.format(', '.join(undefined_flags)))
    return kwargs