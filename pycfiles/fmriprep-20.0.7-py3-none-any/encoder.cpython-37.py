# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-vxs8l7gu/pip/pip/_vendor/toml/encoder.py
# Compiled at: 2020-05-05 12:41:36
# Size of source mod 2**32: 8128 bytes
import datetime, re, sys
from pip._vendor.toml.decoder import InlineTableDict
if sys.version_info >= (3, ):
    unicode = str

def dump(o, f):
    """Writes out dict as toml to a file

    Args:
        o: Object to dump into toml
        f: File descriptor where the toml should be stored

    Returns:
        String containing the toml corresponding to dictionary

    Raises:
        TypeError: When anything other than file descriptor is passed
    """
    if not f.write:
        raise TypeError('You can only dump an object to a file descriptor')
    d = dumps(o)
    f.write(d)
    return d


def dumps(o, encoder=None):
    """Stringifies input dict as toml

    Args:
        o: Object to dump into toml

        preserve: Boolean parameter. If true, preserve inline tables.

    Returns:
        String containing the toml corresponding to dict
    """
    retval = ''
    if encoder is None:
        encoder = TomlEncoder(o.__class__)
    addtoretval, sections = encoder.dump_sections(o, '')
    retval += addtoretval
    while sections:
        newsections = encoder.get_empty_table()
        for section in sections:
            addtoretval, addtosections = encoder.dump_sections(sections[section], section)
            if not addtoretval:
                if not addtoretval:
                    if not addtosections:
                        if retval:
                            if retval[-2:] != '\n\n':
                                retval += '\n'
                        retval += '[' + section + ']\n'
                        if addtoretval:
                            retval += addtoretval
                for s in addtosections:
                    newsections[section + '.' + s] = addtosections[s]

        sections = newsections

    return retval


def _dump_str(v):
    if sys.version_info < (3, ):
        if hasattr(v, 'decode'):
            if isinstance(v, str):
                v = v.decode('utf-8')
    v = '%r' % v
    if v[0] == 'u':
        v = v[1:]
    singlequote = v.startswith("'")
    if singlequote or v.startswith('"'):
        v = v[1:-1]
    if singlequote:
        v = v.replace("\\'", "'")
        v = v.replace('"', '\\"')
    v = v.split('\\x')
    while len(v) > 1:
        i = -1
        if not v[0]:
            v = v[1:]
        else:
            v[0] = v[0].replace('\\\\', '\\')
            joinx = v[0][i] != '\\'
            while v[0][:i] and v[0][i] == '\\':
                joinx = not joinx
                i -= 1

            if joinx:
                joiner = 'x'
            else:
                joiner = 'u00'
        v = [
         v[0] + joiner + v[1]] + v[2:]

    return unicode('"' + v[0] + '"')


def _dump_float(v):
    return '{0:.16}'.format(v).replace('e+0', 'e+').replace('e-0', 'e-')


def _dump_time(v):
    utcoffset = v.utcoffset()
    if utcoffset is None:
        return v.isoformat()
    return v.isoformat()[:-6]


