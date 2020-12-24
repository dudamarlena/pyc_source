# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/dmulholl/dev/src/ivy/ivy/extensions/ivy_jinja.py
# Compiled at: 2019-06-12 17:54:26
# Size of source mod 2**32: 1072 bytes
import sys
from ivy import hooks, site, templates
try:
    import jinja2
except ImportError:
    jinja2 = None

env = None
if jinja2:

    @hooks.register('init')
    def init():
        global env
        settings = {'loader': jinja2.FileSystemLoader(site.theme('templates'))}
        settings.update(site.config.get('jinja', {}))
        env = (jinja2.Environment)(**settings)


    @templates.register('jinja')
    def callback(page, filename):
        template = env.get_template(filename)
        return template.render(page)