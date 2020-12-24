# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/attakei/works/errbot/devel-plugins/backends/webapp/build/lib/errbot_backend_webapp/__init__.py
# Compiled at: 2019-06-24 11:10:36
# Size of source mod 2**32: 154 bytes
from pathlib import Path
__version__ = '0.0.4-alpha.0'

def get_plugin_dir() -> str:
    module_dir = Path(__file__).parent
    return str(module_dir)