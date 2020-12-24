# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/makism/Github/dyconnmap-public-master/docs/sphinxext/numpy_ext/docscrape.py
# Compiled at: 2019-10-19 16:20:24
# Size of source mod 2**32: 15426 bytes
"""Extract reference documentation from the NumPy source tree.

"""
import inspect, textwrap, re, pydoc
from warnings import warn
try:
    from io import StringIO
except:
    from io import StringIO

class Reader(object):
    __doc__ = 'A line-based string reader.\n\n    '

    def __init__(self, data):
        """
        Parameters
        ----------
        data : str
           String with lines separated by '
'.

        """
        if isinstance(data, list):
            self._str = data
        else:
            self._str = data.split('\n')
        self.reset()

    def __getitem__(self, n):
        return self._str[n]

    def reset(self):
        self._l = 0

    def read(self):
        if not self.eof():
            out = self[self._l]
            self._l += 1
            return out
        return ''

    def seek_next_non_empty_line(self):
        for l in self[self._l:]:
            if l.strip():
                break
            else:
                self._l += 1

    def eof(self):
        return self._l >= len(self._str)

    def read_to_condition(self, condition_func):
        start = self._l
        for line in self[start:]:
            if condition_func(line):
                return self[start:self._l]
                self._l += 1
                if self.eof():
                    return self[start:self._l + 1]

        return []

    def read_to_next_empty_line(self):
        self.seek_next_non_empty_line()

        def is_empty(line):
            return not line.strip()

        return self.read_to_condition(is_empty)

    def read_to_next_unindented_line(self):

        def is_unindented(line):
            return line.strip() and len(line.lstrip()) == len(line)

        return self.read_to_condition(is_unindented)

    def peek(self, n=0):
        if self._l + n < len(self._str):
            return self[(self._l + n)]
        return ''

    def is_empty(self):
        return not ''.join(self._str).strip()


