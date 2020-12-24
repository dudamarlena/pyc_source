# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /tmp/pip-install-vxs8l7gu/pip/pip/_vendor/toml.py
# Compiled at: 2020-05-05 12:41:36
# Size of source mod 2**32: 35675 bytes
"""Python module which parses and emits TOML.

Released under the MIT license.
"""
import re, io, datetime
from os import linesep
import sys
__version__ = '0.9.6'
_spec_ = '0.4.0'

class TomlDecodeError(Exception):
    __doc__ = 'Base toml Exception / Error.'


class TomlTz(datetime.tzinfo):

    def __init__(self, toml_offset):
        if toml_offset == 'Z':
            self._raw_offset = '+00:00'
        else:
            self._raw_offset = toml_offset
        self._sign = -1 if self._raw_offset[0] == '-' else 1
        self._hours = int(self._raw_offset[1:3])
        self._minutes = int(self._raw_offset[4:6])

    def tzname(self, dt):
        return 'UTC' + self._raw_offset

    def utcoffset(self, dt):
        return self._sign * datetime.timedelta(hours=(self._hours), minutes=(self._minutes))

    def dst(self, dt):
        return datetime.timedelta(0)


class InlineTableDict(object):
    __doc__ = 'Sentinel subclass of dict for inline tables.'


def _get_empty_inline_table(_dict):

    class DynamicInlineTableDict(_dict, InlineTableDict):
        __doc__ = 'Concrete sentinel subclass for inline tables.\n        It is a subclass of _dict which is passed in dynamically at load time\n        It is also a subclass of InlineTableDict\n        '

    return DynamicInlineTableDict()


try:
    _range = xrange
except NameError:
    unicode = str
    _range = range
    basestring = str
    unichr = chr

try:
    FNFError = FileNotFoundError
except NameError:
    FNFError = IOError

def load(f, _dict=dict):
    """Parses named file or files as toml and returns a dictionary

    Args:
        f: Path to the file to open, array of files to read into single dict
           or a file descriptor
        _dict: (optional) Specifies the class of the returned toml dictionary

    Returns:
        Parsed toml file represented as a dictionary

    Raises:
        TypeError -- When f is invalid type
        TomlDecodeError: Error while decoding toml
        IOError / FileNotFoundError -- When an array with no valid (existing)
        (Python 2 / Python 3)          file paths is passed
    """
    if isinstance(f, basestring):
        with io.open(f, encoding='utf-8') as (ffile):
            return loads(ffile.read(), _dict)
    else:
        if isinstance(f, list):
            from os import path as op
            from warnings import warn
            if not [path for path in f if op.exists(path)]:
                error_msg = 'Load expects a list to contain filenames only.'
                error_msg += linesep
                error_msg += 'The list needs to contain the path of at least one existing file.'
                raise FNFError(error_msg)
            d = _dict()
            for l in f:
                if op.exists(l):
                    d.update(load(l))
                else:
                    warn('Non-existent filename in list with at least one valid filename')

            return d
    try:
        return loads(f.read(), _dict)
    except AttributeError:
        raise TypeError('You can only load a file descriptor, filename or list')


_groupname_re = re.compile('^[A-Za-z0-9_-]+$')

