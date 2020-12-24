# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/tkomiya/work/sphinx/.tox/py37/lib/python3.7/site-packages/docutils/transforms/universal.py
# Compiled at: 2018-11-25 06:19:18
# Size of source mod 2**32: 11102 bytes
"""
Transforms needed by most or all documents:

- `Decorations`: Generate a document's header & footer.
- `Messages`: Placement of system messages stored in
  `nodes.document.transform_messages`.
- `TestMessages`: Like `Messages`, used on test runs.
- `FinalReferences`: Resolve remaining references.
"""
__docformat__ = 'reStructuredText'
import re, sys, time
from docutils import nodes, utils
from docutils.transforms import TransformError, Transform
from docutils.utils import smartquotes

class Decorations(Transform):
    __doc__ = "\n    Populate a document's decoration element (header, footer).\n    "
    default_priority = 820

    def apply(self):
        header_nodes = self.generate_header()
        if header_nodes:
            decoration = self.document.get_decoration()
            header = decoration.get_header()
            header.extend(header_nodes)
        footer_nodes = self.generate_footer()
        if footer_nodes:
            decoration = self.document.get_decoration()
            footer = decoration.get_footer()
            footer.extend(footer_nodes)

    def generate_header(self):
        pass

    def generate_footer--- This code section failed: ---

 L.  56         0  LOAD_FAST                'self'
                2  LOAD_ATTR                document
                4  LOAD_ATTR                settings
                6  STORE_FAST               'settings'

 L.  57         8  LOAD_FAST                'settings'
               10  LOAD_ATTR                generator
               12  POP_JUMP_IF_TRUE     32  'to 32'
               14  LOAD_FAST                'settings'
               16  LOAD_ATTR                datestamp
               18  POP_JUMP_IF_TRUE     32  'to 32'
               20  LOAD_FAST                'settings'
               22  LOAD_ATTR                source_link
               24  POP_JUMP_IF_TRUE     32  'to 32'

 L.  58        26  LOAD_FAST                'settings'
               28  LOAD_ATTR                source_url
               30  POP_JUMP_IF_FALSE   248  'to 248'
             32_0  COME_FROM            24  '24'
             32_1  COME_FROM            18  '18'
             32_2  COME_FROM            12  '12'

 L.  59        32  BUILD_LIST_0          0 
               34  STORE_FAST               'text'

 L.  60        36  LOAD_FAST                'settings'
               38  LOAD_ATTR                source_link
               40  POP_JUMP_IF_FALSE    48  'to 48'
               42  LOAD_FAST                'settings'
               44  LOAD_ATTR                _source
               46  POP_JUMP_IF_TRUE     54  'to 54'
             48_0  COME_FROM            40  '40'

 L.  61        48  LOAD_FAST                'settings'
               50  LOAD_ATTR                source_url
               52  POP_JUMP_IF_FALSE   116  'to 116'
             54_0  COME_FROM            46  '46'

 L.  62        54  LOAD_FAST                'settings'
               56  LOAD_ATTR                source_url
               58  POP_JUMP_IF_FALSE    68  'to 68'

 L.  63        60  LOAD_FAST                'settings'
               62  LOAD_ATTR                source_url
               64  STORE_FAST               'source'
               66  JUMP_FORWARD         84  'to 84'
             68_0  COME_FROM            58  '58'

 L.  65        68  LOAD_GLOBAL              utils
               70  LOAD_METHOD              relative_path
               72  LOAD_FAST                'settings'
               74  LOAD_ATTR                _destination

 L.  66        76  LOAD_FAST                'settings'
               78  LOAD_ATTR                _source
               80  CALL_METHOD_2         2  '2 positional arguments'
               82  STORE_FAST               'source'
             84_0  COME_FROM            66  '66'

 L.  67        84  LOAD_FAST                'text'
               86  LOAD_METHOD              extend

 L.  68        88  LOAD_GLOBAL              nodes
               90  LOAD_ATTR                reference
               92  LOAD_STR                 ''
               94  LOAD_STR                 'View document source'

 L.  69        96  LOAD_FAST                'source'
               98  LOAD_CONST               ('refuri',)
              100  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'

 L.  70       102  LOAD_GLOBAL              nodes
              104  LOAD_METHOD              Text
              106  LOAD_STR                 '.\n'
              108  CALL_METHOD_1         1  '1 positional argument'
              110  BUILD_LIST_2          2 
              112  CALL_METHOD_1         1  '1 positional argument'
              114  POP_TOP          
            116_0  COME_FROM            52  '52'

 L.  71       116  LOAD_FAST                'settings'
              118  LOAD_ATTR                datestamp
              120  POP_JUMP_IF_FALSE   164  'to 164'

 L.  72       122  LOAD_GLOBAL              time
              124  LOAD_METHOD              strftime
              126  LOAD_FAST                'settings'
              128  LOAD_ATTR                datestamp
              130  LOAD_GLOBAL              time
              132  LOAD_METHOD              gmtime
              134  CALL_METHOD_0         0  '0 positional arguments'
              136  CALL_METHOD_2         2  '2 positional arguments'
              138  STORE_FAST               'datestamp'

 L.  73       140  LOAD_FAST                'text'
              142  LOAD_METHOD              append
              144  LOAD_GLOBAL              nodes
              146  LOAD_METHOD              Text
              148  LOAD_STR                 'Generated on: '
              150  LOAD_FAST                'datestamp'
              152  BINARY_ADD       
              154  LOAD_STR                 '.\n'
              156  BINARY_ADD       
              158  CALL_METHOD_1         1  '1 positional argument'
              160  CALL_METHOD_1         1  '1 positional argument'
              162  POP_TOP          
            164_0  COME_FROM           120  '120'

 L.  74       164  LOAD_FAST                'settings'
              166  LOAD_ATTR                generator
              168  POP_JUMP_IF_FALSE   232  'to 232'

 L.  75       170  LOAD_FAST                'text'
              172  LOAD_METHOD              extend

 L.  76       174  LOAD_GLOBAL              nodes
              176  LOAD_METHOD              Text
              178  LOAD_STR                 'Generated by '
              180  CALL_METHOD_1         1  '1 positional argument'

 L.  77       182  LOAD_GLOBAL              nodes
              184  LOAD_ATTR                reference
              186  LOAD_STR                 ''
              188  LOAD_STR                 'Docutils'

 L.  78       190  LOAD_STR                 'http://docutils.sourceforge.net/'
              192  LOAD_CONST               ('refuri',)
              194  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'

 L.  79       196  LOAD_GLOBAL              nodes
              198  LOAD_METHOD              Text
              200  LOAD_STR                 ' from '
              202  CALL_METHOD_1         1  '1 positional argument'

 L.  80       204  LOAD_GLOBAL              nodes
              206  LOAD_ATTR                reference
              208  LOAD_STR                 ''
              210  LOAD_STR                 'reStructuredText'
              212  LOAD_STR                 'http://docutils.sourceforge.net/rst.html'
              214  LOAD_CONST               ('refuri',)
              216  CALL_FUNCTION_KW_3     3  '3 total positional and keyword args'

 L.  82       218  LOAD_GLOBAL              nodes
              220  LOAD_METHOD              Text
              222  LOAD_STR                 ' source.\n'
              224  CALL_METHOD_1         1  '1 positional argument'
              226  BUILD_LIST_5          5 
              228  CALL_METHOD_1         1  '1 positional argument'
              230  POP_TOP          
            232_0  COME_FROM           168  '168'

 L.  83       232  LOAD_GLOBAL              nodes
              234  LOAD_ATTR                paragraph
              236  LOAD_CONST               ('', '')
              238  LOAD_FAST                'text'
              240  BUILD_TUPLE_UNPACK_WITH_CALL_2     2 
              242  CALL_FUNCTION_EX      0  'positional arguments only'
              244  BUILD_LIST_1          1 
              246  RETURN_VALUE     
            248_0  COME_FROM            30  '30'

 L.  85       248  LOAD_CONST               None
              250  RETURN_VALUE     

