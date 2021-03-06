# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/fsc/work/devel/flamingo/flamingo/plugins/rst/bootstrap3.py
# Compiled at: 2020-02-08 07:33:40
# Size of source mod 2**32: 4334 bytes
import re
from docutils.parsers.rst import directives
from docutils.nodes import raw
from .base import NestedDirective

def _gen_directives(context):

    class Container(NestedDirective):

        def run(self):
            nodes = super().run(context)
            nodes.insert(0, raw('', '<div>', format='html'))
            nodes.append(raw('', '<div class="clearfix"></div></div>', format='html'))
            return nodes

    class BootstrapRow(NestedDirective):

        def run(self):
            nodes = super().run(context)
            nodes.insert(0, raw('', '<div class="row">', format='html'))
            nodes.append(raw('', '</div>', format='html'))
            return nodes

    class BootstrapCol(NestedDirective):
        required_arguments = 1
        argument_re = re.compile('(xs|sm|md|lg)-([0-9]{1,2})')

        def parse_argument(self, argument):
            try:
                match = self.argument_re.search(argument)
                if match:
                    aspect, size = match.groups()
                    size = int(size)
                    if 0 < size < 13:
                        return (aspect, size)
            except Exception:
                pass

            raise ValueError("'{}' is no valid Bootstrap3 col".format(argument))

        def run(self):
            nodes = super().run(context)
            aspect, size = self.parse_argument(self.arguments[0])
            nodes.insert(0, raw('', ('<div class="col-{}-{}">'.format(aspect, size)), format='html'))
            nodes.append(raw('', '<div class="clearfix"></div></div>', format='html'))
            return nodes

    class Youtube(NestedDirective):
        has_content = False
        required_arguments = 1
        option_spec = {'privacy-enhanced-mode': directives.unchanged}
        template = '\n            <div class="embed-responsive embed-responsive-16by9">\n                <iframe class="embed-responsive-item" src="{url}"></iframe>\n            </div>\n        '

        def run(self):
            privacy_enhanced_mode = getattr(context.settings, 'RSTBOOTSTRAP3_YOUTUBE_PRIVACY_ENHANCED_MODE', True)
            if 'privacy-enhanced-mode' in self.options:
                _privacy_enhanced_mode = self.options.get('privacy_enhanced_mode').strip().lower()
                privacy_enhanced_mode = {'true':True, 
                 '1':True, 
                 'false':False, 
                 '0':False}[_privacy_enhanced_mode]
            url = 'https://www.youtube{}.com/embed/{}'.format('-nocookie' if privacy_enhanced_mode else '', self.arguments[0].strip())
            return [
             raw('', self.template.format(url=url), format='html')]

    class Alert(NestedDirective):
        has_content = True
        required_arguments = 1

        def run(self):
            valid_alert_types = ('success', 'info', 'warning', 'danger')
            alert_type = self.arguments[0].strip()
            if alert_type not in valid_alert_types:
                raise ValueError("'{}' is no valid alert type ({})".format(alert_type, ', '.join(valid_alert_types)))
            return [
             
              raw('', ('<div class="alert alert-{}" role="alert">'.format(alert_type)),
                format='html'),
             *super().run(context),
             
              raw('', '</div>', format='html')]

    return (
     Container,
     BootstrapRow,
     BootstrapCol,
     Youtube,
     Alert)


class rstBootstrap3:

    def parser_setup(self, context):
        Container, BootstrapRow, BootstrapCol, Youtube, Alert = _gen_directives(context)
        directives.register_directive('div', Container)
        directives.register_directive('row', BootstrapRow)
        directives.register_directive('col', BootstrapCol)
        directives.register_directive('youtube', Youtube)
        directives.register_directive('alert', Alert)