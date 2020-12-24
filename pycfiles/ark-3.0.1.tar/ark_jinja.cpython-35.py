# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/dmlhllnd/dev/src/ark/ark/ext/ark_jinja.py
# Compiled at: 2016-09-06 05:15:48
# Size of source mod 2**32: 1767 bytes
import sys
from ark import hooks, templates, site
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
        env = jinja2.Environment(**settings)


    @templates.register('jinja')
    def callback(page, filename):
        try:
            template = env.get_template(filename)
            return template.render(page)
        except jinja2.TemplateError as err:
            msg = '------------------------\n'
            msg += '  Jinja Template Error  \n'
            msg += '------------------------\n\n'
            msg += '  Template: %s\n' % filename
            msg += '  Page:     %s\n\n' % page['path']
            msg += '  %s: %s' % (err.__class__.__name__, err)
            if err.__context__:
                cause = err.__context__
                msg += '\n\nThe following cause was reported:\n\n'
                msg += '%s: %s' % (cause.__class__.__name__, cause)
            sys.exit(msg)