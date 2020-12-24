# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/dmulholl/dev/src/ivy/ivy/extensions/ivy_ibis.py
# Compiled at: 2019-10-28 14:34:25
# Size of source mod 2**32: 770 bytes
import sys
from ivy import hooks, templates, site
try:
    import ibis
except ImportError:
    ibis = None

if ibis:

    @hooks.register('init')
    def init():
        ibis.config.loader = ibis.loaders.FileLoader(site.theme('templates'))


    @templates.register('ibis')
    def callback(page, filename):
        template = ibis.config.loader(filename)
        return template.render(page)