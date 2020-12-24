# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/sphinxcontrib/drops.py
# Compiled at: 2018-11-27 11:21:13
# Size of source mod 2**32: 33031 bytes
"""
    drops
    ~~~~~~~~~~~~~~~~~~~

    Allow DROPS images to be included in Sphinx-generated documents inline.
    Based on the spinx.ext.graphviz extenstion.

    :copyright: Copyright 2007-2017 by the Sphinx team and Michael Tesch, see AUTHORS.
    :license: BSD, see LICENSE for details.
"""
from __future__ import print_function
import re, sys, json, codecs, posixpath
from os import path
from subprocess import Popen, PIPE
from hashlib import sha1
from docutils import nodes
from docutils.parsers.rst import Directive, directives
from docutils.statemachine import ViewList
import sphinx
from sphinx.errors import SphinxError
from sphinx.locale import _, __
from sphinx.util import logging
from sphinx.util.i18n import search_image_for_language
from sphinx.util.osutil import ensuredir, ENOENT, EPIPE, EINVAL
from docutils.parsers.rst.roles import set_classes
logger = logging.getLogger(__name__)

class DropsError(SphinxError):
    category = 'Drops error'


def nspin_from_pton(pton):
    nspin = 1
    pattern = re.compile('I([0-9]+)([xyzeabpm])')
    for m in re.finditer(pattern, pton):
        nspin = max(nspin, int(m.group(1)))

    pattern = re.compile('\\b(E(4|8))\\b')
    for m in re.finditer(pattern, pton):
        Esize = int(m.group(2))
        if Esize == 4:
            nspin = max(nspin, 2)
        else:
            if Esize == 8:
                nspin = max(nspin, 3)

    return nspin


def pton_remove_latex(pton):
    pton = re.sub('\\\\', '', pton)
    pton = re.sub('\\newline', '', pton)
    return pton


def latex_from_pton(pton):
    latex = re.sub('I([0-9]+[xyze])', 'I_{\\1}', pton)
    latex = re.sub('I([0-9]+)a', 'I_{\\1}^{\\\\alpha}', latex)
    latex = re.sub('I([0-9]+)b', 'I_{\\1}^{\\\\beta}', latex)
    latex = re.sub('I([0-9]+)p', 'I_{\\1}^{+}', latex)
    latex = re.sub('I([0-9]+)m', 'I_{\\1}^{-}', latex)
    latex = re.sub('\\bJ(\\d\\d)\\b', 'J_{\\1}', latex)
    latex = re.sub('\\b([^\\\\])pi\\b', '\\1 \\pi ', latex)
    latex = re.sub('\\*', ' \\cdot ', latex)
    latex = latex.replace('\n', ' ')
    latex = latex.replace('\r', ' ')
    return latex


def guess_length(width_str, nom_len):
    """ Convert `width_str` to some pixel width for image creation. """
    match = re.match('^(\\d+\\.?\\d*)\\s*(\\S*)$', width_str)
    if not match:
        raise ValueError
    else:
        res = width_str
        amount, unit = match.groups()[:2]
        float(amount)
        if unit in ('', 'px'):
            res = '%d' % float(amount)
        else:
            if unit == 'pt':
                res = '%d' % float(amount)
            else:
                if unit == '%':
                    res = '%d' % (nom_len * float(amount) / 100.0)
                else:
                    raise ValueError
    return res


class drops(nodes.General, nodes.Inline, nodes.Element):
    pass


def figure_wrapper(directive, node, caption):
    figure_node = nodes.figure('', node)
    if 'align' in node:
        figure_node['align'] = node.attributes.pop('align')
    parsed = nodes.Element()
    directive.state.nested_parse(ViewList([caption], source=''), directive.content_offset, parsed)
    caption_node = (nodes.caption)(parsed[0].rawsource, '', *parsed[0].children)
    caption_node.source = parsed[0].source
    caption_node.line = parsed[0].line
    if 'classes' in node['options']:
        caption_node['classes'] += node['options']['classes']
    figure_node += caption_node
    return figure_node


