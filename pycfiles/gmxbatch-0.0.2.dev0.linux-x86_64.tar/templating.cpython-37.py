# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /opt/miniconda3/envs/gmxbatch/lib/python3.7/site-packages/gmxbatch/templating.py
# Compiled at: 2020-02-28 04:29:11
# Size of source mod 2**32: 276 bytes
"""A global Jinja2 Environment instance used by gmxbatch at various places"""
import jinja2
jinjaenv = jinja2.Environment(loader=(jinja2.PackageLoader('gmxbatch', 'resource')), trim_blocks=False,
  lstrip_blocks=False,
  keep_trailing_newline=False)