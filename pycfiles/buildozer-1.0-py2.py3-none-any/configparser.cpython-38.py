# uncompyle6 version 3.6.7
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /home/fantomas/dev/buildout-versions-checker-py3/bvc/configparser.py
# Compiled at: 2020-03-06 06:01:13
# Size of source mod 2**32: 3814 bytes
__doc__ = 'Config parser for Buildout Versions Checker'
import re
from configparser import RawConfigParser
from itertools import chain
from bvc.indentation import perfect_indentation
OPERATORS = re.compile('[+-]$')

class VersionsConfigParser(RawConfigParser, object):
    """VersionsConfigParser"""
    optionxform = str

    def __init__(self, *args, **kwargs):
        self.sorting = kwargs.pop('sorting', None)
        self.indentation = kwargs.pop('indentation', -1)
        (super(VersionsConfigParser, self).__init__)(*args, **kwargs)

    def ascii_sorter(self, items):
        return sorted(items,
          key=(lambda x: x[0]))

    def alpha_sorter(self, items):
        return sorted(items,
          key=(lambda x: x[0].lower()))

    def length_sorter(self, items):
        return sorted((self.alpha_sorter(items)),
          key=(lambda x: len(x[0])))

    def write_section(self, fd, section, indentation, sorting):
        """
        Write a section of an .ini-format
        and all the keys within.
        """
        string_section = '[%s]\n' % section
        items = self._sections[section].items()
        try:
            items = getattr(self, '%s_sorter' % sorting)(items)
        except (TypeError, AttributeError):
            pass
        else:
            for key, value in items:
                if key == '__name__':
                    pass
                else:
                    if value is None:
                        value = ''
                    else:
                        operator = ''
                        buildout_operator = OPERATORS.search(key)
                        if buildout_operator:
                            operator = buildout_operator.group(0)
                            key = key[:-1]
                        if key == '<':
                            value = '{value:>{indent}}'.format(value=value,
                              indent=(indentation + len(value) - 1))
                        else:
                            key = '{key:<{indent}}{operator}'.format(key=key,
                              operator=operator,
                              indent=(max(indentation - int(bool(operator)), 0)))
                    value = value.replace('\n', '{:<{indent}}'.format('\n',
                      indent=(indentation + 3)))
                    string_section += '{key}{operator:<{indent}}{value}\n'.format(key=key,
                      operator='=',
                      value=value,
                      indent=(int(bool(indentation)) + 1))

            fd.write(string_section.encode('utf-8'))

    def write--- This code section failed: ---

 L.  99         0  LOAD_FAST                'self'
                2  LOAD_ATTR                indentation
                4  LOAD_CONST               0
                6  COMPARE_OP               <
                8  POP_JUMP_IF_FALSE    18  'to 18'

 L. 100        10  LOAD_FAST                'self'
               12  LOAD_ATTR                perfect_indentation
               14  LOAD_FAST                'self'
               16  STORE_ATTR               indentation
             18_0  COME_FROM             8  '8'

 L. 102        18  LOAD_GLOBAL              open
               20  LOAD_FAST                'source'
               22  LOAD_STR                 'wb'
               24  CALL_FUNCTION_2       2  ''
               26  SETUP_WITH          126  'to 126'
               28  STORE_FAST               'fd'

 L. 103        30  LOAD_GLOBAL              list
               32  LOAD_FAST                'self'
               34  LOAD_ATTR                _sections
               36  LOAD_METHOD              keys
               38  CALL_METHOD_0         0  ''
               40  CALL_FUNCTION_1       1  ''
               42  STORE_FAST               'sections'

 L. 104        44  LOAD_FAST                'sections'
               46  LOAD_CONST               None
               48  LOAD_CONST               -1
               50  BUILD_SLICE_2         2 
               52  BINARY_SUBSCR    
               54  GET_ITER         
               56  FOR_ITER             98  'to 98'
               58  STORE_FAST               'section'

 L. 105        60  LOAD_FAST                'self'
               62  LOAD_METHOD              write_section

 L. 106        64  LOAD_FAST                'fd'

 L. 107        66  LOAD_FAST                'section'

 L. 108        68  LOAD_FAST                'self'
               70  LOAD_ATTR                indentation

 L. 109        72  LOAD_FAST                'self'
               74  LOAD_ATTR                sorting

 L. 105        76  CALL_METHOD_4         4  ''
               78  POP_TOP          

 L. 111        80  LOAD_FAST                'fd'
               82  LOAD_METHOD              write
               84  LOAD_STR                 '\n'
               86  LOAD_METHOD              encode
               88  LOAD_STR                 'utf-8'
               90  CALL_METHOD_1         1  ''
               92  CALL_METHOD_1         1  ''
               94  POP_TOP          
               96  JUMP_BACK            56  'to 56'

 L. 113        98  LOAD_FAST                'self'
              100  LOAD_METHOD              write_section

 L. 114       102  LOAD_FAST                'fd'

 L. 115       104  LOAD_FAST                'sections'
              106  LOAD_CONST               -1
              108  BINARY_SUBSCR    

 L. 116       110  LOAD_FAST                'self'
              112  LOAD_ATTR                indentation

 L. 117       114  LOAD_FAST                'self'
              116  LOAD_ATTR                sorting

 L. 113       118  CALL_METHOD_4         4  ''
              120  POP_TOP          
              122  POP_BLOCK        
              124  BEGIN_FINALLY    
            126_0  COME_FROM_WITH       26  '26'
              126  WITH_CLEANUP_START
              128  WITH_CLEANUP_FINISH
              130  END_FINALLY      

Parse error at or near `BEGIN_FINALLY' instruction at offset 124

    @property
    def perfect_indentation(self, rounding=4):
        """
        Find the perfect indentation required for writing
        the file, by iterating over the different options.
        """
        return perfect_indentation(chain(*[self.options(section) for section in self.sections()]))