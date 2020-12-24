# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: HTMLParser.pyc
# Compiled at: 2010-06-05 01:00:06
"""A parser for HTML and XHTML."""
import markupbase, re
interesting_normal = re.compile('[&<]')
interesting_cdata = re.compile('<(/|\\Z)')
incomplete = re.compile('&[a-zA-Z#]')
entityref = re.compile('&([a-zA-Z][-.a-zA-Z0-9]*)[^a-zA-Z0-9]')
charref = re.compile('&#(?:[0-9]+|[xX][0-9a-fA-F]+)[^0-9a-fA-F]')
starttagopen = re.compile('<[a-zA-Z]')
piclose = re.compile('>')
commentclose = re.compile('--\\s*>')
tagfind = re.compile('[a-zA-Z][-.a-zA-Z0-9:_]*')
attrfind = re.compile('\\s*([a-zA-Z_][-.:a-zA-Z_0-9]*)(\\s*=\\s*(\\\'[^\\\']*\\\'|"[^"]*"|[-a-zA-Z0-9./,:;+*%?!&$\\(\\)_#=~@]*))?')
locatestarttagend = re.compile('\n  <[a-zA-Z][-.a-zA-Z0-9:_]*          # tag name\n  (?:\\s+                             # whitespace before attribute name\n    (?:[a-zA-Z_][-.:a-zA-Z0-9_]*     # attribute name\n      (?:\\s*=\\s*                     # value indicator\n        (?:\'[^\']*\'                   # LITA-enclosed value\n          |\\"[^\\"]*\\"                # LIT-enclosed value\n          |[^\'\\">\\s]+                # bare value\n         )\n       )?\n     )\n   )*\n  \\s*                                # trailing whitespace\n', re.VERBOSE)
endendtag = re.compile('>')
endtagfind = re.compile('</\\s*([a-zA-Z][-.a-zA-Z0-9:_]*)\\s*>')

class HTMLParseError(Exception):
    """Exception raised for all parse errors."""

    def __init__(self, msg, position=(None, None)):
        assert msg
        self.msg = msg
        self.lineno = position[0]
        self.offset = position[1]

    def __str__(self):
        result = self.msg
        if self.lineno is not None:
            result = result + ', at line %d' % self.lineno
        if self.offset is not None:
            result = result + ', column %d' % (self.offset + 1)
        return result