def loads(s, _dict=dict):
    """Parses string as toml

    Args:
        s: String to be parsed
        _dict: (optional) Specifies the class of the returned toml dictionary

    Returns:
        Parsed toml file represented as a dictionary

    Raises:
        TypeError: When a non-string is passed
        TomlDecodeError: Error while decoding toml
    """
    implicitgroups = []
    retval = _dict()
    currentlevel = retval
    if not isinstance(s, basestring):
        raise TypeError('Expecting something like a string')
    if not isinstance(s, unicode):
        s = s.decode('utf8')
    sl = list(s)
    openarr = 0
    openstring = False
    openstrchar = ''
    multilinestr = False
    arrayoftables = False
    beginline = True
    keygroup = False
    keyname = 0
    for i, item in enumerate(sl):
        if item == '\r':
            if sl[(i + 1)] == '\n':
                sl[i] = ' '
                continue
            elif keyname:
                if item == '\n':
                    raise TomlDecodeError('Key name found without value. Reached end of line.')
                if openstring:
                    if item == openstrchar:
                        keyname = 2
                        openstring = False
                        openstrchar = ''
                        continue
                elif keyname == 1:
                    if item.isspace():
                        keyname = 2
                        continue
                elif item.isalnum() or item == '_' or item == '-':
                    continue
            else:
                if keyname == 2:
                    if item.isspace():
                        continue
                    if item == '=':
                        keyname = 0
                    else:
                        raise TomlDecodeError("Found invalid character in key name: '" + item + "'. Try quoting the key name.")
                elif item == "'":
                    if openstrchar != '"':
                        k = 1
                        try:
                            while sl[(i - k)] == "'":
                                k += 1
                                if k == 3:
                                    break

                        except IndexError:
                            pass

                        if k == 3:
                            multilinestr = not multilinestr
                            openstring = multilinestr
                        else:
                            openstring = not openstring
                        if openstring:
                            openstrchar = "'"
                        else:
                            openstrchar = ''
                    elif item == '"':
                        if openstrchar != "'":
                            oddbackslash = False
                            k = 1
                            tripquote = False
                            try:
                                while sl[(i - k)] == '"':
                                    k += 1
                                    if k == 3:
                                        tripquote = True
                                        break

                                if (k == 1 or k) == 3:
                                    if tripquote:
                                        while sl[(i - k)] == '\\':
                                            oddbackslash = not oddbackslash
                                            k += 1

                            except IndexError:
                                pass

                            if not oddbackslash:
                                if tripquote:
                                    multilinestr = not multilinestr
                                    openstring = multilinestr
                                else:
                                    openstring = not openstring
                            if openstring:
                                openstrchar = '"'
                            else:
                                openstrchar = ''
                        if item == '#' and not openstring or keygroup or arrayoftables:
                            j = i
                            try:
                                while sl[j] != '\n':
                                    sl[j] = ' '
                                    j += 1

                            except IndexError:
                                break

                            if item == '[' and not openstring:
                                if not keygroup:
                                    if not arrayoftables:
                                        if beginline:
                                            if len(sl) > i + 1 and sl[(i + 1)] == '[':
                                                arrayoftables = True
                    else:
                        keygroup = True
                else:
                    openarr += 1
            if item == ']' and not openstring:
                if keygroup:
                    keygroup = False
                else:
                    if arrayoftables:
                        if sl[(i - 1)] == ']':
                            arrayoftables = False
                        else:
                            openarr -= 1
                    elif item == '\n':
                        if openstring or multilinestr:
                            if not multilinestr:
                                raise TomlDecodeError('Unbalanced quotes')
                            if sl[(i - 1)] == "'" or sl[(i - 1)] == '"':
                                if sl[(i - 2)] == sl[(i - 1)]:
                                    sl[i] = sl[(i - 1)]
                                    if sl[(i - 3)] == sl[(i - 1)]:
                                        sl[i - 3] = ' '
                    elif openarr:
                        sl[i] = ' '
                    else:
                        beginline = True
            elif beginline:
                if sl[i] != ' ' and sl[i] != '\t':
                    beginline = False
                    if keygroup or arrayoftables or sl[i] == '=':
                        raise TomlDecodeError('Found empty keyname. ')
                keyname = 1

    s = ''.join(sl)
    s = s.split('\n')
    multikey = None
    multilinestr = ''
    multibackslash = False
    for line in s:
        if multilinestr:
            if multibackslash or '\n' not in multilinestr:
                line = line.strip()
            if line == '':
                if multikey:
                    if multibackslash:
                        continue
            if multikey:
                if multibackslash:
                    multilinestr += line
                else:
                    multilinestr += line
                multibackslash = False
                if len(line) > 2 and line[(-1)] == multilinestr[0]:
                    if line[(-2)] == multilinestr[0]:
                        if line[(-3)] == multilinestr[0]:
                            try:
                                value, vtype = _load_value(multilinestr, _dict)
                            except ValueError as err:
                                try:
                                    raise TomlDecodeError(str(err))
                                finally:
                                    err = None
                                    del err

                            currentlevel[multikey] = value
                            multikey = None
                            multilinestr = ''
                    k = len(multilinestr) - 1
                    while k > -1 and multilinestr[k] == '\\':
                        multibackslash = not multibackslash
                        k -= 1

                    if multibackslash:
                        multilinestr = multilinestr[:-1]
                else:
                    multilinestr += '\n'
                    continue
            if line[0] == '[':
                arrayoftables = False
                if len(line) == 1:
                    raise TomlDecodeError('Opening key group bracket on line by itself.')
                if line[1] == '[':
                    arrayoftables = True
                    line = line[2:]
                    splitstr = ']]'
                else:
                    line = line[1:]
                    splitstr = ']'
                i = 1
                quotesplits = _get_split_on_quotes(line)
                quoted = False
                for quotesplit in quotesplits:
                    if not quoted:
                        if splitstr in quotesplit:
                            break
                        i += quotesplit.count(splitstr)
                        quoted = not quoted

                line = line.split(splitstr, i)
                if len(line) < i + 1 or line[(-1)].strip() != '':
                    raise TomlDecodeError('Key group not on a line by itself.')
                groups = splitstr.join(line[:-1]).split('.')
                i = 0
                while i < len(groups):
                    groups[i] = groups[i].strip()
                    if not len(groups[i]) > 0 or groups[i][0] == '"' or groups[i][0] == "'":
                        groupstr = groups[i]
                        j = i + 1
                        while not groupstr[0] == groupstr[(-1)]:
                            j += 1
                            if j > len(groups) + 2:
                                raise TomlDecodeError("Invalid group name '" + groupstr + "' Something " + 'went wrong.')
                            groupstr = '.'.join(groups[i:j]).strip()

                        groups[i] = groupstr[1:-1]
                        groups[i + 1:j] = []
                    else:
                        if not _groupname_re.match(groups[i]):
                            raise TomlDecodeError("Invalid group name '" + groups[i] + "'. Try quoting it.")
                        i += 1

                currentlevel = retval
                for i in _range(len(groups)):
                    group = groups[i]
                    if group == '':
                        raise TomlDecodeError("Can't have a keygroup with an empty name")
                    try:
                        currentlevel[group]
                        if i == len(groups) - 1:
                            if group in implicitgroups:
                                implicitgroups.remove(group)
                                if arrayoftables:
                                    raise TomlDecodeError("An implicitly defined table can't be an array")
                            elif arrayoftables:
                                currentlevel[group].append(_dict())
                            else:
                                raise TomlDecodeError('What? ' + group + ' already exists?' + str(currentlevel))
                    except TypeError:
                        currentlevel = currentlevel[(-1)]
                        try:
                            currentlevel[group]
                        except KeyError:
                            currentlevel[group] = _dict()
                            if i == len(groups) - 1:
                                if arrayoftables:
                                    currentlevel[group] = [
                                     _dict()]

                    except KeyError:
                        if i != len(groups) - 1:
                            implicitgroups.append(group)
                        currentlevel[group] = _dict()
                        if i == len(groups) - 1:
                            if arrayoftables:
                                currentlevel[group] = [
                                 _dict()]

                    currentlevel = currentlevel[group]
                    if arrayoftables:
                        try:
                            currentlevel = currentlevel[(-1)]
                        except KeyError:
                            pass

        elif line[0] == '{':
            if line[(-1)] != '}':
                raise TomlDecodeError('Line breaks are not allowed in inlineobjects')
            try:
                _load_inline_object(line, currentlevel, _dict, multikey, multibackslash)
            except ValueError as err:
                try:
                    raise TomlDecodeError(str(err))
                finally:
                    err = None
                    del err

        elif '=' in line:
            try:
                ret = _load_line(line, currentlevel, _dict, multikey, multibackslash)
            except ValueError as err:
                try:
                    raise TomlDecodeError(str(err))
                finally:
                    err = None
                    del err

            if ret is not None:
                multikey, multilinestr, multibackslash = ret

    return retval


