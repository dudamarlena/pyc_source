# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/qi/Goban/lib/sgflib.py
# Compiled at: 2008-04-06 04:02:05
"""
=============================================
 Smart Game Format Parser Library: sgflib.py
=============================================
version 1.0 (2000-03-27)

Homepage: [[http://gotools.sourceforge.net]]

Copyright (C) 2000 David John Goodger ([[mailto:dgoodger@bigfoot.com]]; davidg
on NNGS, IGS, goclub.org). sgflib.py comes with ABSOLUTELY NO WARRANTY. This is
free software, and you are welcome to redistribute it and/or modify it under the
terms of the GNU Lesser General Public License; see the source code for details.

Description
===========
This library contains a parser and classes for SGF, the Smart Game Format. SGF
is a text only, tree based file format designed to store game records of board
games for two players, most commonly for the game of go. (See the official SGF
specification at [[http://www.POBoxes.com/sgf/]]).

Given a string containing a complete SGF data instance, the 'SGFParser' class
will create a 'Collection' object consisting of one or more 'GameTree''s (one
'GameTree' per game in the SGF file), each containing a sequence of 'Node''s and
(potentially) two or more variation 'GameTree''s (branches). Each 'Node'
contains an ordered dictionary of 'Property' ID/value pairs (note that values
are lists, and can have multiple entries).

Tree traversal methods are provided through the 'Cursor' class.

The default representation (using 'str()' or 'print') of each class of SGF
objects is the Smart Game Format itself."""
import string, re
from typelib import List, Dictionary

class EndOfDataParseError(Exception):
    """ Raised by 'SGFParser.parseVariations()', 'SGFParser.parseNode()'."""
    __module__ = __name__


class GameTreeParseError(Exception):
    """ Raised by 'SGFParser.parseGameTree()'."""
    __module__ = __name__


class NodePropertyParseError(Exception):
    """ Raised by 'SGFParser.parseNode()'."""
    __module__ = __name__


class PropertyValueParseError(Exception):
    """ Raised by 'SGFParser.parsePropertyValue()'."""
    __module__ = __name__


class DirectAccessError(Exception):
    """ Raised by 'Node.__setitem__()', 'Node.update()'."""
    __module__ = __name__


class DuplicatePropertyError(Exception):
    """ Raised by 'Node.addProperty()'."""
    __module__ = __name__


class GameTreeNavigationError(Exception):
    """ Raised by 'Cursor.next()'."""
    __module__ = __name__


class GameTreeEndError(Exception):
    """ Raised by 'Cursor.next()', 'Cursor.previous()'."""
    __module__ = __name__


INT_TYPE = type(0)
MAX_LINE_LEN = 76