def align_spec(argument):
    return directives.choice(argument, ('left', 'center', 'right'))


class Drops(Directive):
    __doc__ = '\n    Directive to insert arbitrary pton markup.\n    '
    has_content = True
    required_arguments = 0
    optional_arguments = 0
    final_argument_whitespace = False
    option_spec = {'alt':directives.unchanged, 
     'align':align_spec, 
     'caption':directives.unchanged, 
     'drops_spindrops':directives.unchanged, 
     'name':directives.unchanged, 
     'link':bool, 
     'pdir':str, 
     'prefs':directives.unchanged, 
     'sequence':str, 
     'window':str, 
     'view':str, 
     'nspin':directives.unchanged, 
     'time':float, 
     'event':str, 
     'height':directives.length_or_unitless, 
     'width':directives.length_or_percentage_or_unitless, 
     'aspect':directives.percentage, 
     'class':directives.class_option}

    def run(self):
        document = self.state.document
        if self.arguments:
            if self.content:
                return [
                 document.reporter.warning((__('Drops directive cannot have both content and a filename argument')),
                   line=(self.lineno))]
            env = self.state.document.settings.env
            argument = search_image_for_language(self.arguments[0], env)
            rel_filename, filename = env.relfn2path(argument)
            env.note_dependency(rel_filename)
            try:
                with codecs.open(filename, 'r', 'utf-8') as (fp):
                    pton = fp.read()
            except (IOError, OSError):
                return [
                 document.reporter.warning((__('External Drops file %r not found or reading it failed') % filename),
                   line=(self.lineno))]

        else:
            pton = ' '.join(self.content)
            if not pton.strip():
                return [
                 self.state_machine.reporter.warning((__('Ignoring "drops" directive without content.')),
                   line=(self.lineno))]
            else:
                set_classes(self.options)
                node = drops((self.block_text), **self.options)
                pton = pton.replace(' ', '').replace('\n', '')
                node['code'] = pton
                node['options'] = self.options
                if 'drops_spindrops' in self.options:
                    node['options']['drops_spindrops'] = self.options['drops_spindrops']
                if 'alt' in self.options:
                    node['alt'] = self.options['alt']
                if 'align' in self.options:
                    node['align'] = self.options['align']
                if 'width' in self.options:
                    node['width'] = self.options['width']
                if 'caption' in self.options:
                    caption = self.options.get('caption')
                else:
                    if 'sequence' in self.options or 'time' in self.options:
                        caption = ':pton:`\\rho_0 = %s`' % node['code']
                    else:
                        caption = ':pton:`%s`' % node['code']
            if caption:
                node = figure_wrapper(self, node, caption)
            self.add_name(node)
            if re.match('−|·', pton):
                return [node,
                 self.state_machine.reporter.warning((__('"drops" directive contains unicode operator(s) {−,·}')),
                   line=(self.lineno))]
            else:
                return [
                 node]


class DropsSimple(Directive):
    __doc__ = '\n    Directive to insert inline drops image.\n    '
    has_content = True
    required_arguments = 1
    optional_arguments = 0
    final_argument_whitespace = False
    option_spec = {'alt':directives.unchanged, 
     'align':align_spec, 
     'caption':directives.unchanged, 
     'drops_spindrops':directives.unchanged, 
     'name':directives.unchanged, 
     'link':bool, 
     'pdir':str, 
     'window':str, 
     'view':str, 
     'nspin':int, 
     'time':float, 
     'sequence':str, 
     'event':str, 
     'prefs':directives.unchanged, 
     'height':directives.length_or_unitless, 
     'width':directives.length_or_percentage_or_unitless, 
     'aspect':directives.percentage, 
     'class':directives.class_option}

    def run(self):
        node = drops((self.block_text), **self.options)
        node['code'] = '%s %s {\n%s\n}\n' % (
         self.name, self.arguments[0], '\n'.join(self.content))
        node['options'] = {}
        if 'drops_spindrops' in self.options:
            node['options']['drops_spindrops'] = self.options['drops_spindrops']
        else:
            if 'alt' in self.options:
                node['alt'] = self.options['alt']
            else:
                if 'align' in self.options:
                    node['align'] = self.options['align']
                if 'width' in self.options:
                    node['width'] = self.options['width']
            if 'caption' in self.options:
                caption = self.options.get('caption')
            else:
                caption = ':pton:`%s`' % node['code']
        if caption:
            node = figure_wrapper(self, node, caption)
        self.add_name(node)
        return [node]


