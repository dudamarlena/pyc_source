# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /srv/RunestoneComponents/runestone/lp/lp.py
# Compiled at: 2020-04-16 12:40:55
# Size of source mod 2**32: 24974 bytes
import re, os
from os import makedirs
from pathlib import Path
import json, pygments
from pygments.lexers import guess_lexer_for_filename
from pygments.formatters import HtmlFormatter
from docutils import nodes
from docutils.transforms import Transform
from docutils.parsers.rst import directives
from docutils.parsers.rst.states import Struct
from CodeChat.CodeToRestSphinx import is_source_code
from CodeChat.CodeToRest import get_lexer
from common.runestonedirective import RunestoneIdDirective, RunestoneNode
from .lp_common_lib import STUDENT_SOURCE_PATH, code_here_comment, SPHINX_CONFIG_NAME
from server.componentdb import addQuestionToDB, addHTMLToDB

def _remove_code_solutions(file_name, src, replacement_func):
    start_token = 'SOLUTION_BEGIN'
    end_token = 'SOLUTION_END'
    lines = src.splitlines(keepends=True)
    current_index = len(lines) - 1
    end_token_index = None
    while current_index >= 0:
        if end_token_index is None:
            if end_token in lines[current_index]:
                end_token_index = current_index
        elif start_token in lines[current_index]:
            del lines[current_index:end_token_index + 1]
            lines.insert(current_index, replacement_func(current_index + 1, end_token_index + 1, file_name))
            end_token_index = None
        current_index -= 1

    return ''.join(lines)


def _assert_has_no_content(self):
    if self.content:
        raise self.error('Content block not allowed for the "%s" directive.' % self.name)


def _source_read(app, docname, source):
    if is_source_code(app.env, docname):
        source[0] = _remove_code_solutions(docname, source[0], _textarea_replacement)


def _textarea_replacement(start_line, end_line, file_name):
    s = TEXTAREA_REPLACEMENT_STRING.format(end_line - 4)
    padding_newlines = end_line - start_line + 1 - s.count('\n')
    if padding_newlines > 0:
        s += '\n' * padding_newlines
    return s


TEXTAREA_REPLACEMENT_STRING = '\n.. raw::\n html\n\n <textarea class="code_snippet"></textarea><br />\n\n..\n\n'

class _LpBuildButtonDirective(RunestoneIdDirective):
    required_arguments = 1
    optional_arguments = 0
    has_content = False
    option_spec = RunestoneIdDirective.option_spec.copy()
    option_spec.update({'include':directives.unchanged, 
     'language':directives.unchanged, 
     'timelimit':directives.unchanged, 
     'stdin':directives.unchanged, 
     'datafile':directives.unchanged, 
     'available_files':directives.unchanged, 
     'builder':directives.unchanged})

    def run(self):
        super(_LpBuildButtonDirective, self).run()
        _assert_has_no_content(self)
        addQuestionToDB(self)
        id_ = self.options['divid']
        self.options['include'] = [x.strip() for x in self.options.get('include', '')]
        env = self.state.document.settings.env
        self.options.setdefault('language', get_lexer(filename=(env.docname)).name)
        self.options.setdefault('timelimit', 25000)
        self.options.setdefault('builder', 'JOBE')
        html = '<div class="runestone">\n    <input type="button" value="Save and run" class="btn btn-success" data-component="lp_build" data-lang="{}" id="{}" />\n    <br />\n    <textarea readonly id="lp-result"></textarea>\n    <br />\n    <div></div>\n</div>'.format(self.options['language'], id_)
        addHTMLToDB(id_, self.options['basecourse'], html, json.dumps(dict(language=(self.options['language']),
          builder=(self.options['builder']),
          timelimit=(self.options['timelimit']),
          include=(self.options['include']),
          source_path=(env.docname),
          sphinx_base_path=(env.app.confdir))))
        raw_node = nodes.raw((self.block_text), html, format='html')
        raw_node.source, raw_node.line = self.state_machine.get_source_and_line(self.lineno)
        return [
         raw_node]