def _load_inline_object--- This code section failed: ---

 L. 410         0  LOAD_FAST                'line'
                2  LOAD_CONST               1
                4  LOAD_CONST               -1
                6  BUILD_SLICE_2         2 
                8  BINARY_SUBSCR    
               10  LOAD_METHOD              split
               12  LOAD_STR                 ','
               14  CALL_METHOD_1         1  '1 positional argument'
               16  STORE_FAST               'candidate_groups'

 L. 411        18  BUILD_LIST_0          0 
               20  STORE_FAST               'groups'

 L. 412        22  LOAD_GLOBAL              len
               24  LOAD_FAST                'candidate_groups'
               26  CALL_FUNCTION_1       1  '1 positional argument'
               28  LOAD_CONST               1
               30  COMPARE_OP               ==
               32  POP_JUMP_IF_FALSE    54  'to 54'
               34  LOAD_FAST                'candidate_groups'
               36  LOAD_CONST               0
               38  BINARY_SUBSCR    
               40  LOAD_METHOD              strip
               42  CALL_METHOD_0         0  '0 positional arguments'
               44  POP_JUMP_IF_TRUE     54  'to 54'

 L. 413        46  LOAD_FAST                'candidate_groups'
               48  LOAD_METHOD              pop
               50  CALL_METHOD_0         0  '0 positional arguments'
               52  POP_TOP          
             54_0  COME_FROM            44  '44'
             54_1  COME_FROM            32  '32'

 L. 414        54  SETUP_LOOP          294  'to 294'
               56  LOAD_GLOBAL              len
               58  LOAD_FAST                'candidate_groups'
               60  CALL_FUNCTION_1       1  '1 positional argument'
               62  LOAD_CONST               0
               64  COMPARE_OP               >
            66_68  POP_JUMP_IF_FALSE   292  'to 292'

 L. 415        70  LOAD_FAST                'candidate_groups'
               72  LOAD_METHOD              pop
               74  LOAD_CONST               0
               76  CALL_METHOD_1         1  '1 positional argument'
               78  STORE_FAST               'candidate_group'

 L. 416        80  SETUP_EXCEPT        102  'to 102'

 L. 417        82  LOAD_FAST                'candidate_group'
               84  LOAD_METHOD              split
               86  LOAD_STR                 '='
               88  LOAD_CONST               1
               90  CALL_METHOD_2         2  '2 positional arguments'
               92  UNPACK_SEQUENCE_2     2 
               94  STORE_FAST               '_'
               96  STORE_FAST               'value'
               98  POP_BLOCK        
              100  JUMP_FORWARD        130  'to 130'
            102_0  COME_FROM_EXCEPT     80  '80'

 L. 418       102  DUP_TOP          
              104  LOAD_GLOBAL              ValueError
              106  COMPARE_OP               exception-match
              108  POP_JUMP_IF_FALSE   128  'to 128'
              110  POP_TOP          
              112  POP_TOP          
              114  POP_TOP          

 L. 419       116  LOAD_GLOBAL              ValueError
              118  LOAD_STR                 'Invalid inline table encountered'
              120  CALL_FUNCTION_1       1  '1 positional argument'
              122  RAISE_VARARGS_1       1  'exception instance'
              124  POP_EXCEPT       
              126  JUMP_FORWARD        130  'to 130'
            128_0  COME_FROM           108  '108'
              128  END_FINALLY      
            130_0  COME_FROM           126  '126'
            130_1  COME_FROM           100  '100'

 L. 420       130  LOAD_FAST                'value'
              132  LOAD_METHOD              strip
              134  CALL_METHOD_0         0  '0 positional arguments'
              136  STORE_FAST               'value'

 L. 421       138  LOAD_FAST                'value'
              140  LOAD_CONST               0
              142  BINARY_SUBSCR    
              144  LOAD_FAST                'value'
              146  LOAD_CONST               -1
              148  BINARY_SUBSCR    
              150  COMPARE_OP               ==
              152  POP_JUMP_IF_FALSE   166  'to 166'
              154  LOAD_FAST                'value'
              156  LOAD_CONST               0
              158  BINARY_SUBSCR    
              160  LOAD_CONST               ('"', "'")
              162  COMPARE_OP               in
              164  POP_JUMP_IF_TRUE    234  'to 234'
            166_0  COME_FROM           152  '152'

 L. 422       166  LOAD_FAST                'value'
              168  LOAD_CONST               0
              170  BINARY_SUBSCR    
              172  LOAD_STR                 '-0123456789'
              174  COMPARE_OP               in
              176  POP_JUMP_IF_TRUE    234  'to 234'

 L. 423       178  LOAD_FAST                'value'
              180  LOAD_CONST               ('true', 'false')
              182  COMPARE_OP               in
              184  POP_JUMP_IF_TRUE    234  'to 234'

 L. 424       186  LOAD_FAST                'value'
              188  LOAD_CONST               0
              190  BINARY_SUBSCR    
              192  LOAD_STR                 '['
              194  COMPARE_OP               ==
              196  POP_JUMP_IF_FALSE   210  'to 210'
              198  LOAD_FAST                'value'
              200  LOAD_CONST               -1
              202  BINARY_SUBSCR    
              204  LOAD_STR                 ']'
              206  COMPARE_OP               ==
              208  POP_JUMP_IF_TRUE    234  'to 234'
            210_0  COME_FROM           196  '196'

 L. 425       210  LOAD_FAST                'value'
              212  LOAD_CONST               0
              214  BINARY_SUBSCR    
              216  LOAD_STR                 '{'
              218  COMPARE_OP               ==
              220  POP_JUMP_IF_FALSE   246  'to 246'
              222  LOAD_FAST                'value'
              224  LOAD_CONST               -1
              226  BINARY_SUBSCR    
              228  LOAD_STR                 '}'
              230  COMPARE_OP               ==
              232  POP_JUMP_IF_FALSE   246  'to 246'
            234_0  COME_FROM           208  '208'
            234_1  COME_FROM           184  '184'
            234_2  COME_FROM           176  '176'
            234_3  COME_FROM           164  '164'

 L. 426       234  LOAD_FAST                'groups'
              236  LOAD_METHOD              append
              238  LOAD_FAST                'candidate_group'
              240  CALL_METHOD_1         1  '1 positional argument'
              242  POP_TOP          
              244  JUMP_BACK            56  'to 56'
            246_0  COME_FROM           232  '232'
            246_1  COME_FROM           220  '220'

 L. 427       246  LOAD_GLOBAL              len
              248  LOAD_FAST                'candidate_groups'
              250  CALL_FUNCTION_1       1  '1 positional argument'
              252  LOAD_CONST               0
              254  COMPARE_OP               >
          256_258  POP_JUMP_IF_FALSE   282  'to 282'

 L. 428       260  LOAD_FAST                'candidate_group'
              262  LOAD_STR                 ','
              264  BINARY_ADD       
              266  LOAD_FAST                'candidate_groups'
              268  LOAD_CONST               0
              270  BINARY_SUBSCR    
              272  BINARY_ADD       
              274  LOAD_FAST                'candidate_groups'
              276  LOAD_CONST               0
              278  STORE_SUBSCR     
              280  JUMP_BACK            56  'to 56'
            282_0  COME_FROM           256  '256'

 L. 430       282  LOAD_GLOBAL              ValueError
              284  LOAD_STR                 'Invalid inline table value encountered'
              286  CALL_FUNCTION_1       1  '1 positional argument'
              288  RAISE_VARARGS_1       1  'exception instance'
              290  JUMP_BACK            56  'to 56'
            292_0  COME_FROM            66  '66'
              292  POP_BLOCK        
            294_0  COME_FROM_LOOP       54  '54'

 L. 431       294  SETUP_LOOP          338  'to 338'
              296  LOAD_FAST                'groups'
              298  GET_ITER         
            300_0  COME_FROM           326  '326'
              300  FOR_ITER            336  'to 336'
              302  STORE_FAST               'group'

 L. 432       304  LOAD_GLOBAL              _load_line
              306  LOAD_FAST                'group'
              308  LOAD_FAST                'currentlevel'
              310  LOAD_FAST                '_dict'
              312  LOAD_FAST                'multikey'

 L. 433       314  LOAD_FAST                'multibackslash'
              316  CALL_FUNCTION_5       5  '5 positional arguments'
              318  STORE_FAST               'status'

 L. 434       320  LOAD_FAST                'status'
              322  LOAD_CONST               None
              324  COMPARE_OP               is-not
          326_328  POP_JUMP_IF_FALSE   300  'to 300'

 L. 435       330  BREAK_LOOP       
          332_334  JUMP_BACK           300  'to 300'
              336  POP_BLOCK        
            338_0  COME_FROM_LOOP      294  '294'