import hashlib

def file_hash(filename):
    h = sha1()
    with open(filename, 'rb', buffering=0) as (f):
        for b in iter(lambda : f.read(131072), b''):
            h.update(b)
            return h.hexdigest()


def render_drops(self, code, options, format, prefix='drops'):
    """Render drops code into a PNG output file."""
    if format not in 'png':
        raise DropsError(__("drops_output_format must be one of 'png', '', but is %r") % format)
    else:
        drops_spindrops = options.get('drops_spindrops', self.builder.config.drops_spindrops)
        hashkey = (code + str(options) + str(drops_spindrops) + str(self.builder.config.drops_spindrops_args)).encode('utf-8')
        tag = ''
        for ch in code:
            if re.match('[a-zA-Z0-9]', ch):
                tag += ch
            else:
                if ch == '.':
                    tag += '_'

        fname = '%s-%s-%s.%s' % (prefix, tag, sha1(hashkey).hexdigest()[0:15], format)
        relfn = posixpath.join(self.builder.imgpath, fname)
        outfn = path.join(self.builder.outdir, self.builder.imagedir, fname)
        dfname = path.join(self.builder.outdir, self.builder.imagedir, fname + '.out')
        if hasattr(self.builder, '_drops_warned_spindrops'):
            if self.builder._drops_warned_spindrops.get(drops_spindrops):
                return (None, None)
        if 'nspin' in options:
            nspin = int(str(options['nspin']).split(';')[0])
            system_settings = str(options['nspin']).split(';')[1:]
        else:
            nspin = nspin_from_pton(code)
            system_settings = []
        sdevent = {'Spin System': {'Channels':[i + 1 for i in range(nspin)], 
                         'Initial State':code, 
                         'Offsets (Hz)':[i for i in range(nspin)], 
                         'Nuclei':['n' + str(i + 1) for i in range(nspin)], 
                         'Labels':['I' + str(i + 1) for i in range(nspin)], 
                         'Couplings (Hz)':[]}}
        for setting in system_settings:
            if len(setting) == 0:
                continue
            else:
                try:
                    s_name, s_val = [s.strip() for s in setting.split('=')]
                    s_val = float(s_val)
                except Exception as ex:
                    raise DropsError(__('nspin arg must be type,J12,J13,J23,v{123}=val; but is %r') % setting)

                if s_name == 'J12':
                    sdevent['Spin System']['Couplings (Hz)'].append(['jcoupling', 0, 1, s_val, False])
                if s_name == 'J13':
                    sdevent['Spin System']['Couplings (Hz)'].append(['jcoupling', 0, 2, s_val, False])
                if s_name == 'J23':
                    sdevent['Spin System']['Couplings (Hz)'].append(['jcoupling', 1, 2, s_val, False])
                if s_name[0] == 'v':
                    sdevent['Spin System']['Offsets (Hz)'][int(s_name[1:]) - 1] = s_val
            if s_name == 'Homonuclear':
                sdevent['Spin System']['Channels'] = [
                 1]
                sdevent['Spin System']['Offsets (Hz)'] = [i for i in range(nspin)]
                sdevent['Spin System']['Nuclei'] = ['n1' for i in range(nspin)]
                sdevent['Spin System']['Labels'] = ['I' + str(i + 1) for i in range(nspin)]

        if not len(system_settings):
            for i in range(nspin):
                for j in range(i + 1, nspin):
                    sdevent['Spin System']['Couplings (Hz)'].append(['jcoupling', i, j, i + j, False])

        if nspin == 1:
            aspect = 1.3333333333333333
        else:
            if nspin == 2:
                aspect = 1.3333333333333333
            else:
                aspect = 1.3333333333333333
            prefs_dir = 'doc' + str(nspin)
            if 'time' in options:
                sdevent['Spin System']['Tick'] = int(options['time'] * 1000000000.0)
            if 'sequence' in options or 'window' in options:
                sdevent['action'] = 'MainFrame'
            else:
                sdevent['action'] = 'SingleFrame'
            if 'pdir' in options:
                prefs_dir = options['pdir']
            if 'aspect' in options:
                aspect = options['aspect'] / 100.0
            if isinstance(self.builder.config.drops_nominal_width, dict):
                width = self.builder.config.drops_nominal_width.get('default', 600)
                width = self.builder.config.drops_nominal_width.get(self.builder.name, width)
            else:
                width = self.builder.config.drops_nominal_width
            if 'width' in options:
                width = guess_length(options['width'], width)
            height = float(width) / aspect
            if 'height' in options:
                height = guess_length(options['height'], height)
            spindrops_args = []
            if 'prefs' in options:
                for prefsetting in options['prefs'].split(';'):
                    prefsetting = prefsetting.strip()
                    if not len(prefsetting):
                        continue
                    tmp = prefsetting.split('=')
                    if len(tmp) != 2:
                        return [document.reporter.warning((__('Drops :prefs: option malformed:' + prefsetting)),
                           line=(self.lineno))]
                    prefname, prefvalue = [x.strip() for x in tmp]
                    pref = '{"name":"' + prefname + '", "value":' + prefvalue + '}'
                    spindrops_args.extend(['-s', pref])

            if 'sequence' in options:
                if '{' not in options['sequence']:
                    sdevent['Spin System']['Sequence'] = options['sequence']
                else:
                    print('encoding ' + str(options['sequence']))
                    seqevent = {'action':'sequence_obj',  'Sequence Obj':json.loads(options['sequence'])}
                    spindrops_args.extend(['-a', json.dumps(seqevent)])
            spindrops_args.extend(['-a', json.dumps(sdevent)])
            if 'window' in options:
                for window in options['window'].split(';'):
                    winevent = {'action':'OpenWindow', 
                     'window':window.strip()}
                    spindrops_args.extend(['-a', json.dumps(winevent)])

            if 'view' in options:
                match = re.match('^([ABCD]?)([pqr]?)(\\d*).*$', options['view'])
                if not match:
                    raise ValueError
                world = match.groups()[0]
                view_scale = match.groups()[2]
                if len(view_scale):
                    view_scale = int(view_scale) / 100.0
                    view = match.groups()[1] if len(match.groups()[1]) else 'p'
                else:
                    view_scale = 1.0
                    view = match.groups()[1]
                worlds = {'A':[
                  [
                   1, 0, 0, 0],
                  [
                   0, 1, 0, 0],
                  [
                   0, 0, 1, 0],
                  [
                   0, 0, 0, 1]], 
                 'B':[
                  [
                   1, 0, 0, 0],
                  [
                   0, 0.9063, 0.4226, 0],
                  [
                   0, -0.4226, 0.9063, 0],
                  [
                   0, 0, 0, 1]], 
                 'C':[
                  [
                   1, 0, 0, 0],
                  [
                   0, 0.259, 0.966, 0],
                  [
                   0, -0.966, 0.259, 0],
                  [
                   0, 0, 0, 1]], 
                 'D':[
                  [
                   1, 0, 0, 0],
                  [
                   0, 0, 1, 0],
                  [
                   0, -1, 0, 0],
                  [
                   0, 0, 0, 1]]}
                views = {'p':[
                  [
                   1, 0, 0, 0],
                  [
                   0, 1, 0, 0.2],
                  [
                   0, 0, 1, -20 / view_scale],
                  [
                   0, 0, 0, 1]], 
                 'q':[
                  [
                   1, 0, 0, 0],
                  [
                   0, 1, 0, -2],
                  [
                   0, 0, 1, -12 / view_scale],
                  [
                   0, 0, 0, 1]], 
                 'r':[
                  [
                   1, 0, 0, -2.5],
                  [
                   0, 1, 0, 0.2],
                  [
                   0, 0, 1, -20 / view_scale],
                  [
                   0, 0, 0, 1]]}
                if world in worlds:
                    pref = '{"name":"World", "value":' + str(worlds[world]) + '}'
                    spindrops_args.extend(['-s', pref])
                if view in views:
                    pref = '{"name":"View", "value":' + str(views[view]) + '}'
                    spindrops_args.extend(['-s', pref])
            if 'event' in options:
                for event in options['event'].split(';'):
                    sdevent2 = {'action':'event', 
                     'EventStr':event.strip()}
                    spindrops_args.extend(['-a', json.dumps(sdevent2)])

            if 'link' in options:
                link = options['link']
            else:
                link = None
        if sdevent['action'] == 'MainFrame' and link != False or link:
            import urllib
            options['cmdline'] = '&'.join(urllib.parse.quote(x) for x in spindrops_args)
    if path.isfile(outfn):
        print('cached drop: ' + outfn)
        return (
         relfn, outfn)
    else:
        ensuredir(path.dirname(outfn))
        print("creating drop '" + code + "', options:", str(options), 'fname:', fname)
        if isinstance(drops_spindrops, str):
            spindrops_args2 = [
             drops_spindrops]
        else:
            spindrops_args2 = drops_spindrops
        spindrops_args2.extend(self.builder.config.drops_spindrops_args)
        if path.isdir(prefs_dir):
            spindrops_args2.extend(['-p', prefs_dir])
        spindrops_args2.extend(['-a', '{"action":"size", "size":[' + str(width) + ',' + str(height) + ']}'])
        spindrops_args[0:0] = spindrops_args2
        spindrops_args.extend(['-a', '{"action":"savepng", "filename":"' + outfn + '"}',
         '-a', '{"action":"quit"}'])
        try:
            p = Popen(spindrops_args, stdout=PIPE, stdin=PIPE, stderr=PIPE)
        except OSError as err:
            if err.errno != ENOENT:
                raise
            raise DropsError(__('SpinDrops command %r cannot be run' % drops_spindrops))
            logger.warning(__('SpinDrops command %r cannot be run (needed for drops output), check the drops_spindrops setting'), drops_spindrops)
            if not hasattr(self.builder, '_drops_warned_spindrops'):
                self.builder._drops_warned_spindrops = {}
            self.builder._drops_warned_spindrops[drops_spindrops] = True
            return (None, None)

        try:
            stdout, stderr = p.communicate()
        except (OSError, IOError) as err:
            if err.errno not in (EPIPE, EINVAL):
                raise
            stdout, stderr = p.stdout.read(), p.stderr.read()
            p.wait()

        if p.returncode != 0:
            raise DropsError(__('SpinDrops (%s) exited with error:\n[stderr]\n%s\n[stdout]\n%s') % (
             ' '.join("'" + ar + "'" for ar in spindrops_args),
             stderr.decode(), stdout.decode()))
        with open(dfname, 'w+') as (f):
            f.write(' '.join("'" + ar + "'" for ar in spindrops_args) + '\n')
            f.write('\nsize:\n')
            f.write(str(self.builder.config.drops_nominal_width))
            f.write(str(self.builder.name))
            f.write('\nstdout:\n')
            f.write(stdout.decode())
            f.write('stderr:\n')
            f.write(stderr.decode())
        if not path.isfile(outfn):
            raise DropsError(__('SpinDrops did not produce an output file:\n[stderr]\n%s\n[stdout]\n%s') % (
             stderr, stdout))
        return (
         relfn, outfn)


