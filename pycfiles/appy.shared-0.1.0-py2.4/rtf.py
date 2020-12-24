# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/appy/shared/rtf.py
# Compiled at: 2008-02-21 11:38:58
"""RTF table parser.

  This parser reads RTF documents that conform to the following.
   - Each table must have a first row with only one cell: the table name.
   - The other rows must all have the same number of columns. This number must
     be strictly greater than 1."""
import re, sys, UserList, UserDict
from StringIO import StringIO

class ParserError(Exception):
    __module__ = __name__


class TypeError(Exception):
    __module__ = __name__


BAD_PARENT_ROW = 'For table "%s", you specified "%s" as parent table, but you referred to row number "%s" within the parent. This value must be a positive integer or zero (we start counting rows at 0).'
PARENT_NOT_FOUND = 'I cannot find table "%s" that you defined as being parent of "%s".'
TABLE_KEY_ERROR = 'Within a row of table "%s", you mention a column named "%s" which does not exist neither in "%s" itself, neither in its parent row(s). '
PARENT_ROW_NOT_FOUND = 'You specified table "%s" as inheriting from table "%s", row "%d", but this row does not exist (table "%s" as a length = %d). Note that we start counting rows at 0.'
PARENT_COLUMN_NOT_FOUND = 'You specified table "%s" as inheriting from table "%s", column "%s", but this column does not exist in table "%s" or parents.'
PARENT_ROW_COL_NOT_FOUND = 'You specified table "%s" as inheriting from table "%s", column "%s", value "%s", but it does not correspond to any row in table "%s".'
NO_ROWS_IN_TABLE_YET = 'In first row of table "%s", you use value \' " \' for referencing the cell value in previous row, which does not exist.'
VALUE_ERROR = 'Value error for column "%s" of table "%s". %s'
TYPE_ERROR = 'Type error for column "%s" of table "%s". %s'
LIST_TYPE_ERROR = 'Maximum number of nested lists is 4.'
BASIC_TYPE_ERROR = 'Letter "%s" does not correspond to any valid type. Valid types are f (float), i (int), g (long) and b (bool).'
BASIC_VALUE_ERROR = 'Value "%s" can\'t be converted to type "%s".'
LIST_VALUE_ERROR = 'Value "%s" is malformed: within it, %s. You should check the use of separators ( , : ; - ) to obtain a schema conform to the type "%s"'

class Type:
    __module__ = __name__
    basicTypes = {'f': float, 'i': int, 'g': long, 'b': bool}
    separators = ['-', ';', ',', ':']

    def __init__(self, typeDecl):
        self.basicType = None
        self.listNumber = 0
        self.analyseTypeDecl(typeDecl)
        if self.listNumber > 4:
            raise TypeError(LIST_TYPE_ERROR)
        self.name = self.computeName()
        return

    def analyseTypeDecl(self, typeDecl):
        for char in typeDecl:
            if char == 'l':
                self.listNumber += 1
            else:
                if char not in Type.basicTypes.keys():
                    raise TypeError(BASIC_TYPE_ERROR % char)
                self.basicType = Type.basicTypes[char]
                break

        if not self.basicType:
            self.basicType = unicode

    def convertBasicValue(self, value):
        try:
            return self.basicType(value.strip())
        except ValueError:
            raise TypeError(BASIC_VALUE_ERROR % (value, self.basicType.__name__))

    def convertValue(self, value):
        """Converts a p_value which is a string into a value conform
        to self."""
        if self.listNumber == 0:
            res = self.convertBasicValue(value)
        else:
            separators = []
            for char in value:
                if char in Type.separators and char not in separators:
                    separators.append(char)

            if len(separators) > self.listNumber:
                nbOfSurplusSeps = len(separators) - self.listNumber
                separators = separators[nbOfSurplusSeps:]
            res = None
            innerList = None
            resIsComplete = False
            if len(separators) < self.listNumber:
                if not value:
                    res = []
                    resIsComplete = True
                else:
                    nbOfMissingSeps = self.listNumber - len(separators)
                    res = []
                    innerList = res
                    for i in range(nbOfMissingSeps - 1):
                        newInnerList = []
                        innerList.append(newInnerList)
                        innerList = newInnerList

            separators.reverse()
            if innerList != None:
                innerList.append(self.convertListItem(value, separators))
            elif not resIsComplete:
                try:
                    res = self.convertListItem(value, separators)
                except TypeError, te:
                    raise TypeError(LIST_VALUE_ERROR % (value, te, self.name))

        return res

    def convertListItem(self, stringItem, remainingSeps):
        if not remainingSeps:
            res = self.convertBasicValue(stringItem)
        else:
            curSep = remainingSeps[0]
            tempRes = stringItem.split(curSep)
            if len(tempRes) == 1 and not tempRes[0]:
                res = []
            else:
                res = []
                for tempItem in tempRes:
                    res.append(self.convertListItem(tempItem, remainingSeps[1:]))

        return res

    def computeName(self):
        prefix = 'list of ' * self.listNumber
        return '<%s%s>' % (prefix, self.basicType.__name__)

    def __repr__(self):
        return self.name