class SGFParser:
    """
        Parser for SGF data. Creates a tree structure based on the SGF standard
        itself. 'SGFParser.parse()' will return a 'Collection' object for the entire
        data.

        Instance Attributes:
        - self.data : string -- The complete SGF data instance.
        - self.datalen : integer -- Length of 'self.data'.
        - self.index : integer -- Current parsing position in 'self.data'.

        Class Attributes:
        - re* : re.RegexObject -- Regular expression text matching patterns.
        - ctrltrans: string[256] -- Control character translation table for
          string.translate(), used to remove all control characters from Property
          values. May be overridden (preferably in instances)."""
    __module__ = __name__
    reGameTreeStart = re.compile('\\s*\\(')
    reGameTreeEnd = re.compile('\\s*\\)')
    reGameTreeNext = re.compile('\\s*(;|\\(|\\))')
    reNodeContents = re.compile('\\s*([A-Za-z]+(?=\\s*\\[))')
    rePropertyStart = re.compile('\\s*\\[')
    rePropertyEnd = re.compile('\\]')
    reEscape = re.compile('\\\\')
    reLineBreak = re.compile('\\r\\n?|\\n\\r?')
    ctrltrans = string.maketrans('\x00\x01\x02\x03\x04\x05\x06\x07' + '\x08\t\x0b\x0c\x0e\x0f\x10\x11\x12\x13\x14\x15\x16\x17' + '\x18\x19\x1a\x1b\x1c\x1d\x1e\x1f', ' ' * 30)

    def __init__(self, data):
        """ Initialize the instance attributes. See the class itself for info."""
        self.data = data
        self.datalen = len(data)
        self.index = 0

    def parse(self):
        """ Parses the SGF data stored in 'self.data', and returns a 'Collection'."""
        c = Collection()
        while self.index < self.datalen:
            g = self.parseOneGame()
            if g:
                c.append(g)
            else:
                break

        return c

    def parseOneGame(self):
        """ Parses one game from 'self.data'. Returns a 'GameTree' containing
                        one game, or 'None' if the end of 'self.data' has been reached."""
        if self.index < self.datalen:
            match = self.reGameTreeStart.match(self.data, self.index)
            if match:
                self.index = match.end()
                return self.parseGameTree()
        return

    def parseGameTree(self):
        """ Called when "(" encountered, ends when a matching ")" encountered.
                        Parses and returns one 'GameTree' from 'self.data'. Raises
                        'GameTreeParseError' if a problem is encountered."""
        g = GameTree()
        while self.index < self.datalen:
            match = self.reGameTreeNext.match(self.data, self.index)
            if match:
                self.index = match.end()
                if match.group(1) == ';':
                    if g.variations:
                        raise GameTreeParseError('A node was encountered after a variation.')
                    g.append(g.makeNode(self.parseNode()))
                elif match.group(1) == '(':
                    g.variations = self.parseVariations()
                else:
                    return g
            else:
                raise GameTreeParseError

        return g

    def parseVariations(self):
        """ Called when "(" encountered inside a 'GameTree', ends when a
                        non-matching ")" encountered. Returns a list of variation
                        'GameTree''s. Raises 'EndOfDataParseError' if the end of 'self.data'
                        is reached before the end of the enclosing 'GameTree'."""
        v = []
        while self.index < self.datalen:
            match = self.reGameTreeEnd.match(self.data, self.index)
            if match:
                return v
            g = self.parseGameTree()
            if g:
                v.append(g)
            match = self.reGameTreeStart.match(self.data, self.index)
            if match:
                self.index = match.end()

        raise EndOfDataParseError

    def parseNode(self):
        """ Called when ";" encountered (& is consumed). Parses and returns one
                        'Node', which can be empty. Raises 'NodePropertyParseError' if no
                        property values are extracted. Raises 'EndOfDataParseError' if the
                        end of 'self.data' is reached before the end of the node (i.e., the
                        start of the next node, the start of a variation, or the end of the
                        enclosing game tree)."""
        n = Node()
        while self.index < self.datalen:
            match = self.reNodeContents.match(self.data, self.index)
            if match:
                self.index = match.end()
                pvlist = self.parsePropertyValue()
                if pvlist:
                    n.addProperty(n.makeProperty(match.group(1), pvlist))
                else:
                    raise NodePropertyParseError
            else:
                return n

        raise EndOfDataParseError

    def parsePropertyValue(self):
        """ Called when "[" encountered (but not consumed), ends when the next
                        property, node, or variation encountered. Parses and returns a list
                        of property values. Raises 'PropertyValueParseError' if there is a
                        problem."""
        pvlist = []
        while self.index < self.datalen:
            match = self.rePropertyStart.match(self.data, self.index)
            if match:
                self.index = match.end()
                v = ''
                mend = self.rePropertyEnd.search(self.data, self.index)
                mesc = self.reEscape.search(self.data, self.index)
                while mesc and mend and mesc.end() < mend.end():
                    v = v + self.data[self.index:mesc.start()]
                    mbreak = self.reLineBreak.match(self.data, mesc.end())
                    if mbreak:
                        self.index = mbreak.end()
                    else:
                        v = v + self.data[mesc.end()]
                        self.index = mesc.end() + 1
                    mend = self.rePropertyEnd.search(self.data, self.index)
                    mesc = self.reEscape.search(self.data, self.index)

                if mend:
                    v = v + self.data[self.index:mend.start()]
                    self.index = mend.end()
                    pvlist.append(self._convertControlChars(v))
                else:
                    raise PropertyValueParseError
            else:
                break

        if len(pvlist) >= 1:
            return pvlist
        else:
            raise PropertyValueParseError

    def _convertControlChars(self, text):
        """ Converts control characters in 'text' to spaces, using the
                        'self.ctrltrans' translation table. Override for variant
                        behaviour."""
        return string.translate(text, self.ctrltrans)


class RootNodeSGFParser(SGFParser):
    """ For parsing only the first 'GameTree''s root Node of an SGF file."""
    __module__ = __name__

    def parseNode(self):
        """ Calls 'SGFParser.parseNode()', sets 'self.index' to point to the end
                        of the data (effectively ending the 'GameTree' and 'Collection'),
                        and returns the single (root) 'Node' parsed."""
        n = SGFParser.parseNode(self)
        self.index = self.datalen
        return n