def render_drops_html(self, node, code, options, prefix='drops', imgcls=None, alt=None):
    output_format = self.builder.config.drops_output_format
    spindrops_url = self.builder.config.drops_spindrops_url
    try:
        if output_format not in 'png':
            raise DropsError(__("drops_output_format must be one of 'png', '', but is %r") % output_format)
        fname, outfn = render_drops(self, code, options, output_format, prefix)
    except DropsError as exc:
        logger.warning('pton %r: ' % code + str(exc))
        raise nodes.SkipNode

    if fname is None:
        self.body.append(self.encode(code))
    else:
        if alt is None:
            alt = node.get('alt', pton_remove_latex(self.encode(code).strip()))
        classes = []
    if imgcls:
        classes += imgcls
    else:
        if 'classes' in options:
            classes += options['classes']
        if len(classes):
            imgcss = 'class="%s"' % ' '.join(classes)
        else:
            imgcss = ''
    if output_format == 'svg':
        svgtag = '<object data="%s" type="image/svg+xml">\n            <p class="warning">%s</p></object>\n' % (fname, alt)
        self.body.append(svgtag)
    else:
        if 'align' in node:
            self.body.append('<div align="%s" class="align-%s">' % (
             node['align'], node['align']))
        else:
            if 'cmdline' in options:
                getargs = options['cmdline']
                self.body.append('<a href="%s/SpinDrops.html?%s" target="_blank">\n' % (spindrops_url, getargs))
                title = alt + ', click to open in SpinDrops-web'
            else:
                title = alt
        self.body.append('<img src="%s" alt="%s" title="%s" %s/>\n' % (fname, alt, title, imgcss))
    if 'cmdline' in options:
        self.body.append('</a>\n')
    if 'align' in node:
        self.body.append('</div>\n')
    raise nodes.SkipNode