class NumpyDocString(object):

    def __init__(self, docstring, config={}):
        docstring = textwrap.dedent(docstring).split('\n')
        self._doc = Reader(docstring)
        self._parsed_data = {'Signature':'', 
         'Summary':[
          ''], 
         'Extended Summary':[],  'Parameters':[],  'Returns':[],  'Raises':[],  'Warns':[],  'Other Parameters':[],  'Attributes':[],  'Methods':[],  'See Also':[],  'Notes':[],  'Warnings':[],  'References':'', 
         'Examples':'', 
         'index':{}}
        self._parse()

    def __getitem__(self, key):
        return self._parsed_data[key]

    def __setitem__(self, key, val):
        if key not in self._parsed_data:
            warn('Unknown section %s' % key)
        else:
            self._parsed_data[key] = val

    def _is_at_section(self):
        self._doc.seek_next_non_empty_line()
        if self._doc.eof():
            return False
        l1 = self._doc.peek().strip()
        if l1.startswith('.. index::'):
            return True
        l2 = self._doc.peek(1).strip()
        return l2.startswith('-' * len(l1)) or l2.startswith('=' * len(l1))

    def _strip(self, doc):
        i = 0
        j = 0
        for i, line in enumerate(doc):
            if line.strip():
                break

        for j, line in enumerate(doc[::-1]):
            if line.strip():
                break

        return doc[i:len(doc) - j]

    def _read_to_next_section(self):
        section = self._doc.read_to_next_empty_line()
        while not self._is_at_section():
            if not self._doc.eof():
                if not self._doc.peek(-1).strip():
                    section += ['']
                section += self._doc.read_to_next_empty_line()

        return section

    def _read_sections(self):
        while not self._doc.eof():
            data = self._read_to_next_section()
            name = data[0].strip()
            if name.startswith('..'):
                yield (
                 name, data[1:])
            elif len(data) < 2:
                yield StopIteration
            else:
                yield (
                 name, self._strip(data[2:]))

    def _parse_param_list(self, content):
        r = Reader(content)
        params = []
        while not r.eof():
            header = r.read().strip()
            if ' : ' in header:
                arg_name, arg_type = header.split(' : ')[:2]
            else:
                arg_name, arg_type = header, ''
            desc = r.read_to_next_unindented_line()
            desc = dedent_lines(desc)
            params.append((arg_name, arg_type, desc))

        return params

    _name_rgx = re.compile('^\\s*(:(?P<role>\\w+):`(?P<name>[a-zA-Z0-9_.-]+)`| (?P<name2>[a-zA-Z0-9_.-]+))\\s*', re.X)

    def _parse_see_also--- This code section failed: ---

 L. 208         0  BUILD_LIST_0          0 
                2  STORE_DEREF              'items'

 L. 210         4  LOAD_CLOSURE             'self'
                6  BUILD_TUPLE_1         1 
                8  LOAD_CODE                <code_object parse_item_name>
               10  LOAD_STR                 'NumpyDocString._parse_see_also.<locals>.parse_item_name'
               12  MAKE_FUNCTION_8          'closure'
               14  STORE_DEREF              'parse_item_name'

 L. 221        16  LOAD_CLOSURE             'items'
               18  LOAD_CLOSURE             'parse_item_name'
               20  BUILD_TUPLE_2         2 
               22  LOAD_CODE                <code_object push_item>
               24  LOAD_STR                 'NumpyDocString._parse_see_also.<locals>.push_item'
               26  MAKE_FUNCTION_8          'closure'
               28  STORE_FAST               'push_item'

 L. 228        30  LOAD_CONST               None
               32  STORE_FAST               'current_func'

 L. 229        34  BUILD_LIST_0          0 
               36  STORE_FAST               'rest'

 L. 231        38  SETUP_LOOP          288  'to 288'
               40  LOAD_FAST                'content'
               42  GET_ITER         
             44_0  COME_FROM           268  '268'
               44  FOR_ITER            286  'to 286'
               46  STORE_FAST               'line'

 L. 232        48  LOAD_FAST                'line'
               50  LOAD_METHOD              strip
               52  CALL_METHOD_0         0  '0 positional arguments'
               54  POP_JUMP_IF_TRUE     58  'to 58'

 L. 233        56  CONTINUE             44  'to 44'
             58_0  COME_FROM            54  '54'

 L. 235        58  LOAD_DEREF               'self'
               60  LOAD_ATTR                _name_rgx
               62  LOAD_METHOD              match
               64  LOAD_FAST                'line'
               66  CALL_METHOD_1         1  '1 positional argument'
               68  STORE_FAST               'm'

 L. 236        70  LOAD_FAST                'm'
               72  POP_JUMP_IF_FALSE   180  'to 180'
               74  LOAD_FAST                'line'
               76  LOAD_FAST                'm'
               78  LOAD_METHOD              end
               80  CALL_METHOD_0         0  '0 positional arguments'
               82  LOAD_CONST               None
               84  BUILD_SLICE_2         2 
               86  BINARY_SUBSCR    
               88  LOAD_METHOD              strip
               90  CALL_METHOD_0         0  '0 positional arguments'
               92  LOAD_METHOD              startswith
               94  LOAD_STR                 ':'
               96  CALL_METHOD_1         1  '1 positional argument'
               98  POP_JUMP_IF_FALSE   180  'to 180'

 L. 237       100  LOAD_FAST                'push_item'
              102  LOAD_FAST                'current_func'
              104  LOAD_FAST                'rest'
              106  CALL_FUNCTION_2       2  '2 positional arguments'
              108  POP_TOP          

 L. 238       110  LOAD_FAST                'line'
              112  LOAD_CONST               None
              114  LOAD_FAST                'm'
              116  LOAD_METHOD              end
              118  CALL_METHOD_0         0  '0 positional arguments'
              120  BUILD_SLICE_2         2 
              122  BINARY_SUBSCR    
              124  LOAD_FAST                'line'
              126  LOAD_FAST                'm'
              128  LOAD_METHOD              end
              130  CALL_METHOD_0         0  '0 positional arguments'
              132  LOAD_CONST               None
              134  BUILD_SLICE_2         2 
              136  BINARY_SUBSCR    
              138  ROT_TWO          
              140  STORE_FAST               'current_func'
              142  STORE_FAST               'line'

 L. 239       144  LOAD_FAST                'line'
              146  LOAD_METHOD              split
              148  LOAD_STR                 ':'
              150  LOAD_CONST               1
              152  CALL_METHOD_2         2  '2 positional arguments'
              154  LOAD_CONST               1
              156  BINARY_SUBSCR    
              158  LOAD_METHOD              strip
              160  CALL_METHOD_0         0  '0 positional arguments'
              162  BUILD_LIST_1          1 
              164  STORE_FAST               'rest'

 L. 240       166  LOAD_FAST                'rest'
              168  LOAD_CONST               0
              170  BINARY_SUBSCR    
              172  POP_JUMP_IF_TRUE    178  'to 178'

 L. 241       174  BUILD_LIST_0          0 
              176  STORE_FAST               'rest'
            178_0  COME_FROM           172  '172'
              178  JUMP_BACK            44  'to 44'
            180_0  COME_FROM            98  '98'
            180_1  COME_FROM            72  '72'

 L. 242       180  LOAD_FAST                'line'
              182  LOAD_METHOD              startswith
              184  LOAD_STR                 ' '
              186  CALL_METHOD_1         1  '1 positional argument'
          188_190  POP_JUMP_IF_TRUE    262  'to 262'

 L. 243       192  LOAD_FAST                'push_item'
              194  LOAD_FAST                'current_func'
              196  LOAD_FAST                'rest'
              198  CALL_FUNCTION_2       2  '2 positional arguments'
              200  POP_TOP          

 L. 244       202  LOAD_CONST               None
              204  STORE_FAST               'current_func'

 L. 245       206  LOAD_STR                 ','
              208  LOAD_FAST                'line'
              210  COMPARE_OP               in
              212  POP_JUMP_IF_FALSE   246  'to 246'

 L. 246       214  SETUP_LOOP          260  'to 260'
              216  LOAD_FAST                'line'
              218  LOAD_METHOD              split
              220  LOAD_STR                 ','
              222  CALL_METHOD_1         1  '1 positional argument'
              224  GET_ITER         
              226  FOR_ITER            242  'to 242'
              228  STORE_FAST               'func'

 L. 247       230  LOAD_FAST                'push_item'
              232  LOAD_FAST                'func'
              234  BUILD_LIST_0          0 
              236  CALL_FUNCTION_2       2  '2 positional arguments'
              238  POP_TOP          
              240  JUMP_BACK           226  'to 226'
              242  POP_BLOCK        
              244  JUMP_FORWARD        260  'to 260'
            246_0  COME_FROM           212  '212'

 L. 248       246  LOAD_FAST                'line'
              248  LOAD_METHOD              strip
              250  CALL_METHOD_0         0  '0 positional arguments'
          252_254  POP_JUMP_IF_FALSE   284  'to 284'

 L. 249       256  LOAD_FAST                'line'
              258  STORE_FAST               'current_func'
            260_0  COME_FROM           244  '244'
            260_1  COME_FROM_LOOP      214  '214'
              260  JUMP_BACK            44  'to 44'
            262_0  COME_FROM           188  '188'

 L. 250       262  LOAD_FAST                'current_func'
              264  LOAD_CONST               None
              266  COMPARE_OP               is-not
              268  POP_JUMP_IF_FALSE    44  'to 44'

 L. 251       270  LOAD_FAST                'rest'
              272  LOAD_METHOD              append
              274  LOAD_FAST                'line'
              276  LOAD_METHOD              strip
              278  CALL_METHOD_0         0  '0 positional arguments'
              280  CALL_METHOD_1         1  '1 positional argument'
              282  POP_TOP          
            284_0  COME_FROM           252  '252'
              284  JUMP_BACK            44  'to 44'
              286  POP_BLOCK        
            288_0  COME_FROM_LOOP       38  '38'

 L. 252       288  LOAD_FAST                'push_item'
              290  LOAD_FAST                'current_func'
              292  LOAD_FAST                'rest'
              294  CALL_FUNCTION_2       2  '2 positional arguments'
              296  POP_TOP          

 L. 253       298  LOAD_DEREF               'items'
              300  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `COME_FROM_LOOP' instruction at offset 260_1

    def _parse_index(self, section, content):
        """
        .. index: default
           :refguide: something, else, and more

        """

        def strip_each_in(lst):
            return [s.strip() for s in lst]

        out = {}
        section = section.split('::')
        if len(section) > 1:
            out['default'] = strip_each_in(section[1].split(','))[0]
        for line in content:
            line = line.split(':')
            if len(line) > 2:
                out[line[1]] = strip_each_in(line[2].split(','))

        return out

    def _parse_summary(self):
        """Grab signature (if given) and summary"""
        if self._is_at_section():
            return
            summary = self._doc.read_to_next_empty_line()
            summary_str = ' '.join([s.strip() for s in summary]).strip()
            if re.compile('^([\\w., ]+=)?\\s*[\\w\\.]+\\(.*\\)$').match(summary_str):
                self['Signature'] = summary_str
                if not self._is_at_section():
                    self['Summary'] = self._doc.read_to_next_empty_line()
        else:
            self['Summary'] = summary
        if not self._is_at_section():
            self['Extended Summary'] = self._read_to_next_section()

    def _parse(self):
        self._doc.reset()
        self._parse_summary()
        for section, content in self._read_sections():
            if not section.startswith('..'):
                section = ' '.join([s.capitalize() for s in section.split(' ')])
            if section in ('Parameters', 'Attributes', 'Methods', 'Returns', 'Raises',
                           'Warns'):
                self[section] = self._parse_param_list(content)
            elif section.startswith('.. index::'):
                self['index'] = self._parse_index(section, content)
            elif section == 'See Also':
                self['See Also'] = self._parse_see_also(content)
            else:
                self[section] = content

    def _str_header(self, name, symbol='-'):
        return [
         name, len(name) * symbol]

    def _str_indent(self, doc, indent=4):
        out = []
        for line in doc:
            out += [' ' * indent + line]

        return out

    def _str_signature(self):
        if self['Signature']:
            return [
             self['Signature'].replace('*', '\\*')] + ['']
        return ['']

    def _str_summary(self):
        if self['Summary']:
            return self['Summary'] + ['']
        return []

    def _str_extended_summary(self):
        if self['Extended Summary']:
            return self['Extended Summary'] + ['']
        return []

    def _str_param_list(self, name):
        out = []
        if self[name]:
            out += self._str_header(name)
            for param, param_type, desc in self[name]:
                out += ['%s : %s' % (param, param_type)]
                out += self._str_indent(desc)

            out += ['']
        return out

    def _str_section(self, name):
        out = []
        if self[name]:
            out += self._str_header(name)
            out += self[name]
            out += ['']
        return out

    def _str_see_also(self, func_role):
        if not self['See Also']:
            return []
        out = []
        out += self._str_header('See Also')
        last_had_desc = True
        for func, desc, role in self['See Also']:
            if role:
                link = ':%s:`%s`' % (role, func)
            else:
                if func_role:
                    link = ':%s:`%s`' % (func_role, func)
                else:
                    link = '`%s`_' % func
            if desc or last_had_desc:
                out += ['']
                out += [link]
            else:
                out[(-1)] += ', %s' % link
            if desc:
                out += self._str_indent([' '.join(desc)])
                last_had_desc = True
            else:
                last_had_desc = False

        out += ['']
        return out

    def _str_index(self):
        idx = self['index']
        out = []
        out += ['.. index:: %s' % idx.get('default', '')]
        for section, references in idx.items():
            if section == 'default':
                continue
            out += ['   :%s: %s' % (section, ', '.join(references))]

        return out

    def __str__(self, func_role=''):
        out = []
        out += self._str_signature()
        out += self._str_summary()
        out += self._str_extended_summary()
        for param_list in ('Parameters', 'Returns', 'Raises'):
            out += self._str_param_list(param_list)

        out += self._str_section('Warnings')
        out += self._str_see_also(func_role)
        for s in ('Notes', 'References', 'Examples'):
            out += self._str_section(s)

        for param_list in ('Attributes', 'Methods'):
            out += self._str_param_list(param_list)

        out += self._str_index()
        return '\n'.join(out)


def indent(str, indent=4):
    indent_str = ' ' * indent
    if str is None:
        return indent_str
    lines = str.split('\n')
    return '\n'.join((indent_str + l for l in lines))


def dedent_lines(lines):
    """Deindent a list of lines maximally"""
    return textwrap.dedent('\n'.join(lines)).split('\n')


def header(text, style='-'):
    return text + '\n' + style * len(text) + '\n'


class FunctionDoc(NumpyDocString):

    def __init__(self, func, role='func', doc=None, config={}):
        self._f = func
        self._role = role
        if doc is None:
            if func is None:
                raise ValueError('No function or docstring given')
            doc = inspect.getdoc(func) or ''
        else:
            NumpyDocString.__init__(self, doc)
            if not self['Signature']:
                if func is not None:
                    func, func_name = self.get_func()
                    try:
                        argspec = inspect.getargspec(func)
                        argspec = (inspect.formatargspec)(*argspec)
                        argspec = argspec.replace('*', '\\*')
                        signature = '%s%s' % (func_name, argspec)
                    except TypeError as e:
                        try:
                            signature = '%s()' % func_name
                        finally:
                            e = None
                            del e

                    self['Signature'] = signature

    def get_func(self):
        func_name = getattr(self._f, '__name__', self.__class__.__name__)
        if inspect.isclass(self._f):
            func = getattr(self._f, '__call__', self._f.__init__)
        else:
            func = self._f
        return (
         func, func_name)

    def __str__(self):
        out = ''
        func, func_name = self.get_func()
        signature = self['Signature'].replace('*', '\\*')
        roles = {'func':'function', 
         'meth':'method'}
        if self._role:
            if self._role not in roles:
                print('Warning: invalid role %s' % self._role)
            out += '.. %s:: %s\n    \n\n' % (roles.get(self._role, ''),
             func_name)
        out += super(FunctionDoc, self).__str__(func_role=(self._role))
        return out


class ClassDoc(NumpyDocString):

    def __init__(self, cls, doc=None, modulename='', func_doc=FunctionDoc, config=None):
        if not inspect.isclass(cls):
            if cls is not None:
                raise ValueError('Expected a class or None, but got %r' % cls)
            else:
                self._cls = cls
                if modulename:
                    modulename.endswith('.') or modulename += '.'
            self._mod = modulename
            if doc is None:
                if cls is None:
                    raise ValueError('No class or documentation string given')
                doc = pydoc.getdoc(cls)
        else:
            NumpyDocString.__init__(self, doc)
            if config is not None:
                if config.get('show_class_members', True):
                    if not self['Methods']:
                        self['Methods'] = [(name, '', '') for name in sorted(self.methods)]
                    if not self['Attributes']:
                        self['Attributes'] = [(name, '', '') for name in sorted(self.properties)]

    @property
    def methods(self):
        if self._cls is None:
            return []
        return [name for name, func in inspect.getmembers(self._cls) if not name.startswith('_') if callable(func)]

    @property
    def properties(self):
        if self._cls is None:
            return []
        return [name for name, func in inspect.getmembers(self._cls) if not name.startswith('_') if func is None]