# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\User\AppData\Local\Temp\pip-install-oj_abz_z\hypothesis\hypothesis\internal\charmap.py
# Compiled at: 2020-01-12 08:06:33
# Size of source mod 2**32: 13293 bytes
import gzip, json, os, sys, tempfile, unicodedata
from typing import Dict, Tuple
from hypothesis.configuration import mkdir_p, storage_directory
from hypothesis.errors import InvalidArgument
intervals = Tuple[(Tuple[(int, int)], ...)]
cache_type = Dict[(Tuple[(Tuple[(str, ...)], int, int, intervals)], intervals)]

def charmap_file():
    return storage_directory('unicode_data', unicodedata.unidata_version, 'charmap.json.gz')


_charmap = None

def charmap():
    """Return a dict that maps a Unicode category, to a tuple of 2-tuples
    covering the codepoint intervals for characters in that category.

    >>> charmap()['Co']
    ((57344, 63743), (983040, 1048573), (1048576, 1114109))
    """
    global _charmap
    if _charmap is None:
        f = charmap_file()
        try:
            with gzip.GzipFile(f, 'rb') as (i):
                data = i.read().decode()
                tmp_charmap = dict(json.loads(data))
        except Exception:
            category = unicodedata.category
            tmp_charmap = {}
            last_cat = category(chr(0))
            last_start = 0
            for i in range(1, sys.maxunicode + 1):
                cat = category(chr(i))
                if cat != last_cat:
                    tmp_charmap.setdefault(last_cat, []).append([last_start, i - 1])
                    last_cat, last_start = cat, i
                tmp_charmap.setdefault(last_cat, []).append([last_start, sys.maxunicode])
                try:
                    tmpdir = storage_directory('tmp')
                    mkdir_p(tmpdir)
                    fd, tmpfile = tempfile.mkstemp(dir=tmpdir)
                    os.close(fd)
                    with gzip.GzipFile(tmpfile, 'wb', mtime=1) as (o):
                        result = json.dumps(sorted(tmp_charmap.items()))
                        o.write(result.encode())
                    os.renames(tmpfile, f)
                except Exception:
                    pass

        else:
            _charmap = {tuple((tuple(pair) for pair in pairs)):k for k, pairs in tmp_charmap.items()}
            for vs in _charmap.values():
                ints = list(sum(vs, ()))
                assert all((isinstance(x, int) for x in ints))
                assert ints == sorted(ints)
                assert all((len(tup) == 2 for tup in vs))

    assert _charmap is not None
    return _charmap


_categories = None

def categories():
    """Return a tuple of Unicode categories in a normalised order.

    >>> categories() # doctest: +ELLIPSIS
    ('Zl', 'Zp', 'Co', 'Me', 'Pc', ..., 'Cc', 'Cs')
    """
    global _categories
    if _categories is None:
        cm = charmap()
        _categories = sorted((cm.keys()), key=(lambda c: len(cm[c])))
        _categories.remove('Cc')
        _categories.remove('Cs')
        _categories.append('Cc')
        _categories.append('Cs')
    return tuple(_categories)


def as_general_categories(cats, name='cats'):
    """Return a tuple of Unicode categories in a normalised order.

    This function expands one-letter designations of a major class to include
    all subclasses:

    >>> as_general_categories(['N'])
    ('Nd', 'Nl', 'No')

    See section 4.5 of the Unicode standard for more on classes:
    https://www.unicode.org/versions/Unicode10.0.0/ch04.pdf

    If the collection ``cats`` includes any elements that do not represent a
    major class or a class with subclass, a deprecation warning is raised.
    """
    if cats is None:
        return
    major_classes = ('L', 'M', 'N', 'P', 'S', 'Z', 'C')
    cs = categories()
    out = set(cats)
    for c in cats:
        if c in major_classes:
            out.discard(c)
            out.update((x for x in cs if x.startswith(c)))
        else:
            if c not in cs:
                raise InvalidArgument('In %s=%r, %r is not a valid Unicode category.' % (name, cats, c))
            return tuple((c for c in cs if c in out))


