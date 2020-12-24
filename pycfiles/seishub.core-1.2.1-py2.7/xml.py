# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\seishub\core\util\xml.py
# Compiled at: 2010-12-23 17:42:44
import re

def toUnicode(data, remove_decl=False):
    """
    Detect the encoding of a XML string via BOM and XML declaration.
    
    Encoding detection works as follows:
        - if detection of the BOM succeeds, the codec name of the
        corresponding unicode charset is returned
        
        - if BOM detection fails, the xml declaration is searched for
        the encoding attribute and its value returned. the "<"
        character has to be the very first in the file then (it's xml
        standard after all).
        
        - if BOM and xml declaration fail, utf-8 is returned. According
        to xml 1.0 it should be utf_8 then, but it wasn't detected by
        the means offered here. at least one can be pretty sure that a
        character coding including most of ASCII is used :-/
    """
    data, enc = detectBOM(data)
    if not enc:
        data, enc = parseXMLDeclaration(data, remove_decl)
    elif remove_decl:
        data = unicode(data, enc)
        data, _ = parseXMLDeclaration(data, True)
    if not isinstance(data, unicode):
        data = unicode(data, enc)
    return (
     data, enc)


def parseXMLDeclaration(data, remove_decl=False):
    """
    Parse XML declaration and return (data, encoding). 
    
    If remove is True, data without the XML declaration is returned. 
    If no declaration can be found, (None, None) is returned.
    """
    xmlDeclPattern = '\n    ^<\\?xml\\s+          # w/o BOM, xmldecl starts with <?xml at the first byte\n        ([^>]*?         # some chars (version info), matched minimal\n    (encoding(\\s*)=(\\s*)# encoding attribute begins\n    ["\']                # attribute start delimiter\n    (?P<encstr>         # what\'s matched in the brackets will be named encstr\n     [^"\']+             # every character not delimiter (not overly exact!)\n    )                   # closes the brackets pair for the named group\n    ["\']))?             # attribute end delimiter\n    [^>]*               # some chars optionally (standalone decl or whitespace)\n    \\?>                 # xmldecl end\n    '
    xmlDeclRE = re.compile(xmlDeclPattern, re.VERBOSE)
    match = xmlDeclRE.search(data)
    enc = 'utf-8'
    if match:
        enc = match.group('encstr') or 'utf-8'
    if remove_decl:
        data = xmlDeclRE.sub('', data)
    return (data.strip(), enc.lower())


def detectBOM(data):
    """
    Attempts to detect the character encoding of the given XML string.
    
    @author: Lars Tiede
    @since: 2005/01/20
    @version: 1.1
    @see: U{http://aspn.activestate.com/ASPN/Cookbook/Python/Recipe/363841}
          U{http://www.w3.org/TR/2006/REC-xml-20060816/#sec-guessing}
    """
    bomDict = {(0, 0, 254, 255): 'utf-32be', 
       (255, 254, 0, 0): 'utf-32le', 
       (254, 255, None, None): 'utf-16be', 
       (255, 254, None, None): 'utf-16le', 
       (239, 187, 191, None): 'utf-8'}
    byte1, byte2, byte3, byte4 = tuple(map(ord, data[0:4]))
    bomDetection = bomDict.get((byte1, byte2, byte3, byte4))
    if not bomDetection:
        bomDetection = bomDict.get((byte1, byte2, byte3, None))
        if not bomDetection:
            bomDetection = bomDict.get((byte1, byte2, None, None))
            if bomDetection:
                data = data[2:]
        else:
            data = data[3:]
    else:
        data = data[4:]
    if bomDetection:
        return (data, bomDetection)
    else:
        return (
         data, None)


def addXMLDeclaration(data, encoding='UTF-8', version='1.0'):
    decl = '<?xml version="%s" encoding="%s"?>\n\n'
    return decl % (version, encoding) + data


def applyMacros(query):
    """
    Replaces defined macros within the given expression.
    
    Macros are defined by {kw=arg, kw2=args} at the beginning of the 
    expression. The macro section may not include one of the following chars:
    '=', '{', ',' or '}'. After the closing bracket you may define markers
    via {kw} which will be replaced with the defined argument in the macro 
    section.
    
        >>> applyMacro('{test=world, blub=!} hello {test}{blub}')
        'hello world!'
    """
    query = (' ').join(query.splitlines()).strip()
    if not query.startswith('{'):
        return query
    macros, query = query.split('}', 1)
    macros = macros.strip(' {}')
    for macro in macros.split(','):
        kw, arg = macro.split('=')
        query = query.replace('{' + kw.strip() + '}', arg.strip())

    return query.strip()