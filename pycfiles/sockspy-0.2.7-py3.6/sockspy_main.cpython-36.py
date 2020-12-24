# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.12-x86_64/egg/sockspy/sockspy_main.py
# Compiled at: 2017-07-27 12:16:51
# Size of source mod 2**32: 282 bytes
from sockspy.core import context, config
from sockspy.socks_impl import socks5

def run():
    cfg = config.get_default_config()
    config.set_default_log_config()
    ctx = context.AppContext(socks5.Socks5Engine, cfg)
    ctx.run()