class Table(UserList.UserList):
    __module__ = __name__

    def __init__(self):
        UserList.UserList.__init__(self)
        self.name = None
        self.parent = None
        self.parentRow = None
        return

    def dump(self, withContent=True):
        res = 'Table "%s"' % self.name
        if self.parent:
            res += ' extends table "%s"' % self.parent.name
            if isinstance(self.parentRow, int):
                res += '(%d)' % self.parentRow
            else:
                res += '(%s=%s)' % self.parentRow
        if withContent:
            res += '\n'
            for line in self:
                res += str(line)

        return res

    def instanceOf(self, tableName):
        res = False
        if self.parent:
            if self.parent.name == tableName:
                res = True
            else:
                res = self.parent.instanceOf(tableName)
        return res

    def asDict(self):
        """If this table as only 2 columns named "key" and "value", it can be
        represented as a Python dict. This method produces this dict."""
        infoDict = {}
        if self.parent:
            for info in self.parent:
                infoDict[info['key']] = info['value']

        for info in self:
            infoDict[info['key']] = info['value']

        return infoDict


class TableRow(UserDict.UserDict):
    __module__ = __name__

    def __init__(self, table):
        UserDict.UserDict.__init__(self)
        self.table = table

    def __getitem__(self, key):
        """This method "implements" row inheritance: if the current row does
        not have an element with p_key, it looks in the parent row of this row,
        via the parent table self.table."""
        keyError = False
        t = self.table
        if self.has_key(key):
            res = UserDict.UserDict.__getitem__(self, key)
        elif t.parent:
            if isinstance(t.parentRow, int):
                if t.parentRow < len(t.parent):
                    try:
                        res = t.parent[t.parentRow][key]
                    except KeyError:
                        keyError = True

                else:
                    raise ParserError(PARENT_ROW_NOT_FOUND % (t.name, t.parent.name, t.parentRow, t.parent.name, len(t.parent)))
            else:
                (tColumn, tValue) = t.parentRow
                rowFound = False
                for row in t.parent:
                    try:
                        curVal = row[tColumn]
                    except KeyError:
                        raise ParserError(PARENT_COLUMN_NOT_FOUND % (t.name, t.parent.name, tColumn, t.parent.name))

                    if curVal == tValue:
                        rowFound = True
                        try:
                            res = row[key]
                        except KeyError:
                            keyError = True
                        else:
                            break

                if not rowFound:
                    raise ParserError(PARENT_ROW_COL_NOT_FOUND % (t.name, t.parent.name, tColumn, tValue, t.parent.name))
        else:
            keyError = True
        if keyError:
            raise KeyError(TABLE_KEY_ERROR % (t.name, key, t.name))
        return res


class NameResolver:
    __module__ = __name__

    def resolveNames(self, tables):
        for (tableName, table) in tables.iteritems():
            if table.parent:
                if not tables.has_key(table.parent):
                    raise ParserError(PARENT_NOT_FOUND % (table.parent, table.name))
                table.parent = tables[table.parent]


