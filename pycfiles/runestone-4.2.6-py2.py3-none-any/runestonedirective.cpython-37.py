# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /srv/RunestoneComponents/runestone/common/runestonedirective.py
# Compiled at: 2020-04-16 12:40:55
# Size of source mod 2**32: 14669 bytes
__author__ = 'bmiller'
from collections import defaultdict
import binascii, os
from docutils import nodes
from docutils.parsers.rst import directives
from docutils.parsers.rst import Directive
from docutils.utils import get_source_line
from docutils.statemachine import ViewList
from sphinx import application
from sphinx.errors import ExtensionError
UNNUMBERED_DIRECTIVES = [
 'activecode',
 'reveal',
 'video',
 'youtube',
 'vimeo',
 'codelens',
 'showeval',
 'poll',
 'tabbed',
 'tab',
 'timed',
 'disqus']

class RunestoneNode(nodes.Node):
    pass


class Struct:

    def __init__(self, **kwargs):
        self.__dict__.update(kwargs)

    def __repr__(self):
        args = ['{}={}'.format(k, repr(v)) for k, v in vars(self).items()]
        return 'Struct({})'.format(', '.join(args))


def _get_runestone_data(env):
    if not hasattr(env, 'runestone_data'):
        env.runestone_data = Struct(id_to_page=(dict()),
          page_to_id=(defaultdict(set)))
    return env.runestone_data


def _purge_runestone_data(app, env, docname):
    runestone_data = _get_runestone_data(env)
    for id_ in runestone_data.page_to_id[docname]:
        runestone_data.id_to_page.pop(id_)

    runestone_data.page_to_id.pop(docname)
    env.assesscounter = 0


def _add_autoversion(self, filename):
    for path in self.config._raw_config['html_static_path']:
        full_path = path
        if not os.path.isabs(full_path):
            full_path = os.path.join(self.confdir, full_path)
        if os.path.isdir(path):
            full_path = os.path.join(path, filename)
        else:
            if os.path.normpath(path).endswith(os.path.normpath(filename)):
                full_path = path
            else:
                continue
            try:
                f = open(os.path.join(path, filename), 'rb')
            except IOError:
                continue
            else:
                with f:
                    crc_str = '{:02X}'.format(binascii.crc32(f.read()))
                return '{}?v={}'.format(filename, crc_str)

    raise ExtensionError('Unable to find {} in html_static_path.'.format(filename))


def _add_autoversioned_javascript(self, filename):
    return self.add_javascript(self.add_autoversion(filename))


def _add_autoversioned_stylesheet(self, filename, *args, **kwargs):
    return (self.add_stylesheet)(self.add_autoversion(filename), *args, **kwargs)


application.Sphinx.add_autoversion = _add_autoversion
application.Sphinx.add_autoversioned_javascript = _add_autoversioned_javascript
application.Sphinx.add_autoversioned_stylesheet = _add_autoversioned_stylesheet

def setup(app):
    app.connect('env-purge-doc', _purge_runestone_data)
    app.add_role('skipreading', SkipReading)
    app.add_config_value('runestone_server_side_grading', False, 'env')
    app.add_config_value('generate_component_labels', True, 'env')


class RunestoneDirective(Directive):
    option_spec = {'author':directives.unchanged, 
     'tags':directives.unchanged, 
     'difficulty':directives.positive_int, 
     'autograde':directives.unchanged, 
     'practice':directives.unchanged, 
     'topics':directives.unchanged}

    def __init__(self, *args, **kwargs):
        (super(RunestoneDirective, self).__init__)(*args, **kwargs)
        env = self.state.document.settings.env
        self.srcpath = env.docname
        split_docname = self.srcpath.split('/')
        if len(split_docname) < 2:
            split_docname.append('')
        self.subchapter = split_docname[(-1)]
        self.chapter = split_docname[(-2)]
        self.basecourse = self.state.document.settings.env.config.html_context.get('basecourse', 'unknown')
        self.options['basecourse'] = self.basecourse
        self.options['chapter'] = self.chapter
        self.options['subchapter'] = self.subchapter


