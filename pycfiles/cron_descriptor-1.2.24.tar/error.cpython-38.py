# uncompyle6 version 3.6.7
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: ./vendor/yaml/error.py
# Compiled at: 2018-06-28 19:00:20
# Size of source mod 2**32: 2533 bytes
__all__ = ['Mark', 'YAMLError', 'MarkedYAMLError']

class Mark:

    def __init__(self, name, index, line, column, buffer, pointer):
        self.name = name
        self.index = index
        self.line = line
        self.column = column
        self.buffer = buffer
        self.pointer = pointer

    def get_snippet(self, indent=4, max_length=75):
        if self.buffer is None:
            return
            head = ''
            start = self.pointer
            while start > 0:
                if self.buffer[(start - 1)] not in '\x00\r\n\x85\u2028\u2029':
                    start -= 1
                    if self.pointer - start > max_length / 2 - 1:
                        head = ' ... '
                        start += 5
                        break

            tail = ''
            end = self.pointer
        else:
            while end < len(self.buffer):
                if self.buffer[end] not in '\x00\r\n\x85\u2028\u2029':
                    end += 1
                    if end - self.pointer > max_length / 2 - 1:
                        tail = ' ... '
                        end -= 5
                        break

        snippet = self.buffer[start:end]
        return ' ' * indent + head + snippet + tail + '\n' + ' ' * (indent + self.pointer - start + len(head)) + '^'

    def __str__(self):
        snippet = self.get_snippet()
        where = '  in "%s", line %d, column %d' % (
         self.name, self.line + 1, self.column + 1)
        if snippet is not None:
            where += ':\n' + snippet
        return where


class YAMLError(Exception):
    pass


class MarkedYAMLError(YAMLError):

    def __init__(self, context=None, context_mark=None, problem=None, problem_mark=None, note=None):
        self.context = context
        self.context_mark = context_mark
        self.problem = problem
        self.problem_mark = problem_mark
        self.note = note

    def __str__--- This code section failed: ---

 L.  59         0  BUILD_LIST_0          0 
                2  STORE_FAST               'lines'

 L.  60         4  LOAD_FAST                'self'
                6  LOAD_ATTR                context
                8  LOAD_CONST               None
               10  COMPARE_OP               is-not
               12  POP_JUMP_IF_FALSE    26  'to 26'

 L.  61        14  LOAD_FAST                'lines'
               16  LOAD_METHOD              append
               18  LOAD_FAST                'self'
               20  LOAD_ATTR                context
               22  CALL_METHOD_1         1  ''
               24  POP_TOP          
             26_0  COME_FROM            12  '12'

 L.  62        26  LOAD_FAST                'self'
               28  LOAD_ATTR                context_mark
               30  LOAD_CONST               None
               32  COMPARE_OP               is-not
               34  POP_JUMP_IF_FALSE   120  'to 120'

 L.  63        36  LOAD_FAST                'self'
               38  LOAD_ATTR                problem
               40  LOAD_CONST               None
               42  COMPARE_OP               is

 L.  62        44  POP_JUMP_IF_TRUE    104  'to 104'

 L.  63        46  LOAD_FAST                'self'
               48  LOAD_ATTR                problem_mark
               50  LOAD_CONST               None
               52  COMPARE_OP               is

 L.  62        54  POP_JUMP_IF_TRUE    104  'to 104'

 L.  64        56  LOAD_FAST                'self'
               58  LOAD_ATTR                context_mark
               60  LOAD_ATTR                name
               62  LOAD_FAST                'self'
               64  LOAD_ATTR                problem_mark
               66  LOAD_ATTR                name
               68  COMPARE_OP               !=

 L.  62        70  POP_JUMP_IF_TRUE    104  'to 104'

 L.  65        72  LOAD_FAST                'self'
               74  LOAD_ATTR                context_mark
               76  LOAD_ATTR                line
               78  LOAD_FAST                'self'
               80  LOAD_ATTR                problem_mark
               82  LOAD_ATTR                line
               84  COMPARE_OP               !=

 L.  62        86  POP_JUMP_IF_TRUE    104  'to 104'

 L.  66        88  LOAD_FAST                'self'
               90  LOAD_ATTR                context_mark
               92  LOAD_ATTR                column
               94  LOAD_FAST                'self'
               96  LOAD_ATTR                problem_mark
               98  LOAD_ATTR                column
              100  COMPARE_OP               !=

 L.  62       102  POP_JUMP_IF_FALSE   120  'to 120'
            104_0  COME_FROM            86  '86'
            104_1  COME_FROM            70  '70'
            104_2  COME_FROM            54  '54'
            104_3  COME_FROM            44  '44'

 L.  67       104  LOAD_FAST                'lines'
              106  LOAD_METHOD              append
              108  LOAD_GLOBAL              str
              110  LOAD_FAST                'self'
              112  LOAD_ATTR                context_mark
              114  CALL_FUNCTION_1       1  ''
              116  CALL_METHOD_1         1  ''
              118  POP_TOP          
            120_0  COME_FROM           102  '102'
            120_1  COME_FROM            34  '34'

 L.  68       120  LOAD_FAST                'self'
              122  LOAD_ATTR                problem
              124  LOAD_CONST               None
              126  COMPARE_OP               is-not
              128  POP_JUMP_IF_FALSE   142  'to 142'

 L.  69       130  LOAD_FAST                'lines'
              132  LOAD_METHOD              append
              134  LOAD_FAST                'self'
              136  LOAD_ATTR                problem
              138  CALL_METHOD_1         1  ''
              140  POP_TOP          
            142_0  COME_FROM           128  '128'

 L.  70       142  LOAD_FAST                'self'
              144  LOAD_ATTR                problem_mark
              146  LOAD_CONST               None
              148  COMPARE_OP               is-not
              150  POP_JUMP_IF_FALSE   168  'to 168'

 L.  71       152  LOAD_FAST                'lines'
              154  LOAD_METHOD              append
              156  LOAD_GLOBAL              str
              158  LOAD_FAST                'self'
              160  LOAD_ATTR                problem_mark
              162  CALL_FUNCTION_1       1  ''
              164  CALL_METHOD_1         1  ''
              166  POP_TOP          
            168_0  COME_FROM           150  '150'

 L.  72       168  LOAD_FAST                'self'
              170  LOAD_ATTR                note
              172  LOAD_CONST               None
              174  COMPARE_OP               is-not
              176  POP_JUMP_IF_FALSE   190  'to 190'

 L.  73       178  LOAD_FAST                'lines'
              180  LOAD_METHOD              append
              182  LOAD_FAST                'self'
              184  LOAD_ATTR                note
              186  CALL_METHOD_1         1  ''
              188  POP_TOP          
            190_0  COME_FROM           176  '176'

 L.  74       190  LOAD_STR                 '\n'
              192  LOAD_METHOD              join
              194  LOAD_FAST                'lines'
              196  CALL_METHOD_1         1  ''
              198  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `RETURN_VALUE' instruction at offset 198


# NOTE: have internal decompilation grammar errors.
# Use -t option to show full context.
# not in loop:
#	break
#      L.  24        92  BREAK_LOOP           96  'to 96'
# not in loop:
#	break
#      L.  32       176  BREAK_LOOP          180  'to 180'