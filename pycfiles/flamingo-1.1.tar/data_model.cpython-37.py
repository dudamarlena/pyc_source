# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/fsc/work/devel/flamingo/flamingo/core/data_model.py
# Compiled at: 2020-03-29 13:24:11
# Size of source mod 2**32: 10665 bytes
import operator
from flamingo.core.errors import MultipleObjectsReturned, ObjectDoesNotExist
AND = operator.and_
NOT = operator.not_
OR = operator.or_
QUOTE_KEYS = ('content_body', 'template_context')

def quote(value):
    types = {str: lambda v: '<str({})>'.format(len(v)), 
     list: lambda v: '<list({})>'.format(len(v)), 
     tuple: lambda v: '<tuple({})>'.format(len(v)), 
     dict: '<dict(...)>', 
     Content: '<Content(...)>', 
     ContentSet: lambda v: '<ContentSet({})>'.format(len(v))}
    t = type(value)
    if t in types:
        if callable(types[t]):
            return types[t](value)
        return types[t]
    return str(value)


def _str(s):
    if s is not None:
        return str(s)
    return ''


LOGIC_FUNCTIONS = {'eq':lambda a, b: a == b, 
 'ne':lambda a, b: a != b, 
 'lt':lambda a, b: a < b, 
 'lte':lambda a, b: a <= b, 
 'gt':lambda a, b: a > b, 
 'gte':lambda a, b: a >= b, 
 'in':lambda a, b: a in b, 
 'contains':lambda a, b: _str(b) in _str(a), 
 'icontains':lambda a, b: _str(b).lower() in _str(a).lower(), 
 'isnull':lambda a, b:  if b:
a is None # Avoid dead code: a is not None, 
 'isfalse':lambda a, b:  if b:
not bool(a) # Avoid dead code: bool(a), 
 'startswith':lambda a, b: _str(a).startswith(b), 
 'endswith':lambda a, b: _str(a).endswith(b), 
 'passes':lambda a, b: b(a)}

class F:

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return "F('{}')".format(self.name)