class HTMLParser(markupbase.ParserBase):
    """Find tags and other markup and call handler functions.

    Usage:
        p = HTMLParser()
        p.feed(data)
        ...
        p.close()

    Start tags are handled by calling self.handle_starttag() or
    self.handle_startendtag(); end tags by self.handle_endtag().  The
    data between tags is passed from the parser to the derived class
    by calling self.handle_data() with the data as argument (the data
    may be split up in arbitrary chunks).  Entity references are
    passed by calling self.handle_entityref() with the entity
    reference as the argument.  Numeric character references are
    passed to self.handle_charref() with the string containing the
    reference as the argument.
    """
    CDATA_CONTENT_ELEMENTS = ('script', 'style')

    def __init__(self):
        """Initialize and reset this instance."""
        self.reset()

    def reset(self):
        """Reset this instance.  Loses all unprocessed data."""
        self.rawdata = ''
        self.lasttag = '???'
        self.interesting = interesting_normal
        markupbase.ParserBase.reset(self)

    def feed(self, data):
        """Feed data to the parser.

        Call this as often as you want, with as little or as much text
        as you want (may include '
').
        """
        self.rawdata = self.rawdata + data
        self.goahead(0)

    def close(self):
        """Handle any buffered data."""
        self.goahead(1)

    def error(self, message):
        raise HTMLParseError(message, self.getpos())

    __starttag_text = None

    def get_starttag_text(self):
        """Return full source of start tag: '<...>'."""
        return self.__starttag_text

    def set_cdata_mode(self):
        self.interesting = interesting_cdata

    def clear_cdata_mode(self):
        self.interesting = interesting_normal

    def goahead(self, end):
        rawdata = self.rawdata
        i = 0
        n = len(rawdata)
        while i < n:
            match = self.interesting.search(rawdata, i)
            if match:
                j = match.start()
            else:
                j = n
            if i < j:
                self.handle_data(rawdata[i:j])
            i = self.updatepos(i, j)
            if i == n:
                break
            startswith = rawdata.startswith
            if startswith('<', i):
                if starttagopen.match(rawdata, i):
                    k = self.parse_starttag(i)
                elif startswith('</', i):
                    k = self.parse_endtag(i)
                elif startswith('<!--', i):
                    k = self.parse_comment(i)
                elif startswith('<?', i):
                    k = self.parse_pi(i)
                elif startswith('<!', i):
                    k = self.parse_declaration(i)
                elif i + 1 < n:
                    self.handle_data('<')
                    k = i + 1
                else:
                    break
                if k < 0:
                    if end:
                        self.error('EOF in middle of construct')
                    break
                i = self.updatepos(i, k)
            elif startswith('&#', i):
                match = charref.match(rawdata, i)
                if match:
                    name = match.group()[2:-1]
                    self.handle_charref(name)
                    k = match.end()
                    if not startswith(';', k - 1):
                        k = k - 1
                    i = self.updatepos(i, k)
                    continue
                else:
                    if ';' in rawdata[i:]:
                        self.handle_data(rawdata[0:2])
                        i = self.updatepos(i, 2)
                    break
            elif startswith('&', i):
                match = entityref.match(rawdata, i)
                if match:
                    name = match.group(1)
                    self.handle_entityref(name)
                    k = match.end()
                    if not startswith(';', k - 1):
                        k = k - 1
                    i = self.updatepos(i, k)
                    continue
                match = incomplete.match(rawdata, i)
                if match:
                    if end and match.group() == rawdata[i:]:
                        self.error('EOF in middle of entity or char ref')
                    break
                elif i + 1 < n:
                    self.handle_data('&')
                    i = self.updatepos(i, i + 1)
                else:
                    break
            elif not 0:
                raise AssertionError, 'interesting.search() lied'

        if end and i < n:
            self.handle_data(rawdata[i:n])
            i = self.updatepos(i, n)
        self.rawdata = rawdata[i:]

    def parse_pi(self, i):
        rawdata = self.rawdata
        if not rawdata[i:i + 2] == '<?':
            raise AssertionError, 'unexpected call to parse_pi()'
            match = piclose.search(rawdata, i + 2)
            return match or -1
        j = match.start()
        self.handle_pi(rawdata[i + 2:j])
        j = match.end()
        return j

    def parse_starttag--- This code section failed: ---

 L. 228         0  LOAD_CONST               None
                3  LOAD_FAST             0  'self'
                6  STORE_ATTR            1  '__starttag_text'

 L. 229         9  LOAD_FAST             0  'self'
               12  LOAD_ATTR             2  'check_for_whole_start_tag'
               15  LOAD_FAST             1  'i'
               18  CALL_FUNCTION_1       1  None
               21  STORE_FAST            2  'endpos'

 L. 230        24  LOAD_FAST             2  'endpos'
               27  LOAD_CONST               0
               30  COMPARE_OP            0  <
               33  POP_JUMP_IF_FALSE    40  'to 40'

 L. 231        36  LOAD_FAST             2  'endpos'
               39  RETURN_END_IF    
             40_0  COME_FROM            33  '33'

 L. 232        40  LOAD_FAST             0  'self'
               43  LOAD_ATTR             3  'rawdata'
               46  STORE_FAST            3  'rawdata'

 L. 233        49  LOAD_FAST             3  'rawdata'
               52  LOAD_FAST             1  'i'
               55  LOAD_FAST             2  'endpos'
               58  SLICE+3          
               59  LOAD_FAST             0  'self'
               62  STORE_ATTR            1  '__starttag_text'

 L. 236        65  BUILD_LIST_0          0 
               68  STORE_FAST            4  'attrs'

 L. 237        71  LOAD_GLOBAL           4  'tagfind'
               74  LOAD_ATTR             5  'match'
               77  LOAD_FAST             3  'rawdata'
               80  LOAD_FAST             1  'i'
               83  LOAD_CONST               1
               86  BINARY_ADD       
               87  CALL_FUNCTION_2       2  None
               90  STORE_FAST            5  'match'

 L. 238        93  LOAD_FAST             5  'match'
               96  POP_JUMP_IF_TRUE    108  'to 108'
               99  LOAD_ASSERT              AssertionError
              102  LOAD_CONST               'unexpected call to parse_starttag()'
              105  RAISE_VARARGS_2       2  None

 L. 239       108  LOAD_FAST             5  'match'
              111  LOAD_ATTR             7  'end'
              114  CALL_FUNCTION_0       0  None
              117  STORE_FAST            6  'k'

 L. 240       120  LOAD_FAST             3  'rawdata'
              123  LOAD_FAST             1  'i'
              126  LOAD_CONST               1
              129  BINARY_ADD       
              130  LOAD_FAST             6  'k'
              133  SLICE+3          
              134  LOAD_ATTR             8  'lower'
              137  CALL_FUNCTION_0       0  None
              140  DUP_TOP          
              141  LOAD_FAST             0  'self'
              144  STORE_ATTR            9  'lasttag'
              147  STORE_FAST            7  'tag'

 L. 242       150  SETUP_LOOP          229  'to 382'
              153  LOAD_FAST             6  'k'
              156  LOAD_FAST             2  'endpos'
              159  COMPARE_OP            0  <
              162  POP_JUMP_IF_FALSE   381  'to 381'

 L. 243       165  LOAD_GLOBAL          10  'attrfind'
              168  LOAD_ATTR             5  'match'
              171  LOAD_FAST             3  'rawdata'
              174  LOAD_FAST             6  'k'
              177  CALL_FUNCTION_2       2  None
              180  STORE_FAST            8  'm'

 L. 244       183  LOAD_FAST             8  'm'
              186  POP_JUMP_IF_TRUE    193  'to 193'

 L. 245       189  BREAK_LOOP       
              190  JUMP_FORWARD          0  'to 193'
            193_0  COME_FROM           190  '190'

 L. 246       193  LOAD_FAST             8  'm'
              196  LOAD_ATTR            11  'group'
              199  LOAD_CONST               1
              202  LOAD_CONST               2
              205  LOAD_CONST               3
              208  CALL_FUNCTION_3       3  None
              211  UNPACK_SEQUENCE_3     3 
              214  STORE_FAST            9  'attrname'
              217  STORE_FAST           10  'rest'
              220  STORE_FAST           11  'attrvalue'

 L. 247       223  LOAD_FAST            10  'rest'
              226  POP_JUMP_IF_TRUE    238  'to 238'

 L. 248       229  LOAD_CONST               None
              232  STORE_FAST           11  'attrvalue'
              235  JUMP_FORWARD        103  'to 341'

 L. 249       238  LOAD_FAST            11  'attrvalue'
              241  LOAD_CONST               1
              244  SLICE+2          
              245  LOAD_CONST               "'"
              248  DUP_TOP          
              249  ROT_THREE        
              250  COMPARE_OP            2  ==
              253  JUMP_IF_FALSE_OR_POP   269  'to 269'
              256  LOAD_FAST            11  'attrvalue'
              259  LOAD_CONST               -1
              262  SLICE+1          
              263  COMPARE_OP            2  ==
              266  JUMP_FORWARD          2  'to 271'
            269_0  COME_FROM           253  '253'
              269  ROT_TWO          
              270  POP_TOP          
            271_0  COME_FROM           266  '266'
              271  POP_JUMP_IF_TRUE    310  'to 310'

 L. 250       274  LOAD_FAST            11  'attrvalue'
              277  LOAD_CONST               1
              280  SLICE+2          
              281  LOAD_CONST               '"'
              284  DUP_TOP          
              285  ROT_THREE        
              286  COMPARE_OP            2  ==
              289  JUMP_IF_FALSE_OR_POP   305  'to 305'
              292  LOAD_FAST            11  'attrvalue'
              295  LOAD_CONST               -1
              298  SLICE+1          
              299  COMPARE_OP            2  ==
              302  JUMP_FORWARD          2  'to 307'
            305_0  COME_FROM           289  '289'
              305  ROT_TWO          
              306  POP_TOP          
            307_0  COME_FROM           302  '302'
            307_1  COME_FROM           271  '271'
              307  POP_JUMP_IF_FALSE   341  'to 341'

 L. 251       310  LOAD_FAST            11  'attrvalue'
              313  LOAD_CONST               1
              316  LOAD_CONST               -1
              319  SLICE+3          
              320  STORE_FAST           11  'attrvalue'

 L. 252       323  LOAD_FAST             0  'self'
              326  LOAD_ATTR            12  'unescape'
              329  LOAD_FAST            11  'attrvalue'
              332  CALL_FUNCTION_1       1  None
              335  STORE_FAST           11  'attrvalue'
              338  JUMP_FORWARD          0  'to 341'
            341_0  COME_FROM           338  '338'
            341_1  COME_FROM           235  '235'

 L. 253       341  LOAD_FAST             4  'attrs'
              344  LOAD_ATTR            13  'append'
              347  LOAD_FAST             9  'attrname'
              350  LOAD_ATTR             8  'lower'
              353  CALL_FUNCTION_0       0  None
              356  LOAD_FAST            11  'attrvalue'
              359  BUILD_TUPLE_2         2 
              362  CALL_FUNCTION_1       1  None
              365  POP_TOP          

 L. 254       366  LOAD_FAST             8  'm'
              369  LOAD_ATTR             7  'end'
              372  CALL_FUNCTION_0       0  None
              375  STORE_FAST            6  'k'
              378  JUMP_BACK           153  'to 153'
              381  POP_BLOCK        
            382_0  COME_FROM           150  '150'

 L. 256       382  LOAD_FAST             3  'rawdata'
              385  LOAD_FAST             6  'k'
              388  LOAD_FAST             2  'endpos'
              391  SLICE+3          
              392  LOAD_ATTR            14  'strip'
              395  CALL_FUNCTION_0       0  None
              398  STORE_FAST           12  'end'

 L. 257       401  LOAD_FAST            12  'end'
              404  LOAD_CONST               ('>', '/>')
              407  COMPARE_OP            7  not-in
              410  POP_JUMP_IF_FALSE   555  'to 555'

 L. 258       413  LOAD_FAST             0  'self'
              416  LOAD_ATTR            15  'getpos'
              419  CALL_FUNCTION_0       0  None
              422  UNPACK_SEQUENCE_2     2 
              425  STORE_FAST           13  'lineno'
              428  STORE_FAST           14  'offset'

 L. 259       431  LOAD_CONST               '\n'
              434  LOAD_FAST             0  'self'
              437  LOAD_ATTR             1  '__starttag_text'
              440  COMPARE_OP            6  in
              443  POP_JUMP_IF_FALSE   502  'to 502'

 L. 260       446  LOAD_FAST            13  'lineno'
              449  LOAD_FAST             0  'self'
              452  LOAD_ATTR             1  '__starttag_text'
              455  LOAD_ATTR            16  'count'
              458  LOAD_CONST               '\n'
              461  CALL_FUNCTION_1       1  None
              464  BINARY_ADD       
              465  STORE_FAST           13  'lineno'

 L. 261       468  LOAD_GLOBAL          17  'len'
              471  LOAD_FAST             0  'self'
              474  LOAD_ATTR             1  '__starttag_text'
              477  CALL_FUNCTION_1       1  None

 L. 262       480  LOAD_FAST             0  'self'
              483  LOAD_ATTR             1  '__starttag_text'
              486  LOAD_ATTR            18  'rfind'
              489  LOAD_CONST               '\n'
              492  CALL_FUNCTION_1       1  None
              495  BINARY_SUBTRACT  
              496  STORE_FAST           14  'offset'
              499  JUMP_FORWARD         19  'to 521'

 L. 264       502  LOAD_FAST            14  'offset'
              505  LOAD_GLOBAL          17  'len'
              508  LOAD_FAST             0  'self'
              511  LOAD_ATTR             1  '__starttag_text'
              514  CALL_FUNCTION_1       1  None
              517  BINARY_ADD       
              518  STORE_FAST           14  'offset'
            521_0  COME_FROM           499  '499'

 L. 265       521  LOAD_FAST             0  'self'
              524  LOAD_ATTR            19  'error'
              527  LOAD_CONST               'junk characters in start tag: %r'

 L. 266       530  LOAD_FAST             3  'rawdata'
              533  LOAD_FAST             6  'k'
              536  LOAD_FAST             2  'endpos'
              539  SLICE+3          
              540  LOAD_CONST               20
              543  SLICE+2          
              544  BUILD_TUPLE_1         1 
              547  BINARY_MODULO    
              548  CALL_FUNCTION_1       1  None
              551  POP_TOP          
              552  JUMP_FORWARD          0  'to 555'
            555_0  COME_FROM           552  '552'

 L. 267       555  LOAD_FAST            12  'end'
              558  LOAD_ATTR            20  'endswith'
              561  LOAD_CONST               '/>'
              564  CALL_FUNCTION_1       1  None
              567  POP_JUMP_IF_FALSE   589  'to 589'

 L. 269       570  LOAD_FAST             0  'self'
              573  LOAD_ATTR            21  'handle_startendtag'
              576  LOAD_FAST             7  'tag'
              579  LOAD_FAST             4  'attrs'
              582  CALL_FUNCTION_2       2  None
              585  POP_TOP          
              586  JUMP_FORWARD         44  'to 633'

 L. 271       589  LOAD_FAST             0  'self'
              592  LOAD_ATTR            22  'handle_starttag'
              595  LOAD_FAST             7  'tag'
              598  LOAD_FAST             4  'attrs'
              601  CALL_FUNCTION_2       2  None
              604  POP_TOP          

 L. 272       605  LOAD_FAST             7  'tag'
              608  LOAD_FAST             0  'self'
              611  LOAD_ATTR            23  'CDATA_CONTENT_ELEMENTS'
              614  COMPARE_OP            6  in
              617  POP_JUMP_IF_FALSE   633  'to 633'

 L. 273       620  LOAD_FAST             0  'self'
              623  LOAD_ATTR            24  'set_cdata_mode'
              626  CALL_FUNCTION_0       0  None
              629  POP_TOP          
              630  JUMP_FORWARD          0  'to 633'
            633_0  COME_FROM           630  '630'
            633_1  COME_FROM           586  '586'

 L. 274       633  LOAD_FAST             2  'endpos'
              636  RETURN_VALUE     