def _union_intervals(x, y):
    """Merge two sequences of intervals into a single tuple of intervals.

    Any integer bounded by `x` or `y` is also bounded by the result.

    >>> _union_intervals([(3, 10)], [(1, 2), (5, 17)])
    ((1, 17),)
    """
    if not x:
        return tuple(((u, v) for u, v in y))
    else:
        if not y:
            return tuple(((u, v) for u, v in x))
        intervals = sorted((x + y), reverse=True)
        result = [intervals.pop()]
        while intervals:
            u, v = intervals.pop()
            a, b = result[(-1)]
            if u <= b + 1:
                result[-1] = (a, max(v, b))
            else:
                result.append((u, v))

    return tuple(result)


def _subtract_intervals(x, y):
    """Set difference for lists of intervals. That is, returns a list of
    intervals that bounds all values bounded by x that are not also bounded by
    y. x and y are expected to be in sorted order.

    For example _subtract_intervals([(1, 10)], [(2, 3), (9, 15)]) would
    return [(1, 1), (4, 8)], removing the values 2, 3, 9 and 10 from the
    interval.
    """
    if not y:
        return tuple(x)
    else:
        x = list(map(list, x))
        i = 0
        j = 0
        result = []
        while i < len(x):
            if j < len(y):
                xl, xr = x[i]
                assert xl <= xr
                yl, yr = y[j]
                assert yl <= yr
                if yr < xl:
                    j += 1
                elif yl > xr:
                    result.append(x[i])
                    i += 1
                elif yl <= xl:
                    if yr >= xr:
                        i += 1
                    else:
                        x[i][0] = yr + 1
                        j += 1
                else:
                    result.append((xl, yl - 1))
                    if yr + 1 <= xr:
                        x[i][0] = yr + 1
                        j += 1
                    else:
                        i += 1

    result.extend(x[i:])
    return tuple(map(tuple, result))


def _intervals(s):
    """Return a tuple of intervals, covering the codepoints of characters in
    `s`.

    >>> _intervals('abcdef0123456789')
    ((48, 57), (97, 102))
    """
    intervals = tuple(((ord(c), ord(c)) for c in sorted(s)))
    return _union_intervals(intervals, intervals)


category_index_cache = {(): ()}

def _category_key(exclude, include):
    """Return a normalised tuple of all Unicode categories that are in
    `include`, but not in `exclude`.

    If include is None then default to including all categories.
    Any item in include that is not a unicode character will be excluded.

    >>> _category_key(exclude=['So'], include=['Lu', 'Me', 'Cs', 'So'])
    ('Me', 'Lu', 'Cs')
    """
    cs = categories()
    if include is None:
        include = set(cs)
    else:
        include = set(include)
    exclude = set(exclude or ())
    assert include.issubset(cs)
    assert exclude.issubset(cs)
    include -= exclude
    result = tuple((c for c in cs if c in include))
    return result