class Q:

    def __init__(self, *qs, **lookups):
        self.connector = 'AND'
        self.negated = False
        self.qs = None
        self.lookups = None
        if not qs:
            if not lookups:
                raise TypeError('to few arguments')
        if qs:
            if lookups:
                raise TypeError('to many arguments')
        if not lookups:
            if len(qs) == 1:
                if isinstance(qs[0], dict):
                    lookups = qs[0]
                    qs = []
        if qs:
            self.qs = qs
        if lookups:
            self.lookups = lookups

    def __repr__(self):
        if self.qs:
            repr_str = ', '.join([repr(q) for q in self.qs])
        else:
            if self.lookups:
                repr_str = ', '.join(['{}={}'.format(k, repr(v)) for k, v in self.lookups.items()])
        return '<{}{}({})>'.format('NOT ' if self.negated else '', self.connector, repr_str)

    def __or__(self, other):
        q = Q(self, other)
        q.connector = 'OR'
        return q

    def __and__(self, other):
        return Q(self, other)

    def __invert__(self):
        self.negated = not self.negated
        return self

    def check--- This code section failed: ---

 L. 118         0  BUILD_LIST_0          0 
                2  STORE_FAST               'results'

 L. 119         4  LOAD_CONST               None
                6  STORE_FAST               'end_result'

 L. 121         8  LOAD_FAST                'self'
               10  LOAD_ATTR                qs
               12  POP_JUMP_IF_FALSE    48  'to 48'

 L. 122        14  SETUP_LOOP          184  'to 184'
               16  LOAD_FAST                'self'
               18  LOAD_ATTR                qs
               20  GET_ITER         
               22  FOR_ITER             44  'to 44'
               24  STORE_FAST               'q'

 L. 123        26  LOAD_FAST                'results'
               28  LOAD_METHOD              append
               30  LOAD_FAST                'q'
               32  LOAD_METHOD              check
               34  LOAD_FAST                'obj'
               36  CALL_METHOD_1         1  '1 positional argument'
               38  CALL_METHOD_1         1  '1 positional argument'
               40  POP_TOP          
               42  JUMP_BACK            22  'to 22'
               44  POP_BLOCK        
               46  JUMP_FORWARD        184  'to 184'
             48_0  COME_FROM            12  '12'

 L. 125        48  LOAD_FAST                'self'
               50  LOAD_ATTR                lookups
               52  POP_JUMP_IF_FALSE   184  'to 184'

 L. 126        54  SETUP_LOOP          184  'to 184'
               56  LOAD_FAST                'self'
               58  LOAD_ATTR                lookups
               60  LOAD_METHOD              items
               62  CALL_METHOD_0         0  '0 positional arguments'
               64  GET_ITER         
               66  FOR_ITER            182  'to 182'
               68  UNPACK_SEQUENCE_2     2 
               70  STORE_FAST               'field_name'
               72  STORE_FAST               'value'

 L. 127        74  LOAD_STR                 'eq'
               76  STORE_FAST               'logic_function'

 L. 129        78  LOAD_STR                 '__'
               80  LOAD_FAST                'field_name'
               82  COMPARE_OP               in
               84  POP_JUMP_IF_FALSE   100  'to 100'

 L. 130        86  LOAD_FAST                'field_name'
               88  LOAD_METHOD              split
               90  LOAD_STR                 '__'
               92  CALL_METHOD_1         1  '1 positional argument'
               94  UNPACK_SEQUENCE_2     2 
               96  STORE_FAST               'field_name'
               98  STORE_FAST               'logic_function'
            100_0  COME_FROM            84  '84'

 L. 132       100  LOAD_GLOBAL              isinstance
              102  LOAD_FAST                'value'
              104  LOAD_GLOBAL              F
              106  CALL_FUNCTION_2       2  '2 positional arguments'
              108  POP_JUMP_IF_FALSE   120  'to 120'

 L. 133       110  LOAD_FAST                'obj'
              112  LOAD_FAST                'value'
              114  LOAD_ATTR                name
              116  BINARY_SUBSCR    
              118  STORE_FAST               'value'
            120_0  COME_FROM           108  '108'

 L. 135       120  SETUP_EXCEPT        150  'to 150'

 L. 136       122  LOAD_FAST                'results'
              124  LOAD_METHOD              append

 L. 137       126  LOAD_GLOBAL              LOGIC_FUNCTIONS
              128  LOAD_FAST                'logic_function'
              130  BINARY_SUBSCR    

 L. 138       132  LOAD_FAST                'obj'
              134  LOAD_FAST                'field_name'
              136  BINARY_SUBSCR    
              138  LOAD_FAST                'value'
              140  CALL_FUNCTION_2       2  '2 positional arguments'
              142  CALL_METHOD_1         1  '1 positional argument'
              144  POP_TOP          
              146  POP_BLOCK        
              148  JUMP_BACK            66  'to 66'
            150_0  COME_FROM_EXCEPT    120  '120'

 L. 140       150  DUP_TOP          
              152  LOAD_GLOBAL              TypeError
              154  COMPARE_OP               exception-match
              156  POP_JUMP_IF_FALSE   178  'to 178'
              158  POP_TOP          
              160  POP_TOP          
              162  POP_TOP          

 L. 141       164  LOAD_FAST                'results'
              166  LOAD_METHOD              append
              168  LOAD_CONST               False
              170  CALL_METHOD_1         1  '1 positional argument'
              172  POP_TOP          
              174  POP_EXCEPT       
              176  JUMP_BACK            66  'to 66'
            178_0  COME_FROM           156  '156'
              178  END_FINALLY      
              180  JUMP_BACK            66  'to 66'
              182  POP_BLOCK        
            184_0  COME_FROM_LOOP       54  '54'
            184_1  COME_FROM            52  '52'
            184_2  COME_FROM            46  '46'
            184_3  COME_FROM_LOOP       14  '14'

 L. 143       184  LOAD_FAST                'self'
              186  LOAD_ATTR                connector
              188  LOAD_STR                 'AND'
              190  COMPARE_OP               ==
              192  POP_JUMP_IF_FALSE   204  'to 204'

 L. 144       194  LOAD_GLOBAL              all
              196  LOAD_FAST                'results'
              198  CALL_FUNCTION_1       1  '1 positional argument'
              200  STORE_FAST               'end_result'
              202  JUMP_FORWARD        240  'to 240'
            204_0  COME_FROM           192  '192'

 L. 146       204  LOAD_FAST                'self'
              206  LOAD_ATTR                connector
              208  LOAD_STR                 'OR'
              210  COMPARE_OP               ==
              212  POP_JUMP_IF_FALSE   224  'to 224'

 L. 147       214  LOAD_GLOBAL              any
              216  LOAD_FAST                'results'
              218  CALL_FUNCTION_1       1  '1 positional argument'
              220  STORE_FAST               'end_result'
              222  JUMP_FORWARD        240  'to 240'
            224_0  COME_FROM           212  '212'

 L. 150       224  LOAD_GLOBAL              ValueError
              226  LOAD_STR                 "unknown connector '{}'"
              228  LOAD_METHOD              format
              230  LOAD_FAST                'self'
              232  LOAD_ATTR                connector
              234  CALL_METHOD_1         1  '1 positional argument'
              236  CALL_FUNCTION_1       1  '1 positional argument'
              238  RAISE_VARARGS_1       1  'exception instance'
            240_0  COME_FROM           222  '222'
            240_1  COME_FROM           202  '202'

 L. 152       240  LOAD_FAST                'self'
              242  LOAD_ATTR                negated
              244  POP_JUMP_IF_FALSE   252  'to 252'

 L. 153       246  LOAD_FAST                'end_result'
              248  UNARY_NOT        
              250  STORE_FAST               'end_result'
            252_0  COME_FROM           244  '244'

 L. 155       252  LOAD_FAST                'end_result'
              254  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `COME_FROM_LOOP' instruction at offset 184_3


class Content:

    def __init__(self, **data):
        self.data = data

    def __repr__(self, pretty=True, recursion_stack=None):
        if pretty:
            from flamingo.core.utils.pprint import pformat
            return pformat(self)
        recursion_stack = recursion_stack or []
        repr_string = []
        recursion_stack.append(self)
        for k, v in self.data.items():
            if k in QUOTE_KEYS:
                repr_string.append('{}={}'.format(k, quote(v)))
            elif isinstance(v, (Content, ContentSet)):
                if v in recursion_stack:
                    repr_string.append('{}={}'.format(k, quote(v)))
                else:
                    repr_string.append('{}={}'.format(k, v.__repr__(pretty=pretty, recursion_stack=recursion_stack)))
            else:
                repr_string.append('{}={}'.format(k, repr(v)))

        return '<Content({})>'.format(', '.join(repr_string))

    def __getitem__(self, key):
        if key in self.data:
            return self.data[key]

    def __setitem__(self, key, item):
        return_value = self.data.__setitem__(key, item)
        return return_value

    def __contains__(self, key):
        return key in self.data

    def get(self, *args, **kwargs):
        return (self.data.get)(*args, **kwargs)


class ContentSet:

    def __init__(self, contents=None, query=None):
        self.contents = contents or []
        self._query = query

    @property
    def query(self):
        return self._query

    def add(self, *args, **kwargs):
        for arg in args:
            if isinstance(arg, Content):
                self.contents.append(arg)

        if kwargs:
            self.contents.append(Content(**kwargs))

    def _filter(self, negated, *args, **kwargs):
        if (kwargs or len(args)) == 1 and isinstance(args[0], dict):
            query = Q(**args[0])
        else:
            query = Q(*args, **kwargs)
        if negated:
            query = ~query
        content_set = self.__class__(query=(self.query & query if self.query else query))
        for content in self.contents:
            if query.check(content):
                content_set.add(content)

        return content_set

    def filter(self, *args, **kwargs):
        return (self._filter)(False, *args, **kwargs)

    def exclude(self, *args, **kwargs):
        return (self._filter)(True, *args, **kwargs)

    def get(self, *args, **kwargs):
        if args or kwargs:
            contents = (self.filter)(*args, **kwargs)
        else:
            contents = self
        if len(contents) > 1:
            raise MultipleObjectsReturned(query=(contents.query))
        if len(contents) < 1:
            raise ObjectDoesNotExist(query=(contents.query))
        return contents[0]

    def exists(self):
        if len(self.contents) > 0:
            return True
        return False

    def first(self):
        if len(self.contents) < 1:
            raise ObjectDoesNotExist(query=(self.query))
        return self.contents[0]

    def last(self):
        if len(self.contents) < 1:
            raise ObjectDoesNotExist(query=(self.query))
        return self.contents[(-1)]

    def values(self, *field_names):
        return_values = []
        for content in self:
            return_values.append(tuple())
            for field_name in field_names:
                return_values[(-1)] += (content[field_name],)

            if len(field_names) == 1:
                if return_values[(-1)][0] is None:
                    return_values.pop()
                else:
                    return_values[-1] = return_values[(-1)][0]

        if len(field_names) == 1:
            dirty_return_values = return_values
            return_values = []
            for i in dirty_return_values:
                if i not in return_values:
                    return_values.append(i)

        return return_values

    def order_by(self, field_name):
        reverse = False
        if field_name.startswith('-'):
            field_name = field_name[1:]
            reverse = True
        return self.__class__(contents=sorted((self.contents),
          key=(lambda x: (
         x[field_name] is None, x[field_name])),
          reverse=reverse))

    def count(self):
        return len(self.contents)

    def __len__(self):
        return self.contents.__len__()

    def __getitem__(self, key):
        contents = self.contents.__getitem__(key)
        if isinstance(key, slice):
            contents = self.__class__(contents=contents)
        return contents

    def __iter__(self):
        return self.contents.__iter__()

    def __repr__(self, pretty=True, recursion_stack=None):
        if pretty:
            from flamingo.core.utils.pprint import pformat
            return pformat(self)
        repr_strings = []
        recursion_stack = recursion_stack or []
        recursion_stack.append(self)
        for content in self.contents:
            repr_strings.append(content.__repr__(pretty=pretty, recursion_stack=recursion_stack))

        return '<ContentSet({})>'.format(', '.join(repr_strings))

    def __add__(self, other):
        if not isinstance(other, (ContentSet, Content)):
            raise TypeError("unsupported operand type(s) for '+'")
        if isinstance(other, Content):
            return ContentSet(contents=(self.contents + [other]))
        return ContentSet(contents=(self.contents + other.contents))

    def __iadd__(self, other):
        if not isinstance(other, (ContentSet, Content)):
            raise TypeError("unsupported operand type(s) for '+='")
        elif isinstance(other, Content):
            self.add(other)
        else:
            self.add(other.contents)
        return self

    def __sub__(self, other):
        if not isinstance(other, (ContentSet, Content)):
            raise TypeError("unsupported operand type(s) for '-'")
        else:
            content_set = ContentSet(contents=(self.contents))
            if isinstance(other, Content):
                content_set.contents.remove(other)
            else:
                for content in other.contents:
                    content_set.contents.remove(content)

        return content_set

    def __isub__(self, other):
        if not isinstance(other, (ContentSet, Content)):
            raise TypeError("unsupported operand type(s) for '-='")
        elif isinstance(other, Content):
            self.contents.remove(other)
        else:
            for content in other.contents:
                self.contents.remove(content)

        return self