# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/dmulholl/dev/src/ivy/ivy/extensions/ivy_ibis.py
# Compiled at: 2020-04-05 16:36:38
# Size of source mod 2**32: 775 bytes
import sys, ivy
try:
    import ibis
except ImportError:
    ibis = None
else:
    if ibis:

        @ivy.hooks.register('init')
        def init():
            ibis.config.loader = ibis.loaders.FileLoader(ivy.site.theme('templates'))


        @ivy.templates.register('ibis')
        def callback(page, filename):
            template = ibis.config.loader(filename)
            return template.render(page)