def _doctree_resolved(app, doctree, docname):
    env = app.builder.env
    if is_source_code(env, docname):
        src_path = env.doc2path(docname, None)
        src_abs_path = Path(env.srcdir) / src_path
        with src_abs_path.open(encoding='utf-8') as (f_in):
            str_ = f_in.read()
        runestone_directives_to_remove = []
        for node in doctree.traverse(RunestoneNode):
            parent_node = node.parent
            while 1:
                if parent_node:
                    if isinstance(parent_node, RunestoneNode):
                        break
                    parent_node = parent_node.parent
            else:
                if node.line and node.rawsource:
                    runestone_directives_to_remove += [
                     [
                      node.line, node.line + len(node.rawsource.splitlines())]]

        if runestone_directives_to_remove:
            l = str_.splitlines(keepends=True)
            for fb in reversed(runestone_directives_to_remove):
                del l[fb[0]:fb[1]]

            str_ = ''.join(l)
        str_ = _remove_code_solutions(docname, str_, lambda start_line, end_line, file_name: code_here_comment(file_name))
        dest_path = Path(app.outdir) / STUDENT_SOURCE_PATH / src_path
        makedirs((str(dest_path.parent)), exist_ok=True)
        with dest_path.open('w', encoding='utf-8') as (f_out):
            f_out.write(str_)
        try:
            lexer = guess_lexer_for_filename(docname, str_)
        except pygments.util.ClassNotFound:
            pass
        else:
            cssfile = os.path.relpath('/_static/pygments.css', '/' + str(Path(docname).parent))
            makedirs((app.outdir + '/_static'), exist_ok=True)
            formatter = HtmlFormatter(full=True,
              title=(env.titles[docname]),
              cssfile=cssfile,
              noclobber_cssfile=True)
            pygments_name = Path(app.outdir) / (docname + '-source.html')
            makedirs((str(pygments_name.parent)), exist_ok=True)
            with pygments_name.open('w', encoding='utf-8') as (f_out):
                pygments.highlight(str_, lexer, formatter, f_out)


def _alink_role(roleName, rawtext, text, lineno, inliner, options={}, content=[]):
    m = re.search('(.*\\s+<[^#]+)(#.+)(>\\s*)$', text)
    if not m:
        msg = inliner.reporter.error('Expected "title <refname#anchor>", but saw "{}"'.format(text))
        prb = inliner.problematic(rawtext, rawtext, msg)
        return ([prb], [msg])
    anchor = m.group(2)
    no_anchor_reference = '`' + m.group(1) + '_' + m.group(3) + '`_'
    memo = Struct(reporter=(inliner.reporter),
      document=(inliner.document),
      language=(inliner.language))
    parsed_nodes, system_messages = inliner.parse(no_anchor_reference, lineno, memo, inliner.parent)
    assert isinstance(parsed_nodes[0], nodes.reference)
    assert isinstance(parsed_nodes[1], nodes.target)
    parsed_nodes[0]['anchor'] = anchor
    return (
     parsed_nodes, system_messages)


class ExternalAnchorTargets(Transform):
    __doc__ = '\n    Given:\n\n    .. code-block:: xml\n\n        <paragraph>\n            <reference refname="direct external#anchor">\n                direct external\n        <target id="id1" name="direct external" refuri="http://direct">\n\n    The "refname" attribute is replaced by the direct "refuri" attribute with #anchor appended:\n\n    .. code-block:: xml\n\n        <paragraph>\n            <reference refuri="http://direct#anchor">\n                direct external\n        <target id="id1" name="direct external" refuri="http://direct">\n    '
    default_priority = 639

    def apply(self):
        for target in self.document.traverse(nodes.target):
            if target.hasattr('refuri'):
                refuri = target['refuri']
                for name in target['names']:
                    reflist = self.document.refnames.get(name, [])
                    if reflist:
                        target.note_referenced_by(name=name)
                    for ref in reflist:
                        if ref.resolved:
                            continue
                        del ref['refname']
                        ref['refuri'] = refuri + ref.get('anchor', '')
                        ref.resolved = 1


def _docname_role(roleName, rawtext, text, lineno, inliner, options={}, content=[]):
    env = inliner.document.settings.env
    try:
        p = Path(env.docname)
        path_component = str(getattr(p, text, p))
    except Exception as e:
        try:
            msg = inliner.reporter.error(('Invalid path component {}: {}'.format(text, e)),
              line=lineno)
            prb = inliner.problematic(rawtext, rawtext, msg)
            return ([prb], [msg])
        finally:
            e = None
            del e

    refuri = str(Path(env.docname).name) + '-source.html'
    return ([(nodes.reference)(rawtext, path_component, refuri=refuri, **options)], [])


def setup(app):
    app.setup_extension('CodeChat.CodeToRestSphinx')
    app.add_role('alink', _alink_role)
    app.add_role('docname', _docname_role)
    app.add_transform(ExternalAnchorTargets)
    app.add_directive('lp_build', _LpBuildButtonDirective)
    app.connect('source-read', _source_read)
    app.connect('doctree-resolved', _doctree_resolved)
    with open(SPHINX_CONFIG_NAME, 'w', encoding='utf-8') as (f):
        f.write(json.dumps({'SPHINX_SOURCE_PATH':str(Path(app.srcdir).relative_to(Path.cwd())), 
         'SPHINX_OUT_PATH':str(Path(app.outdir).relative_to(Path.cwd()))}))
    return {'version':'0.0.1', 
     'parallel_read_safe':True}