# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/luke/Code/OSS/django-pgfields/docs/_ext/pgfields_docs.py
# Compiled at: 2014-05-21 13:29:17
# Size of source mod 2**32: 2001 bytes
import os
from sphinx import addnodes
from sphinx.util.compat import Directive

def setup(app):
    app.add_directive('versionadded', NewInVersionDirective)
    app.add_directive('versionmodified', ChangedInVersionDirective)
    app.add_config_value('next_version', '1.5', True)


class NewInVersionDirective(Directive):
    __doc__ = 'Directive class for adding version notes.'
    has_content = True
    required_arguments = 1
    optional_arguments = 1
    final_argument_whitespace = True
    option_spec = {}
    _prefix = 'New in'

    def run(self):
        """Translate the directive to the appropriate markup."""
        answer = []
        if len(self.arguments) != 1:
            raise self.error('%s takes exactly one argument.' % self.name)
        env = self.state.document.settings.env
        if self.arguments[0] == env.config.next_version:
            version = 'Development'
            version_string = 'development version'
        else:
            version = self.arguments[0]
            version_string = 'version %s' % version
        kwargs = {}
        if not os.environ.get('READTHEDOCS', None):
            kwargs['text'] = '%s %s.' % (self._prefix, version_string)
        node = addnodes.versionmodified(**kwargs)
        answer.append(node)
        node['type'] = self.name
        node['version'] = version
        node['style'] = 'font-size: 60%; text-style: italic;'
        return answer


class ChangedInVersionDirective(NewInVersionDirective):
    _prefix = 'Changed in'