class RunestoneIdDirective(RunestoneDirective):

    def getNumber(self):
        env = self.state.document.settings.env
        if self.name in UNNUMBERED_DIRECTIVES or env.config.generate_component_labels is False:
            return ''
        env.assesscounter += 1
        res = 'Q-%d'
        if hasattr(env, 'assessprefix'):
            res = env.assessprefix + '%d'
        res = res % env.assesscounter
        if hasattr(env, 'assesssuffix'):
            res += env.assesssuffix
        return res

    def updateContent(self):
        if self.content:
            if self.content[0][:2] == '..':
                self.content = ViewList([
                 self.options['qnumber'] + ':', ''], self.content.source(0)) + self.content
            else:
                if self.options['qnumber']:
                    self.content[0] = self.options['qnumber'] + ': ' + self.content[0]

    def run(self):
        if not self.required_arguments >= 1:
            raise AssertionError
        else:
            if 'divid' not in self.options:
                id_ = self.options['divid'] = self.arguments[0]
            else:
                id_ = self.options['divid']
            self.options['qnumber'] = self.getNumber()
            env = self.state.document.settings.env
            runestone_data = _get_runestone_data(env)
            id_to_page = runestone_data.id_to_page
            page_to_id = runestone_data.page_to_id
            if id_ in id_to_page:
                page = id_to_page[id_]
                if page.docname != env.docname or page.lineno != self.lineno:
                    raise self.error('Duplicate ID -- see {}, line {}'.format(page.docname, page.lineno))
                assert id_ in page_to_id[page.docname]
            else:
                id_to_page[id_] = Struct(docname=(env.docname), lineno=(self.lineno))
                page_to_id[env.docname].add(id_)


def first_time(app, *keys):
    key = '$'.join(keys)
    if not hasattr(app, 'runestone_flags'):
        app.runestone_flags = set()
    if key not in app.runestone_flags:
        app.runestone_flags.add(key)
        return True
    return False


def add_i18n_js(app, supported_langs, *i18n_resources):
    if first_time(app, 'add_i18n_js'):
        app.add_autoversioned_javascript('jquery_i18n/CLDRPluralRuleParser.js')
        app.add_autoversioned_javascript('jquery_i18n/jquery.i18n.js')
        app.add_autoversioned_javascript('jquery_i18n/jquery.i18n.messagestore.js')
        app.add_autoversioned_javascript('jquery_i18n/jquery.i18n.fallbacks.js')
        app.add_autoversioned_javascript('jquery_i18n/jquery.i18n.language.js')
        app.add_autoversioned_javascript('jquery_i18n/jquery.i18n.parser.js')
        app.add_autoversioned_javascript('jquery_i18n/jquery.i18n.emitter.js')
        app.add_autoversioned_javascript('jquery_i18n/jquery.i18n.emitter.bidi.js')
    for res in i18n_resources:
        if first_time(app, 'add_i18n_js', res):
            app.add_autoversioned_javascript(res + '.en.js')
            if app.config.language and app.config.language != 'en' and app.config.language in supported_langs:
                app.add_autoversioned_javascript(res + '.' + app.config.language + '.js')


def add_skulpt_js(app):
    if first_time(app, 'add_skulpt_js'):
        app.add_autoversioned_javascript('skulpt.min.js')
        app.add_autoversioned_javascript('skulpt-stdlib.js')
        app.add_javascript('https://cdn.jsdelivr.net/npm/vega@4.0.0-rc.2/build/vega.js')
        app.add_javascript('https://cdn.jsdelivr.net/npm/vega-lite@2.5.0/build/vega-lite.js')
        app.add_javascript('https://cdn.jsdelivr.net/npm/vega-embed@3.14.0/build/vega-embed.js')


def get_node_line(node):
    return get_source_line(node)[1]


def SkipReading(roleName, rawtext, text, lineno, inliner, options={}, content=[]):
    docname = inliner.document.settings.env.docname
    if not hasattr(inliner.document.settings.env, 'skipreading'):
        inliner.document.settings.env.skipreading = set()
    print('ADDING {} to skipreading'.format(docname))
    inliner.document.settings.env.skipreading.add(docname)
    return ([], [])