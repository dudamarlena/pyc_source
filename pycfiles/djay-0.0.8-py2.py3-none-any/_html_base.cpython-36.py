# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-m_4qh6p6/docutils/docutils/writers/_html_base.py
# Compiled at: 2019-07-30 18:47:12
# Size of source mod 2**32: 64036 bytes
"""common definitions for Docutils HTML writers"""
import sys, os.path, re, urllib.request, urllib.parse, urllib.error
try:
    import PIL.Image
except ImportError:
    try:
        import Image

        class PIL(object):
            pass


        PIL.Image = Image
    except ImportError:
        PIL = None

import docutils
from docutils import nodes, utils, writers, languages, io
from docutils.utils.error_reporting import SafeString
from docutils.transforms import writer_aux
from docutils.utils.math import unichar2tex, pick_math_environment, math2html, latex2mathml, tex2mathml_extern

class Writer(writers.Writer):
    supported = ('html', 'xhtml')
    default_template = 'template.txt'
    settings_defaults = {'output_encoding_error_handler': 'xmlcharrefreplace'}
    config_section_dependencies = [
     'writers', 'html writers']
    visitor_attributes = ('head_prefix', 'head', 'stylesheet', 'body_prefix', 'body_pre_docinfo',
                          'docinfo', 'body', 'body_suffix', 'title', 'subtitle',
                          'header', 'footer', 'meta', 'fragment', 'html_prolog',
                          'html_head', 'html_title', 'html_subtitle', 'html_body')

    def get_transforms(self):
        return writers.Writer.get_transforms(self) + [writer_aux.Admonitions]

    def translate(self):
        self.visitor = visitor = self.translator_class(self.document)
        self.document.walkabout(visitor)
        for attr in self.visitor_attributes:
            setattr(self, attr, getattr(visitor, attr))

        self.output = self.apply_template()

    def apply_template(self):
        template_file = open(self.document.settings.template, 'rb')
        template = str(template_file.read(), 'utf-8')
        template_file.close()
        subs = self.interpolation_dict()
        return template % subs

    def interpolation_dict(self):
        subs = {}
        settings = self.document.settings
        for attr in self.visitor_attributes:
            subs[attr] = ''.join(getattr(self, attr)).rstrip('\n')

        subs['encoding'] = settings.output_encoding
        subs['version'] = docutils.__version__
        return subs

    def assemble_parts(self):
        writers.Writer.assemble_parts(self)
        for part in self.visitor_attributes:
            self.parts[part] = ''.join(getattr(self, part))


