# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/jnvilo/Projects/web/mycms/mycms/creole/creole2html/emitter.py
# Compiled at: 2019-02-05 11:01:21
# Size of source mod 2**32: 14163 bytes
"""
    WikiCreole to HTML converter

    :copyleft: 2008-2014 by python-creole team, see AUTHORS for more details.
    :license: GNU GPL v3 or above, see LICENSE for more details.
"""
from __future__ import division, absolute_import, print_function, unicode_literals
from xml.sax.saxutils import escape
import sys, traceback
from mycms.creole.creole2html.parser import CreoleParser
from mycms.creole.py3compat import TEXT_TYPE, repr2
from mycms.creole.shared.utils import string2dict

class TableOfContent(object):

    def __init__(self):
        self.max_depth = None
        self.headlines = []
        self._created = False
        self._current_level = 0

    def __call__(self, depth=None, **kwargs):
        """Called when if the macro <<toc>> is defined when it is emitted."""
        if self._created:
            return '&lt;&lt;toc&gt;&gt;'
        self._created = True
        if depth is not None:
            self.max_depth = depth
        return '<<toc>>'

    def add_headline(self, level, content):
        """Add the current header to the toc."""
        if self.max_depth is None or level <= self.max_depth:
            self.headlines.append((
             level, content))

    def flat_list2nest_list--- This code section failed: ---

 L.  52         0  BUILD_LIST_0          0 
                2  STORE_FAST               'tree'

 L.  53         4  LOAD_FAST                'tree'
                6  BUILD_LIST_1          1 
                8  STORE_FAST               'stack'

 L.  55        10  SETUP_LOOP          128  'to 128'
               12  LOAD_FAST                'flat_list'
               14  GET_ITER         
               16  FOR_ITER            126  'to 126'
               18  UNPACK_SEQUENCE_2     2 
               20  STORE_FAST               'index'
               22  STORE_FAST               'element'

 L.  56        24  LOAD_GLOBAL              len
               26  LOAD_FAST                'stack'
               28  CALL_FUNCTION_1       1  '1 positional argument'
               30  STORE_FAST               'stack_length'

 L.  58        32  LOAD_FAST                'index'
               34  LOAD_FAST                'stack_length'
               36  COMPARE_OP               >
               38  POP_JUMP_IF_FALSE    90  'to 90'

 L.  59        40  SETUP_LOOP          110  'to 110'
               42  LOAD_GLOBAL              range
               44  LOAD_FAST                'stack_length'
               46  LOAD_FAST                'index'
               48  CALL_FUNCTION_2       2  '2 positional arguments'
               50  GET_ITER         
               52  FOR_ITER             86  'to 86'
               54  STORE_FAST               '_'

 L.  60        56  BUILD_LIST_0          0 
               58  STORE_FAST               'l'

 L.  61        60  LOAD_FAST                'stack'
               62  LOAD_CONST               -1
               64  BINARY_SUBSCR    
               66  LOAD_METHOD              append
               68  LOAD_FAST                'l'
               70  CALL_METHOD_1         1  '1 positional argument'
               72  POP_TOP          

 L.  62        74  LOAD_FAST                'stack'
               76  LOAD_METHOD              append
               78  LOAD_FAST                'l'
               80  CALL_METHOD_1         1  '1 positional argument'
               82  POP_TOP          
               84  JUMP_BACK            52  'to 52'
               86  POP_BLOCK        
               88  JUMP_FORWARD        110  'to 110'
             90_0  COME_FROM            38  '38'

 L.  63        90  LOAD_FAST                'index'
               92  LOAD_FAST                'stack_length'
               94  COMPARE_OP               <
               96  POP_JUMP_IF_FALSE   110  'to 110'

 L.  64        98  LOAD_FAST                'stack'
              100  LOAD_CONST               None
              102  LOAD_FAST                'index'
              104  BUILD_SLICE_2         2 
              106  BINARY_SUBSCR    
              108  STORE_FAST               'stack'
            110_0  COME_FROM            96  '96'
            110_1  COME_FROM            88  '88'
            110_2  COME_FROM_LOOP       40  '40'

 L.  66       110  LOAD_FAST                'stack'
              112  LOAD_CONST               -1
              114  BINARY_SUBSCR    
              116  LOAD_METHOD              append
              118  LOAD_FAST                'element'
              120  CALL_METHOD_1         1  '1 positional argument'
              122  POP_TOP          
              124  JUMP_BACK            16  'to 16'
              126  POP_BLOCK        
            128_0  COME_FROM_LOOP       10  '10'

 L.  68       128  LOAD_FAST                'tree'
              130  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `LOAD_FAST' instruction at offset 110

    def nested_headlines2html(self, nested_headlines, level=0):
        """Convert a python nested list like the one representing the toc to an html equivalent."""
        indent = '\t' * level
        if isinstancenested_headlinesTEXT_TYPE:
            return '%s<li><a href="#%s">%s</a></li>\n' % (indent, nested_headlines, nested_headlines)
        if isinstancenested_headlineslist:
            html = '%s<ul>\n' % indent
            for elt in nested_headlines:
                html += self.nested_headlines2html(elt, level + 1)

            html += '%s</ul>' % indent
            if level > 0:
                html += '\n'
            return html

    def emit(self, document):
        """Emit the toc where the <<toc>> macro was."""
        nested_headlines = self.flat_list2nest_list(self.headlines)
        html = self.nested_headlines2html(nested_headlines)
        html = '<div class="creole_macro toc"><span class="toc">{}</span></div>'.format(html)
        if '<p><<toc>></p>' in document:
            document = document.replace('<p><<toc>></p>', html, 1)
        else:
            document = document.replace('<<toc>>', html, 1)
        return document


class HtmlEmitter(object):
    __doc__ = '\n    Generate HTML output for the document\n    tree consisting of DocNodes.\n    '

    def __init__(self, root, macros=None, verbose=None, stderr=None, view=None):
        self.root = root
        self.view = view
        if callable(macros) == True:
            raise TypeError('Callable macros are not supported anymore!')
        elif macros is None:
            self.macros = {}
        else:
            self.macros = macros
        if 'toc' not in root.used_macros:
            self.toc = None
        else:
            if isinstanceself.macrosdict:
                if 'toc' in self.macros:
                    self.toc = self.macros['toc']
                else:
                    self.toc = TableOfContent()
                    self.macros['toc'] = self.toc
            else:
                try:
                    self.toc = getattrself.macros'toc'
                except AttributeError:
                    self.toc = TableOfContent()
                    self.macros.toc = self.toc

            if verbose is None:
                self.verbose = 1
            else:
                self.verbose = verbose
            if stderr is None:
                self.stderr = sys.stderr
            else:
                self.stderr = stderr

    def get_text(self, node):
        """Try to emit whatever text is in the node."""
        try:
            return node.children[0].content or ''
        except:
            return node.content or ''

    def html_escape(self, text):
        return escape(text)

    def attr_escape(self, text):
        return self.html_escape(text).replace('"', '&quot')

    def document_emit(self, node):
        return self.emit_children(node)

    def text_emit(self, node):
        return self.html_escape(node.content)

    def separator_emit(self, node):
        return '<hr />\n\n'

    def paragraph_emit(self, node):
        return '<p>%s</p>\n' % self.emit_children(node)

    def _list_emit(self, node, list_type):
        if node.parent.kind in ('document', ):
            formatter = ''
        else:
            formatter = '\n'
        if list_type == 'li':
            formatter += '%(i)s<%(t)s>%(c)s</%(t)s>'
        else:
            formatter += '%(i)s<%(t)s>%(c)s\n%(i)s</%(t)s>'
        return formatter % {'i':'\t' * node.level, 
         'c':self.emit_children(node), 
         't':list_type}

    def bullet_list_emit(self, node):
        return self._list_emit(node, list_type='ul')

    def number_list_emit(self, node):
        return self._list_emit(node, list_type='ol')

    def list_item_emit(self, node):
        return self._list_emit(node, list_type='li')

    def table_emit(self, node):
        return '<table>\n%s</table>\n' % self.emit_children(node)

    def table_row_emit(self, node):
        return '<tr>\n%s</tr>\n' % self.emit_children(node)

    def table_cell_emit(self, node):
        return '\t<td>%s</td>\n' % self.emit_children(node)

    def table_head_emit(self, node):
        return '\t<th>%s</th>\n' % self.emit_children(node)

    def _typeface(self, node, tag):
        return '<%(tag)s>%(data)s</%(tag)s>' % {'tag':tag, 
         'data':self.emit_children(node)}

    def emphasis_emit(self, node):
        return self._typeface(node, tag='i')

    def strong_emit(self, node):
        return self._typeface(node, tag='strong')

    def monospace_emit(self, node):
        return self._typeface(node, tag='tt')

    def superscript_emit(self, node):
        return self._typeface(node, tag='sup')

    def subscript_emit(self, node):
        return self._typeface(node, tag='sub')

    def underline_emit(self, node):
        return self._typeface(node, tag='u')

    def small_emit(self, node):
        return self._typeface(node, tag='small')

    def delete_emit(self, node):
        return self._typeface(node, tag='del')

    def header_emit(self, node):
        header = '<h%d>%s</h%d>' % (
         node.level, self.html_escape(node.content), node.level)
        if self.toc is not None:
            self.toc.add_headline(node.level, node.content)
            header = '<a name="%s">%s</a>' % (
             self.html_escape(node.content), header)
        header += '\n'
        return header

    def preformatted_emit(self, node):
        return '<pre>%s</pre>' % self.html_escape(node.content)

    def link_emit(self, node):
        target = node.content
        if node.children:
            inside = self.emit_children(node)
        else:
            inside = self.html_escape(target)
        return '<a href="%s">%s</a>' % (
         self.attr_escape(target), inside)

    def image_emit(self, node):
        target = node.content
        text = self.attr_escape(self.get_text(node))
        return '<img src="%s" title="%s" alt="%s" />' % (
         self.attr_escape(target), text, text)

    def macro_emit(self, node):
        macro_name = node.macro_name
        text = node.content
        macro = None
        args = node.macro_args
        try:
            macro_kwargs = string2dict(args)
        except ValueError as e:
            try:
                exc_info = sys.exc_info()
                return self.error("Wrong macro arguments: %s for macro '%s' (maybe wrong macro tag syntax?)" % (
                 repr2(args), macro_name), exc_info)
            finally:
                e = None
                del e

        macro_kwargs['text'] = text
        macro_kwargs['view'] = self.view
        exc_info = None
        if isinstanceself.macrosdict:
            try:
                macro = self.macros[macro_name]
            except KeyError as e:
                try:
                    exc_info = sys.exc_info()
                finally:
                    e = None
                    del e

        else:
            try:
                macro = getattrself.macrosmacro_name
            except AttributeError as e:
                try:
                    exc_info = sys.exc_info()
                finally:
                    e = None
                    del e

            if macro == None:
                return self.error("Macro '%s' doesn't exist" % macro_name, exc_info)
            try:
                result = macro(**macro_kwargs)
            except TypeError as err:
                try:
                    msg = "Macro '%s' error: %s" % (macro_name, err)
                    exc_info = sys.exc_info()
                    if self.verbose > 1:
                        if self.verbose > 2:
                            raise
                        etype, evalue, etb = exc_info
                        import inspect
                        try:
                            filename = inspect.getfile(macro)
                        except TypeError:
                            pass
                        else:
                            try:
                                sourceline = inspect.getsourcelines(macro)[0][0].strip()
                            except IOError as err:
                                try:
                                    evalue = etype('%s (error getting sourceline: %s from %s)' % (evalue, err, filename))
                                finally:
                                    err = None
                                    del err

                            else:
                                evalue = etype('%s (sourceline: %r from %s)' % (evalue, sourceline, filename))
                            exc_info = (
                             etype, evalue, etb)
                    return self.error(msg, exc_info)
                finally:
                    err = None
                    del err

            except Exception as err:
                try:
                    return self.error(("Macro '%s' error: %s" % (macro_name, err)),
                      exc_info=(sys.exc_info()))
                finally:
                    err = None
                    del err

            if not isinstanceresultTEXT_TYPE:
                msg = "Macro '%s' doesn't return a unicode string!" % macro_name
                if self.verbose > 1:
                    msg += ' - returns: %r, type %r' % (result, type(result))
                return self.error(msg)
            if node.kind == 'macro_block':
                result += '\n'
            return result

    macro_inline_emit = macro_emit
    macro_block_emit = macro_emit

    def break_emit(self, node):
        if node.parent.kind == 'list_item':
            return '<br />\n' + '\t' * node.parent.level
        if node.parent.kind in ('table_head', 'table_cell'):
            return '<br />\n\t\t'
        return '<br />\n'

    def line_emit(self, node):
        return '\n'

    def pre_block_emit(self, node):
        """ pre block, with newline at the end """
        return '<pre>%s</pre>\n' % self.html_escape(node.content)

    def pre_inline_emit(self, node):
        """ pre without newline at the end """
        return '<tt>%s</tt>' % self.html_escape(node.content)

    def default_emit(self, node):
        """Fallback function for emitting unknown nodes."""
        raise NotImplementedError("Node '%s' unknown" % node.kind)

    def emit_children(self, node):
        """Emit all the children of a node."""
        return ''.join([self.emit_node(child) for child in node.children])

    def emit_node(self, node):
        """Emit a single node."""
        emit = getattr(self, '%s_emit' % node.kind, self.default_emit)
        return emit(node)

    def emit(self):
        """Emit the document represented by self.root DOM tree."""
        document = self.emit_node(self.root).strip()
        if self.toc is not None:
            return self.toc.emit(document)
        return document

    def error(self, text, exc_info=None):
        """
        Error Handling.
        """
        if self.verbose > 1:
            if exc_info:
                exc_type, exc_value, exc_traceback = exc_info
                exception = ''.join(traceback.format_exception(exc_type, exc_value, exc_traceback))
                self.stderr.write(exception)
        if self.verbose > 0:
            return '[Error: %s]\n' % text
        return ''


if __name__ == '__main__':
    txt = 'Local test\n<<toc>>\n= headline 1 level 1\n== headline 2 level 2\n== headline 3 level 2\n==== headline 4 level 4\n= headline 5 level 1\n=== headline 6 level 3\n'
    print('--------------------------------------------------------------------------------')
    p = CreoleParser(txt)
    document = p.parse()
    p.debug()
    html = HtmlEmitter(document, verbose=999).emit()
    print(html)
    print('-------------------------------------------------------------------------------')
    print(html.replace(' ', '.').replace('\n', '\\n\n'))