def html_visit_drops(self, node):
    render_drops_html(self, node, (node['code']), (node['options']), imgcls=('classes' in node and node['classes']))


def render_drops_latex(self, node, code, options, prefix='drops'):
    try:
        fname, outfn = render_drops(self, code, options, 'png', prefix)
    except DropsError as exc:
        logger.warning('pton %r: ' % code + str(exc))
        raise nodes.SkipNode

    is_inline = self.is_inline(node)
    if is_inline:
        para_separator = ''
    else:
        para_separator = '\n'
    if fname is not None:
        post = None
        if not is_inline:
            if 'align' in node:
                if node['align'] == 'left':
                    self.body.append('{')
                    post = '\\hspace*{\\fill}}'
                elif node['align'] == 'right':
                    self.body.append('{\\hspace*{\\fill}')
                    post = '}'
        self.body.append('%s\\sphinxincludegraphics{%s}%s' % (
         para_separator, fname, para_separator))
        if post:
            self.body.append(post)
    raise nodes.SkipNode


def latex_visit_drops(self, node):
    render_drops_latex(self, node, node['code'], node['options'])


def render_drops_texinfo(self, node, code, options, prefix='drops'):
    try:
        fname, outfn = render_drops(self, code, options, 'png', prefix)
    except DropsError as exc:
        logger.warning('pton %r: ' % code + str(exc))
        raise nodes.SkipNode

    if fname is not None:
        self.body.append('@image{%s,,,[drops],png}\n' % fname[:-4])
    raise nodes.SkipNode