class HTMLTranslator(nodes.NodeVisitor):
    __doc__ = '\n    Generic Docutils to HTML translator.\n\n    See the `html4css1` and `html5_polyglot` writers for full featured\n    HTML writers.\n\n    .. IMPORTANT::\n      The `visit_*` and `depart_*` methods use a\n      heterogeneous stack, `self.context`.\n      When subclassing, make sure to be consistent in its use!\n\n      Examples for robust coding:\n\n      a) Override both `visit_*` and `depart_*` methods, don\'t call the\n         parent functions.\n\n      b) Extend both and unconditionally call the parent functions::\n\n           def visit_example(self, node):\n               if foo:\n                   self.body.append(\'<div class="foo">\')\n               html4css1.HTMLTranslator.visit_example(self, node)\n\n           def depart_example(self, node):\n               html4css1.HTMLTranslator.depart_example(self, node)\n               if foo:\n                   self.body.append(\'</div>\')\n\n      c) Extend both, calling the parent functions under the same\n         conditions::\n\n           def visit_example(self, node):\n               if foo:\n                   self.body.append(\'<div class="foo">\n\')\n               else: # call the parent method\n                   _html_base.HTMLTranslator.visit_example(self, node)\n\n           def depart_example(self, node):\n               if foo:\n                   self.body.append(\'</div>\n\')\n               else: # call the parent method\n                   _html_base.HTMLTranslator.depart_example(self, node)\n\n      d) Extend one method (call the parent), but don\'t otherwise use the\n         `self.context` stack::\n\n           def depart_example(self, node):\n               _html_base.HTMLTranslator.depart_example(self, node)\n               if foo:\n                   # implementation-specific code\n                   # that does not use `self.context`\n                   self.body.append(\'</div>\n\')\n\n      This way, changes in stack use will not bite you.\n    '
    xml_declaration = '<?xml version="1.0" encoding="%s" ?>\n'
    doctype = '<!DOCTYPE html>\n'
    doctype_mathml = doctype
    head_prefix_template = '<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="%(lang)s" lang="%(lang)s">\n<head>\n'
    content_type = '<meta charset="%s"/>\n'
    generator = '<meta name="generator" content="Docutils %s: http://docutils.sourceforge.net/" />\n'
    mathjax_script = '<script type="text/javascript" src="%s"></script>\n'
    mathjax_url = 'file:/usr/share/javascript/mathjax/MathJax.js'
    stylesheet_link = '<link rel="stylesheet" href="%s" type="text/css" />\n'
    embedded_stylesheet = '<style type="text/css">\n\n%s\n</style>\n'
    words_and_spaces = re.compile('[^ \\n]+| +|\\n')
    in_word_wrap_point = re.compile('.+\\W\\W.+|[-?].+', re.U)
    lang_attribute = 'lang'
    special_characters = {ord('&'): '&amp;', 
     ord('<'): '&lt;', 
     ord('"'): '&quot;', 
     ord('>'): '&gt;', 
     ord('@'): '&#64;'}

    def __init__(self, document):
        nodes.NodeVisitor.__init__(self, document)
        self.settings = settings = document.settings
        lcode = settings.language_code
        self.language = languages.get_language(lcode, document.reporter)
        self.meta = [self.generator % docutils.__version__]
        self.head_prefix = []
        self.html_prolog = []
        if settings.xml_declaration:
            self.head_prefix.append(self.xml_declaration % settings.output_encoding)
            self.html_prolog.append(self.xml_declaration)
        self.head = self.meta[:]
        self.stylesheet = [self.stylesheet_call(path) for path in utils.get_stylesheet_list(settings)]
        self.body_prefix = ['</head>\n<body>\n']
        self.body_pre_docinfo = []
        self.docinfo = []
        self.body = []
        self.fragment = []
        self.body_suffix = [
         '</body>\n</html>\n']
        self.section_level = 0
        self.initial_header_level = int(settings.initial_header_level)
        self.math_output = settings.math_output.split()
        self.math_output_options = self.math_output[1:]
        self.math_output = self.math_output[0].lower()
        self.context = []
        self.topic_classes = []
        self.colspecs = []
        self.compact_p = True
        self.compact_simple = False
        self.compact_field_list = False
        self.in_docinfo = False
        self.in_sidebar = False
        self.in_footnote_list = False
        self.title = []
        self.subtitle = []
        self.header = []
        self.footer = []
        self.html_head = [self.content_type]
        self.html_title = []
        self.html_subtitle = []
        self.html_body = []
        self.in_document_title = 0
        self.in_mailto = False
        self.author_in_authors = False
        self.math_header = []

    def astext(self):
        return ''.join(self.head_prefix + self.head + self.stylesheet + self.body_prefix + self.body_pre_docinfo + self.docinfo + self.body + self.body_suffix)

    def encode(self, text):
        """Encode special characters in `text` & return."""
        text = str(text)
        return text.translate(self.special_characters)

    def cloak_mailto(self, uri):
        """Try to hide a mailto: URL from harvesters."""
        return uri.replace('@', '%40')

    def cloak_email(self, addr):
        """Try to hide the link text of a email link from harversters."""
        addr = addr.replace('&#64;', '<span>&#64;</span>')
        addr = addr.replace('.', '<span>&#46;</span>')
        return addr

    def attval(self, text, whitespace=re.compile('[\n\r\t\x0b\x0c]')):
        """Cleanse, HTML encode, and return attribute value text."""
        encoded = self.encode(whitespace.sub(' ', text))
        if self.in_mailto:
            if self.settings.cloak_email_addresses:
                encoded = encoded.replace('%40', '&#37;&#52;&#48;')
                encoded = encoded.replace('.', '&#46;')
        return encoded

    def stylesheet_call(self, path):
        """Return code to reference or embed stylesheet file `path`"""
        if self.settings.embed_stylesheet:
            try:
                content = io.FileInput(source_path=path, encoding='utf-8').read()
                self.settings.record_dependencies.add(path)
            except IOError as err:
                msg = "Cannot embed stylesheet '%s': %s." % (
                 path, SafeString(err.strerror))
                self.document.reporter.error(msg)
                return '<--- %s --->\n' % msg

            return self.embedded_stylesheet % content
        else:
            if self.settings.stylesheet_path:
                path = utils.relative_path(self.settings._destination, path)
            return self.stylesheet_link % self.encode(path)

    def starttag(self, node, tagname, suffix='\n', empty=False, **attributes):
        """
        Construct and return a start tag given a node (id & class attributes
        are extracted), tag name, and optional attributes.
        """
        tagname = tagname.lower()
        prefix = []
        atts = {}
        ids = []
        for name, value in list(attributes.items()):
            atts[name.lower()] = value

        classes = []
        languages = []
        for cls in node.get('classes', []) + atts.pop('class', '').split():
            if cls.startswith('language-'):
                languages.append(cls[9:])
            else:
                if cls.strip() and cls not in classes:
                    classes.append(cls)

        if languages:
            atts[self.lang_attribute] = languages[0]
        else:
            if classes:
                atts['class'] = ' '.join(classes)
            assert 'id' not in atts
        ids.extend(node.get('ids', []))
        if 'ids' in atts:
            ids.extend(atts['ids'])
            del atts['ids']
        else:
            if ids:
                atts['id'] = ids[0]
                for id in ids[1:]:
                    if empty or isinstance(node, (
                     nodes.bullet_list, nodes.docinfo,
                     nodes.definition_list, nodes.enumerated_list,
                     nodes.field_list, nodes.option_list,
                     nodes.table)):
                        prefix.append('<span id="%s"></span>' % id)
                    else:
                        suffix += '<span id="%s"></span>' % id

            attlist = list(atts.items())
            attlist.sort()
            parts = [tagname]
            for name, value in attlist:
                if not value is not None:
                    raise AssertionError
                else:
                    if isinstance(value, list):
                        values = [str(v) for v in value]
                        parts.append('%s="%s"' % (name.lower(),
                         self.attval(' '.join(values))))
                    else:
                        parts.append('%s="%s"' % (name.lower(),
                         self.attval(str(value))))

            if empty:
                infix = ' /'
            else:
                infix = ''
        return ''.join(prefix) + '<%s%s>' % (' '.join(parts), infix) + suffix

    def emptytag(self, node, tagname, suffix='\n', **attributes):
        """Construct and return an XML-compatible empty tag."""
        return (self.starttag)(node, tagname, suffix, empty=True, **attributes)

    def set_class_on_child(self, node, class_, index=0):
        """
        Set class `class_` on the visible child no. index of `node`.
        Do nothing if node has fewer children than `index`.
        """
        children = [n for n in node if not isinstance(n, nodes.Invisible)]
        try:
            child = children[index]
        except IndexError:
            return
        else:
            child['classes'].append(class_)

    def visit_Text(self, node):
        text = node.astext()
        encoded = self.encode(text)
        if self.in_mailto:
            if self.settings.cloak_email_addresses:
                encoded = self.cloak_email(encoded)
        self.body.append(encoded)

    def depart_Text(self, node):
        pass

    def visit_abbreviation(self, node):
        self.body.append(self.starttag(node, 'abbr', ''))

    def depart_abbreviation(self, node):
        self.body.append('</abbr>')

    def visit_acronym(self, node):
        self.body.append(self.starttag(node, 'acronym', ''))

    def depart_acronym(self, node):
        self.body.append('</acronym>')

    def visit_address(self, node):
        self.visit_docinfo_item(node, 'address', meta=False)
        self.body.append(self.starttag(node, 'pre', suffix='',
          CLASS='address'))

    def depart_address(self, node):
        self.body.append('\n</pre>\n')
        self.depart_docinfo_item()

    def visit_admonition(self, node):
        node['classes'].insert(0, 'admonition')
        self.body.append(self.starttag(node, 'div'))

    def depart_admonition(self, node=None):
        self.body.append('</div>\n')

    attribution_formats = {'dash':('—', ''), 
     'parentheses':('(', ')'), 
     'parens':('(', ')'), 
     'none':('', '')}

    def visit_attribution(self, node):
        prefix, suffix = self.attribution_formats[self.settings.attribution]
        self.context.append(suffix)
        self.body.append(self.starttag(node, 'p', prefix, CLASS='attribution'))

    def depart_attribution(self, node):
        self.body.append(self.context.pop() + '</p>\n')

    def visit_author(self, node):
        if not isinstance(node.parent, nodes.authors):
            self.visit_docinfo_item(node, 'author')
        self.body.append('<p>')

    def depart_author(self, node):
        self.body.append('</p>')
        if isinstance(node.parent, nodes.authors):
            self.body.append('\n')
        else:
            self.depart_docinfo_item()

    def visit_authors(self, node):
        self.visit_docinfo_item(node, 'authors')

    def depart_authors(self, node):
        self.depart_docinfo_item()

    def visit_block_quote(self, node):
        self.body.append(self.starttag(node, 'blockquote'))

    def depart_block_quote(self, node):
        self.body.append('</blockquote>\n')

    def check_simple_list(self, node):
        """Check for a simple list that can be rendered compactly."""
        visitor = SimpleListChecker(self.document)
        try:
            node.walk(visitor)
        except nodes.NodeFound:
            return False
        else:
            return True

    def is_compactable(self, node):
        if 'compact' in node['classes']:
            return True
        else:
            if 'open' in node['classes']:
                return False
            else:
                if isinstance(node, (nodes.field_list, nodes.definition_list)):
                    if not self.settings.compact_field_lists:
                        return False
                if isinstance(node, (nodes.enumerated_list, nodes.bullet_list)):
                    if not self.settings.compact_lists:
                        return False
                if self.topic_classes == ['contents']:
                    return True
            return self.check_simple_list(node)

    def visit_bullet_list(self, node):
        atts = {}
        old_compact_simple = self.compact_simple
        self.context.append((self.compact_simple, self.compact_p))
        self.compact_p = None
        self.compact_simple = self.is_compactable(node)
        if self.compact_simple:
            if not old_compact_simple:
                atts['class'] = 'simple'
        self.body.append((self.starttag)(node, 'ul', **atts))

    def depart_bullet_list(self, node):
        self.compact_simple, self.compact_p = self.context.pop()
        self.body.append('</ul>\n')

    def visit_caption(self, node):
        self.body.append(self.starttag(node, 'p', '', CLASS='caption'))

    def depart_caption(self, node):
        self.body.append('</p>\n')

    def visit_citation(self, node):
        if not self.in_footnote_list:
            self.body.append('<dl class="citation">\n')
            self.in_footnote_list = True

    def depart_citation(self, node):
        self.body.append('</dd>\n')
        if not isinstance(node.next_node(descend=False, siblings=True), nodes.citation):
            self.body.append('</dl>\n')
            self.in_footnote_list = False

    def visit_citation_reference(self, node):
        href = '#'
        if 'refid' in node:
            href += node['refid']
        else:
            if 'refname' in node:
                href += self.document.nameids[node['refname']]
        self.body.append(self.starttag(node,
          'a', '[', CLASS='citation-reference', href=href))

    def depart_citation_reference(self, node):
        self.body.append(']</a>')

    def visit_classifier(self, node):
        self.body.append(self.starttag(node, 'span', '', CLASS='classifier'))

    def depart_classifier(self, node):
        self.body.append('</span>')

    def visit_colspec(self, node):
        self.colspecs.append(node)
        node.parent.stubs.append(node.attributes.get('stub'))

    def depart_colspec(self, node):
        if isinstance(node.next_node(descend=False, siblings=True), nodes.colspec):
            return
        if 'colwidths-auto' in node.parent.parent['classes'] or 'colwidths-auto' in self.settings.table_style and 'colwidths-given' not in node.parent.parent['classes']:
            return
        total_width = sum(node['colwidth'] for node in self.colspecs)
        self.body.append(self.starttag(node, 'colgroup'))
        for node in self.colspecs:
            colwidth = int(node['colwidth'] * 100.0 / total_width + 0.5)
            self.body.append(self.emptytag(node, 'col', style=('width: %i%%' % colwidth)))

        self.body.append('</colgroup>\n')

    def visit_comment(self, node, sub=re.compile('-(?=-)').sub):
        """Escape double-dashes in comment text."""
        self.body.append('<!-- %s -->\n' % sub('- ', node.astext()))
        raise nodes.SkipNode

    def visit_compound(self, node):
        self.body.append(self.starttag(node, 'div', CLASS='compound'))
        if len(node) > 1:
            node[0]['classes'].append('compound-first')
            node[(-1)]['classes'].append('compound-last')
            for child in node[1:-1]:
                child['classes'].append('compound-middle')

    def depart_compound(self, node):
        self.body.append('</div>\n')

    def visit_container(self, node):
        self.body.append(self.starttag(node, 'div', CLASS='docutils container'))

    def depart_container(self, node):
        self.body.append('</div>\n')

    def visit_contact(self, node):
        self.visit_docinfo_item(node, 'contact', meta=False)

    def depart_contact(self, node):
        self.depart_docinfo_item()

    def visit_copyright(self, node):
        self.visit_docinfo_item(node, 'copyright')

    def depart_copyright(self, node):
        self.depart_docinfo_item()

    def visit_date(self, node):
        self.visit_docinfo_item(node, 'date')

    def depart_date(self, node):
        self.depart_docinfo_item()

    def visit_decoration(self, node):
        pass

    def depart_decoration(self, node):
        pass

    def visit_definition(self, node):
        self.body.append('</dt>\n')
        self.body.append(self.starttag(node, 'dd', ''))

    def depart_definition(self, node):
        self.body.append('</dd>\n')

    def visit_definition_list(self, node):
        classes = node.setdefault('classes', [])
        if self.is_compactable(node):
            classes.append('simple')
        self.body.append(self.starttag(node, 'dl'))

    def depart_definition_list(self, node):
        self.body.append('</dl>\n')

    def visit_definition_list_item(self, node):
        node.children[0]['classes'] = node.get('classes', []) + node.children[0].get('classes', [])
        node.children[0]['ids'] = node.get('ids', []) + node.children[0].get('ids', [])
        node.children[0]['names'] = node.get('names', []) + node.children[0].get('names', [])

    def depart_definition_list_item(self, node):
        pass

    def visit_description(self, node):
        self.body.append(self.starttag(node, 'dd', ''))

    def depart_description(self, node):
        self.body.append('</dd>\n')

    def visit_docinfo(self, node):
        self.context.append(len(self.body))
        classes = 'docinfo'
        if self.is_compactable(node):
            classes += ' simple'
        self.body.append(self.starttag(node, 'dl', CLASS=classes))

    def depart_docinfo(self, node):
        self.body.append('</dl>\n')
        start = self.context.pop()
        self.docinfo = self.body[start:]
        self.body = []

    def visit_docinfo_item(self, node, name, meta=True):
        if meta:
            meta_tag = '<meta name="%s" content="%s" />\n' % (
             name, self.attval(node.astext()))
            self.add_meta(meta_tag)
        self.body.append('<dt class="%s">%s</dt>\n' % (
         name, self.language.labels[name]))
        self.body.append(self.starttag(node, 'dd', '', CLASS=name))

    def depart_docinfo_item(self):
        self.body.append('</dd>\n')

    def visit_doctest_block(self, node):
        self.body.append(self.starttag(node, 'pre', suffix='', CLASS='code python doctest'))

    def depart_doctest_block(self, node):
        self.body.append('\n</pre>\n')

    def visit_document(self, node):
        title = node.get('title', '') or os.path.basename(node['source']) or 'docutils document without title'
        self.head.append('<title>%s</title>\n' % self.encode(title))

    def depart_document(self, node):
        self.head_prefix.extend([self.doctype,
         self.head_prefix_template % {'lang': self.settings.language_code}])
        self.html_prolog.append(self.doctype)
        self.meta.insert(0, self.content_type % self.settings.output_encoding)
        self.head.insert(0, self.content_type % self.settings.output_encoding)
        if 'name="dcterms.' in ''.join(self.meta):
            self.head.append('<link rel="schema.dcterms" href="http://purl.org/dc/terms/">')
        else:
            if self.math_header:
                if self.math_output == 'mathjax':
                    self.head.extend(self.math_header)
                else:
                    self.stylesheet.extend(self.math_header)
            self.html_head.extend(self.head[1:])
            self.body_prefix.append(self.starttag(node, 'div', CLASS='document'))
            self.body_suffix.insert(0, '</div>\n')
            self.fragment.extend(self.body)
            self.html_body.extend(self.body_prefix[1:] + self.body_pre_docinfo + self.docinfo + self.body + self.body_suffix[:-1])
            assert not self.context, 'len(context) = %s' % len(self.context)

    def visit_emphasis(self, node):
        self.body.append(self.starttag(node, 'em', ''))

    def depart_emphasis(self, node):
        self.body.append('</em>')

    def visit_entry(self, node):
        atts = {'class': []}
        if isinstance(node.parent.parent, nodes.thead):
            atts['class'].append('head')
        else:
            if node.parent.parent.parent.stubs[node.parent.column]:
                atts['class'].append('stub')
            if atts['class']:
                tagname = 'th'
                atts['class'] = ' '.join(atts['class'])
            else:
                tagname = 'td'
                del atts['class']
        node.parent.column += 1
        if 'morerows' in node:
            atts['rowspan'] = node['morerows'] + 1
        if 'morecols' in node:
            atts['colspan'] = node['morecols'] + 1
            node.parent.column += node['morecols']
        self.body.append((self.starttag)(node, tagname, '', **atts))
        self.context.append('</%s>\n' % tagname.lower())

    def depart_entry(self, node):
        self.body.append(self.context.pop())

    def visit_enumerated_list(self, node):
        atts = {}
        if 'start' in node:
            atts['start'] = node['start']
        if 'enumtype' in node:
            atts['class'] = node['enumtype']
        if self.is_compactable(node):
            atts['class'] = (atts.get('class', '') + ' simple').strip()
        self.body.append((self.starttag)(node, 'ol', **atts))

    def depart_enumerated_list(self, node):
        self.body.append('</ol>\n')

    def visit_field_list(self, node):
        classes = 'field-list'
        if self.is_compactable(node):
            classes += ' simple'
        self.body.append(self.starttag(node, 'dl', CLASS=classes))

    def depart_field_list(self, node):
        self.body.append('</dl>\n')

    def visit_field(self, node):
        pass

    def depart_field(self, node):
        pass

    def visit_field_name(self, node):
        self.body.append(self.starttag(node, 'dt', '', CLASS=(''.join(node.parent['classes']))))

    def depart_field_name(self, node):
        self.body.append('</dt>\n')

    def visit_field_body(self, node):
        self.body.append(self.starttag(node, 'dd', '', CLASS=(''.join(node.parent['classes']))))
        if not node.children:
            self.body.append('<p></p>')

    def depart_field_body(self, node):
        self.body.append('</dd>\n')

    def visit_figure(self, node):
        atts = {'class': 'figure'}
        if node.get('width'):
            atts['style'] = 'width: %s' % node['width']
        if node.get('align'):
            atts['class'] += ' align-' + node['align']
        self.body.append((self.starttag)(node, 'div', **atts))

    def depart_figure(self, node):
        self.body.append('</div>\n')

    def visit_footer(self, node):
        self.context.append(len(self.body))

    def depart_footer(self, node):
        start = self.context.pop()
        footer = [self.starttag(node, 'div', CLASS='footer'),
         '<hr class="footer" />\n']
        footer.extend(self.body[start:])
        footer.append('\n</div>\n')
        self.footer.extend(footer)
        self.body_suffix[:0] = footer
        del self.body[start:]

    def visit_footnote(self, node):
        if not self.in_footnote_list:
            classes = 'footnote ' + self.settings.footnote_references
            self.body.append('<dl class="%s">\n' % classes)
            self.in_footnote_list = True

    def depart_footnote(self, node):
        self.body.append('</dd>\n')
        if not isinstance(node.next_node(descend=False, siblings=True), nodes.footnote):
            self.body.append('</dl>\n')
            self.in_footnote_list = False

    def visit_footnote_reference(self, node):
        href = '#' + node['refid']
        classes = 'footnote-reference ' + self.settings.footnote_references
        self.body.append(self.starttag(node, 'a', '', CLASS=classes,
          href=href))

    def depart_footnote_reference(self, node):
        self.body.append('</a>')

    def visit_generated(self, node):
        if 'sectnum' in node['classes']:
            sectnum = node.astext().rstrip('\xa0')
            self.body.append('<span class="sectnum">%s</span> ' % self.encode(sectnum))
            raise nodes.SkipNode

    def depart_generated(self, node):
        pass

    def visit_header(self, node):
        self.context.append(len(self.body))

    def depart_header(self, node):
        start = self.context.pop()
        header = [self.starttag(node, 'div', CLASS='header')]
        header.extend(self.body[start:])
        header.append('\n<hr class="header"/>\n</div>\n')
        self.body_prefix.extend(header)
        self.header.extend(header)
        del self.body[start:]

    object_image_types = {'.swf': 'application/x-shockwave-flash'}

    def visit_image(self, node):
        atts = {}
        uri = node['uri']
        ext = os.path.splitext(uri)[1].lower()
        if ext in self.object_image_types:
            atts['data'] = uri
            atts['type'] = self.object_image_types[ext]
        else:
            atts['src'] = uri
            atts['alt'] = node.get('alt', uri)
        if 'width' in node:
            atts['width'] = node['width']
        if 'height' in node:
            atts['height'] = node['height']
        if 'scale' in node:
            if PIL and not ('width' in node and 'height' in node) and self.settings.file_insertion_enabled:
                imagepath = urllib.request.url2pathname(uri)
                try:
                    img = PIL.Image.open(imagepath.encode(sys.getfilesystemencoding()))
                except (IOError, UnicodeEncodeError):
                    pass
                else:
                    self.settings.record_dependencies.add(imagepath.replace('\\', '/'))
                    if 'width' not in atts:
                        atts['width'] = '%dpx' % img.size[0]
                    if 'height' not in atts:
                        atts['height'] = '%dpx' % img.size[1]
                    del img
            for att_name in ('width', 'height'):
                if att_name in atts:
                    match = re.match('([0-9.]+)(\\S*)$', atts[att_name])
                    assert match
                    atts[att_name] = '%s%s' % (
                     float(match.group(1)) * (float(node['scale']) / 100),
                     match.group(2))

        style = []
        for att_name in ('width', 'height'):
            if att_name in atts:
                if re.match('^[0-9.]+$', atts[att_name]):
                    atts[att_name] += 'px'
                style.append('%s: %s;' % (att_name, atts[att_name]))
                del atts[att_name]

        if style:
            atts['style'] = ' '.join(style)
        else:
            if isinstance(node.parent, nodes.TextElement) or isinstance(node.parent, nodes.reference) and not isinstance(node.parent.parent, nodes.TextElement):
                suffix = ''
            else:
                suffix = '\n'
            if 'align' in node:
                atts['class'] = 'align-%s' % node['align']
            if ext in self.object_image_types:
                self.body.append((self.starttag)(node, 'object', suffix, **atts) + node.get('alt', uri) + '</object>' + suffix)
            else:
                self.body.append((self.emptytag)(node, 'img', suffix, **atts))

    def depart_image(self, node):
        pass

    def visit_inline(self, node):
        self.body.append(self.starttag(node, 'span', ''))

    def depart_inline(self, node):
        self.body.append('</span>')

    def visit_label(self, node):
        if isinstance(node.parent, nodes.footnote):
            classes = self.settings.footnote_references
        else:
            classes = 'brackets'
        self.body.append(self.starttag((node.parent), 'dt', '', CLASS='label'))
        self.body.append(self.starttag(node, 'span', '', CLASS=classes))
        if self.settings.footnote_backlinks:
            backrefs = node.parent['backrefs']
            if len(backrefs) == 1:
                self.body.append('<a class="fn-backref" href="#%s">' % backrefs[0])

    def depart_label(self, node):
        if self.settings.footnote_backlinks:
            backrefs = node.parent['backrefs']
            if len(backrefs) == 1:
                self.body.append('</a>')
        self.body.append('</span>')
        if self.settings.footnote_backlinks:
            if len(backrefs) > 1:
                backlinks = ['<a href="#%s">%s</a>' % (ref, i) for i, ref in enumerate(backrefs, 1)]
                self.body.append('<span class="fn-backref">(%s)</span>' % ','.join(backlinks))
        self.body.append('</dt>\n<dd>')

    def visit_legend(self, node):
        self.body.append(self.starttag(node, 'div', CLASS='legend'))

    def depart_legend(self, node):
        self.body.append('</div>\n')

    def visit_line(self, node):
        self.body.append(self.starttag(node, 'div', suffix='', CLASS='line'))
        if not len(node):
            self.body.append('<br />')

    def depart_line(self, node):
        self.body.append('</div>\n')

    def visit_line_block(self, node):
        self.body.append(self.starttag(node, 'div', CLASS='line-block'))

    def depart_line_block(self, node):
        self.body.append('</div>\n')

    def visit_list_item(self, node):
        self.body.append(self.starttag(node, 'li', ''))

    def depart_list_item(self, node):
        self.body.append('</li>\n')

    def visit_literal(self, node):
        classes = node.get('classes', [])
        if 'code' in classes:
            node['classes'] = [cls for cls in classes if cls != 'code']
            self.body.append(self.starttag(node, 'code', ''))
            return
        self.body.append(self.starttag(node, 'span', '', CLASS='docutils literal'))
        text = node.astext()
        if not isinstance(node.parent, nodes.literal_block):
            text = text.replace('\n', ' ')
        for token in self.words_and_spaces.findall(text):
            if token.strip() and self.in_word_wrap_point.search(token):
                self.body.append('<span class="pre">%s</span>' % self.encode(token))
            else:
                self.body.append(self.encode(token))

        self.body.append('</span>')
        raise nodes.SkipNode

    def depart_literal(self, node):
        self.body.append('</code>')

    def visit_literal_block(self, node):
        self.body.append(self.starttag(node, 'pre', '', CLASS='literal-block'))
        if 'code' in node.get('classes', []):
            self.body.append('<code>')

    def depart_literal_block(self, node):
        if 'code' in node.get('classes', []):
            self.body.append('</code>')
        self.body.append('</pre>\n')

    math_tags = {'mathml':('div', '', ''), 
     'html':('div', 'span', 'formula'), 
     'mathjax':('div', 'span', 'math'), 
     'latex':('pre', 'tt', 'math')}

    def visit_math(self, node, math_env=''):
        if self.math_output not in self.math_tags:
            self.document.reporter.error('math-output format "%s" not supported falling back to "latex"' % self.math_output)
            self.math_output = 'latex'
        else:
            tag = self.math_tags[self.math_output][(math_env == '')]
            clsarg = self.math_tags[self.math_output][2]
            wrappers = {'mathml':('$%s$', '\\begin{%s}\n%s\n\\end{%s}'), 
             'html':('$%s$', '\\begin{%s}\n%s\n\\end{%s}'), 
             'mathjax':('\\(%s\\)', '\\begin{%s}\n%s\n\\end{%s}'), 
             'latex':(None, None)}
            wrapper = wrappers[self.math_output][(math_env != '')]
            if self.math_output == 'mathml':
                if not self.math_output_options or self.math_output_options[0] == 'blahtexml':
                    wrapper = None
            math_code = node.astext().translate(unichar2tex.uni2tex_table)
            if wrapper:
                try:
                    math_code = wrapper % (math_env, math_code, math_env)
                except TypeError:
                    math_code = wrapper % math_code

            if self.math_output in ('latex', 'mathjax'):
                math_code = self.encode(math_code)
            if self.math_output == 'mathjax':
                if not self.math_header:
                    try:
                        self.mathjax_url = self.math_output_options[0]
                    except IndexError:
                        self.document.reporter.warning('No MathJax URL specified, using local fallback (see config.html)')

                    if '?' not in self.mathjax_url:
                        self.mathjax_url += '?config=TeX-AMS_CHTML'
                    self.math_header = [
                     self.mathjax_script % self.mathjax_url]
            if self.math_output == 'html':
                if self.math_output_options:
                    if not self.math_header:
                        self.math_header = [self.stylesheet_call(utils.find_file_in_dirs(s, self.settings.stylesheet_dirs)) for s in self.math_output_options[0].split(',')]
                math2html.DocumentParameters.displaymode = math_env != ''
                math_code = math2html.math2html(math_code)
            else:
                if self.math_output == 'mathml':
                    if 'XHTML 1' in self.doctype:
                        self.doctype = self.doctype_mathml
                        self.content_type = self.content_type_mathml
                    converter = ' '.join(self.math_output_options).lower()
                    try:
                        if converter == 'latexml':
                            math_code = tex2mathml_extern.latexml(math_code, self.document.reporter)
                        else:
                            if converter == 'ttm':
                                math_code = tex2mathml_extern.ttm(math_code, self.document.reporter)
                            else:
                                if converter == 'blahtexml':
                                    math_code = tex2mathml_extern.blahtexml(math_code, inline=(not math_env),
                                      reporter=(self.document.reporter))
                                else:
                                    if not converter:
                                        math_code = latex2mathml.tex2mathml(math_code, inline=(not math_env))
                                    else:
                                        self.document.reporter.error('option "%s" not supported with math-output "MathML"')
                    except OSError:
                        raise OSError('is "latexmlmath" in your PATH?')
                    except SyntaxError as err:
                        err_node = self.document.reporter.error(err, base_node=node)
                        self.visit_system_message(err_node)
                        self.body.append(self.starttag(node, 'p'))
                        self.body.append(','.join(err.args))
                        self.body.append('</p>\n')
                        self.body.append(self.starttag(node, 'pre', CLASS='literal-block'))
                        self.body.append(self.encode(math_code))
                        self.body.append('\n</pre>\n')
                        self.depart_system_message(err_node)
                        raise nodes.SkipNode

            if tag:
                self.body.append(self.starttag(node, tag, suffix=('\n' * bool(math_env)),
                  CLASS=clsarg))
            self.body.append(math_code)
            if math_env:
                self.body.append('\n')
            if tag:
                self.body.append('</%s>' % tag)
            if math_env:
                self.body.append('\n')
        raise nodes.SkipNode

    def depart_math(self, node):
        pass

    def visit_math_block(self, node):
        math_env = pick_math_environment(node.astext())
        self.visit_math(node, math_env=math_env)

    def depart_math_block(self, node):
        pass

    def visit_meta(self, node):
        meta = (self.emptytag)(node, 'meta', **node.non_default_attributes())
        self.add_meta(meta)

    def depart_meta(self, node):
        pass

    def add_meta(self, tag):
        self.meta.append(tag)
        self.head.append(tag)

    def visit_option(self, node):
        self.body.append(self.starttag(node, 'span', '', CLASS='option'))

    def depart_option(self, node):
        self.body.append('</span>')
        if isinstance(node.next_node(descend=False, siblings=True), nodes.option):
            self.body.append(', ')

    def visit_option_argument(self, node):
        self.body.append(node.get('delimiter', ' '))
        self.body.append(self.starttag(node, 'var', ''))

    def depart_option_argument(self, node):
        self.body.append('</var>')

    def visit_option_group(self, node):
        self.body.append(self.starttag(node, 'dt', ''))
        self.body.append('<kbd>')

    def depart_option_group(self, node):
        self.body.append('</kbd></dt>\n')

    def visit_option_list(self, node):
        self.body.append(self.starttag(node, 'dl', CLASS='option-list'))

    def depart_option_list(self, node):
        self.body.append('</dl>\n')

    def visit_option_list_item(self, node):
        pass

    def depart_option_list_item(self, node):
        pass

    def visit_option_string(self, node):
        pass

    def depart_option_string(self, node):
        pass

    def visit_organization(self, node):
        self.visit_docinfo_item(node, 'organization')

    def depart_organization(self, node):
        self.depart_docinfo_item()

    def visit_paragraph(self, node):
        self.body.append(self.starttag(node, 'p', ''))

    def depart_paragraph(self, node):
        self.body.append('</p>')
        if not (isinstance(node.parent, (nodes.list_item, nodes.entry)) and len(node.parent) == 1):
            self.body.append('\n')

    def visit_problematic(self, node):
        if node.hasattr('refid'):
            self.body.append('<a href="#%s">' % node['refid'])
            self.context.append('</a>')
        else:
            self.context.append('')
        self.body.append(self.starttag(node, 'span', '', CLASS='problematic'))

    def depart_problematic(self, node):
        self.body.append('</span>')
        self.body.append(self.context.pop())

    def visit_raw(self, node):
        if 'html' in node.get('format', '').split():
            t = isinstance(node.parent, nodes.TextElement) and 'span' or 'div'
            if node['classes']:
                self.body.append(self.starttag(node, t, suffix=''))
            self.body.append(node.astext())
            if node['classes']:
                self.body.append('</%s>' % t)
        raise nodes.SkipNode

    def visit_reference(self, node):
        atts = {'class': 'reference'}
        if 'refuri' in node:
            atts['href'] = node['refuri']
            if self.settings.cloak_email_addresses:
                if atts['href'].startswith('mailto:'):
                    atts['href'] = self.cloak_mailto(atts['href'])
                    self.in_mailto = True
            atts['class'] += ' external'
        else:
            assert 'refid' in node, 'References must have "refuri" or "refid" attribute.'
            atts['href'] = '#' + node['refid']
            atts['class'] += ' internal'
        if not isinstance(node.parent, nodes.TextElement):
            assert len(node) == 1 and isinstance(node[0], nodes.image)
            atts['class'] += ' image-reference'
        self.body.append((self.starttag)(node, 'a', '', **atts))

    def depart_reference(self, node):
        self.body.append('</a>')
        if not isinstance(node.parent, nodes.TextElement):
            self.body.append('\n')
        self.in_mailto = False

    def visit_revision(self, node):
        self.visit_docinfo_item(node, 'revision', meta=False)

    def depart_revision(self, node):
        self.depart_docinfo_item()

    def visit_row(self, node):
        self.body.append(self.starttag(node, 'tr', ''))
        node.column = 0

    def depart_row(self, node):
        self.body.append('</tr>\n')

    def visit_rubric(self, node):
        self.body.append(self.starttag(node, 'p', '', CLASS='rubric'))

    def depart_rubric(self, node):
        self.body.append('</p>\n')

    def visit_section(self, node):
        self.section_level += 1
        self.body.append(self.starttag(node, 'div', CLASS='section'))

    def depart_section(self, node):
        self.section_level -= 1
        self.body.append('</div>\n')

    def visit_sidebar(self, node):
        self.body.append(self.starttag(node, 'div', CLASS='sidebar'))
        self.in_sidebar = True

    def depart_sidebar(self, node):
        self.body.append('</div>\n')
        self.in_sidebar = False

    def visit_status(self, node):
        self.visit_docinfo_item(node, 'status', meta=False)

    def depart_status(self, node):
        self.depart_docinfo_item()

    def visit_strong(self, node):
        self.body.append(self.starttag(node, 'strong', ''))

    def depart_strong(self, node):
        self.body.append('</strong>')

    def visit_subscript(self, node):
        self.body.append(self.starttag(node, 'sub', ''))

    def depart_subscript(self, node):
        self.body.append('</sub>')

    def visit_substitution_definition(self, node):
        """Internal only."""
        raise nodes.SkipNode

    def visit_substitution_reference(self, node):
        self.unimplemented_visit(node)

    def visit_subtitle(self, node):
        if isinstance(node.parent, nodes.sidebar):
            classes = 'sidebar-subtitle'
        else:
            if isinstance(node.parent, nodes.document):
                classes = 'subtitle'
                self.in_document_title = len(self.body) + 1
            else:
                if isinstance(node.parent, nodes.section):
                    classes = 'section-subtitle'
        self.body.append(self.starttag(node, 'p', '', CLASS=classes))

    def depart_subtitle(self, node):
        self.body.append('</p>\n')
        if isinstance(node.parent, nodes.document):
            self.subtitle = self.body[self.in_document_title:-1]
            self.in_document_title = 0
            self.body_pre_docinfo.extend(self.body)
            self.html_subtitle.extend(self.body)
            del self.body[:]

    def visit_superscript(self, node):
        self.body.append(self.starttag(node, 'sup', ''))

    def depart_superscript(self, node):
        self.body.append('</sup>')

    def visit_system_message(self, node):
        self.body.append(self.starttag(node, 'div', CLASS='system-message'))
        self.body.append('<p class="system-message-title">')
        backref_text = ''
        if len(node['backrefs']):
            backrefs = node['backrefs']
            if len(backrefs) == 1:
                backref_text = '; <em><a href="#%s">backlink</a></em>' % backrefs[0]
            else:
                i = 1
                backlinks = []
                for backref in backrefs:
                    backlinks.append('<a href="#%s">%s</a>' % (backref, i))
                    i += 1

                backref_text = '; <em>backlinks: %s</em>' % ', '.join(backlinks)
        else:
            if node.hasattr('line'):
                line = ', line %s' % node['line']
            else:
                line = ''
        self.body.append('System Message: %s/%s (<span class="docutils literal">%s</span>%s)%s</p>\n' % (
         node['type'], node['level'],
         self.encode(node['source']), line, backref_text))

    def depart_system_message(self, node):
        self.body.append('</div>\n')

    def visit_table(self, node):
        atts = {}
        classes = [cls.strip(' \t\n') for cls in self.settings.table_style.split(',')]
        if 'align' in node:
            classes.append('align-%s' % node['align'])
        if 'width' in node:
            atts['style'] = 'width: %s' % node['width']
        tag = (self.starttag)(node, 'table', CLASS=' '.join(classes), **atts)
        self.body.append(tag)

    def depart_table(self, node):
        self.body.append('</table>\n')

    def visit_target(self, node):
        if not ('refuri' in node or 'refid' in node or 'refname' in node):
            self.body.append(self.starttag(node, 'span', '', CLASS='target'))
            self.context.append('</span>')
        else:
            self.context.append('')

    def depart_target(self, node):
        self.body.append(self.context.pop())

    def visit_tbody(self, node):
        self.body.append(self.starttag(node, 'tbody'))

    def depart_tbody(self, node):
        self.body.append('</tbody>\n')

    def visit_term(self, node):
        self.body.append(self.starttag(node, 'dt', ''))

    def depart_term(self, node):
        """
        Leave the end tag to `self.visit_definition()`, in case there's a
        classifier.
        """
        pass

    def visit_tgroup(self, node):
        self.colspecs = []
        node.stubs = []

    def depart_tgroup(self, node):
        pass

    def visit_thead(self, node):
        self.body.append(self.starttag(node, 'thead'))

    def depart_thead(self, node):
        self.body.append('</thead>\n')

    def visit_title(self, node):
        """Only 6 section levels are supported by HTML."""
        check_id = 0
        close_tag = '</p>\n'
        if isinstance(node.parent, nodes.topic):
            self.body.append(self.starttag(node, 'p', '', CLASS='topic-title first'))
        else:
            if isinstance(node.parent, nodes.sidebar):
                self.body.append(self.starttag(node, 'p', '', CLASS='sidebar-title'))
            else:
                if isinstance(node.parent, nodes.Admonition):
                    self.body.append(self.starttag(node, 'p', '', CLASS='admonition-title'))
                else:
                    if isinstance(node.parent, nodes.table):
                        self.body.append(self.starttag(node, 'caption', ''))
                        close_tag = '</caption>\n'
                    else:
                        if isinstance(node.parent, nodes.document):
                            self.body.append(self.starttag(node, 'h1', '', CLASS='title'))
                            close_tag = '</h1>\n'
                            self.in_document_title = len(self.body)
                        else:
                            if not isinstance(node.parent, nodes.section):
                                raise AssertionError
                            else:
                                h_level = self.section_level + self.initial_header_level - 1
                                atts = {}
                                if len(node.parent) >= 2:
                                    if isinstance(node.parent[1], nodes.subtitle):
                                        atts['CLASS'] = 'with-subtitle'
                                self.body.append((self.starttag)(node, ('h%s' % h_level), '', **atts))
                                atts = {}
                                if node.hasattr('refid'):
                                    atts['class'] = 'toc-backref'
                                    atts['href'] = '#' + node['refid']
                            if atts:
                                self.body.append((self.starttag)({}, 'a', '', **atts))
                                close_tag = '</a></h%s>\n' % h_level
                            else:
                                close_tag = '</h%s>\n' % h_level
        self.context.append(close_tag)

    def depart_title(self, node):
        self.body.append(self.context.pop())
        if self.in_document_title:
            self.title = self.body[self.in_document_title:-1]
            self.in_document_title = 0
            self.body_pre_docinfo.extend(self.body)
            self.html_title.extend(self.body)
            del self.body[:]

    def visit_title_reference(self, node):
        self.body.append(self.starttag(node, 'cite', ''))

    def depart_title_reference(self, node):
        self.body.append('</cite>')

    def visit_topic(self, node):
        self.body.append(self.starttag(node, 'div', CLASS='topic'))
        self.topic_classes = node['classes']

    def depart_topic(self, node):
        self.body.append('</div>\n')
        self.topic_classes = []

    def visit_transition(self, node):
        self.body.append(self.emptytag(node, 'hr', CLASS='docutils'))

    def depart_transition(self, node):
        pass

    def visit_version(self, node):
        self.visit_docinfo_item(node, 'version', meta=False)

    def depart_version(self, node):
        self.depart_docinfo_item()

    def unimplemented_visit(self, node):
        raise NotImplementedError('visiting unimplemented node type: %s' % node.__class__.__name__)


