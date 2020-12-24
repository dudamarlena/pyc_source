# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\derek_2\Google Drive\nvda-addon-exploded\notepad++\scons-local-2.5.0\SCons\Tool\rpcgen.py
# Compiled at: 2016-07-07 03:21:35
"""SCons.Tool.rpcgen

Tool-specific initialization for RPCGEN tools.

Three normally shouldn't be any need to import this module directly.
It will usually be imported through the generic SCons.Tool.Tool()
selection method.
"""
__revision__ = 'src/engine/SCons/Tool/rpcgen.py rel_2.5.0:3543:937e55cd78f7 2016/04/09 11:29:54 bdbaddog'
from SCons.Builder import Builder
import SCons.Util
cmd = 'cd ${SOURCE.dir} && $RPCGEN -%s $RPCGENFLAGS %s -o ${TARGET.abspath} ${SOURCE.file}'
rpcgen_client = cmd % ('l', '$RPCGENCLIENTFLAGS')
rpcgen_header = cmd % ('h', '$RPCGENHEADERFLAGS')
rpcgen_service = cmd % ('m', '$RPCGENSERVICEFLAGS')
rpcgen_xdr = cmd % ('c', '$RPCGENXDRFLAGS')

def generate(env):
    """Add RPCGEN Builders and construction variables for an Environment."""
    client = Builder(action=rpcgen_client, suffix='_clnt.c', src_suffix='.x')
    header = Builder(action=rpcgen_header, suffix='.h', src_suffix='.x')
    service = Builder(action=rpcgen_service, suffix='_svc.c', src_suffix='.x')
    xdr = Builder(action=rpcgen_xdr, suffix='_xdr.c', src_suffix='.x')
    env.Append(BUILDERS={'RPCGenClient': client, 'RPCGenHeader': header, 
       'RPCGenService': service, 
       'RPCGenXDR': xdr})
    env['RPCGEN'] = 'rpcgen'
    env['RPCGENFLAGS'] = SCons.Util.CLVar('')
    env['RPCGENCLIENTFLAGS'] = SCons.Util.CLVar('')
    env['RPCGENHEADERFLAGS'] = SCons.Util.CLVar('')
    env['RPCGENSERVICEFLAGS'] = SCons.Util.CLVar('')
    env['RPCGENXDRFLAGS'] = SCons.Util.CLVar('')


def exists(env):
    return env.Detect('rpcgen')