# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: markupbase.pyc
# Compiled at: 2006-06-09 17:13:00
"""Shared support for scanning document type declarations in HTML and XHTML.

This module is used as a foundation for the HTMLParser and sgmllib
modules (indirectly, for htmllib as well).  It has no documented
public API and should not be used directly.

"""
import re
_declname_match = re.compile('[a-zA-Z][-_.a-zA-Z0-9]*\\s*').match
_declstringlit_match = re.compile('(\\\'[^\\\']*\\\'|"[^"]*")\\s*').match
_commentclose = re.compile('--\\s*>')
_markedsectionclose = re.compile(']\\s*]\\s*>')
_msmarkedsectionclose = re.compile(']\\s*>')
del re

class ParserBase:
    """Parser base class which provides some common support methods used
    by the SGML/HTML and XHTML parsers."""

    def __init__(self):
        if self.__class__ is ParserBase:
            raise RuntimeError('markupbase.ParserBase must be subclassed')

    def error(self, message):
        raise NotImplementedError('subclasses of ParserBase must override error()')

    def reset(self):
        self.lineno = 1
        self.offset = 0

    def getpos(self):
        """Return current line number and offset."""
        return (
         self.lineno, self.offset)

    def updatepos(self, i, j):
        if i >= j:
            return j
        rawdata = self.rawdata
        nlines = rawdata.count('\n', i, j)
        if nlines:
            self.lineno = self.lineno + nlines
            pos = rawdata.rindex('\n', i, j)
            self.offset = j - (pos + 1)
        else:
            self.offset = self.offset + j - i
        return j

    _decl_otherchars = ''

    def parse_declaration--- This code section failed: ---

 L.  76         0  LOAD_FAST             0  'self'
                3  LOAD_ATTR             0  'rawdata'
                6  STORE_FAST            2  'rawdata'

 L.  77         9  LOAD_FAST             1  'i'
               12  LOAD_CONST               2
               15  BINARY_ADD       
               16  STORE_FAST            3  'j'

 L.  78        19  LOAD_FAST             2  'rawdata'
               22  LOAD_FAST             1  'i'
               25  LOAD_FAST             3  'j'
               28  SLICE+3          
               29  LOAD_CONST               '<!'
               32  COMPARE_OP            2  ==
               35  POP_JUMP_IF_TRUE     47  'to 47'
               38  LOAD_ASSERT              AssertionError
               41  LOAD_CONST               'unexpected call to parse_declaration'
               44  RAISE_VARARGS_2       2  None

 L.  79        47  LOAD_FAST             2  'rawdata'
               50  LOAD_FAST             3  'j'
               53  LOAD_FAST             3  'j'
               56  LOAD_CONST               1
               59  BINARY_ADD       
               60  SLICE+3          
               61  LOAD_CONST               '>'
               64  COMPARE_OP            2  ==
               67  POP_JUMP_IF_FALSE    78  'to 78'

 L.  81        70  LOAD_FAST             3  'j'
               73  LOAD_CONST               1
               76  BINARY_ADD       
               77  RETURN_END_IF    
             78_0  COME_FROM            67  '67'

 L.  82        78  LOAD_FAST             2  'rawdata'
               81  LOAD_FAST             3  'j'
               84  LOAD_FAST             3  'j'
               87  LOAD_CONST               1
               90  BINARY_ADD       
               91  SLICE+3          
               92  LOAD_CONST               ('-', '')
               95  COMPARE_OP            6  in
               98  POP_JUMP_IF_FALSE   105  'to 105'

 L.  85       101  LOAD_CONST               -1
              104  RETURN_END_IF    
            105_0  COME_FROM            98  '98'

 L.  87       105  LOAD_GLOBAL           2  'len'
              108  LOAD_FAST             2  'rawdata'
              111  CALL_FUNCTION_1       1  None
              114  STORE_FAST            4  'n'

 L.  88       117  LOAD_FAST             2  'rawdata'
              120  LOAD_FAST             3  'j'
              123  LOAD_FAST             3  'j'
              126  LOAD_CONST               2
              129  BINARY_ADD       
              130  SLICE+3          
              131  LOAD_CONST               '--'
              134  COMPARE_OP            2  ==
              137  POP_JUMP_IF_FALSE   153  'to 153'

 L.  90       140  LOAD_FAST             0  'self'
              143  LOAD_ATTR             3  'parse_comment'
              146  LOAD_FAST             1  'i'
              149  CALL_FUNCTION_1       1  None
              152  RETURN_END_IF    
            153_0  COME_FROM           137  '137'

 L.  91       153  LOAD_FAST             2  'rawdata'
              156  LOAD_FAST             3  'j'
              159  BINARY_SUBSCR    
              160  LOAD_CONST               '['
              163  COMPARE_OP            2  ==
              166  POP_JUMP_IF_FALSE   182  'to 182'

 L.  96       169  LOAD_FAST             0  'self'
              172  LOAD_ATTR             4  'parse_marked_section'
              175  LOAD_FAST             1  'i'
              178  CALL_FUNCTION_1       1  None
              181  RETURN_END_IF    
            182_0  COME_FROM           166  '166'

 L.  98       182  LOAD_FAST             0  'self'
              185  LOAD_ATTR             5  '_scan_name'
              188  LOAD_FAST             3  'j'
              191  LOAD_FAST             1  'i'
              194  CALL_FUNCTION_2       2  None
              197  UNPACK_SEQUENCE_2     2 
              200  STORE_FAST            5  'decltype'
              203  STORE_FAST            3  'j'

 L.  99       206  LOAD_FAST             3  'j'
              209  LOAD_CONST               0
              212  COMPARE_OP            0  <
              215  POP_JUMP_IF_FALSE   222  'to 222'

 L. 100       218  LOAD_FAST             3  'j'
              221  RETURN_END_IF    
            222_0  COME_FROM           215  '215'

 L. 101       222  LOAD_FAST             5  'decltype'
              225  LOAD_CONST               'doctype'
              228  COMPARE_OP            2  ==
              231  POP_JUMP_IF_FALSE   246  'to 246'

 L. 102       234  LOAD_CONST               ''
              237  LOAD_FAST             0  'self'
              240  STORE_ATTR            6  '_decl_otherchars'
              243  JUMP_FORWARD          0  'to 246'
            246_0  COME_FROM           243  '243'

 L. 103       246  SETUP_LOOP          357  'to 606'
              249  LOAD_FAST             3  'j'
              252  LOAD_FAST             4  'n'
              255  COMPARE_OP            0  <
              258  POP_JUMP_IF_FALSE   605  'to 605'

 L. 104       261  LOAD_FAST             2  'rawdata'
              264  LOAD_FAST             3  'j'
              267  BINARY_SUBSCR    
              268  STORE_FAST            6  'c'

 L. 105       271  LOAD_FAST             6  'c'
              274  LOAD_CONST               '>'
              277  COMPARE_OP            2  ==
              280  POP_JUMP_IF_FALSE   349  'to 349'

 L. 107       283  LOAD_FAST             2  'rawdata'
              286  LOAD_FAST             1  'i'
              289  LOAD_CONST               2
              292  BINARY_ADD       
              293  LOAD_FAST             3  'j'
              296  SLICE+3          
              297  STORE_FAST            7  'data'

 L. 108       300  LOAD_FAST             5  'decltype'
              303  LOAD_CONST               'doctype'
              306  COMPARE_OP            2  ==
              309  POP_JUMP_IF_FALSE   328  'to 328'

 L. 109       312  LOAD_FAST             0  'self'
              315  LOAD_ATTR             7  'handle_decl'
              318  LOAD_FAST             7  'data'
              321  CALL_FUNCTION_1       1  None
              324  POP_TOP          
              325  JUMP_FORWARD         13  'to 341'

 L. 111       328  LOAD_FAST             0  'self'
              331  LOAD_ATTR             8  'unknown_decl'
              334  LOAD_FAST             7  'data'
              337  CALL_FUNCTION_1       1  None
              340  POP_TOP          
            341_0  COME_FROM           325  '325'

 L. 112       341  LOAD_FAST             3  'j'
              344  LOAD_CONST               1
              347  BINARY_ADD       
              348  RETURN_END_IF    
            349_0  COME_FROM           280  '280'

 L. 113       349  LOAD_FAST             6  'c'
              352  LOAD_CONST               '"\''
              355  COMPARE_OP            6  in
              358  POP_JUMP_IF_FALSE   401  'to 401'

 L. 114       361  LOAD_GLOBAL           9  '_declstringlit_match'
              364  LOAD_FAST             2  'rawdata'
              367  LOAD_FAST             3  'j'
              370  CALL_FUNCTION_2       2  None
              373  STORE_FAST            8  'm'

 L. 115       376  LOAD_FAST             8  'm'
              379  POP_JUMP_IF_TRUE    386  'to 386'

 L. 116       382  LOAD_CONST               -1
              385  RETURN_END_IF    
            386_0  COME_FROM           379  '379'

 L. 117       386  LOAD_FAST             8  'm'
              389  LOAD_ATTR            10  'end'
              392  CALL_FUNCTION_0       0  None
              395  STORE_FAST            3  'j'
              398  JUMP_FORWARD        185  'to 586'

 L. 118       401  LOAD_FAST             6  'c'
              404  LOAD_CONST               'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
              407  COMPARE_OP            6  in
              410  POP_JUMP_IF_FALSE   440  'to 440'

 L. 119       413  LOAD_FAST             0  'self'
              416  LOAD_ATTR             5  '_scan_name'
              419  LOAD_FAST             3  'j'
              422  LOAD_FAST             1  'i'
              425  CALL_FUNCTION_2       2  None
              428  UNPACK_SEQUENCE_2     2 
              431  STORE_FAST            9  'name'
              434  STORE_FAST            3  'j'
              437  JUMP_FORWARD        146  'to 586'

 L. 120       440  LOAD_FAST             6  'c'
              443  LOAD_FAST             0  'self'
              446  LOAD_ATTR             6  '_decl_otherchars'
              449  COMPARE_OP            6  in
              452  POP_JUMP_IF_FALSE   468  'to 468'

 L. 121       455  LOAD_FAST             3  'j'
              458  LOAD_CONST               1
              461  BINARY_ADD       
              462  STORE_FAST            3  'j'
              465  JUMP_FORWARD        118  'to 586'

 L. 122       468  LOAD_FAST             6  'c'
              471  LOAD_CONST               '['
              474  COMPARE_OP            2  ==
              477  POP_JUMP_IF_FALSE   565  'to 565'

 L. 124       480  LOAD_FAST             5  'decltype'
              483  LOAD_CONST               'doctype'
              486  COMPARE_OP            2  ==
              489  POP_JUMP_IF_FALSE   517  'to 517'

 L. 125       492  LOAD_FAST             0  'self'
              495  LOAD_ATTR            11  '_parse_doctype_subset'
              498  LOAD_FAST             3  'j'
              501  LOAD_CONST               1
              504  BINARY_ADD       
              505  LOAD_FAST             1  'i'
              508  CALL_FUNCTION_2       2  None
              511  STORE_FAST            3  'j'
              514  JUMP_ABSOLUTE       586  'to 586'

 L. 126       517  LOAD_FAST             5  'decltype'
              520  LOAD_CONST               ('attlist', 'linktype', 'link', 'element')
              523  COMPARE_OP            6  in
              526  POP_JUMP_IF_FALSE   549  'to 549'

 L. 131       529  LOAD_FAST             0  'self'
              532  LOAD_ATTR            12  'error'
              535  LOAD_CONST               "unsupported '[' char in %s declaration"
              538  LOAD_FAST             5  'decltype'
              541  BINARY_MODULO    
              542  CALL_FUNCTION_1       1  None
              545  POP_TOP          
              546  JUMP_ABSOLUTE       586  'to 586'

 L. 133       549  LOAD_FAST             0  'self'
              552  LOAD_ATTR            12  'error'
              555  LOAD_CONST               "unexpected '[' char in declaration"
              558  CALL_FUNCTION_1       1  None
              561  POP_TOP          
              562  JUMP_FORWARD         21  'to 586'

 L. 135       565  LOAD_FAST             0  'self'
              568  LOAD_ATTR            12  'error'

 L. 136       571  LOAD_CONST               'unexpected %r char in declaration'
              574  LOAD_FAST             2  'rawdata'
              577  LOAD_FAST             3  'j'
              580  BINARY_SUBSCR    
              581  BINARY_MODULO    
              582  CALL_FUNCTION_1       1  None
              585  POP_TOP          
            586_0  COME_FROM           562  '562'
            586_1  COME_FROM           465  '465'
            586_2  COME_FROM           437  '437'
            586_3  COME_FROM           398  '398'

 L. 137       586  LOAD_FAST             3  'j'
              589  LOAD_CONST               0
              592  COMPARE_OP            0  <
              595  POP_JUMP_IF_FALSE   249  'to 249'

 L. 138       598  LOAD_FAST             3  'j'
              601  RETURN_END_IF    
            602_0  COME_FROM           595  '595'
              602  JUMP_BACK           249  'to 249'
              605  POP_BLOCK        
            606_0  COME_FROM           246  '246'

 L. 139       606  LOAD_CONST               -1
              609  RETURN_VALUE     
               -1  RETURN_LAST      

