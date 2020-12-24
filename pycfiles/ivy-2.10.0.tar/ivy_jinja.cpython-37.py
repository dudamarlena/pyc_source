# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/dmulholl/dev/src/ivy/ivy/extensions/ivy_jinja.py
# Compiled at: 2020-04-05 16:34:25
# Size of source mod 2**32: 1060 bytes
import sys, ivy
try:
    import jinja2
except ImportError:
    jinja2 = None

env = None
if jinja2:

    @ivy.hooks.register('init')
    def init():
        global env
        settings = {'loader': jinja2.FileSystemLoader(ivy.site.theme('templates'))}
        settings.update(ivy.site.config.get('jinja', {}))
        env = (jinja2.Environment)(**settings)


    @ivy.templates.register('jinja')
    def callback(page, filename):
        template = env.get_template(filename)
        return template.render(page)