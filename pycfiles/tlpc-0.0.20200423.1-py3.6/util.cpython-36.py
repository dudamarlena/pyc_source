# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/tlp/util.py
# Compiled at: 2020-04-23 19:40:12
# Size of source mod 2**32: 870 bytes
import shutil, subprocess
from typing import Tuple

def clang_format(code: str, *args: str) -> str:
    """Apply clang-format with given arguments, if possible."""
    for version in range(10, 4, -1):
        clang_format_exe = shutil.which('clang-format-%d' % version)
        if clang_format_exe is not None:
            break
    else:
        clang_format_exe = shutil.which('clang-format')

    if clang_format_exe is not None:
        proc = subprocess.run([clang_format_exe, *args], input=code,
          stdout=(subprocess.PIPE),
          check=True,
          universal_newlines=True)
        proc.check_returncode()
        return proc.stdout
    else:
        return code


def get_instance_name(item: Tuple[(str, int)]) -> str:
    return '_'.join(map(str, item))


def get_module_name(module: str) -> str:
    return f"{module}_{module}"