class Collection(List):
    """
        An SGF collection: multiple 'GameTree''s. Instance atributes:
        - self[.data] : list of 'GameTree' -- One 'GameTree' per game."""
    __module__ = __name__

    def __str__(self):
        """ SGF representation. Separates game trees with a blank line."""
        return string.join(map(str, self.data), '\n' * 2)

    def cursor(self, gamenum=0):
        """ Returns a 'Cursor' object for navigation of the given 'GameTree'."""
        return Cursor(self[gamenum])


class GameTree(List):
    """
        An SGF game tree: a game or variation. Instance attributes:
        - self[.data] : list of 'Node' -- game tree 'trunk'.
        - self.variations : list of 'GameTree' -- 0 or 2+ variations.
          'self.variations[0]' contains the main branch (sequence actually played)."""
    __module__ = __name__

    def __init__(self, nodelist=None, variations=None):
        """
                        Initialize the 'GameTree'. Arguments:
                        - nodelist : 'GameTree' or list of 'Node' -- Stored in 'self.data'.
                        - variations : list of 'GameTree' -- Stored in 'self.variations'."""
        List.__init__(self, nodelist)
        self.variations = variations or []

    def __str__(self):
        """ SGF representation, with proper line breaks between nodes."""
        if len(self):
            s = '(' + str(self[0])
            l = len(string.split(s, '\n')[(-1)])
            for n in map(str, self[1:]):
                if l + len(string.split(n, '\n')[0]) > MAX_LINE_LEN:
                    s = s + '\n'
                    l = 0
                s = s + n
                l = len(string.split(s, '\n')[(-1)])

            return s + string.join(map(str, [''] + self.variations), '\n') + ')'
        else:
            return ''

    def mainline(self):
        """ Returns the main line of the game (variation A) as a 'GameTree'."""
        if self.variations:
            return GameTree(self.data + self.variations[0].mainline())
        else:
            return self

    def makeNode(self, plist):
        """
                        Create a new 'Node' containing the properties contained in 'plist'.
                        Override/extend to create 'Node' subclass instances (move, setup).
                        Argument:
                        - plist : 'Node' or list of 'Property'"""
        return Node(plist)

    def cursor(self):
        """ Returns a 'Cursor' object for navigation of this 'GameTree'."""
        return Cursor(self)

    def propertySearch(self, pid, getall=0):
        """
                        Searches this 'GameTree' for nodes containing matching properties.
                        Returns a 'GameTree' containing the matched node(s). Arguments:
                        - pid : string -- ID of properties to search for.
                        - getall : boolean -- Set to true (1) to return all 'Node''s that
                          match, or to false (0) to return only the first match."""
        matches = []
        for n in self:
            if n.has_key(pid):
                matches.append(n)
                if not getall:
                    break
        else:
            for v in self.variations:
                matches = matches + v.propertySearch(pid, getall)
                if not getall and matches:
                    break

        return GameTree(matches)