Parse error at or near `COME_FROM' instruction at offset 246_1


_number_with_underscores = re.compile('([0-9])(_([0-9]))*')

def _strictly_valid_num(n):
    n = n.strip()
    if not n:
        return False
    if n[0] == '_':
        return False
    if n[(-1)] == '_':
        return False
    if '_.' in n or '._' in n:
        return False
    if len(n) == 1:
        return True
    if n[0] == '0':
        if n[1] != '.':
            return False
    if n[0] == '+' or n[0] == '-':
        n = n[1:]
        if n[0] == '0':
            if n[1] != '.':
                return False
    if '__' in n:
        return False
    return True


def _get_split_on_quotes(line):
    doublequotesplits = line.split('"')
    quoted = False
    quotesplits = []
    if len(doublequotesplits) > 1:
        if "'" in doublequotesplits[0]:
            singlequotesplits = doublequotesplits[0].split("'")
            doublequotesplits = doublequotesplits[1:]
            while len(singlequotesplits) % 2 == 0 and len(doublequotesplits):
                singlequotesplits[(-1)] += '"' + doublequotesplits[0]
                doublequotesplits = doublequotesplits[1:]
                if "'" in singlequotesplits[(-1)]:
                    singlequotesplits = singlequotesplits[:-1] + singlequotesplits[(-1)].split("'")

            quotesplits += singlequotesplits
    for doublequotesplit in doublequotesplits:
        if quoted:
            quotesplits.append(doublequotesplit)
        else:
            quotesplits += doublequotesplit.split("'")
            quoted = not quoted

    return quotesplits


def _load_line(line, currentlevel, _dict, multikey, multibackslash):
    i = 1
    quotesplits = _get_split_on_quotes(line)
    quoted = False
    for quotesplit in quotesplits:
        if not quoted:
            if '=' in quotesplit:
                break
        i += quotesplit.count('=')
        quoted = not quoted

    pair = line.split('=', i)
    strictly_valid = _strictly_valid_num(pair[(-1)])
    if _number_with_underscores.match(pair[(-1)]):
        pair[-1] = pair[(-1)].replace('_', '')
    else:
        while len(pair[(-1)]) and pair[(-1)][0] != ' ' and pair[(-1)][0] != '\t' and pair[(-1)][0] != "'" and pair[(-1)][0] != '"' and pair[(-1)][0] != '[' and pair[(-1)][0] != '{' and pair[(-1)] != 'true' and pair[(-1)] != 'false':
            try:
                float(pair[(-1)])
                break
            except ValueError:
                pass

            if _load_date(pair[(-1)]) is not None:
                break
            i += 1
            prev_val = pair[(-1)]
            pair = line.split('=', i)
            if prev_val == pair[(-1)]:
                raise ValueError('Invalid date or number')
            if strictly_valid:
                strictly_valid = _strictly_valid_num(pair[(-1)])

        pair = [
         '='.join(pair[:-1]).strip(), pair[(-1)].strip()]
        if pair[0][0] == '"' or pair[0][0] == "'":
            if pair[0][(-1)] == '"' or pair[0][(-1)] == "'":
                pair[0] = pair[0][1:-1]
        if len(pair[1]) > 2:
            if pair[1][0] == '"' or pair[1][0] == "'":
                if pair[1][1] == pair[1][0] and pair[1][2] == pair[1][0]:
                    if len(pair[1]) > 5:
                        if pair[1][(-1)] == pair[1][0]:
                            if not (pair[1][(-2)] == pair[1][0] and pair[1][(-3)] == pair[1][0]):
                                k = len(pair[1]) - 1
                                while k > -1 and pair[1][k] == '\\':
                                    multibackslash = not multibackslash
                                    k -= 1

                                if multibackslash:
                                    multilinestr = pair[1][:-1]
                        else:
                            multilinestr = pair[1] + '\n'
                        multikey = pair[0]
                    else:
                        pass
        value, vtype = _load_value(pair[1], _dict, strictly_valid)
    try:
        currentlevel[pair[0]]
        raise ValueError('Duplicate keys!')
    except KeyError:
        if multikey:
            return (
             multikey, multilinestr, multibackslash)
        currentlevel[pair[0]] = value


def _load_date(val):
    microsecond = 0
    tz = None
    try:
        if len(val) > 19:
            if val[19] == '.':
                if val[(-1)].upper() == 'Z':
                    subsecondval = val[20:-1]
                    tzval = 'Z'
                else:
                    subsecondvalandtz = val[20:]
                    if '+' in subsecondvalandtz:
                        splitpoint = subsecondvalandtz.index('+')
                        subsecondval = subsecondvalandtz[:splitpoint]
                        tzval = subsecondvalandtz[splitpoint:]
                    else:
                        if '-' in subsecondvalandtz:
                            splitpoint = subsecondvalandtz.index('-')
                            subsecondval = subsecondvalandtz[:splitpoint]
                            tzval = subsecondvalandtz[splitpoint:]
                tz = TomlTz(tzval)
                microsecond = int(int(subsecondval) * 10 ** (6 - len(subsecondval)))
            else:
                tz = TomlTz(val[19:])
    except ValueError:
        tz = None

    if '-' not in val[1:]:
        return
    try:
        d = datetime.datetime(int(val[:4]), int(val[5:7]), int(val[8:10]), int(val[11:13]), int(val[14:16]), int(val[17:19]), microsecond, tz)
    except ValueError:
        return
    else:
        return d


def _load_unicode_escapes(v, hexbytes, prefix):
    skip = False
    i = len(v) - 1
    while i > -1 and v[i] == '\\':
        skip = not skip
        i -= 1

    for hx in hexbytes:
        if skip:
            skip = False
            i = len(hx) - 1
            while i > -1 and hx[i] == '\\':
                skip = not skip
                i -= 1

            v += prefix
            v += hx
            continue
        hxb = ''
        i = 0
        hxblen = 4
        if prefix == '\\U':
            hxblen = 8
        hxb = ''.join(hx[i:i + hxblen]).lower()
        if hxb.strip('0123456789abcdef'):
            raise ValueError('Invalid escape sequence: ' + hxb)
        if hxb[0] == 'd':
            if hxb[1].strip('01234567'):
                raise ValueError('Invalid escape sequence: ' + hxb + '. Only scalar unicode points are allowed.')
        v += unichr(int(hxb, 16))
        v += unicode(hx[len(hxb):])

    return v


_escapes = [
 '0', 'b', 'f', 'n', 'r', 't', '"']
_escapedchars = [
 '\x00', '\x08', '\x0c', '\n', '\r', '\t', '"']
_escape_to_escapedchars = dict(zip(_escapes, _escapedchars))

def _unescape(v):
    """Unescape characters in a TOML string."""
    i = 0
    backslash = False
    while i < len(v):
        if backslash:
            backslash = False
            if v[i] in _escapes:
                v = v[:i - 1] + _escape_to_escapedchars[v[i]] + v[i + 1:]
        elif v[i] == '\\':
            v = v[:i - 1] + v[i:]
        else:
            if not v[i] == 'u':
                if v[i] == 'U':
                    i += 1
                else:
                    raise ValueError('Reserved escape sequence used')
                continue
            elif v[i] == '\\':
                backslash = True
            i += 1

    return v


def _load_value(v, _dict, strictly_valid=True):
    if not v:
        raise ValueError('Empty value is invalid')
    else:
        if v == 'true':
            return (True, 'bool')
            if v == 'false':
                return (False, 'bool')
            if v[0] == '"':
                testv = v[1:].split('"')
                triplequote = False
                triplequotecount = 0
                if len(testv) > 1:
                    if testv[0] == '':
                        if testv[1] == '':
                            testv = testv[2:]
                            triplequote = True
                closed = False
                for tv in testv:
                    if tv == '':
                        if triplequote:
                            triplequotecount += 1
                        else:
                            closed = True

                escapeseqs = v.split('\\')[1:]
                backslash = False
                for i in escapeseqs:
                    if i == '':
                        backslash = not backslash
                    elif i[0] not in _escapes and i[0] != 'u' and i[0] != 'U':
                        if not backslash:
                            raise ValueError('Reserved escape sequence used')
                    if backslash:
                        backslash = False

                for prefix in ('\\u', '\\U'):
                    if prefix in v:
                        hexbytes = v.split(prefix)
                        v = _load_unicode_escapes(hexbytes[0], hexbytes[1:], prefix)

                v = _unescape(v)
                if len(v) > 1 and v[1] == '"' and not len(v) < 3:
                    if v[1] == v[2]:
                        v = v[2:-2]
                return (
                 v[1:-1], 'str')
            if v[0] == "'":
                if not v[1] == "'" or len(v) < 3 or v[1] == v[2]:
                    v = v[2:-2]
        else:
            return (
             v[1:-1], 'str')
        if v[0] == '[':
            return (
             _load_array(v, _dict), 'array')
        if v[0] == '{':
            inline_object = _get_empty_inline_table(_dict)
            _load_inline_object(v, inline_object, _dict)
            return (inline_object, 'inline_object')
        parsed_date = _load_date(v)
        if parsed_date is not None:
            return (
             parsed_date, 'date')
        assert strictly_valid, 'Weirdness with leading zeroes or underscores in your number.'
    itype = 'int'
    neg = False
    if v[0] == '-':
        neg = True
        v = v[1:]
    else:
        if v[0] == '+':
            v = v[1:]
        else:
            v = v.replace('_', '')
            if '.' in v or 'e' in v or 'E' in v:
                if '.' in v:
                    if v.split('.', 1)[1] == '':
                        raise ValueError('This float is missing digits after the point')
                    if v[0] not in '0123456789':
                        raise ValueError("This float doesn't have a leading digit")
                    v = float(v)
                    itype = 'float'
                else:
                    pass
            v = int(v)
        if neg:
            return (
             0 - v, itype)
        return (
         v, itype)


def _bounded_string(s):
    if len(s) == 0:
        return True
    if s[(-1)] != s[0]:
        return False
    i = -2
    backslash = False
    while len(s) + i > 0:
        if s[i] == '\\':
            backslash = not backslash
            i -= 1
        else:
            break

    return not backslash


def _load_array(a, _dict):
    atype = None
    retval = []
    a = a.strip()
    if '[' not in a[1:-1] or '' != a[1:-1].split('[')[0].strip():
        strarray = False
        tmpa = a[1:-1].strip()
        if tmpa != '':
            if tmpa[0] == '"' or tmpa[0] == "'":
                strarray = True
        if not a[1:-1].strip().startswith('{'):
            a = a[1:-1].split(',')
        else:
            new_a = []
            start_group_index = 1
            end_group_index = 2
            in_str = False
            while end_group_index < len(a[1:]) and not a[end_group_index] == '"':
                if a[end_group_index] == "'":
                    if in_str:
                        backslash_index = end_group_index - 1
                        while backslash_index > -1 and a[backslash_index] == '\\':
                            in_str = not in_str
                            backslash_index -= 1

                    in_str = not in_str
                if in_str or a[end_group_index] != '}':
                    end_group_index += 1
                    continue
                end_group_index += 1
                new_a.append(a[start_group_index:end_group_index])
                start_group_index = end_group_index + 1
                while start_group_index < len(a[1:]) and a[start_group_index] != '{':
                    start_group_index += 1

                end_group_index = start_group_index + 1

            a = new_a
        b = 0
        if strarray:
            while b < len(a) - 1:
                ab = a[b].strip()
                while _bounded_string(ab):
                    if len(ab) > 2:
                        if ab[0] == ab[1] == ab[2]:
                            if not ab[(-2)] != ab[0] or ab[(-3)] != ab[0]:
                                a[b] = a[b] + ',' + a[(b + 1)]
                                ab = a[b].strip()
                                if b < len(a) - 2:
                                    a = a[:b + 1] + a[b + 2:]
                                else:
                                    a = a[:b + 1]

                b += 1

    else:
        al = list(a[1:-1])
        a = []
        openarr = 0
        j = 0
        for i in _range(len(al)):
            if al[i] == '[':
                openarr += 1
            else:
                if al[i] == ']':
                    openarr -= 1

        a.append(''.join(al[j:]))
    for i in _range(len(a)):
        a[i] = a[i].strip()
        if a[i] != '':
            nval, ntype = _load_value(a[i], _dict)
            if atype:
                if ntype != atype:
                    raise ValueError('Not a homogeneous array')
            else:
                atype = ntype
            retval.append(nval)

    return retval


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


def dumps(o, preserve=False):
    """Stringifies input dict as toml

    Args:
        o: Object to dump into toml

        preserve: Boolean parameter. If true, preserve inline tables.

    Returns:
        String containing the toml corresponding to dict
    """
    retval = ''
    addtoretval, sections = _dump_sections(o, '')
    retval += addtoretval
    while sections != {}:
        newsections = {}
        for section in sections:
            addtoretval, addtosections = _dump_sections(sections[section], section, preserve)
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


def _dump_sections--- This code section failed: ---

 L. 909         0  LOAD_STR                 ''
                2  STORE_FAST               'retstr'

 L. 910         4  LOAD_FAST                'sup'
                6  LOAD_STR                 ''
                8  COMPARE_OP               !=
               10  POP_JUMP_IF_FALSE    32  'to 32'
               12  LOAD_FAST                'sup'
               14  LOAD_CONST               -1
               16  BINARY_SUBSCR    
               18  LOAD_STR                 '.'
               20  COMPARE_OP               !=
               22  POP_JUMP_IF_FALSE    32  'to 32'

 L. 911        24  LOAD_FAST                'sup'
               26  LOAD_STR                 '.'
               28  INPLACE_ADD      
               30  STORE_FAST               'sup'
             32_0  COME_FROM            22  '22'
             32_1  COME_FROM            10  '10'

 L. 912        32  LOAD_FAST                'o'
               34  LOAD_METHOD              __class__
               36  CALL_METHOD_0         0  '0 positional arguments'
               38  STORE_FAST               'retdict'

 L. 913        40  LOAD_STR                 ''
               42  STORE_FAST               'arraystr'

 L. 914     44_46  SETUP_LOOP          558  'to 558'
               48  LOAD_FAST                'o'
               50  GET_ITER         
            52_54  FOR_ITER            556  'to 556'
               56  STORE_FAST               'section'

 L. 915        58  LOAD_GLOBAL              unicode
               60  LOAD_FAST                'section'
               62  CALL_FUNCTION_1       1  '1 positional argument'
               64  STORE_FAST               'section'

 L. 916        66  LOAD_FAST                'section'
               68  STORE_FAST               'qsection'

 L. 917        70  LOAD_GLOBAL              re
               72  LOAD_METHOD              match
               74  LOAD_STR                 '^[A-Za-z0-9_-]+$'
               76  LOAD_FAST                'section'
               78  CALL_METHOD_2         2  '2 positional arguments'
               80  POP_JUMP_IF_TRUE    116  'to 116'

 L. 918        82  LOAD_STR                 '"'
               84  LOAD_FAST                'section'
               86  COMPARE_OP               in
               88  POP_JUMP_IF_FALSE   104  'to 104'

 L. 919        90  LOAD_STR                 "'"
               92  LOAD_FAST                'section'
               94  BINARY_ADD       
               96  LOAD_STR                 "'"
               98  BINARY_ADD       
              100  STORE_FAST               'qsection'
              102  JUMP_FORWARD        116  'to 116'
            104_0  COME_FROM            88  '88'

 L. 921       104  LOAD_STR                 '"'
              106  LOAD_FAST                'section'
              108  BINARY_ADD       
              110  LOAD_STR                 '"'
              112  BINARY_ADD       
              114  STORE_FAST               'qsection'
            116_0  COME_FROM           102  '102'
            116_1  COME_FROM            80  '80'

 L. 922       116  LOAD_GLOBAL              isinstance
              118  LOAD_FAST                'o'
              120  LOAD_FAST                'section'
              122  BINARY_SUBSCR    
              124  LOAD_GLOBAL              dict
              126  CALL_FUNCTION_2       2  '2 positional arguments'
          128_130  POP_JUMP_IF_TRUE    494  'to 494'

 L. 923       132  LOAD_CONST               False
              134  STORE_FAST               'arrayoftables'

 L. 924       136  LOAD_GLOBAL              isinstance
              138  LOAD_FAST                'o'
              140  LOAD_FAST                'section'
              142  BINARY_SUBSCR    
              144  LOAD_GLOBAL              list
              146  CALL_FUNCTION_2       2  '2 positional arguments'
              148  POP_JUMP_IF_FALSE   182  'to 182'

 L. 925       150  SETUP_LOOP          182  'to 182'
              152  LOAD_FAST                'o'
              154  LOAD_FAST                'section'
              156  BINARY_SUBSCR    
              158  GET_ITER         
            160_0  COME_FROM           172  '172'
              160  FOR_ITER            180  'to 180'
              162  STORE_FAST               'a'

 L. 926       164  LOAD_GLOBAL              isinstance
              166  LOAD_FAST                'a'
              168  LOAD_GLOBAL              dict
              170  CALL_FUNCTION_2       2  '2 positional arguments'
              172  POP_JUMP_IF_FALSE   160  'to 160'

 L. 927       174  LOAD_CONST               True
              176  STORE_FAST               'arrayoftables'
              178  JUMP_BACK           160  'to 160'
              180  POP_BLOCK        
            182_0  COME_FROM_LOOP      150  '150'
            182_1  COME_FROM           148  '148'

 L. 928       182  LOAD_FAST                'arrayoftables'
          184_186  POP_JUMP_IF_FALSE   446  'to 446'

 L. 929       188  SETUP_LOOP          444  'to 444'
              190  LOAD_FAST                'o'
              192  LOAD_FAST                'section'
              194  BINARY_SUBSCR    
              196  GET_ITER         
              198  FOR_ITER            442  'to 442'
              200  STORE_FAST               'a'

 L. 930       202  LOAD_STR                 '\n'
              204  STORE_FAST               'arraytabstr'

 L. 931       206  LOAD_FAST                'arraystr'
              208  LOAD_STR                 '[['
              210  LOAD_FAST                'sup'
              212  BINARY_ADD       
              214  LOAD_FAST                'qsection'
              216  BINARY_ADD       
              218  LOAD_STR                 ']]\n'
              220  BINARY_ADD       
              222  INPLACE_ADD      
              224  STORE_FAST               'arraystr'

 L. 932       226  LOAD_GLOBAL              _dump_sections
              228  LOAD_FAST                'a'
              230  LOAD_FAST                'sup'
              232  LOAD_FAST                'qsection'
              234  BINARY_ADD       
              236  CALL_FUNCTION_2       2  '2 positional arguments'
              238  UNPACK_SEQUENCE_2     2 
              240  STORE_FAST               's'
              242  STORE_FAST               'd'

 L. 933       244  LOAD_FAST                's'
          246_248  POP_JUMP_IF_FALSE   282  'to 282'

 L. 934       250  LOAD_FAST                's'
              252  LOAD_CONST               0
              254  BINARY_SUBSCR    
              256  LOAD_STR                 '['
              258  COMPARE_OP               ==
          260_262  POP_JUMP_IF_FALSE   274  'to 274'

 L. 935       264  LOAD_FAST                'arraytabstr'
              266  LOAD_FAST                's'
              268  INPLACE_ADD      
              270  STORE_FAST               'arraytabstr'
              272  JUMP_FORWARD        282  'to 282'
            274_0  COME_FROM           260  '260'

 L. 937       274  LOAD_FAST                'arraystr'
              276  LOAD_FAST                's'
              278  INPLACE_ADD      
              280  STORE_FAST               'arraystr'
            282_0  COME_FROM           272  '272'
            282_1  COME_FROM           246  '246'

 L. 938       282  SETUP_LOOP          432  'to 432'
              284  LOAD_FAST                'd'
              286  BUILD_MAP_0           0 
              288  COMPARE_OP               !=
          290_292  POP_JUMP_IF_FALSE   430  'to 430'

 L. 939       294  BUILD_MAP_0           0 
              296  STORE_FAST               'newd'

 L. 940       298  SETUP_LOOP          422  'to 422'
              300  LOAD_FAST                'd'
              302  GET_ITER         
              304  FOR_ITER            420  'to 420'
              306  STORE_FAST               'dsec'

 L. 941       308  LOAD_GLOBAL              _dump_sections
              310  LOAD_FAST                'd'
              312  LOAD_FAST                'dsec'
              314  BINARY_SUBSCR    

 L. 942       316  LOAD_FAST                'sup'
              318  LOAD_FAST                'qsection'
              320  BINARY_ADD       
              322  LOAD_STR                 '.'
              324  BINARY_ADD       
              326  LOAD_FAST                'dsec'
              328  BINARY_ADD       
              330  CALL_FUNCTION_2       2  '2 positional arguments'
              332  UNPACK_SEQUENCE_2     2 
              334  STORE_FAST               's1'
              336  STORE_FAST               'd1'

 L. 943       338  LOAD_FAST                's1'
          340_342  POP_JUMP_IF_FALSE   380  'to 380'

 L. 944       344  LOAD_FAST                'arraytabstr'

 L. 945       346  LOAD_STR                 '['
              348  LOAD_FAST                'sup'
              350  BINARY_ADD       
              352  LOAD_FAST                'qsection'
              354  BINARY_ADD       
              356  LOAD_STR                 '.'
              358  BINARY_ADD       
              360  LOAD_FAST                'dsec'
              362  BINARY_ADD       
              364  LOAD_STR                 ']\n'
              366  BINARY_ADD       
              368  INPLACE_ADD      
              370  STORE_FAST               'arraytabstr'

 L. 946       372  LOAD_FAST                'arraytabstr'
              374  LOAD_FAST                's1'
              376  INPLACE_ADD      
              378  STORE_FAST               'arraytabstr'
            380_0  COME_FROM           340  '340'

 L. 947       380  SETUP_LOOP          416  'to 416'
              382  LOAD_FAST                'd1'
              384  GET_ITER         
              386  FOR_ITER            414  'to 414'
              388  STORE_FAST               's1'

 L. 948       390  LOAD_FAST                'd1'
              392  LOAD_FAST                's1'
              394  BINARY_SUBSCR    
              396  LOAD_FAST                'newd'
              398  LOAD_FAST                'dsec'
              400  LOAD_STR                 '.'
              402  BINARY_ADD       
              404  LOAD_FAST                's1'
              406  BINARY_ADD       
              408  STORE_SUBSCR     
          410_412  JUMP_BACK           386  'to 386'
              414  POP_BLOCK        
            416_0  COME_FROM_LOOP      380  '380'
          416_418  JUMP_BACK           304  'to 304'
              420  POP_BLOCK        
            422_0  COME_FROM_LOOP      298  '298'

 L. 949       422  LOAD_FAST                'newd'
              424  STORE_FAST               'd'
          426_428  JUMP_BACK           284  'to 284'
            430_0  COME_FROM           290  '290'
              430  POP_BLOCK        
            432_0  COME_FROM_LOOP      282  '282'

 L. 950       432  LOAD_FAST                'arraystr'
              434  LOAD_FAST                'arraytabstr'
              436  INPLACE_ADD      
              438  STORE_FAST               'arraystr'
              440  JUMP_BACK           198  'to 198'
              442  POP_BLOCK        
            444_0  COME_FROM_LOOP      188  '188'
              444  JUMP_FORWARD        492  'to 492'
            446_0  COME_FROM           184  '184'

 L. 952       446  LOAD_FAST                'o'
              448  LOAD_FAST                'section'
              450  BINARY_SUBSCR    
              452  LOAD_CONST               None
              454  COMPARE_OP               is-not
          456_458  POP_JUMP_IF_FALSE   554  'to 554'

 L. 953       460  LOAD_FAST                'retstr'

 L. 954       462  LOAD_FAST                'qsection'
              464  LOAD_STR                 ' = '
              466  BINARY_ADD       
              468  LOAD_GLOBAL              unicode
              470  LOAD_GLOBAL              _dump_value
              472  LOAD_FAST                'o'
              474  LOAD_FAST                'section'
              476  BINARY_SUBSCR    
              478  CALL_FUNCTION_1       1  '1 positional argument'
              480  CALL_FUNCTION_1       1  '1 positional argument'
              482  BINARY_ADD       
              484  LOAD_STR                 '\n'
              486  BINARY_ADD       
              488  INPLACE_ADD      
              490  STORE_FAST               'retstr'
            492_0  COME_FROM           444  '444'
              492  JUMP_BACK            52  'to 52'
            494_0  COME_FROM           128  '128'

 L. 955       494  LOAD_FAST                'preserve'
          496_498  POP_JUMP_IF_FALSE   542  'to 542'
              500  LOAD_GLOBAL              isinstance
              502  LOAD_FAST                'o'
              504  LOAD_FAST                'section'
              506  BINARY_SUBSCR    
              508  LOAD_GLOBAL              InlineTableDict
              510  CALL_FUNCTION_2       2  '2 positional arguments'
          512_514  POP_JUMP_IF_FALSE   542  'to 542'

 L. 956       516  LOAD_FAST                'retstr'
              518  LOAD_FAST                'qsection'
              520  LOAD_STR                 ' = '
              522  BINARY_ADD       
              524  LOAD_GLOBAL              _dump_inline_table
              526  LOAD_FAST                'o'
              528  LOAD_FAST                'section'
              530  BINARY_SUBSCR    
              532  CALL_FUNCTION_1       1  '1 positional argument'
              534  BINARY_ADD       
              536  INPLACE_ADD      
              538  STORE_FAST               'retstr'
              540  JUMP_BACK            52  'to 52'
            542_0  COME_FROM           512  '512'
            542_1  COME_FROM           496  '496'

 L. 958       542  LOAD_FAST                'o'
              544  LOAD_FAST                'section'
              546  BINARY_SUBSCR    
              548  LOAD_FAST                'retdict'
              550  LOAD_FAST                'qsection'
              552  STORE_SUBSCR     
            554_0  COME_FROM           456  '456'
              554  JUMP_BACK            52  'to 52'
              556  POP_BLOCK        
            558_0  COME_FROM_LOOP       44  '44'

 L. 959       558  LOAD_FAST                'retstr'
              560  LOAD_FAST                'arraystr'
              562  INPLACE_ADD      
              564  STORE_FAST               'retstr'

 L. 960       566  LOAD_FAST                'retstr'
              568  LOAD_FAST                'retdict'
              570  BUILD_TUPLE_2         2 
              572  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `JUMP_BACK' instruction at offset 554