class TableParser:
    __module__ = __name__
    IGNORE = 0
    READING_CONTROL_WORD = 1
    READING_CONTENT = 2
    READING_SPECIAL_CHAR = 3

    def __init__(self, fileName):
        self.input = open(fileName)
        self.state = None
        self.alpha = re.compile('[a-zA-Z_\\-\\*]')
        self.numeric = re.compile('[0-9]')
        self.whiteSpaces = (' ', '\t', '\n', '\r', '\x0c', '\x0b')
        self.specialChars = {91: "'", 92: "'", 93: '"', 94: '"', 85: '...', 81: '�', 4: '', 5: ''}
        self.state = TableParser.READING_CONTENT
        self.controlWordBuffer = ''
        self.contentBuffer = StringIO()
        self.specialCharBuffer = ''
        self.rtfTables = {}
        self.nbOfColumns = 0
        self.currentRow = []
        self.previousRow = []
        self.currentTable = Table()
        self.currentTableName = None
        self.currentColumnNames = None
        self.currentColumnTypes = None
        self.rowIsHeader = False
        self.tableNameRex = re.compile('([^\\(]+)(?:\\((.*)\\))?')
        return

    def isGroupDelimiter(self, char):
        return char == '{' or char == '}'

    def isControlWordStart(self, char):
        return char == '\\'

    def isAlpha(self, char):
        return self.alpha.match(char)

    def isNumeric(self, char):
        return self.numeric.match(char)

    def isWhiteSpace(self, char):
        return char in self.whiteSpaces

    def isQuote(self, char):
        return char == "'"

    def manageControlWord(self):
        self.state = TableParser.READING_CONTENT
        cWord = self.controlWordBuffer
        if cWord == 'trowd':
            self.contentBuffer.truncate(0)
        elif cWord == 'row':
            self.onRow()
            self.contentBuffer.truncate(0)
        elif cWord == 'cell':
            self.onColumn(self.contentBuffer.getvalue().strip())
            self.contentBuffer.truncate(0)
        elif cWord in ('bkmkstart', 'bkmkend'):
            self.state = TableParser.IGNORE
        self.controlWordBuffer = ''

    def manageSpecialChar(self):
        specialChar = int(self.specialCharBuffer)
        self.specialCharBuffer = ''
        if self.specialChars.has_key(specialChar):
            self.contentBuffer.write(self.specialChars[specialChar])
        else:
            print 'Warning: char %d not known.' % specialChar
        self.state = TableParser.READING_CONTENT

    def bufferize(self, char):
        if self.state == TableParser.READING_CONTROL_WORD:
            self.controlWordBuffer += char
        elif self.state == TableParser.READING_CONTENT:
            self.contentBuffer.write(char)
        elif self.state == TableParser.READING_SPECIAL_CHAR:
            self.specialCharBuffer += char

    def parse(self):
        for line in self.input:
            for char in line:
                if self.isGroupDelimiter(char):
                    if self.state == TableParser.READING_SPECIAL_CHAR:
                        self.manageSpecialChar()
                    self.state = TableParser.READING_CONTENT
                elif self.isControlWordStart(char):
                    if self.state == TableParser.READING_CONTROL_WORD:
                        self.manageControlWord()
                    elif self.state == TableParser.READING_SPECIAL_CHAR:
                        self.manageSpecialChar()
                    self.controlWordBuffer = ''
                    self.state = TableParser.READING_CONTROL_WORD
                elif self.isAlpha(char):
                    if self.state == TableParser.READING_SPECIAL_CHAR:
                        self.manageSpecialChar()
                    self.bufferize(char)
                elif self.isNumeric(char):
                    self.bufferize(char)
                elif self.isWhiteSpace(char):
                    if self.state == TableParser.READING_CONTROL_WORD:
                        self.manageControlWord()
                    elif self.state == TableParser.READING_CONTENT:
                        if char not in ['\n', '\r']:
                            self.contentBuffer.write(char)
                    elif self.state == TableParser.READING_SPECIAL_CHAR:
                        self.manageSpecialChar()
                        if char not in ['\n', '\r']:
                            self.contentBuffer.write(char)
                elif self.isQuote(char):
                    if self.state == TableParser.READING_CONTROL_WORD and not self.controlWordBuffer:
                        self.state = TableParser.READING_SPECIAL_CHAR
                    elif self.state == TableParser.READING_SPECIAL_CHAR:
                        self.manageSpecialChar()
                        self.bufferize(char)
                    else:
                        self.bufferize(char)
                elif self.state == TableParser.READING_CONTENT:
                    self.contentBuffer.write(char)
                elif self.state == TableParser.READING_SPECIAL_CHAR:
                    self.manageSpecialChar()
                    self.contentBuffer.write(char)

        if self.controlWordBuffer:
            self.manageControlWord()
        if self.currentTableName:
            self.addTable(self.currentTableName, self.currentTable)
        return self.rtfTables

    def getColumnInfos(self, columnHeaders):
        """Get, from the column headers, column names and types."""
        columnNames = []
        columnTypes = []
        for header in columnHeaders:
            if header.find(':') != -1:
                (name, typeDecl) = header.split(':')
                columnNames.append(name.strip())
                try:
                    columnTypes.append(Type(typeDecl.strip()))
                except TypeError, te:
                    raise ParserError(TYPE_ERROR % (header, self.currentTableName, te))

            else:
                columnNames.append(header)
                columnTypes.append(None)

        return (
         columnNames, columnTypes)

    def onRow(self):
        if self.nbOfColumns == 0 or not self.currentRow:
            pass
        else:
            if self.rowIsHeader:
                (self.currentColumnNames, self.currentColumnTypes) = self.getColumnInfos(self.currentRow)
                self.rowIsHeader = False
            elif self.nbOfColumns == 1:
                self.rowIsHeader = True
                if self.currentTableName:
                    self.addTable(self.currentTableName, self.currentTable)
                self.currentTable = Table()
                self.currentTableName = self.currentRow[0]
            else:
                self.addRow()
            del self.currentRow[:]
            self.nbOfColumns = 0

    def onColumn(self, content):
        self.currentRow.append(content)
        self.nbOfColumns += 1

    def addRow(self):
        i = 0
        row = TableRow(self.currentTable)
        for columnName in self.currentColumnNames:
            columnValue = self.currentRow[i]
            if columnValue == '"':
                if len(self.currentTable) == 0:
                    raise ParserError(NO_ROWS_IN_TABLE_YET % self.currentTableName)
                else:
                    lastRow = self.currentTable[(len(self.currentTable) - 1)]
                    columnValue = lastRow[columnName]
            else:
                columnType = self.currentColumnTypes[i]
                if columnType:
                    try:
                        columnValue = columnType.convertValue(columnValue)
                    except TypeError, te:
                        raise ParserError(VALUE_ERROR % (columnName, self.currentTableName, te))

            row[columnName] = columnValue
            i += 1

        self.currentTable.append(row)

    def addTable(self, tableName, table):
        res = self.tableNameRex.search(tableName)
        (tName, parentSpec) = res.groups()
        table.name = tName
        if parentSpec:
            res = parentSpec.split(':')
            if len(res) == 1:
                table.parent = parentSpec.strip()
                table.parentRow = 0
            else:
                table.parent = res[0].strip()
                res = res[1].split('=')
                if len(res) == 1:
                    try:
                        table.parentRow = int(res[0])
                    except ValueError:
                        raise ParserError(BAD_PARENT_ROW % (table.name, table.parent, res[0]))
                    else:
                        if table.parentRow < 0:
                            raise ParserError(BAD_PARENT_ROW % (table.name, table.parent, res[0]))
                else:
                    table.parentRow = (
                     res[0].strip(), res[1].strip())
        self.rtfTables[table.name] = table


class RtfTablesParser:
    __module__ = __name__

    def __init__(self, fileName):
        self.tableParser = TableParser(fileName)
        self.nameResolver = NameResolver()

    def parse(self):
        tables = self.tableParser.parse()
        self.nameResolver.resolveNames(tables)
        return tables


if __name__ == '__main__':
    tables = RtfTablesParser('Tests.rtf').parse()
    for (key, item) in tables.iteritems():
        print 'Table %s' % key
        print item
        print