# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/webias/gnosis/xml/xmlmap.py
# Compiled at: 2015-04-13 16:10:50
__all__ = [
 'usplit', 'is_legal_xml', 'is_legal_xml_char']
import re
try:
    a = True
except:
    True = 1
    False = 0

def usplit(uval):
    r"""
    Split Unicode string into a sequence of characters.
    \U sequences are considered to be a single character.

    You should assume you will get a sequence, and not assume
    anything about the type of sequence (i.e. list vs. tuple vs. string).
    """
    clist = []
    i = 0
    while i < len(uval):
        if len(uval[i:]) > 1 and uval[i] >= unichr(55296) and uval[i] <= unichr(56319) and uval[(i + 1)] >= unichr(56320) and uval[(i + 1)] <= unichr(57343):
            clist.append(uval[i:i + 2])
            i += 2
        else:
            clist.append(uval[i])
            i += 1

    return clist


def make_illegal_xml_regex():
    r"""        
    I want to define a regexp to match *illegal* characters.
    That way, I can do "re.search()" to find a single character,
    instead of "re.match()" to match the entire string. [Based on
    my assumption that .search() would be faster in this case.]

    Here is a verbose map of the XML character space (as defined
    in section 2.2 of the XML specification):
    
         u0000 - u0008             = Illegal
         u0009 - u000A             = Legal
         u000B - u000C             = Illegal
         u000D                             = Legal
         u000E - u0019             = Illegal
         u0020 - uD7FF             = Legal
         uD800 - uDFFF             = Illegal (See note!)
         uE000 - uFFFD             = Legal
         uFFFE - uFFFF             = Illegal
         U00010000 - U0010FFFF = Legal (See note!)
    
    Note:
    
       The range U00010000 - U0010FFFF is coded as 2-character sequences
       using the codes (D800-DBFF),(DC00-DFFF), which are both illegal
       when used as single chars, from above.
    
       Python won't let you define \U character ranges, so you can't
       just say '\U00010000-\U0010FFFF'. However, you can take advantage
       of the fact that (D800-DBFF) and (DC00-DFFF) are illegal, unless
       part of a 2-character sequence, to match for the \U characters.
    """
    re_xml_illegal = '([\x00-\x08\x0b-\x0c\x0e-\x19\ufffe-\uffff])'
    re_xml_illegal += '|'
    re_xml_illegal += '([%s-%s][^%s-%s])|([^%s-%s][%s-%s])|([%s-%s]$)|(^[%s-%s])' % (
     unichr(55296), unichr(56319), unichr(56320), unichr(57343),
     unichr(55296), unichr(56319), unichr(56320), unichr(57343),
     unichr(55296), unichr(56319), unichr(56320), unichr(57343))
    return re.compile(re_xml_illegal)


c_re_xml_illegal = make_illegal_xml_regex()

def is_legal_xml(uval):
    """
    Given a Unicode object, figure out if it is legal
    to place it in an XML file.
    """
    return c_re_xml_illegal.search(uval) == None


def is_legal_xml_char(uchar):
    r"""
    Check if a single unicode char is XML-legal.
    (This is faster that running the full 'is_legal_xml()' regexp
    when you need to go character-at-a-time. For string-at-a-time
    of course you want to use is_legal_xml().)

    USAGE NOTE:
       If you want to use this in a 'for' loop,
       make sure use usplit(), e.g.:
          
       for c in usplit( uval ):
          if is_legal_xml_char(c):
                 ... 

       Otherwise, the first char of a legal 2-character
       sequence will be incorrectly tagged as illegal, on
       Pythons where \U is stored as 2-chars.
    """
    if len(uchar) == 1:
        return not (uchar >= '\x00' and uchar <= '\x08' or uchar >= '\x0b' and uchar <= '\x0c' or uchar >= '\x0e' and uchar <= '\x19' or uchar >= unichr(55296) and uchar <= unichr(57343) or uchar >= '\ufffe' and uchar <= '\uffff')
    if len(uchar) == 2:
        return True
    raise Exception('Must pass a single character to is_legal_xml_char')