class Node(Dictionary):
    """
        An SGF node. Instance Attributes:
        - self[.data] : ordered dictionary -- '{Property.id:Property}' mapping.
          (Ordered dictionary: allows offset-indexed retrieval). Properties *must*
          be added using 'self.addProperty()'.

        Example: Let 'n' be a 'Node' parsed from ';B[aa]BL[250]C[comment]':
        - 'str(n["BL"])'  =>  '"BL[250]"'
        - 'str(n[0])'     =>  '"B[aa]"'
        - 'map(str, n)'   =>  '["B[aa]","BL[250]","C[comment]"]'"""
    __module__ = __name__

    def __init__(self, plist=[]):
        """
                        Initializer. Argument:
                        - plist: Node or list of 'Property'."""
        Dictionary.__init__(self)
        self.order = []
        for p in plist:
            self.addProperty(p)

    def __getitem__(self, key):
        """ On 'self[key]', 'x in self', 'for x in self'. Implements all
                        indexing-related operations. Allows both key- and offset-indexed
                        retrieval. Membership and iteration ('in', 'for') repeatedly index
                        from 0 until 'IndexError'."""
        if type(key) is INT_TYPE:
            return self.order[key]
        else:
            return self.data[key]

    def __setitem__(self, key, x):
        """ On 'self[key]=x'. Allows assignment to existing items only. Raises 
                        'DirectAccessError' on new item assignment."""
        if self.has_key(key):
            self.order[self.order.index(self[key])] = x
            Dictionary.__setitem__(self, key, x)
        else:
            raise DirectAccessError('Properties may not be added directly; use addProperty() instead.')

    def __delitem__(self, key):
        """ On 'del self[key]'. Updates 'self.order' to maintain consistency."""
        self.order.remove(self[key])
        Dictionary.__delitem__(self, key)

    def __getslice__(self, low, high):
        """ On 'self[low:high]'."""
        return self.order[low:high]

    def __str__(self):
        """ SGF representation, with proper line breaks between properties."""
        if len(self):
            s = ';' + str(self[0])
            l = len(string.split(s, '\n')[(-1)])
            for p in map(str, self[1:]):
                if l + len(string.split(p, '\n')[0]) > MAX_LINE_LEN:
                    s = s + '\n'
                    l = 0
                s = s + p
                l = len(string.split(s, '\n')[(-1)])

            return s
        else:
            return ';'

    def update(self, dict):
        """ 'Dictionary' method not applicable to 'Node'. Raises 
                        'DirectAccessError'."""
        raise DirectAccessError('The update() method is not supported by Node; use addProperty() instead.')

    def addProperty(self, property):
        """
                        Adds a 'Property' to this 'Node'. Checks for duplicate properties
                        (illegal), and maintains the property order. Argument:
                        - property : 'Property'"""
        if self.has_key(property.id):
            raise DuplicatePropertyError
        else:
            self.data[property.id] = property
            self.order.append(property)

    def makeProperty(self, id, valuelist):
        """
                        Create a new 'Property'. Override/extend to create 'Property'
                        subclass instances (move, setup, game-info, etc.). Arguments:
                        - id : string
                        - valuelist : 'Property' or list of values"""
        return Property(id, valuelist)


class Property(List):
    """
        An SGF property: a set of label and value(s). Instance attributes:
        - self[.data] : list -- property values.
        - self.id : string -- SGF standard property label.
        - self.name : string -- actual label used in the SGF data. For example, the
          property 'CoPyright[...]' has name 'CoPyright' and id 'CP'."""
    __module__ = __name__

    def __init__(self, id, values, name=None):
        """
                        Initialize the 'Property'. Arguments:
                        - id : string
                        - name : string (optional) -- If not given, 'self.name' 
                        - nodelist : 'GameTree' or list of 'Node' -- Stored in 'self.data'.
                        - variations : list of 'GameTree' -- Stored in 'self.variations'."""
        List.__init__(self, values)
        self.id = id
        self.name = name or id

    def __str__(self):
        return self.name + '[' + string.join(map(_escapeText, self), '][') + ']'

    def propValue(self):
        return string.join(map(_escapeText, self), '][')


