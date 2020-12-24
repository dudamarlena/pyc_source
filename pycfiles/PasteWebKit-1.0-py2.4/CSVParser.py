# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/paste/webkit/FakeWebware/MiscUtils/CSVParser.py
# Compiled at: 2006-10-22 17:01:01
StartRecord = 0
StartField = 1
InField = 2
QuoteInField = 3
InQuotedField = 4
QuoteInQuotedField = 5
EndQuotedField = 6
Finished = 10

class ParseError(Exception):
    __module__ = __name__


class CSVParser:
    """
        Parses CSV files including all subtleties such as:
                * commas in fields
                * double quotes in fields
                * embedded newlines in fields
                        - Examples of programs that produce such beasts include
                          MySQL and Excel

        For a higher-level, friendlier CSV class with many conveniences,
        see DataTable (which uses this class for its parsing).

        Example:
                records = []
                parse = CSVParser().parse
                for line in lines:
                        results = parse(line)
                        if results is not None:
                                records.append(results)

        CREDIT

        The algorithm was taken directly from the open source Python
        C-extension, csv:
                http://www.object-craft.com.au/projects/csv/

        It would be nice to use the csv module when present, since it is
        substantially faster. Before that can be done, it needs to support
        allowComments and stripWhitespace, and pass the TestCSVParser.py
        test suite.
        """
    __module__ = __name__

    def __init__(self, allowComments=1, stripWhitespace=1, fieldSep=',', autoReset=1, doubleQuote=1):
        """
                @@ document
                """
        self._allowComments = allowComments
        self._stripWhitespace = stripWhitespace
        self._doubleQuote = doubleQuote
        self._fieldSep = fieldSep
        self._autoReset = autoReset
        self._state = StartRecord
        self._fields = []
        self._hadParseError = 0
        self._field = []
        self.addChar = self._field.append
        self._handlers = [
         self.startRecord, self.startField, self.inField, self.quoteInField, self.inQuotedField, self.quoteInQuotedField, self.endQuotedField]

    def parse(self, line):
        """
                Parse the single line and return a list or string fields, or
                None if the CSV record contains embedded newlines and the
                record is not yet complete.
                """
        if self._autoReset and self._hadParseError:
            self.reset()
        handlers = self._handlers
        i = 0
        lineLen = len(line)
        while i < lineLen:
            c = line[i]
            if c == '\r':
                i += 1
                if i == lineLen:
                    break
                c = line[i]
                if c == '\n':
                    i += 1
                    if i == lineLen:
                        break
                self._hadParseError = 1
                raise ParseError('Newline inside string')
            elif c == '\n':
                i += 1
                if i == lineLen:
                    break
                self._hadParseError = 1
                raise ParseError('Newline inside string')
            elif handlers[self._state](c) == Finished:
                break
            i += 1

        handlers[self._state]('\x00')
        if self._state == StartRecord:
            fields = self._fields
            self._fields = []
            if self._stripWhitespace:
                fields = [ field.strip() for field in fields ]
            return fields
        else:
            return
        return

    def reset(self):
        """
                Resets the parser to a fresh state in order to recover from
                exceptions. But if autoReset is true (the default), this is
                done automatically.
                """
        self._fields = []
        self._state = StartRecord
        self.hasParseError = 0

    def startRecord(self, c):
        if c != '\x00':
            if c == '#' and self._allowComments:
                return Finished
            else:
                self._state = StartField
                self.startField(c)

    def startField(self, c):
        if c == '"':
            self._state = InQuotedField
        elif c == self._fieldSep:
            self.saveField()
        elif c == ' ' and self._stripWhitespace:
            pass
        elif c == '\x00':
            self.saveField()
            self._state = StartRecord
        else:
            self.addChar(c)
            self._state = InField

    def inField(self, c):
        if c == self._fieldSep:
            self.saveField()
            self._state = StartField
        elif c == '\x00':
            self.saveField()
            self._state = StartRecord
        elif c == '"' and self._doubleQuote:
            self._state = QuoteInField
        else:
            self.addChar(c)

    def quoteInField(self, c):
        self.addChar('"')
        if c == '"':
            self._state = InField
        elif c == '\x00':
            self.saveField()
            self._state = StartRecord
        elif c == self._fieldSep:
            self.saveField()
            self._state = StartField
        else:
            self.addChar(c)
            self._state = InField

    def inQuotedField(self, c):
        if c == '"':
            if self._doubleQuote:
                self._state = QuoteInQuotedField
            else:
                self.saveField()
                self._state = EndQuotedField
        elif c == '\x00':
            self.addChar('\n')
        else:
            self.addChar(c)

    def quoteInQuotedField(self, c):
        if c == '"':
            self.addChar('"')
            self._state = InQuotedField
        elif c == self._fieldSep:
            self.saveField()
            self._state = StartField
        elif c == ' ' and self._stripWhitespace:
            pass
        elif c == '\x00':
            self.saveField()
            self._state = StartRecord
        else:
            self._hadParseError = 1
            raise ParseError, '%s expected after "' % self._fieldSep

    def endQuotedField(self, c):
        if c == self._fieldSep:
            self._state = StartField
        elif c == '\x00':
            self._state = StartRecord
        else:
            self._hadParseError = 1
            raise ParseError, '%s expected after "' % self._fieldSep

    def saveField(self):
        self._fields.append(('').join(self._field))
        self._field = []
        self.addChar = self._field.append


_parser = CSVParser()
parse = _parser.parse
import types

def joinCSVFields(fields):
    """
        Returns a CSV record (eg a string) from a sequence of fields.
        Fields containing commands (,) or double quotes (") are quoted
        and double quotes are escaped (""). The terminating newline is
        NOT included.
        """
    newFields = []
    for field in fields:
        assert type(field) is types.StringType
        if field.find('"') != -1:
            newField = '"' + field.replace('"', '""') + '"'
        elif field.find(',') != -1:
            newField = '"' + field + '"'
        else:
            newField = field
        newFields.append(newField)

    return (',').join(newFields)