def texinfo_visit_drops(self, node):
    render_drops_texinfo(self, node, node['code'], node['options'])


def text_visit_drops(self, node):
    if 'alt' in node.attributes:
        self.add_text(_('[drops: %s]') % node['alt'])
    else:
        self.add_text(_('[drops]'))
    raise nodes.SkipNode


def man_visit_drops(self, node):
    if 'alt' in node.attributes:
        self.body.append(_('[drops: %s]') % node['alt'])
    else:
        self.body.append(_('[drops]'))
    raise nodes.SkipNode


def pton_role():
    """ replace PTON with suitable LaTex """

    def role(name, rawtext, text, lineno, inliner, options={}, content=[]):
        text = rawtext.split('`')[1]
        latex = latex_from_pton(text)
        node = (nodes.math)(rawtext, text, latex=latex, **options)
        return ([node], [])

    return role


def figure_role_wrapper(node, rawtext, text, lineno, inliner):
    figure_node = nodes.figure('', node)
    if 'caption' in node['options']:
        caption = node['options']['caption']
        caption_node = nodes.caption(rawtext, '', nodes.math(rawtext, caption, latex=caption))
    else:
        latex = latex_from_pton(node['code'])
        caption_node = nodes.caption(rawtext, '', nodes.math(rawtext, text, latex=latex))
    caption_node.source = 'drops'
    caption_node.line = lineno
    figure_node += caption_node
    return figure_node