def _dump_inline_table(section):
    """Preserve inline table in its compact syntax instead of expanding
    into subsection.

    https://github.com/toml-lang/toml#user-content-inline-table
    """
    retval = ''
    if isinstance(section, dict):
        val_list = []
        for k, v in section.items():
            val = _dump_inline_table(v)
            val_list.append(k + ' = ' + val)

        retval += '{ ' + ', '.join(val_list) + ' }\n'
        return retval
    return unicode(_dump_value(section))


def _dump_value(v):
    dump_funcs = {str: _dump_str, 
     unicode: _dump_str, 
     list: _dump_list, 
     int: lambda v: v, 
     bool: lambda v: unicode(v).lower(), 
     float: _dump_float, 
     datetime.datetime: lambda v: v.isoformat().replace('+00:00', 'Z')}
    dump_fn = dump_funcs.get(type(v))
    if dump_fn is None:
        if hasattr(v, '__iter__'):
            dump_fn = dump_funcs[list]
    if dump_fn is not None:
        return dump_fn(v)
    return dump_funcs[str](v)


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


def _dump_list(v):
    retval = '['
    for u in v:
        retval += ' ' + unicode(_dump_value(u)) + ','

    retval += ']'
    return retval


def _dump_float(v):
    return '{0:.16}'.format(v).replace('e+0', 'e+').replace('e-0', 'e-')