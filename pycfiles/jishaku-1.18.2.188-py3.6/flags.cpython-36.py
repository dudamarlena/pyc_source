# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/jishaku/flags.py
# Compiled at: 2020-03-05 23:53:06
# Size of source mod 2**32: 1067 bytes
"""
jishaku.flags
~~~~~~~~~~~~~~

The Jishaku cog base, which contains most of the actual functionality of Jishaku.

:copyright: (c) 2020 Devon (Gorialis) R
:license: MIT, see LICENSE for more details.

"""
import os
ENABLED_SYMBOLS = ('true', 't', 'yes', 'y', 'on', '1')

def enabled(flag: str) -> bool:
    """
    Returns whether an environment flag is enabled.
    """
    return os.getenv(flag, '').lower() in ENABLED_SYMBOLS


JISHAKU_HIDE = enabled('JISHAKU_HIDE')
JISHAKU_RETAIN = enabled('JISHAKU_RETAIN')
JISHAKU_NO_UNDERSCORE = enabled('JISHAKU_NO_UNDERSCORE')
SCOPE_PREFIX = '' if JISHAKU_NO_UNDERSCORE else '_'
JISHAKU_NO_DM_TRACEBACK = enabled('JISHAKU_NO_DM_TRACEBACK')