def _query_for_key--- This code section failed: ---

 L. 312         0  SETUP_FINALLY        12  'to 12'

 L. 313         2  LOAD_GLOBAL              category_index_cache
                4  LOAD_FAST                'key'
                6  BINARY_SUBSCR    
                8  POP_BLOCK        
               10  RETURN_VALUE     
             12_0  COME_FROM_FINALLY     0  '0'

 L. 314        12  DUP_TOP          
               14  LOAD_GLOBAL              KeyError
               16  COMPARE_OP               exception-match
               18  POP_JUMP_IF_FALSE    30  'to 30'
               20  POP_TOP          
               22  POP_TOP          
               24  POP_TOP          

 L. 315        26  POP_EXCEPT       
               28  JUMP_FORWARD         32  'to 32'
             30_0  COME_FROM            18  '18'
               30  END_FINALLY      
             32_0  COME_FROM            28  '28'

 L. 316        32  LOAD_FAST                'key'
               34  POP_JUMP_IF_TRUE     40  'to 40'
               36  LOAD_ASSERT              AssertionError
               38  RAISE_VARARGS_1       1  'exception instance'
             40_0  COME_FROM            34  '34'

 L. 317        40  LOAD_GLOBAL              set
               42  LOAD_FAST                'key'
               44  CALL_FUNCTION_1       1  ''
               46  LOAD_GLOBAL              set
               48  LOAD_GLOBAL              categories
               50  CALL_FUNCTION_0       0  ''
               52  CALL_FUNCTION_1       1  ''
               54  COMPARE_OP               ==
               56  POP_JUMP_IF_FALSE    72  'to 72'

 L. 318        58  LOAD_CONST               0
               60  LOAD_GLOBAL              sys
               62  LOAD_ATTR                maxunicode
               64  BUILD_TUPLE_2         2 
               66  BUILD_TUPLE_1         1 
               68  STORE_FAST               'result'
               70  JUMP_FORWARD        104  'to 104'
             72_0  COME_FROM            56  '56'

 L. 320        72  LOAD_GLOBAL              _union_intervals
               74  LOAD_GLOBAL              _query_for_key
               76  LOAD_FAST                'key'
               78  LOAD_CONST               None
               80  LOAD_CONST               -1
               82  BUILD_SLICE_2         2 
               84  BINARY_SUBSCR    
               86  CALL_FUNCTION_1       1  ''
               88  LOAD_GLOBAL              charmap
               90  CALL_FUNCTION_0       0  ''
               92  LOAD_FAST                'key'
               94  LOAD_CONST               -1
               96  BINARY_SUBSCR    
               98  BINARY_SUBSCR    
              100  CALL_FUNCTION_2       2  ''
              102  STORE_FAST               'result'
            104_0  COME_FROM            70  '70'

 L. 321       104  LOAD_FAST                'result'
              106  LOAD_GLOBAL              category_index_cache
              108  LOAD_FAST                'key'
              110  STORE_SUBSCR     

 L. 322       112  LOAD_FAST                'result'
              114  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `POP_TOP' instruction at offset 22


limited_category_index_cache = {}

def query--- This code section failed: ---

 L. 351         0  LOAD_FAST                'min_codepoint'
                2  LOAD_CONST               None
                4  COMPARE_OP               is
                6  POP_JUMP_IF_FALSE    12  'to 12'

 L. 352         8  LOAD_CONST               0
               10  STORE_FAST               'min_codepoint'
             12_0  COME_FROM             6  '6'

 L. 353        12  LOAD_FAST                'max_codepoint'
               14  LOAD_CONST               None
               16  COMPARE_OP               is
               18  POP_JUMP_IF_FALSE    26  'to 26'

 L. 354        20  LOAD_GLOBAL              sys
               22  LOAD_ATTR                maxunicode
               24  STORE_FAST               'max_codepoint'
             26_0  COME_FROM            18  '18'

 L. 355        26  LOAD_GLOBAL              _category_key
               28  LOAD_FAST                'exclude_categories'
               30  LOAD_FAST                'include_categories'
               32  CALL_FUNCTION_2       2  ''
               34  STORE_FAST               'catkey'

 L. 356        36  LOAD_GLOBAL              _intervals
               38  LOAD_FAST                'include_characters'
               40  JUMP_IF_TRUE_OR_POP    44  'to 44'
               42  LOAD_STR                 ''
             44_0  COME_FROM            40  '40'
               44  CALL_FUNCTION_1       1  ''
               46  STORE_FAST               'character_intervals'

 L. 357        48  LOAD_GLOBAL              _intervals
               50  LOAD_FAST                'exclude_characters'
               52  JUMP_IF_TRUE_OR_POP    56  'to 56'
               54  LOAD_STR                 ''
             56_0  COME_FROM            52  '52'
               56  CALL_FUNCTION_1       1  ''
               58  STORE_FAST               'exclude_intervals'

 L. 359        60  LOAD_FAST                'catkey'

 L. 360        62  LOAD_FAST                'min_codepoint'

 L. 361        64  LOAD_FAST                'max_codepoint'

 L. 362        66  LOAD_FAST                'character_intervals'

 L. 363        68  LOAD_FAST                'exclude_intervals'

 L. 358        70  BUILD_TUPLE_5         5 
               72  STORE_FAST               'qkey'

 L. 365        74  SETUP_FINALLY        86  'to 86'

 L. 366        76  LOAD_GLOBAL              limited_category_index_cache
               78  LOAD_FAST                'qkey'
               80  BINARY_SUBSCR    
               82  POP_BLOCK        
               84  RETURN_VALUE     
             86_0  COME_FROM_FINALLY    74  '74'

 L. 367        86  DUP_TOP          
               88  LOAD_GLOBAL              KeyError
               90  COMPARE_OP               exception-match
               92  POP_JUMP_IF_FALSE   104  'to 104'
               94  POP_TOP          
               96  POP_TOP          
               98  POP_TOP          

 L. 368       100  POP_EXCEPT       
              102  JUMP_FORWARD        106  'to 106'
            104_0  COME_FROM            92  '92'
              104  END_FINALLY      
            106_0  COME_FROM           102  '102'

 L. 369       106  LOAD_GLOBAL              _query_for_key
              108  LOAD_FAST                'catkey'
              110  CALL_FUNCTION_1       1  ''
              112  STORE_FAST               'base'

 L. 370       114  BUILD_LIST_0          0 
              116  STORE_FAST               'result'

 L. 371       118  LOAD_FAST                'base'
              120  GET_ITER         
            122_0  COME_FROM           144  '144'
            122_1  COME_FROM           136  '136'
              122  FOR_ITER            174  'to 174'
              124  UNPACK_SEQUENCE_2     2 
              126  STORE_FAST               'u'
              128  STORE_FAST               'v'

 L. 372       130  LOAD_FAST                'v'
              132  LOAD_FAST                'min_codepoint'
              134  COMPARE_OP               >=
              136  POP_JUMP_IF_FALSE   122  'to 122'
              138  LOAD_FAST                'u'
              140  LOAD_FAST                'max_codepoint'
              142  COMPARE_OP               <=
              144  POP_JUMP_IF_FALSE   122  'to 122'

 L. 373       146  LOAD_FAST                'result'
              148  LOAD_METHOD              append
              150  LOAD_GLOBAL              max
              152  LOAD_FAST                'u'
              154  LOAD_FAST                'min_codepoint'
              156  CALL_FUNCTION_2       2  ''
              158  LOAD_GLOBAL              min
              160  LOAD_FAST                'v'
              162  LOAD_FAST                'max_codepoint'
              164  CALL_FUNCTION_2       2  ''
              166  BUILD_TUPLE_2         2 
              168  CALL_METHOD_1         1  ''
              170  POP_TOP          
              172  JUMP_BACK           122  'to 122'

 L. 374       174  LOAD_GLOBAL              tuple
              176  LOAD_FAST                'result'
              178  CALL_FUNCTION_1       1  ''
              180  STORE_FAST               'result'

 L. 375       182  LOAD_GLOBAL              _union_intervals
              184  LOAD_FAST                'result'
              186  LOAD_FAST                'character_intervals'
              188  CALL_FUNCTION_2       2  ''
              190  STORE_FAST               'result'

 L. 376       192  LOAD_GLOBAL              _subtract_intervals
              194  LOAD_FAST                'result'
              196  LOAD_FAST                'exclude_intervals'
              198  CALL_FUNCTION_2       2  ''
              200  STORE_FAST               'result'

 L. 377       202  LOAD_FAST                'result'
              204  LOAD_GLOBAL              limited_category_index_cache
              206  LOAD_FAST                'qkey'
              208  STORE_SUBSCR     

 L. 378       210  LOAD_FAST                'result'
              212  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `POP_TOP' instruction at offset 96