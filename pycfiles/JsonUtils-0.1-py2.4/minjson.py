# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/jsonutils/minjson.py
# Compiled at: 2006-09-18 22:08:38
from re import compile, sub, search, DOTALL
alwaysStripWhiteSpace = False
badOperators = '*'
slashstarcomment = compile('/\\*.*?\\*/', DOTALL)
doubleslashcomment = compile('//.*\\n')

def _Read(aString):
    """Use eval in a 'safe' way to turn javascript expression into
           a python expression.  Allow only True, False, and None in global
           __builtins__, and since those map as true, false, null in
           javascript, pass those as locals
        """
    try:
        result = eval(aString, {'__builtins__': {'True': True, 'False': False, 'None': None}}, {'null': None, 'true': True, 'false': False})
    except NameError:
        raise ReadException, "Strings must be quoted. Could not read '%s'." % aString
    except SyntaxError:
        raise ReadException, "Syntax error.  Could not read '%s'." % aString

    return result


regexes = {}
for operator in badOperators:
    if operator in '+*':
        regexes[(operator, 'numeric operation')] = compile('\\d*\\s*\\%s|\\%s\\s*\\d*' % (operator, operator))
    else:
        regexes[(operator, 'numeric operation')] = compile('\\d*\\s*%s|%s\\s*\\d*' % (operator, operator))

def _getStringState(aSequence):
    """return the list of required quote closures if the end of aString needs them
    to close quotes.
    """
    state = []
    for k in aSequence:
        if k in ['"', "'"]:
            if state and k == state[(-1)]:
                state.pop()
            else:
                state.append(k)

    return state


def _sanityCheckMath(aString):
    """just need to check that, if there is a math operator in the
       client's JSON, it is inside a quoted string. This is mainly to
       keep client from successfully sending 'D0S'*9**9**9**9...
       Return True if OK, False otherwise
    """
    for operator in badOperators:
        if regexes[(operator, 'numeric operation')].search(aString) is not None:
            getlocs = regexes[(operator, 'numeric operation')].finditer(aString)
            locs = [ item.span() for item in getlocs ]
            halfStrLen = len(aString) / 2
            for loc in locs:
                exprStart = loc[0]
                exprEnd = loc[1]
                if exprStart <= halfStrLen:
                    teststr = aString[:exprStart]
                else:
                    teststr = list(aString[exprEnd + 1:])
                    teststr.reverse()
                if not _getStringState(teststr):
                    return False

    return True


def safeRead(aString):
    """turn the js into happier python and check for bad operations
       before sending it to the interpreter
    """
    CHR0 = chr(0)
    while aString.endswith(CHR0):
        aString = aString[:-1]

    aString = aString.strip()
    aString = slashstarcomment.sub('', aString)
    aString = doubleslashcomment.sub('', aString)
    if _sanityCheckMath(aString):
        return _Read(aString)
    else:
        raise ReadException, 'Unacceptable JSON expression: %s' % aString


read = safeRead
tfnTuple = (
 ('True', 'true'), ('False', 'false'), ('None', 'null'))

def _replaceTrueFalseNone(aString):
    """replace True, False, and None with javascript counterparts"""
    for k in tfnTuple:
        if k[0] in aString:
            aString = aString.replace(k[0], k[1])

    return aString


def _handleCode(subStr, stripWhiteSpace):
    """replace True, False, and None with javascript counterparts if
       appropriate, remove unicode u's, fix long L's, make tuples
       lists, and strip white space if requested
    """
    if 'e' in subStr:
        subStr = _replaceTrueFalseNone(subStr)
    if stripWhiteSpace:
        subStr = subStr.replace(' ', '')
    if subStr[(-1)] in 'uU':
        subStr = subStr[:-1]
    if 'L' in subStr:
        subStr = subStr.replace('L', '')
    if '(' in subStr:
        subStr = subStr.replace('(', '[')
    if ')' in subStr:
        subStr = subStr.replace(')', ']')
    return subStr


redoublequotedstring = compile('"[^"]*\\\'[^"]*"[,\\]\\}:\\)]')
escapedSingleQuote = "\\'"
escapedDoubleQuote = '\\"'

def doQuotesSwapping(aString):
    """rewrite doublequoted strings with single quotes as singlequoted strings with
    escaped single quotes"""
    s = []
    foundlocs = redoublequotedstring.finditer(aString)
    prevend = 0
    for loc in foundlocs:
        (start, end) = loc.span()
        s.append(aString[prevend:start])
        tempstr = aString[start:end]
        endchar = tempstr[(-1)]
        ts1 = tempstr[1:-2]
        ts1 = ts1.replace("'", escapedSingleQuote)
        ts1 = "'%s'%s" % (ts1, endchar)
        s.append(ts1)
        prevend = end

    s.append(aString[prevend:])
    return ('').join(s)


def _pyexpr2jsexpr(aString, stripWhiteSpace):
    """Take advantage of python's formatting of string representations of
    objects.  Python always uses "'" to delimit strings.  Except it doesn't when
    there is ' in the string.  Fix that, then, if we split
    on that delimiter, we have a list that alternates non-string text with
    string text.  Since string text is already properly escaped, we
    only need to replace True, False, and None in non-string text and
    remove any unicode 'u's preceding string values.

    if stripWhiteSpace is True, remove spaces, etc from the non-string
    text.
    """
    inSingleQuote = False
    inDoubleQuote = False
    if redoublequotedstring.search(aString):
        aString = doQuotesSwapping(aString)
    marker = None
    if escapedSingleQuote in aString:
        marker = markerBase = '|'
        markerCount = 1
        while marker in aString:
            markerCount += 1
            marker = markerBase * markerCount

        aString = aString.replace(escapedSingleQuote, marker)
    aString = aString.replace('"', escapedDoubleQuote)
    splitStr = aString.split("'")
    outList = []
    alt = True
    for subStr in splitStr:
        if alt:
            subStr = _handleCode(subStr, stripWhiteSpace)
        outList.append(subStr)
        alt = not alt

    result = ('"').join(outList)
    if marker:
        result = result.replace(marker, "'")
    return result


def write(obj, encoding='utf-8', stripWhiteSpace=alwaysStripWhiteSpace):
    """Represent the object as a string.  Do any necessary fix-ups
    with pyexpr2jsexpr"""
    try:
        aString = str(obj).encode(encoding)
    except UnicodeEncodeError:
        aString = obj.encode(encoding)

    if isinstance(obj, basestring):
        if '"' in aString:
            aString = aString.replace(escapedDoubleQuote, '"')
            result = '"%s"' % aString.replace('"', escapedDoubleQuote)
        else:
            result = '"%s"' % aString
    else:
        result = _pyexpr2jsexpr(aString, stripWhiteSpace).encode(encoding)
    return result


class ReadException(Exception):
    __module__ = __name__


class WriteException(Exception):
    __module__ = __name__