Parse error at or near `LOAD_FAST' instruction at offset 633

    def check_for_whole_start_tag(self, i):
        rawdata = self.rawdata
        m = locatestarttagend.match(rawdata, i)
        if m:
            j = m.end()
            next = rawdata[j:j + 1]
            if next == '>':
                return j + 1
            if next == '/':
                if rawdata.startswith('/>', j):
                    return j + 2
                if rawdata.startswith('/', j):
                    return -1
                self.updatepos(i, j + 1)
                self.error('malformed empty start tag')
            if next == '':
                return -1
            if next in 'abcdefghijklmnopqrstuvwxyz=/ABCDEFGHIJKLMNOPQRSTUVWXYZ':
                return -1
            self.updatepos(i, j)
            self.error('malformed start tag')
        raise AssertionError('we should not get here!')

    def parse_endtag(self, i):
        rawdata = self.rawdata
        if not rawdata[i:i + 2] == '</':
            raise AssertionError, 'unexpected call to parse_endtag'
            match = endendtag.search(rawdata, i + 1)
            if not match:
                return -1
            j = match.end()
            match = endtagfind.match(rawdata, i)
            match or self.error('bad end tag: %r' % (rawdata[i:j],))
        tag = match.group(1)
        self.handle_endtag(tag.lower())
        self.clear_cdata_mode()
        return j

    def handle_startendtag(self, tag, attrs):
        self.handle_starttag(tag, attrs)
        self.handle_endtag(tag)

    def handle_starttag(self, tag, attrs):
        pass

    def handle_endtag(self, tag):
        pass

    def handle_charref(self, name):
        pass

    def handle_entityref(self, name):
        pass

    def handle_data(self, data):
        pass

    def handle_comment(self, data):
        pass

    def handle_decl(self, decl):
        pass

    def handle_pi(self, data):
        pass

    def unknown_decl(self, data):
        self.error('unknown declaration: %r' % (data,))

    entitydefs = None

    def unescape(self, s):
        if '&' not in s:
            return s

        def replaceEntities(s):
            s = s.groups()[0]
            if s[0] == '#':
                s = s[1:]
                if s[0] in ('x', 'X'):
                    c = int(s[1:], 16)
                else:
                    c = int(s)
                return unichr(c)
            else:
                import htmlentitydefs
                if HTMLParser.entitydefs is None:
                    entitydefs = HTMLParser.entitydefs = {'apos': "'"}
                    for k, v in htmlentitydefs.name2codepoint.iteritems():
                        entitydefs[k] = unichr(v)

                try:
                    return self.entitydefs[s]
                except KeyError:
                    return '&' + s + ';'

                return

        return re.sub('&(#?[xX]?(?:[0-9a-fA-F]+|\\w{1,8}));', replaceEntities, s)