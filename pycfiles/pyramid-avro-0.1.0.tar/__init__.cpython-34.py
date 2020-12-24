# uncompyle6 version 3.6.7
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/guillaume/workspace/git/pyramid_asyncio/pyramid_asyncio/scaffolds/__init__.py
# Compiled at: 2015-02-18 15:11:02
# Size of source mod 2**32: 180 bytes
from pyramid.scaffolds import PyramidTemplate

class AioJinja2Template(PyramidTemplate):
    _template_dir = 'aio_jinja2'
    summary = 'Pyramid project using asyncio and jinja2'