Parse error at or near `RETURN_VALUE' instruction at offset 609

    def parse_marked_section(self, i, report=1):
        rawdata = self.rawdata
        if not rawdata[i:i + 3] == '<![':
            raise AssertionError, 'unexpected call to parse_marked_section()'
            sectName, j = self._scan_name(i + 3, i)
            if j < 0:
                return j
            if sectName in ('temp', 'cdata', 'ignore', 'include', 'rcdata'):
                match = _markedsectionclose.search(rawdata, i + 3)
            elif sectName in ('if', 'else', 'endif'):
                match = _msmarkedsectionclose.search(rawdata, i + 3)
            else:
                self.error('unknown status keyword %r in marked section' % rawdata[i + 3:j])
            return match or -1
        if report:
            j = match.start(0)
            self.unknown_decl(rawdata[i + 3:j])
        return match.end(0)

    def parse_comment(self, i, report=1):
        rawdata = self.rawdata
        if rawdata[i:i + 4] != '<!--':
            self.error('unexpected call to parse_comment()')
        match = _commentclose.search(rawdata, i + 4)
        if not match:
            return -1
        if report:
            j = match.start(0)
            self.handle_comment(rawdata[i + 4:j])
        return match.end(0)

    def _parse_doctype_subset(self, i, declstartpos):
        rawdata = self.rawdata
        n = len(rawdata)
        j = i
        while j < n:
            c = rawdata[j]
            if c == '<':
                s = rawdata[j:j + 2]
                if s == '<':
                    return -1
                if s != '<!':
                    self.updatepos(declstartpos, j + 1)
                    self.error('unexpected char in internal subset (in %r)' % s)
                if j + 2 == n:
                    return -1
                if j + 4 > n:
                    return -1
                if rawdata[j:j + 4] == '<!--':
                    j = self.parse_comment(j, report=0)
                    if j < 0:
                        return j
                    continue
                name, j = self._scan_name(j + 2, declstartpos)
                if j == -1:
                    return -1
                if name not in ('attlist', 'element', 'entity', 'notation'):
                    self.updatepos(declstartpos, j + 2)
                    self.error('unknown declaration %r in internal subset' % name)
                meth = getattr(self, '_parse_doctype_' + name)
                j = meth(j, declstartpos)
                if j < 0:
                    return j
            elif c == '%':
                if j + 1 == n:
                    return -1
                s, j = self._scan_name(j + 1, declstartpos)
                if j < 0:
                    return j
                if rawdata[j] == ';':
                    j = j + 1
            elif c == ']':
                j = j + 1
                while j < n and rawdata[j].isspace():
                    j = j + 1

                if j < n:
                    if rawdata[j] == '>':
                        return j
                    self.updatepos(declstartpos, j)
                    self.error('unexpected char after internal subset')
                else:
                    return -1
            elif c.isspace():
                j = j + 1
            else:
                self.updatepos(declstartpos, j)
                self.error('unexpected char %r in internal subset' % c)

        return -1

    def _parse_doctype_element(self, i, declstartpos):
        name, j = self._scan_name(i, declstartpos)
        if j == -1:
            return -1
        rawdata = self.rawdata
        if '>' in rawdata[j:]:
            return rawdata.find('>', j) + 1
        return -1

    def _parse_doctype_attlist(self, i, declstartpos):
        rawdata = self.rawdata
        name, j = self._scan_name(i, declstartpos)
        c = rawdata[j:j + 1]
        if c == '':
            return -1
        if c == '>':
            return j + 1
        while 1:
            name, j = self._scan_name(j, declstartpos)
            if j < 0:
                return j
            c = rawdata[j:j + 1]
            if c == '':
                return -1
            if c == '(':
                if ')' in rawdata[j:]:
                    j = rawdata.find(')', j) + 1
                else:
                    return -1
                while rawdata[j:j + 1].isspace():
                    j = j + 1

                if not rawdata[j:]:
                    return -1
            else:
                name, j = self._scan_name(j, declstartpos)
            c = rawdata[j:j + 1]
            if not c:
                return -1
            if c in '\'"':
                m = _declstringlit_match(rawdata, j)
                if m:
                    j = m.end()
                else:
                    return -1
                c = rawdata[j:j + 1]
                if not c:
                    return -1
            if c == '#':
                if rawdata[j:] == '#':
                    return -1
                name, j = self._scan_name(j + 1, declstartpos)
                if j < 0:
                    return j
                c = rawdata[j:j + 1]
                if not c:
                    return -1
            if c == '>':
                return j + 1

    def _parse_doctype_notation(self, i, declstartpos):
        name, j = self._scan_name(i, declstartpos)
        if j < 0:
            return j
        rawdata = self.rawdata
        while 1:
            c = rawdata[j:j + 1]
            if not c:
                return -1
            if c == '>':
                return j + 1
            if c in '\'"':
                m = _declstringlit_match(rawdata, j)
                if not m:
                    return -1
                j = m.end()
            else:
                name, j = self._scan_name(j, declstartpos)
                if j < 0:
                    return j

    def _parse_doctype_entity(self, i, declstartpos):
        rawdata = self.rawdata
        if rawdata[i:i + 1] == '%':
            j = i + 1
            while 1:
                c = rawdata[j:j + 1]
                if not c:
                    return -1
                if c.isspace():
                    j = j + 1
            else:
                break
                continue

        else:
            j = i
        name, j = self._scan_name(j, declstartpos)
        if j < 0:
            return j
        while 1:
            c = self.rawdata[j:j + 1]
            if not c:
                return -1
            if c in '\'"':
                m = _declstringlit_match(rawdata, j)
                if m:
                    j = m.end()
                else:
                    return -1
        else:
            if c == '>':
                return j + 1
            name, j = self._scan_name(j, declstartpos)
            if j < 0:
                return j

    def _scan_name(self, i, declstartpos):
        rawdata = self.rawdata
        n = len(rawdata)
        if i == n:
            return (None, -1)
        else:
            m = _declname_match(rawdata, i)
            if m:
                s = m.group()
                name = s.strip()
                if i + len(s) == n:
                    return (None, -1)
                return (name.lower(), m.end())
            self.updatepos(declstartpos, i)
            self.error('expected name token at %r' % rawdata[declstartpos:declstartpos + 20])
            return

    def unknown_decl(self, data):
        pass