class Cursor:
    """
        'GameTree' navigation tool. Instance attributes:
        - self.game : 'GameTree' -- The root 'GameTree'.
        - self.gametree : 'GameTree' -- The current 'GameTree'.
        - self.node : 'Node' -- The current Node.
        - self.nodenum : integer -- The offset of 'self.node' from the root of
          'self.game'. The nodenum of the root node is 0.
        - self.index : integer -- The offset of 'self.node' within 'self.gametree'.
        - self.stack : list of 'GameTree' -- A record of 'GameTree''s traversed.
        - self.children : list of 'Node' -- All child nodes of the current node.
        - self.atEnd : boolean -- Flags if we are at the end of a branch.
        - self.atStart : boolean -- Flags if we are at the start of the game."""
    __module__ = __name__

    def __init__(self, gametree):
        """ Initialize root 'GameTree' and instance variables."""
        self.game = gametree
        self.reset()

    def reset(self):
        """ Set 'Cursor' to point to the start of the root 'GameTree', 'self.game'."""
        self.gametree = self.game
        self.nodenum = 0
        self.index = 0
        self.stack = []
        self.node = self.gametree[self.index]
        self._setChildren()
        self._setFlags()

    def next(self, varnum=0):
        """
                        Moves the 'Cursor' to & returns the next 'Node'. Raises
                        'GameTreeEndError' if the end of a branch is exceeded. Raises
                        'GameTreeNavigationError' if a non-existent variation is accessed.
                        Argument:
                        - varnum : integer, default 0 -- Variation number. Non-zero only
                          valid at a branching, where variations exist."""
        if self.index + 1 < len(self.gametree):
            if varnum != 0:
                raise GameTreeNavigationError('Nonexistent variation.')
            self.index = self.index + 1
        elif self.gametree.variations:
            if varnum < len(self.gametree.variations):
                self.stack.append(self.gametree)
                self.gametree = self.gametree.variations[varnum]
                self.index = 0
            else:
                raise GameTreeNavigationError('Nonexistent variation.')
        else:
            raise GameTreeEndError
        self.node = self.gametree[self.index]
        self.nodenum = self.nodenum + 1
        self._setChildren()
        self._setFlags()
        return self.node

    def previous(self):
        """ Moves the 'Cursor' to & returns the previous 'Node'. Raises
                        'GameTreeEndError' if the start of a branch is exceeded."""
        if self.index - 1 >= 0:
            self.index = self.index - 1
        elif self.stack:
            self.gametree = self.stack.pop()
            self.index = len(self.gametree) - 1
        else:
            raise GameTreeEndError
        self.node = self.gametree[self.index]
        self.nodenum = self.nodenum - 1
        self._setChildren()
        self._setFlags()
        return self.node

    def _setChildren(self):
        """ Sets up 'self.children'."""
        if self.index + 1 < len(self.gametree):
            self.children = [
             self.gametree[(self.index + 1)]]
        else:
            self.children = map(lambda list: list[0], self.gametree.variations)

    def _setFlags(self):
        """ Sets up the flags 'self.atEnd' and 'self.atStart'."""
        self.atEnd = not self.gametree.variations and self.index + 1 == len(self.gametree)
        self.atStart = not self.stack and self.index == 0


reCharsToEscape = re.compile('\\]|\\\\')

def _escapeText(text):
    """ Adds backslash-escapes to property value characters that need them."""
    output = ''
    index = 0
    match = reCharsToEscape.search(text, index)
    while match:
        output = output + text[index:match.start()] + '\\' + text[match.start()]
        index = match.end()
        match = reCharsToEscape.search(text, index)

    output = output + text[index:]
    return output


def selfTest1(onConsole=0):
    """ Canned data test case"""
    sgfdata = '  \t (;GM [1]US[someone]CoPyright[\\\n  Permission to reproduce this game is given.]GN[a-b]EV[None]RE[B+Resign]\nPW[a]WR[2k*]PB[b]BR[4k*]PC[somewhere]DT[2000-01-16]SZ[19]TM[300]KM[4.5]\nHA[3]AB[pd][dp][dd];W[pp];B[nq];W[oq]C[ x started observation.\n](;B[qc]C[ [b\\]: \\\\ hi x! ;-) \\\\];W[kc])(;B[hc];W[oe]))   '
    print '\n\n********** Self-Test 1 **********\n'
    print 'Input data:\n'
    print sgfdata
    print '\n\nParsed data: '
    col = SGFParser(sgfdata).parse()
    print 'done\n'
    cstr = str(col)
    print cstr, '\n'
    print 'Mainline:\n'
    m = col[0].mainline()
    print m, '\n'
    print 'Tree traversal (forward):\n'
    c = col.cursor()
    while 1:
        print 'nodenum: %s; index: %s; children: %s; node: %s' % (c.nodenum, c.index, len(c.children), c.node)
        if c.atEnd:
            break
        c.next()

    print '\nTree traversal (backward):\n'
    while 1:
        print 'nodenum: %s; index: %s; children: %s; node: %s' % (c.nodenum, c.index, len(c.children), c.node)
        if c.atStart:
            break
        c.previous()

    print "\nSearch for property 'B':"
    print col[0].propertySearch('B', 1)
    print "\nSearch for property 'C':"
    print col[0].propertySearch('C', 1)


def selfTest2(onConsole=0):
    """ Macintosh-based SGF file test"""
    import macfs
    print '\n\n********** Self-Test 2 (Mac) **********\n'
    thefile = macfs.PromptGetFile('Please choose an SGF file:')
    if not thefile[1]:
        return
    srcpath = thefile[0].as_pathname()
    src = open(srcpath, 'r')
    sgfdata = src.read()
    print 'Input data:\n'
    print sgfdata
    print '\n\nParsed data:'
    col = SGFParser(sgfdata).parse()
    print 'done\n'
    print str(col)


if __name__ == '__main__':
    print __doc__
    selfTest1()
    import os
    if os.name == 'mac':
        selfTest2()