# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: puke/Utils.py
# Compiled at: 2011-12-05 13:53:25
import collections, os, stat, re, functools, operator

def quacks_like_dict(object):
    """Check if object is dict-like"""
    return isinstance(object, collections.Mapping)


def deepmerge--- This code section failed: ---

 L.  24         0  LOAD_GLOBAL           0  'quacks_like_dict'
                3  LOAD_FAST             0  'a'
                6  CALL_FUNCTION_1       1  None
                9  POP_JUMP_IF_TRUE     27  'to 27'
               12  LOAD_ASSERT              AssertionError
               15  LOAD_GLOBAL           0  'quacks_like_dict'
               18  LOAD_FAST             1  'b'
               21  CALL_FUNCTION_1       1  None
               24  RAISE_VARARGS_2       2  None

 L.  25        27  LOAD_FAST             0  'a'
               30  LOAD_ATTR             2  'copy'
               33  CALL_FUNCTION_0       0  None
               36  STORE_FAST            2  'dst'

 L.  27        39  LOAD_FAST             2  'dst'
               42  LOAD_FAST             1  'b'
               45  BUILD_TUPLE_2         2 
               48  BUILD_LIST_1          1 
               51  STORE_FAST            3  'stack'

 L.  28        54  SETUP_LOOP          150  'to 207'
               57  LOAD_FAST             3  'stack'
               60  POP_JUMP_IF_FALSE   206  'to 206'

 L.  29        63  LOAD_FAST             3  'stack'
               66  LOAD_ATTR             3  'pop'
               69  CALL_FUNCTION_0       0  None
               72  UNPACK_SEQUENCE_2     2 
               75  STORE_FAST            4  'current_dst'
               78  STORE_FAST            5  'current_src'

 L.  30        81  SETUP_LOOP          119  'to 203'
               84  LOAD_FAST             5  'current_src'
               87  GET_ITER         
               88  FOR_ITER            111  'to 202'
               91  STORE_FAST            6  'key'

 L.  31        94  LOAD_FAST             6  'key'
               97  LOAD_FAST             4  'current_dst'
              100  COMPARE_OP            7  not-in
              103  POP_JUMP_IF_FALSE   123  'to 123'

 L.  32       106  LOAD_FAST             5  'current_src'
              109  LOAD_FAST             6  'key'
              112  BINARY_SUBSCR    
              113  LOAD_FAST             4  'current_dst'
              116  LOAD_FAST             6  'key'
              119  STORE_SUBSCR     
              120  JUMP_BACK            88  'to 88'

 L.  34       123  LOAD_GLOBAL           0  'quacks_like_dict'
              126  LOAD_FAST             5  'current_src'
              129  LOAD_FAST             6  'key'
              132  BINARY_SUBSCR    
              133  CALL_FUNCTION_1       1  None
              136  POP_JUMP_IF_FALSE   185  'to 185'
              139  LOAD_GLOBAL           0  'quacks_like_dict'
              142  LOAD_FAST             4  'current_dst'
              145  LOAD_FAST             6  'key'
              148  BINARY_SUBSCR    
              149  CALL_FUNCTION_1       1  None
            152_0  COME_FROM           136  '136'
              152  POP_JUMP_IF_FALSE   185  'to 185'

 L.  35       155  LOAD_FAST             3  'stack'
              158  LOAD_ATTR             4  'append'
              161  LOAD_FAST             4  'current_dst'
              164  LOAD_FAST             6  'key'
              167  BINARY_SUBSCR    
              168  LOAD_FAST             5  'current_src'
              171  LOAD_FAST             6  'key'
              174  BINARY_SUBSCR    
              175  BUILD_TUPLE_2         2 
              178  CALL_FUNCTION_1       1  None
              181  POP_TOP          
              182  JUMP_BACK            88  'to 88'

 L.  37       185  LOAD_FAST             5  'current_src'
              188  LOAD_FAST             6  'key'
              191  BINARY_SUBSCR    
              192  LOAD_FAST             4  'current_dst'
              195  LOAD_FAST             6  'key'
              198  STORE_SUBSCR     
              199  JUMP_BACK            88  'to 88'
              202  POP_BLOCK        
            203_0  COME_FROM            81  '81'
              203  JUMP_BACK            57  'to 57'
              206  POP_BLOCK        
            207_0  COME_FROM            54  '54'

 L.  38       207  LOAD_FAST             2  'dst'
              210  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `RETURN_VALUE' instruction at offset 210


_rechmod = re.compile('(?P<who>[uoga]?)(?P<op>[+\\-=])(?P<value>[ugo]|[rwx]*)')
_stat_prefix = dict(u='USR', g='GRP', o='OTH')

def octalmode(location, symbolic):
    """chmod(location, description) --> None
    Change the access permissions of file, using a symbolic description
    of the mode, similar to the format of the shell command chmod.
    The format of description is
        * an optional letter in o, g, u, a (no letter means a)
        * an operator in +, -, =
        * a sequence of letters in r, w, x, or a single letter in o, g, u
    Example:
        chmod(myfile, "u+x")    # make the file executable for it's owner.
        chmod(myfile, "o-rwx")  # remove all permissions for all users not in the group. 
    See also the man page of chmod.
    """
    mo = _rechmod.match(symbolic)
    who, op, value = mo.group('who'), mo.group('op'), mo.group('value')
    if not who:
        who = 'a'
    mode = os.stat(location)[stat.ST_MODE]
    if value in ('o', 'g', 'u'):
        mask = _ors(_stat_bit(who, z) for z in 'rwx' if mode & _stat_bit(value, z))
    else:
        mask = _ors(_stat_bit(who, z) for z in value)
    if op == '=':
        mode &= ~_ors(_stat_bit(who, z) for z in 'rwx')
    mode = mode & ~mask if op == '-' else mode | mask
    return mode


def _stat_bit(who, letter):
    if who == 'a':
        return _stat_bit('o', letter) | _stat_bit('g', letter) | _stat_bit('u', letter)
    return getattr(stat, 'S_I%s%s' % (letter.upper(), _stat_prefix[who]))


def _ors(sequence, initial=0):
    return functools.reduce(operator.__or__, sequence, initial)