# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/magical/__init__.py
# Compiled at: 2016-09-07 10:58:39
# Size of source mod 2**32: 312 bytes
from magical.magic import magical
from magical.recipes import register_jinja2_magic, register_mistune_magic, register_yaml_magic
__version__ = '0.0.9'
magical
__all__ = [
 'magical', 'register_jinja2_magic',
 'register_mistune_magic', 'register_yaml_magic']