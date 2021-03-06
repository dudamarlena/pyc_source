# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/paste/webkit/FakeWebware/MiscUtils/DictForArgs.py
# Compiled at: 2006-10-22 17:01:01
"""
DictForArgs.py

See the doc string for the DictForArgs() function.

Also, there is a test suite in Testing/TestDictForArgs.py
"""
import re, string

class DictForArgsError(Exception):
    __module__ = __name__


def _SyntaxError(s):
    raise DictForArgsError, 'Syntax error: %s' % repr(s)


def DictForArgs(s):
    """
        Dictionary for arguments
        
        Takes an input such as::
        
                        x=3
                        name="foo"
                        first='john' last='doe'
                        required border=3

        And returns a dictionary representing the same. For keys that aren't
        given an explicit value (such as 'required' above), the value is '1'.

        All values are interpreted as strings. If you want ints and floats,
        you'll have to convert them yourself.

        This syntax is equivalent to what you find in HTML and close to other
        ML languages such as XML.

        Returns {} for an empty string.

        The informal grammar is::
        
                (NAME [=NAME|STRING])*

        Will raise DictForArgsError if the string is invalid.

        See also: PyDictForArgs() and ExpandDictWithExtras() in this module
        """
    s = string.strip(s)
    nameRE = re.compile('\\w+')
    equalsRE = re.compile('\\=')
    stringRE = re.compile('\n\t\t\t\t\t"[^"]+"|\n\t\t\t\t\t\'[^\']+\'|\n\t\t\t\t\t\\S+', re.VERBOSE)
    whiteRE = re.compile('\\s+')
    REs = [nameRE, equalsRE, stringRE, whiteRE]
    verbose = 0
    matches = []
    start = 0
    sLen = len(s)
    if verbose:
        print '>> DictForArgs(%s)' % repr(s)
        print '>> sLen:', sLen
    while start < sLen:
        for regEx in REs:
            if verbose:
                print '>> try:', regEx
            match = regEx.match(s, start)
            if verbose:
                print '>> match:', match
            if match is not None:
                if match.re is not whiteRE:
                    matches.append(match)
                start = match.end()
                if verbose:
                    print '>> new start:', start
                break
        else:
            _SyntaxError(s)

    if verbose:
        names = []
        for match in matches:
            if match.re is nameRE:
                name = 'name'
            elif match.re is equalsRE:
                name = 'equals'
            elif match.re is stringRE:
                name = 'string'
            elif match.re is whiteRE:
                name = 'white'
            names.append(name)

        print '>> names =', names
    dict = {}
    matchesLen = len(matches)
    i = 0
    while i < matchesLen:
        match = matches[i]
        if i + 1 < matchesLen:
            peekMatch = matches[(i + 1)]
        else:
            peekMatch = None
        if match.re is nameRE:
            if peekMatch is not None:
                if peekMatch.re is nameRE:
                    dict[match.group()] = '1'
                    i = i + 1
                    continue
                if peekMatch.re is equalsRE:
                    if i + 2 < matchesLen:
                        target = matches[(i + 2)]
                        if target.re is nameRE or target.re is stringRE:
                            value = target.group()
                            if value[0] == "'" or value[0] == '"':
                                value = value[1:-1]
                            dict[match.group()] = value
                            i = i + 3
                            continue
            else:
                dict[match.group()] = '1'
                i = i + 1
                continue
        _SyntaxError(s)

    if verbose:
        print
    return dict


from string import letters

def PyDictForArgs(s):
    """
        Takes an input such as:
                        x=3
                        name="foo"
                        first='john'; last='doe'
                        list=[1, 2, 3]; name='foo'

        And returns a dictionary representing the same.

        All values are interpreted as Python expressions. Any error in these
        expressions will raise the appropriate Python exception. This syntax
        allows much more power than DictForArgs() since you can include
        lists, dictionaries, actual ints and floats, etc.

        This could also open the door to hacking your software if the input
        comes from a tainted source such as an HTML form or an unprotected
        configuration file.

        Returns {} for an empty string.

        See also: DictForArgs() and ExpandDictWithExtras() in this module
        """
    if s:
        s = s.strip()
    if not s:
        return {}
    if s.find(' ') == -1 and s.find('=') == -1 and s[0] in letters:
        s += '=1'
    results = {}
    exec s in results
    del results['__builtins__']
    return results


def ExpandDictWithExtras(dict, key='Extras', delKey=1, dictForArgs=DictForArgs):
    """
        Returns a dictionary with the 'Extras' column expanded by DictForArgs().

        For example, given::

                { 'Name': 'foo', 'Extras': 'x=1 y=2' }
                
        The return value is::
        
                { 'Name': 'foo', 'x': '1', 'y': '2' }

        The key argument controls what key in the dictionary is used to hold the extra arguments. The delKey argument controls whether that key and its corresponding value are retained.

        The same dictionary may be returned if there is no extras key.

        The most typical use of this function is to pass a row from a DataTable that was initialized from a CSV file (e.g., a spreadsheet or tabular file). FormKit and MiddleKit both use CSV files and allow for an Extras column to specify attributes that occur infrequently.
        """
    if dict.has_key(key):
        newDict = {}
        for (k, v) in dict.items():
            newDict[k] = v

        if delKey:
            del newDict[key]
        newDict.update(dictForArgs(dict[key]))
        return newDict
    else:
        return dict