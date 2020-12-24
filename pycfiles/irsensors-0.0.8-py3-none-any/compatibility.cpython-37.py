# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\ISEN\AppData\Local\Temp\pip-install-whg15vss\serial\serial\utilities\compatibility.py
# Compiled at: 2019-09-23 04:34:10
# Size of source mod 2**32: 845 bytes
from __future__ import nested_scopes, generators, division, absolute_import, with_statement, print_function, unicode_literals
import inspect
BACKWARDS_COMPATIBILITY_IMPORTS = '\n'.join(('# region Backwards Compatibility', 'from __future__ import nested_scopes, generators, division, absolute_import, with_statement, \\',
                                             '   print_function, unicode_literals',
                                             'from future import standard_library',
                                             'standard_library.install_aliases()',
                                             'from future.builtins import *', '# endregion'))

def backport():
    frame_info = inspect.stack()[1]
    try:
        frame = frame_info.frame
    except AttributeError:
        frame = frame_info[0]

    exec(BACKWARDS_COMPATIBILITY_IMPORTS, frame.f_globals, frame.f_locals)