class SimpleListChecker(nodes.GenericNodeVisitor):
    __doc__ = '\n    Raise `nodes.NodeFound` if non-simple list item is encountered.\n\n    Here "simple" means a list item containing nothing other than a single\n    paragraph, a simple list, or a paragraph followed by a simple list.\n\n    This version also checks for simple field lists and docinfo.\n    '

    def default_visit(self, node):
        raise nodes.NodeFound

    def visit_list_item(self, node):
        children = [child for child in node.children if not isinstance(child, nodes.Invisible)]
        if children:
            if isinstance(children[0], nodes.paragraph):
                if isinstance(children[(-1)], nodes.bullet_list) or isinstance(children[(-1)], nodes.enumerated_list) or isinstance(children[(-1)], nodes.field_list):
                    children.pop()
        if len(children) <= 1:
            return
        raise nodes.NodeFound

    def pass_node(self, node):
        pass

    def ignore_node(self, node):
        raise nodes.SkipNode

    visit_Text = ignore_node
    visit_paragraph = ignore_node
    visit_bullet_list = pass_node
    visit_enumerated_list = pass_node
    visit_docinfo = pass_node
    visit_author = ignore_node
    visit_authors = visit_list_item
    visit_address = visit_list_item
    visit_contact = pass_node
    visit_copyright = ignore_node
    visit_date = ignore_node
    visit_organization = ignore_node
    visit_status = ignore_node
    visit_version = visit_list_item
    visit_definition_list = pass_node
    visit_definition_list_item = pass_node
    visit_term = ignore_node
    visit_classifier = pass_node
    visit_definition = visit_list_item
    visit_field_list = pass_node
    visit_field = pass_node
    visit_field_body = visit_list_item
    visit_field_name = ignore_node
    visit_comment = ignore_node
    visit_substitution_definition = ignore_node
    visit_target = ignore_node
    visit_pending = ignore_node