def drop_role():
    """  """

    def role(name, rawtext, text, lineno, inliner, options={}, content=[]):
        node = drops(rawtext, **options)
        options = options.copy()
        node['options'] = options
        options['width'] = '200'
        flags = ''
        text = rawtext.split('`')[1]
        text = text.replace('\n', ' ')
        warning = []
        if '−' in text:
            text = text.replace('−', '-')
            warning = [inliner.reporter.warning(__(':drop: `' + text + '` contains unicode operator, −, replacing with -.'))]
        while len(text) and text[0] in './%#"|{@^[':
            flag = text[0]
            flags += flag
            text = text[1:]
            if flag == '.':
                match = re.match('^([^\\s]+).*$', text)
                if not match:
                    raise ValueError
                scheme = match.groups()[0]
                text = text[len(scheme):]
                options['pdir'] = scheme
            if flag == '^':
                match = re.match('^([A-Z]?[a-z]?\\d*).*$', text)
                if not match:
                    raise ValueError
                view = match.groups()[0]
                text = text[len(view):]
                options['view'] = view
            if flag == '/':
                match = re.match('^(\\d+).*$', text)
                if not match:
                    raise ValueError
                numcol = match.groups()[0]
                text = text[len(numcol):]
                options['width'] = '%3.3f%%' % (99.0 / int(numcol))
            if flag == '[':
                match = re.match('^([^\\]]+)].*$', text)
                if not match:
                    raise ValueError
                prefs = match.groups()[0]
                text = text[len(prefs) + 1:]
                options['prefs'] = prefs
            if flag == '%':
                match = re.match('^(\\d+).*$', text)
                if not match:
                    raise ValueError
                aspect = match.groups()[0]
                text = text[len(aspect):]
                options['aspect'] = int(aspect)
            if flag == '#':
                match = re.match('^(\\d+).*$', text)
                if not match:
                    raise ValueError
                nspin = match.groups()[0]
                text = text[len(nspin):]
                options['nspin'] = int(nspin)
            if flag == '"':
                match = re.match('^([^"]*)".*$', text)
                if not match:
                    print('text', text)
                    raise ValueError
                caption = match.groups()[0]
                text = text[1 + len(caption):]
                options['caption'] = caption

        if '|' in flags:
            options['classes'] = [
             'border']
        if '{' in flags:
            options['aspect'] = 50
            if 'prefs' not in options:
                options['prefs'] = ''
            options['prefs'] += ';Current Separation=3'
        text = text.replace(' ', '')
        node['code'] = text
        print('node', str(node), 'options', options)
        if isinstance(inliner.parent, nodes.entry):
            if '@' not in flags:
                node = figure_role_wrapper(node, rawtext, text, lineno, inliner)
        return (
         [
          node], warning)

    return role


def setup(app):
    app.add_node(drops, html=(
     html_visit_drops, None),
      latex=(
     latex_visit_drops, None),
      texinfo=(
     texinfo_visit_drops, None),
      text=(
     text_visit_drops, None),
      man=(
     man_visit_drops, None))
    app.add_role('pton', pton_role())
    app.add_role('drop', drop_role())
    app.add_directive('drops', Drops)
    app.add_directive('dropsimp', DropsSimple)
    app.add_config_value('drops_spindrops', 'SpinDrops', 'html')
    app.add_config_value('drops_spindrops_args', [], 'html')
    app.add_config_value('drops_nominal_width', {'default':600,  'html':600,  'latex':500}, 'html')
    app.add_config_value('drops_output_format', 'png', 'html')
    app.add_config_value('drops_spindrops_url', '', 'html')
    return {'version':'0.9',  'parallel_read_safe':True}