Parse error at or near `LOAD_CONST' instruction at offset 248


class ExposeInternals(Transform):
    __doc__ = '\n    Expose internal attributes if ``expose_internals`` setting is set.\n    '
    default_priority = 840

    def not_Text(self, node):
        return not isinstance(node, nodes.Text)

    def apply(self):
        if self.document.settings.expose_internals:
            for node in self.document.traverse(self.not_Text):
                for att in self.document.settings.expose_internals:
                    value = getattr(node, att, None)
                    if value is not None:
                        node['internal:' + att] = value


class Messages(Transform):
    __doc__ = '\n    Place any system messages generated after parsing into a dedicated section\n    of the document.\n    '
    default_priority = 860

    def apply(self):
        unfiltered = self.document.transform_messages
        threshold = self.document.reporter.report_level
        messages = []
        for msg in unfiltered:
            if msg['level'] >= threshold:
                msg.parent or messages.append(msg)

        if messages:
            section = nodes.section(classes=['system-messages'])
            section += nodes.title'''Docutils System Messages'
            section += messages
            self.document.transform_messages[:] = []
            self.document += section


class FilterMessages(Transform):
    __doc__ = '\n    Remove system messages below verbosity threshold.\n    '
    default_priority = 870

    def apply(self):
        for node in self.document.traverse(nodes.system_message):
            if node['level'] < self.document.reporter.report_level:
                node.parent.remove(node)


class TestMessages(Transform):
    __doc__ = '\n    Append all post-parse system messages to the end of the document.\n\n    Used for testing purposes.\n    '
    default_priority = 880

    def apply(self):
        for msg in self.document.transform_messages:
            if not msg.parent:
                self.document += msg


class StripComments(Transform):
    __doc__ = '\n    Remove comment elements from the document tree (only if the\n    ``strip_comments`` setting is enabled).\n    '
    default_priority = 740

    def apply(self):
        if self.document.settings.strip_comments:
            for node in self.document.traverse(nodes.comment):
                node.parent.remove(node)


class StripClassesAndElements(Transform):
    __doc__ = '\n    Remove from the document tree all elements with classes in\n    `self.document.settings.strip_elements_with_classes` and all "classes"\n    attribute values in `self.document.settings.strip_classes`.\n    '
    default_priority = 420

    def apply(self):
        if not self.document.settings.strip_elements_with_classes:
            if not self.document.settings.strip_classes:
                return
        self.strip_elements = dict([(key, None) for key in self.document.settings.strip_elements_with_classes or []])
        self.strip_classes = dict([(key, None) for key in self.document.settings.strip_classes or []])
        for node in self.document.traverse(self.check_classes):
            node.parent.remove(node)

    def check_classes(self, node):
        if isinstance(node, nodes.Element):
            for class_value in node['classes'][:]:
                if class_value in self.strip_classes:
                    node['classes'].remove(class_value)
                if class_value in self.strip_elements:
                    return 1


class SmartQuotes(Transform):
    __doc__ = '\n    Replace ASCII quotation marks with typographic form.\n\n    Also replace multiple dashes with em-dash/en-dash characters.\n    '
    default_priority = 850
    nodes_to_skip = (
     nodes.FixedTextElement, nodes.Special)
    literal_nodes = (
     nodes.image, nodes.literal, nodes.math,
     nodes.raw, nodes.problematic)
    smartquotes_action = 'qDe'

    def __init__(self, document, startnode):
        Transform.__init__(self, document, startnode=startnode)
        self.unsupported_languages = set()

    def get_tokens(self, txtnodes):
        texttype = {True:'literal', 
         False:'plain'}
        for txtnode in txtnodes:
            nodetype = texttype[isinstance(txtnode.parent, self.literal_nodes)]
            yield (nodetype, txtnode.astext())

    def apply(self):
        smart_quotes = self.document.settings.smart_quotes
        if not smart_quotes:
            return
        try:
            alternative = smart_quotes.startswith('alt')
        except AttributeError:
            alternative = False

        document_language = self.document.settings.language_code
        lc_smartquotes = self.document.settings.smartquotes_locales
        if lc_smartquotes:
            smartquotes.smartchars.quotes.update(dict(lc_smartquotes))
        for node in self.document.traverse(nodes.TextElement):
            if isinstance(node, self.nodes_to_skip):
                continue
            else:
                if isinstance(node.parent, nodes.TextElement):
                    continue
                txtnodes = [txtnode for txtnode in node.traverse(nodes.Text) if not isinstance(txtnode.parent, nodes.option_string)]
                lang = node.get_language_code(document_language)
                if alternative:
                    if '-x-altquot' in lang:
                        lang = lang.replace'-x-altquot'''
                    else:
                        lang += '-x-altquot'
            for tag in utils.normalize_language_tag(lang):
                if tag in smartquotes.smartchars.quotes:
                    lang = tag
                    break
            else:
                if lang not in self.unsupported_languages:
                    self.document.reporter.warning(('No smart quotes defined for language "%s".' % lang),
                      base_node=node)
                self.unsupported_languages.add(lang)
                lang = ''

            teacher = smartquotes.educate_tokens((self.get_tokens(txtnodes)), attr=(self.smartquotes_action),
              language=lang)
            for txtnode, newtext in zip(txtnodes, teacher):
                txtnode.parent.replacetxtnodenodes.Text(newtext, rawsource=(txtnode.rawsource))

        self.unsupported_languages = set()