class TomlEncoder(object):

    def __init__(self, _dict=dict, preserve=False):
        self._dict = _dict
        self.preserve = preserve
        self.dump_funcs = {str: _dump_str, 
         unicode: _dump_str, 
         list: self.dump_list, 
         bool: lambda v: unicode(v).lower(), 
         int: lambda v: v, 
         float: _dump_float, 
         datetime.datetime: lambda v: v.isoformat().replace('+00:00', 'Z'), 
         datetime.time: _dump_time, 
         datetime.date: lambda v: v.isoformat()}

    def get_empty_table(self):
        return self._dict()

    def dump_list(self, v):
        retval = '['
        for u in v:
            retval += ' ' + unicode(self.dump_value(u)) + ','

        retval += ']'
        return retval

    def dump_inline_table(self, section):
        """Preserve inline table in its compact syntax instead of expanding
        into subsection.

        https://github.com/toml-lang/toml#user-content-inline-table
        """
        retval = ''
        if isinstance(section, dict):
            val_list = []
            for k, v in section.items():
                val = self.dump_inline_table(v)
                val_list.append(k + ' = ' + val)

            retval += '{ ' + ', '.join(val_list) + ' }\n'
            return retval
        return unicode(self.dump_value(section))

    def dump_value(self, v):
        dump_fn = self.dump_funcs.get(type(v))
        if dump_fn is None:
            if hasattr(v, '__iter__'):
                dump_fn = self.dump_funcs[list]
        if dump_fn is not None:
            return dump_fn(v)
        return self.dump_funcs[str](v)

    def dump_sections--- This code section failed: ---

 L. 163         0  LOAD_STR                 ''
                2  STORE_FAST               'retstr'

 L. 164         4  LOAD_FAST                'sup'
                6  LOAD_STR                 ''
                8  COMPARE_OP               !=
               10  POP_JUMP_IF_FALSE    32  'to 32'
               12  LOAD_FAST                'sup'
               14  LOAD_CONST               -1
               16  BINARY_SUBSCR    
               18  LOAD_STR                 '.'
               20  COMPARE_OP               !=
               22  POP_JUMP_IF_FALSE    32  'to 32'

 L. 165        24  LOAD_FAST                'sup'
               26  LOAD_STR                 '.'
               28  INPLACE_ADD      
               30  STORE_FAST               'sup'
             32_0  COME_FROM            22  '22'
             32_1  COME_FROM            10  '10'

 L. 166        32  LOAD_FAST                'self'
               34  LOAD_METHOD              _dict
               36  CALL_METHOD_0         0  '0 positional arguments'
               38  STORE_FAST               'retdict'

 L. 167        40  LOAD_STR                 ''
               42  STORE_FAST               'arraystr'

 L. 168     44_46  SETUP_LOOP          570  'to 570'
               48  LOAD_FAST                'o'
               50  GET_ITER         
            52_54  FOR_ITER            568  'to 568'
               56  STORE_FAST               'section'

 L. 169        58  LOAD_GLOBAL              unicode
               60  LOAD_FAST                'section'
               62  CALL_FUNCTION_1       1  '1 positional argument'
               64  STORE_FAST               'section'

 L. 170        66  LOAD_FAST                'section'
               68  STORE_FAST               'qsection'

 L. 171        70  LOAD_GLOBAL              re
               72  LOAD_METHOD              match
               74  LOAD_STR                 '^[A-Za-z0-9_-]+$'
               76  LOAD_FAST                'section'
               78  CALL_METHOD_2         2  '2 positional arguments'
               80  POP_JUMP_IF_TRUE    116  'to 116'

 L. 172        82  LOAD_STR                 '"'
               84  LOAD_FAST                'section'
               86  COMPARE_OP               in
               88  POP_JUMP_IF_FALSE   104  'to 104'

 L. 173        90  LOAD_STR                 "'"
               92  LOAD_FAST                'section'
               94  BINARY_ADD       
               96  LOAD_STR                 "'"
               98  BINARY_ADD       
              100  STORE_FAST               'qsection'
              102  JUMP_FORWARD        116  'to 116'
            104_0  COME_FROM            88  '88'

 L. 175       104  LOAD_STR                 '"'
              106  LOAD_FAST                'section'
              108  BINARY_ADD       
              110  LOAD_STR                 '"'
              112  BINARY_ADD       
              114  STORE_FAST               'qsection'
            116_0  COME_FROM           102  '102'
            116_1  COME_FROM            80  '80'

 L. 176       116  LOAD_GLOBAL              isinstance
              118  LOAD_FAST                'o'
              120  LOAD_FAST                'section'
              122  BINARY_SUBSCR    
              124  LOAD_GLOBAL              dict
              126  CALL_FUNCTION_2       2  '2 positional arguments'
          128_130  POP_JUMP_IF_TRUE    502  'to 502'

 L. 177       132  LOAD_CONST               False
              134  STORE_FAST               'arrayoftables'

 L. 178       136  LOAD_GLOBAL              isinstance
              138  LOAD_FAST                'o'
              140  LOAD_FAST                'section'
              142  BINARY_SUBSCR    
              144  LOAD_GLOBAL              list
              146  CALL_FUNCTION_2       2  '2 positional arguments'
              148  POP_JUMP_IF_FALSE   182  'to 182'

 L. 179       150  SETUP_LOOP          182  'to 182'
              152  LOAD_FAST                'o'
              154  LOAD_FAST                'section'
              156  BINARY_SUBSCR    
              158  GET_ITER         
            160_0  COME_FROM           172  '172'
              160  FOR_ITER            180  'to 180'
              162  STORE_FAST               'a'

 L. 180       164  LOAD_GLOBAL              isinstance
              166  LOAD_FAST                'a'
              168  LOAD_GLOBAL              dict
              170  CALL_FUNCTION_2       2  '2 positional arguments'
              172  POP_JUMP_IF_FALSE   160  'to 160'

 L. 181       174  LOAD_CONST               True
              176  STORE_FAST               'arrayoftables'
              178  JUMP_BACK           160  'to 160'
              180  POP_BLOCK        
            182_0  COME_FROM_LOOP      150  '150'
            182_1  COME_FROM           148  '148'

 L. 182       182  LOAD_FAST                'arrayoftables'
          184_186  POP_JUMP_IF_FALSE   452  'to 452'

 L. 183   188_190  SETUP_LOOP          500  'to 500'
              192  LOAD_FAST                'o'
              194  LOAD_FAST                'section'
              196  BINARY_SUBSCR    
              198  GET_ITER         
              200  FOR_ITER            448  'to 448'
              202  STORE_FAST               'a'

 L. 184       204  LOAD_STR                 '\n'
              206  STORE_FAST               'arraytabstr'

 L. 185       208  LOAD_FAST                'arraystr'
              210  LOAD_STR                 '[['
              212  LOAD_FAST                'sup'
              214  BINARY_ADD       
              216  LOAD_FAST                'qsection'
              218  BINARY_ADD       
              220  LOAD_STR                 ']]\n'
              222  BINARY_ADD       
              224  INPLACE_ADD      
              226  STORE_FAST               'arraystr'

 L. 186       228  LOAD_FAST                'self'
              230  LOAD_METHOD              dump_sections
              232  LOAD_FAST                'a'
              234  LOAD_FAST                'sup'
              236  LOAD_FAST                'qsection'
              238  BINARY_ADD       
              240  CALL_METHOD_2         2  '2 positional arguments'
              242  UNPACK_SEQUENCE_2     2 
              244  STORE_FAST               's'
              246  STORE_FAST               'd'

 L. 187       248  LOAD_FAST                's'
          250_252  POP_JUMP_IF_FALSE   286  'to 286'

 L. 188       254  LOAD_FAST                's'
              256  LOAD_CONST               0
              258  BINARY_SUBSCR    
              260  LOAD_STR                 '['
              262  COMPARE_OP               ==
          264_266  POP_JUMP_IF_FALSE   278  'to 278'

 L. 189       268  LOAD_FAST                'arraytabstr'
              270  LOAD_FAST                's'
              272  INPLACE_ADD      
              274  STORE_FAST               'arraytabstr'
              276  JUMP_FORWARD        286  'to 286'
            278_0  COME_FROM           264  '264'

 L. 191       278  LOAD_FAST                'arraystr'
              280  LOAD_FAST                's'
              282  INPLACE_ADD      
              284  STORE_FAST               'arraystr'
            286_0  COME_FROM           276  '276'
            286_1  COME_FROM           250  '250'

 L. 192       286  SETUP_LOOP          438  'to 438'
              288  LOAD_FAST                'd'
          290_292  POP_JUMP_IF_FALSE   436  'to 436'

 L. 193       294  LOAD_FAST                'self'
              296  LOAD_METHOD              _dict
              298  CALL_METHOD_0         0  '0 positional arguments'
              300  STORE_FAST               'newd'

 L. 194       302  SETUP_LOOP          428  'to 428'
              304  LOAD_FAST                'd'
              306  GET_ITER         
              308  FOR_ITER            426  'to 426'
              310  STORE_FAST               'dsec'

 L. 195       312  LOAD_FAST                'self'
              314  LOAD_METHOD              dump_sections
              316  LOAD_FAST                'd'
              318  LOAD_FAST                'dsec'
              320  BINARY_SUBSCR    

 L. 196       322  LOAD_FAST                'sup'
              324  LOAD_FAST                'qsection'
              326  BINARY_ADD       
              328  LOAD_STR                 '.'
              330  BINARY_ADD       

 L. 197       332  LOAD_FAST                'dsec'
              334  BINARY_ADD       
              336  CALL_METHOD_2         2  '2 positional arguments'
              338  UNPACK_SEQUENCE_2     2 
              340  STORE_FAST               's1'
              342  STORE_FAST               'd1'

 L. 198       344  LOAD_FAST                's1'
          346_348  POP_JUMP_IF_FALSE   386  'to 386'

 L. 199       350  LOAD_FAST                'arraytabstr'

 L. 200       352  LOAD_STR                 '['
              354  LOAD_FAST                'sup'
              356  BINARY_ADD       
              358  LOAD_FAST                'qsection'
              360  BINARY_ADD       
              362  LOAD_STR                 '.'
              364  BINARY_ADD       
              366  LOAD_FAST                'dsec'
              368  BINARY_ADD       
              370  LOAD_STR                 ']\n'
              372  BINARY_ADD       
              374  INPLACE_ADD      
              376  STORE_FAST               'arraytabstr'

 L. 201       378  LOAD_FAST                'arraytabstr'
              380  LOAD_FAST                's1'
              382  INPLACE_ADD      
              384  STORE_FAST               'arraytabstr'
            386_0  COME_FROM           346  '346'

 L. 202       386  SETUP_LOOP          422  'to 422'
              388  LOAD_FAST                'd1'
              390  GET_ITER         
              392  FOR_ITER            420  'to 420'
              394  STORE_FAST               's1'

 L. 203       396  LOAD_FAST                'd1'
              398  LOAD_FAST                's1'
              400  BINARY_SUBSCR    
              402  LOAD_FAST                'newd'
              404  LOAD_FAST                'dsec'
              406  LOAD_STR                 '.'
              408  BINARY_ADD       
              410  LOAD_FAST                's1'
              412  BINARY_ADD       
              414  STORE_SUBSCR     
          416_418  JUMP_BACK           392  'to 392'
              420  POP_BLOCK        
            422_0  COME_FROM_LOOP      386  '386'
          422_424  JUMP_BACK           308  'to 308'
              426  POP_BLOCK        
            428_0  COME_FROM_LOOP      302  '302'

 L. 204       428  LOAD_FAST                'newd'
              430  STORE_FAST               'd'
          432_434  JUMP_BACK           288  'to 288'
            436_0  COME_FROM           290  '290'
              436  POP_BLOCK        
            438_0  COME_FROM_LOOP      286  '286'

 L. 205       438  LOAD_FAST                'arraystr'
              440  LOAD_FAST                'arraytabstr'
              442  INPLACE_ADD      
              444  STORE_FAST               'arraystr'
              446  JUMP_BACK           200  'to 200'
              448  POP_BLOCK        
              450  JUMP_FORWARD        500  'to 500'
            452_0  COME_FROM           184  '184'

 L. 207       452  LOAD_FAST                'o'
              454  LOAD_FAST                'section'
              456  BINARY_SUBSCR    
              458  LOAD_CONST               None
              460  COMPARE_OP               is-not
          462_464  POP_JUMP_IF_FALSE   566  'to 566'

 L. 208       466  LOAD_FAST                'retstr'

 L. 209       468  LOAD_FAST                'qsection'
              470  LOAD_STR                 ' = '
              472  BINARY_ADD       
              474  LOAD_GLOBAL              unicode
              476  LOAD_FAST                'self'
              478  LOAD_METHOD              dump_value
              480  LOAD_FAST                'o'
              482  LOAD_FAST                'section'
              484  BINARY_SUBSCR    
              486  CALL_METHOD_1         1  '1 positional argument'
              488  CALL_FUNCTION_1       1  '1 positional argument'
              490  BINARY_ADD       
              492  LOAD_STR                 '\n'
              494  BINARY_ADD       
              496  INPLACE_ADD      
              498  STORE_FAST               'retstr'
            500_0  COME_FROM           450  '450'
            500_1  COME_FROM_LOOP      188  '188'
              500  JUMP_BACK            52  'to 52'
            502_0  COME_FROM           128  '128'

 L. 210       502  LOAD_FAST                'self'
              504  LOAD_ATTR                preserve
          506_508  POP_JUMP_IF_FALSE   554  'to 554'
              510  LOAD_GLOBAL              isinstance
              512  LOAD_FAST                'o'
              514  LOAD_FAST                'section'
              516  BINARY_SUBSCR    
              518  LOAD_GLOBAL              InlineTableDict
              520  CALL_FUNCTION_2       2  '2 positional arguments'
          522_524  POP_JUMP_IF_FALSE   554  'to 554'

 L. 211       526  LOAD_FAST                'retstr'
              528  LOAD_FAST                'qsection'
              530  LOAD_STR                 ' = '
              532  BINARY_ADD       

 L. 212       534  LOAD_FAST                'self'
              536  LOAD_METHOD              dump_inline_table
              538  LOAD_FAST                'o'
              540  LOAD_FAST                'section'
              542  BINARY_SUBSCR    
              544  CALL_METHOD_1         1  '1 positional argument'
              546  BINARY_ADD       
              548  INPLACE_ADD      
              550  STORE_FAST               'retstr'
              552  JUMP_BACK            52  'to 52'
            554_0  COME_FROM           522  '522'
            554_1  COME_FROM           506  '506'

 L. 214       554  LOAD_FAST                'o'
              556  LOAD_FAST                'section'
              558  BINARY_SUBSCR    
              560  LOAD_FAST                'retdict'
              562  LOAD_FAST                'qsection'
              564  STORE_SUBSCR     
            566_0  COME_FROM           462  '462'
              566  JUMP_BACK            52  'to 52'
              568  POP_BLOCK        
            570_0  COME_FROM_LOOP       44  '44'

 L. 215       570  LOAD_FAST                'retstr'
              572  LOAD_FAST                'arraystr'
              574  INPLACE_ADD      
              576  STORE_FAST               'retstr'

 L. 216       578  LOAD_FAST                'retstr'
              580  LOAD_FAST                'retdict'
              582  BUILD_TUPLE_2         2 
              584  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `COME_FROM_LOOP' instruction at offset 500_1


class TomlPreserveInlineDictEncoder(TomlEncoder):

    def __init__(self, _dict=dict):
        super(TomlPreserveInlineDictEncoder, self).__init__(_dict, True)


class TomlArraySeparatorEncoder(TomlEncoder):

    def __init__(self, _dict=dict, preserve=False, separator=','):
        super(TomlArraySeparatorEncoder, self).__init__(_dict, preserve)
        if separator.strip() == '':
            separator = ',' + separator
        else:
            if separator.strip(' \t\n\r,'):
                raise ValueError('Invalid separator for arrays')
        self.separator = separator

    def dump_list(self, v):
        t = []
        retval = '['
        for u in v:
            t.append(self.dump_value(u))

        while t != []:
            s = []
            for u in t:
                if isinstance(u, list):
                    for r in u:
                        s.append(r)

                else:
                    retval += ' ' + unicode(u) + self.separator

            t = s

        retval += ']'
        return retval