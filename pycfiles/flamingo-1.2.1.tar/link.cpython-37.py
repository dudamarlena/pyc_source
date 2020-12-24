# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/fsc/work/devel/flamingo/flamingo/plugins/rst/link.py
# Compiled at: 2020-04-28 06:15:31
# Size of source mod 2**32: 2634 bytes
from urllib.parse import urlparse
from docutils.parsers.rst import roles
from docutils.nodes import raw
from .utils import parse_role_text, parse_bool

class LinkRole:
    options = {}

    def __init__(self, context):
        self.context = context
        self.rst_base_plugin = self.context.plugins.get_plugin('reStructuredText')

    def __call__(self, name, rawtext, text, lineno, inliner):
        role_args = parse_role_text(text)
        options = role_args['options']
        if len(role_args['args']) == 1:
            target = role_args['args'][0]
            name = ''
        else:
            name, target = role_args['args']
        result = urlparse(target)
        if result.scheme:
            if not name:
                name = target
            return (
             [
              raw('',
                ('<a href="{}">{}</a>'.format(target, name)),
                format='html')], [])
        abs_lineno = self.rst_base_plugin.offsets.get(self.context.content['path'], 0) + lineno
        if not (self.context.settings.PRE_RENDER_CONTENT and self.context.content.get('is_template', True)):
            self.context.logger.error('%s:%s: LinkError: internal links depend on content pre rendering which is disabled by your %s', self.context.content['path'], abs_lineno, 'settings' if not self.context.settings.PRE_RENDER_CONTENT else 'content file')
        options['_content_path'] = self.context.content['path']
        options['_content_lineno'] = abs_lineno
        if 'i18n' in options:
            options['i18n'] = parse_bool(options['i18n'])
        if 'find_name' in options:
            options['find_name'] = parse_bool(options['find_name'])
        if 'find_name' not in options:
            options['find_name'] = True
        return (
         [
          raw('',
            ("{{{{ link(path='{}', name='{}', {}) }}}}".format(target, name, ', '.join(['{}={}'.format(k, repr(v)) for k, v in options.items()]))),
            format='html')], [])


class rstLink:

    def parser_setup(self, context):
        roles.register_canonical_role('link', LinkRole(context))