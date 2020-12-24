# uncompyle6 version 3.7.4
# Python bytecode 3.3 (3230)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\patrom.py
# Compiled at: 2017-01-28 08:50:54
# Size of source mod 2**32: 10900 bytes
import os, sys, io, tokenize, traceback, random, string, html.parser

class TemplateError(Exception):

    def __init__(self, msg, parser, text):
        self.msg = msg
        self.line, self.column = parser.getpos()
        self.text = text

    def __str__(self):
        return '{} line {}'.format(self.msg, self.line)


class TemplateParser(html.parser.HTMLParser):
    forbidden = [
     'import', 'exec', '__builtins__', '__import__']
    PY_TAG = 'py'

    def __init__(self, *args, **kw):
        kw.setdefault('convert_charrefs', True)
        try:
            html.parser.HTMLParser.__init__(self, *args, **kw)
        except TypeError:
            del kw['convert_charrefs']
            html.parser.HTMLParser.__init__(self, *args, **kw)

        self.src = ''
        self.indent = 0
        self.py_tags = []
        self.pyline = 0
        self.line_mapping = {}

    def _randname(self):
        return ''.join(random.choice(string.ascii_letters) for i in range(8))

    def add(self, source, text):
        line, column = self.getpos()
        self.src += self.indent * '    ' + source + '\n'
        self.pyline += 1 + source.count('\n')
        self.line_mapping[self.pyline] = (line, column, text)

    def control(self, source, text):
        """Control that Python source code doesn't include sensible
        names"""
        reader = io.BytesIO(source.encode('utf-8')).readline
        for tok_type, tok, *args in tokenize.tokenize(reader):
            if tok_type == tokenize.NAME:
                if tok in self.forbidden:
                    msg = 'forbidden name "{}"'
                    raise TemplateError(msg.format(tok), self, text)
                else:
                    continue

    def handle_starttag(self, tag, attrs):
        """Handle a start tag
        If tag is PY_TAG :
        - add its attribute "code" to generated source code
        - if the code starts a block (ie ends with ":"), increment indentation.

        Else print the tag, formatted by method _format()
        """
        text = self.get_starttag_text()
        line, column = self.getpos()
        if tag == self.PY_TAG:
            for name, value in attrs:
                if name == 'code':
                    has_code = True
                    value = value.rstrip()
                    self.control(value, text)
                    self.add(value, text)
                    self.py_tags.append([value, self.get_starttag_text(),
                     (
                      line, column)])
                    if value.endswith(':'):
                        self.indent += 1
                    break
                elif name == 'expr':
                    raise TemplateError('attribute expr is only supported in start/end tags, not in start tags', self, text)
                else:
                    msg = 'unknown attribute "{}"'
                    raise TemplateError(msg.format(name), self, text)
            else:
                msg = 'py tag missing attribute "code"'
                raise TemplateError(msg, self, text)

        else:
            self.handle_attrs(tag, attrs, text)

    def handle_startendtag(self, tag, attrs):
        """Handle a startend tag, ie a tag ending with />"""
        text = self.get_starttag_text()
        if tag == self.PY_TAG:
            line, column = self.getpos()
            has_expr = False
            for name, value in attrs:
                if name == 'code':
                    has_expr = True
                    value = value.rstrip()
                    self.control(value, text)
                    if value.endswith(':'):
                        msg = 'A single py tag cannot start a code block : {}'
                        raise TemplateError(msg.format(text), self, text)
                    self.add(value, text)
                elif name == 'expr':
                    has_expr = True
                    value = value.strip()
                    self.add('print({}, end="")'.format(value), text)
                elif name == 'include':
                    has_expr = True
                    path = os.path.join(os.path.dirname(self.filename), value.strip())
                    res = TemplateParser().render(path, **self.kw)
                    if value.strip() == 'header.html':
                        with open('trace_header.py', 'w', encoding='utf-8') as (out):
                            out.write(res)
                    self.add('print("""{}""", end="")'.format(res), text)
                else:
                    msg = 'unknown attribute "{}" - use "code"'
                    raise TemplateError(msg.format(name), self, text)

            if not has_expr:
                msg = 'py/ tag missing attribute "code" or "expr"'
                raise TemplateError(msg, self, text)
        else:
            self.handle_attrs(tag, attrs, text)

    def handle_endtag(self, tag):
        text = '</{}>'.format(tag)
        if tag == self.PY_TAG:
            if not self.py_tags:
                msg = 'unexpected closing tag </py>'
                raise TemplateError(msg, self, text)
            value, text, pos = self.py_tags.pop()
            if value.endswith(':'):
                self.indent -= 1
        else:
            self.add('print("{}")'.format(text), text)

    def handle_data(self, data):
        """Data is printed unchanged"""
        if data.strip():
            self.add('print("""{}""", end="")'.format(data), data)

    def handle_decl(self, decl):
        """Declaration is printed unchanged"""
        self.add('print("""<!{}>""")'.format(decl), decl)

    def handle_attrs(self, tag, attrs, text):
        """Used for tags other than <py> ; if they have an attribute named 
        "attrs", its value must be of the form key1=value1, key2=value2... ; 
        this value is used as argument of dict(), and the resulting dictionary 
        is used to generate tag attributes "key1=value1 key2=value2 ...".
        If the value associated with a key is True, only the key is added
        (eg selected=True) ; if it is False, the key is ignored"""
        if 'attrs' not in [name for name, value in attrs]:
            self.add('print("""{}""", end="")'.format(text), text)
            return
        txt = '<{} '.format(tag)
        simple = ['{}=\\"{}\\"'.format(name, value.replace("'", "\\'")) for name, value in attrs if name != 'attrs']
        txt += ' '.join(simple)
        self.add('print("{}", end="")'.format(txt), text)
        for name, args in attrs:
            if name == 'attrs':
                key_name = 'key_{}'.format(self._randname())
                value_name = 'value_{}'.format(self._randname())
                self.add('for {}, {} in dict({}).items():'.format(key_name, value_name, args), text)
                self.add('    if not isinstance({}, bool):'.format(value_name), text)
                self.add('        print("{{}}=\\"{{}}\\" ".format({}, {}), end=" ")'.format(key_name, value_name), text)
                self.add('    elif {}:'.format(value_name), text)
                self.add('        print("{{}}".format({}), end=" ")'.format(key_name), text)
                continue

        self.add('print(">", end="")', text)

    def render--- This code section failed: ---

 L. 203         0  LOAD_DEREF               'filename'
                3  LOAD_DEREF               'self'
                6  STORE_ATTR               filename

 L. 204         9  LOAD_FAST                'kw'
               12  LOAD_DEREF               'self'
               15  STORE_ATTR               kw

 L. 206        18  LOAD_CLOSURE             'exc'
               21  LOAD_CLOSURE             'filename'
               24  LOAD_CLOSURE             'self'
               27  BUILD_TUPLE_3         3 
               30  LOAD_CODE                <code_object _debug>
               33  LOAD_STR                 'TemplateParser.render.<locals>._debug'
               36  MAKE_CLOSURE_0           '0 positional, 0 keyword only, 0 annotated'
               39  STORE_FAST               '_debug'

 L. 233        42  LOAD_GLOBAL              sys
               45  LOAD_ATTR                stdout
               48  STORE_FAST               'save_stdout'

 L. 236        51  LOAD_GLOBAL              open
               54  LOAD_DEREF               'filename'
               57  LOAD_STR                 'encoding'
               60  LOAD_STR                 'utf-8'
               63  CALL_FUNCTION_257   257  '1 positional, 1 named'
               66  SETUP_WITH           88  'to 88'
               69  STORE_FAST               'fobj'

 L. 237        72  LOAD_FAST                'fobj'
               75  LOAD_ATTR                read
               78  CALL_FUNCTION_0       0  '0 positional, 0 named'
               81  STORE_FAST               'tmpl_source'
               84  POP_BLOCK        
               85  LOAD_CONST               None
             88_0  COME_FROM_WITH       66  '66'
               88  WITH_CLEANUP     
               89  END_FINALLY      

 L. 239        90  SETUP_FINALLY       390  'to 390'
               93  SETUP_EXCEPT        306  'to 306'

 L. 240        96  LOAD_DEREF               'self'
               99  LOAD_ATTR                feed
              102  LOAD_FAST                'tmpl_source'
              105  CALL_FUNCTION_1       1  '1 positional, 0 named'
              108  POP_TOP          

 L. 241       109  LOAD_DEREF               'self'
              112  LOAD_ATTR                close
              115  CALL_FUNCTION_0       0  '0 positional, 0 named'
              118  POP_TOP          

 L. 243       119  LOAD_DEREF               'self'
              122  LOAD_ATTR                py_tags
              125  POP_JUMP_IF_FALSE   185  'to 185'

 L. 244       128  LOAD_DEREF               'self'
              131  LOAD_ATTR                py_tags
              134  LOAD_ATTR                pop
              137  CALL_FUNCTION_0       0  '0 positional, 0 named'
              140  UNPACK_SEQUENCE_3     3 
              143  STORE_FAST               'value'
              146  STORE_FAST               'text'
              149  UNPACK_SEQUENCE_2     2 
              152  STORE_FAST               'line'
              155  STORE_FAST               'column'

 L. 245       158  LOAD_STR                 'Unclosed py tag line {} column {} : {}'
              161  STORE_FAST               'msg'

 L. 246       164  LOAD_GLOBAL              TemplateError
              167  LOAD_FAST                'msg'
              170  LOAD_DEREF               'self'
              173  LOAD_FAST                'text'
              176  CALL_FUNCTION_3       3  '3 positional, 0 named'
              179  RAISE_VARARGS_1       1  'exception'
              182  JUMP_FORWARD        185  'to 185'
            185_0  COME_FROM           182  '182'

 L. 248       185  LOAD_GLOBAL              io
              188  LOAD_ATTR                StringIO
              191  CALL_FUNCTION_0       0  '0 positional, 0 named'
              194  LOAD_GLOBAL              sys
              197  STORE_ATTR               stdout

 L. 250       200  LOAD_STR                 'trace.py'
              203  STORE_FAST               'trace'

 L. 251       206  LOAD_GLOBAL              open
              209  LOAD_FAST                'trace'
              212  LOAD_STR                 'w'
              215  LOAD_STR                 'encoding'
              218  LOAD_STR                 'utf-8'
              221  CALL_FUNCTION_258   258  '2 positional, 1 named'
              224  SETUP_WITH          269  'to 269'
              227  STORE_FAST               'out'

 L. 252       230  LOAD_FAST                'out'
              233  LOAD_ATTR                write
              236  LOAD_DEREF               'self'
              239  LOAD_ATTR                src
              242  CALL_FUNCTION_1       1  '1 positional, 0 named'
              245  POP_TOP          

 L. 253       246  LOAD_FAST                'out'
              249  LOAD_ATTR                write
              252  LOAD_GLOBAL              str
              255  LOAD_FAST                'kw'
              258  CALL_FUNCTION_1       1  '1 positional, 0 named'
              261  CALL_FUNCTION_1       1  '1 positional, 0 named'
              264  POP_TOP          
              265  POP_BLOCK        
              266  LOAD_CONST               None
            269_0  COME_FROM_WITH      224  '224'
              269  WITH_CLEANUP     
              270  END_FINALLY      

 L. 254       271  LOAD_GLOBAL              exec
              274  LOAD_DEREF               'self'
              277  LOAD_ATTR                src
              280  LOAD_FAST                'kw'
              283  CALL_FUNCTION_2       2  '2 positional, 0 named'
              286  STORE_FAST               'res'

 L. 255       289  LOAD_GLOBAL              sys
              292  LOAD_ATTR                stdout
              295  LOAD_ATTR                getvalue
              298  CALL_FUNCTION_0       0  '0 positional, 0 named'
              301  RETURN_VALUE     
              302  POP_BLOCK        
              303  JUMP_FORWARD        386  'to 386'
            306_0  COME_FROM_EXCEPT     93  '93'

 L. 257       306  DUP_TOP          
              307  LOAD_GLOBAL              Exception
              310  COMPARE_OP               exception-match
              313  POP_JUMP_IF_FALSE   385  'to 385'
              316  POP_TOP          
              317  STORE_DEREF              'exc'
              320  POP_TOP          
              321  SETUP_FINALLY       372  'to 372'

 L. 258       324  LOAD_FAST                '_debug'
              327  CALL_FUNCTION_0       0  '0 positional, 0 named'
              330  STORE_FAST               'message'

 L. 259       333  LOAD_GLOBAL              print
              336  LOAD_STR                 'error message'
              339  LOAD_FAST                'message'
              342  LOAD_STR                 '--end of error message'
              345  CALL_FUNCTION_3       3  '3 positional, 0 named'
              348  POP_TOP          

 L. 260       349  LOAD_GLOBAL              TemplateError
              352  LOAD_FAST                'message'
              355  LOAD_DEREF               'self'
              358  LOAD_FAST                'tmpl_source'
              361  CALL_FUNCTION_3       3  '3 positional, 0 named'
              364  RAISE_VARARGS_1       1  'exception'
              367  POP_BLOCK        
              368  POP_EXCEPT       
              369  LOAD_CONST               None
            372_0  COME_FROM_FINALLY   321  '321'
              372  LOAD_CONST               None
              375  STORE_DEREF              'exc'
              378  DELETE_DEREF             'exc'
              381  END_FINALLY      
              382  JUMP_FORWARD        386  'to 386'
              385  END_FINALLY      
            386_0  COME_FROM           382  '382'
            386_1  COME_FROM           303  '303'
              386  POP_BLOCK        
              387  LOAD_CONST               None
            390_0  COME_FROM_FINALLY    90  '90'

 L. 263       390  LOAD_FAST                'save_stdout'
              393  LOAD_GLOBAL              sys
              396  STORE_ATTR               stdout
              399  END_FINALLY      

Parse error at or near `DELETE_DEREF' instruction at offset 378


def render(src, **kw):
    tempname = 'template_test.html'
    with open(tempname, 'w', encoding='utf-8') as (out):
        out.write(src)
    return TemplateParser().render(tempname, **kw)