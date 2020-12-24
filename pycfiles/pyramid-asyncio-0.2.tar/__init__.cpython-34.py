# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/guillaume/workspace/git/pyramid_asyncio/pyramid_asyncio/scaffolds/__init__.py
# Compiled at: 2015-02-18 15:11:02
# Size of source mod 2**32: 180 bytes
from pyramid.scaffolds import PyramidTemplate

class AioJinja2Template(PyramidTemplate):
    _template_dir = 'aio_jinja2'
    summary = 'Pyramid project using asyncio and jinja2'