# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.6-universal/egg/picalo/lib/delimitedtext.py
# Compiled at: 2008-12-09 22:31:28
"""
This module implements a memory-efficient CSV reader and writer.  Although 
Python 2.4+ has a built-in csv module, real-world tests by me show that it
is not memory efficient.  In other words, it runs out of memory on files
with 25 million or more records in it.

While this implementation may not be as fast (because it is written in
pure Python), it only holds one line at a time in memory.  It is up to
the calling application to make efficient use of these records.
"""
import os, cStringIO, codecs
from chardet.universaldetector import UniversalDetector

def make_unicode(value):
    """Makes a value (of any type) into unicode using utf_8"""
    if isinstance(value, unicode):
        return value
    else:
        if isinstance(value, str):
            return unicode(value, 'utf_8')
        return unicode(repr(value), 'utf_8')


class DelimitedWriter:
    """A writer of delimited text files"""

    def __init__(self, f, delimiter=',', qualifier='"', line_ending=os.linesep, none='', encoding='utf_8'):
        """Constructor for a delimited writer object.
    
       @param f:            A file object that allows writing.  You must have already opened the file for writing.  This class does NOT close the writer.
       @type  f:            str
       @param delimiter:    A field delimiter character, defaults to a comma (,)
       @type  delimiter:    str
       @param qualifier:    A qualifier to use when delimiters exist in field records, defaults to a double quote (")
       @type  qualifier:    str
       @param line_ending:  A line ending to separate rows with, defaults to os.linesep (
 on Unix, 
 on Windows)
       @type  line_ending:  str
       @param none:         An parameter specifying what to write for cells that have the None value, defaults to an empty string ('')
       @type  none:         str
       @param encoding:     The unicode encoding to write with.  This should be a value from the codecs module, defaults to 'utf_8'.
       @type  encoding:     str
    """
        self.f = codecs.EncodedFile(f, 'utf_8', encoding)
        self.delimiter = make_unicode(delimiter)
        self.qualifier = make_unicode(qualifier)
        self.doublequalifier = self.qualifier + self.qualifier
        self.line_ending = make_unicode(line_ending)
        self.none = none
        self.encoding = encoding

    def writerow(self, row, lastrow=False):
        """Writes a row to the file.  This method is not thread-safe on the same DelimitedWriter object.
    
    @param row:     An iterable object to encode, such as a Python list or tuple.
    @type  row:     iterable object
    @param lastrow: Whether this is the last row of the file.  If True, no line ending is written.
    @type  lastrow: bool
    """
        fields = []
        for val in row:
            val = make_unicode(val)
            if self.delimiter in val or self.qualifier in val or self.line_ending in val:
                fields.append(self.qualifier + val.replace(self.qualifier, self.doublequalifier) + self.qualifier)
            else:
                fields.append(val)

        self.f.write(self.delimiter.join(fields).encode(self.encoding))
        if not lastrow:
            self.f.write(self.line_ending)
        self.f.flush()


class DelimitedReader:
    """A reader for delimited text files"""

    def __init__(self, f, delimiter=',', qualifier='"', encoding=None, errors='replace'):
        """Constructor for a delimited text file reader.  Windows, Unix, and Mac line endings are automatically supported.
       The object can be iterated across (ex: for row in DelimitedReader(...) ) efficiently.  Each iteration produces
       a list of fields for the current row.  StopIteration is raised when no more records exist.

       @param f:            A file object that allows writing.  You must have already opened the file for writing.  This class does NOT close the writer.
       @type  f:            str
       @param delimiter:    A field delimiter character, defaults to a comma (,)
       @type  delimiter:    str
       @param qualifier:    A qualifier that denotes fields with special characters in them, defaults to a double quote (")
       @type  qualifier:    str
       @param encoding:     The unicode encoding to read with.  This should be a value from the codecs module.  If None, the encoding is guessed to utf_8, utf-16, utf-16-be, or utf-16-le
       @type  encoding:     str
       @param errors:       How to handle characters that cannot be decoded.  Options are 'replace', 'strict', and 'ignore'.  See 'codecs' in the Python documentation for more information.
       @type  errors:       str
    """
        self.delimiter = delimiter
        self.qualifier = qualifier
        self.doublequalifier = qualifier + qualifier
        if encoding != None:
            self.encoding = encoding
        else:
            startpos = f.tell()
            detector = UniversalDetector()
            while True:
                block = f.read(1024)
                detector.feed(block)
                if detector.done or not block:
                    break

            detector.close()
            f.seek(startpos)
            self.encoding = detector.result['encoding']
        self.f = codecs.EncodedFile(f, 'utf_8', self.encoding, errors)
        return

    def __iter__(self):
        """Returns an iterator to this DelimitedReader.  This allows code like the following:
    
       for record in delimitedtext.DelimitedReader(file):
         print record
    """
        return self

    def _getnextline(self):
        """Internal method that retrieves the next line of the file, separating the text from the line separator"""
        line = unicode(self.f.next(), 'utf_8')
        if line[-2:] in ('\r\n', '\n\r'):
            return (line[:-2], line[-2:])
        if line[-1:] in ('\n', '\r'):
            return (line[:-1], line[-1:])
        return (
         line, '')

    def _isendqualifier(self, field):
        """Internal method that returns true if the given field ends with a qualifier.
       A field ends with a qualifier when it has an *odd* number
       of qualifiers at the end.  If it has an even number of qualifiers,
       the qualifiers are part of the actual field rather than a qualifier.
    """
        qualifiers = self.qualifier
        count = 0
        while field.endswith(qualifiers):
            count += 1
            qualifiers += self.qualifier

        return count % 2 == 1

    def next(self):
        """Reads a CSV record from the file and returns a list of fields encoded as unicode objects.
       A CSV record normally corresponds to a single line of the file, but it can span more than one
       line if the record contains hard returns in the values.  The method can handle these multi-line
       records.
       
       The method raises a StopIteration when done.  This supports the python Iterator interface.
       
       @returns  The fields from the next row.
       @rtype    list
    """
        record = []
        combofield = None
        while True:
            (line, linesep) = self._getnextline()
            fields = line.split(self.delimiter)
            for field in fields:
                if combofield == None:
                    if field.startswith(self.qualifier) and self._isendqualifier(field[len(self.qualifier):]):
                        field = field[len(self.qualifier):-1 * len(self.qualifier)]
                        record.append(field.replace(self.doublequalifier, self.qualifier))
                    elif field.startswith(self.qualifier):
                        combofield = field[len(self.qualifier):]
                    else:
                        record.append(field.replace(self.doublequalifier, self.qualifier))
                elif self._isendqualifier(field[len(self.qualifier):]):
                    combofield += self.delimiter + field[:-1 * len(self.qualifier)]
                    record.append(combofield.replace(self.doublequalifier, self.qualifier))
                    combofield = None
                else:
                    combofield += self.delimiter + field

            if combofield == None:
                return record
            combofield += linesep

        return

    def readrow(self):
        """Reads a CSV record from the file and returns a list of fields encoded as unicode objects.
       A CSV record normally corresponds to a single line of the file, but it can span more than one
       line if the record contains hard returns in the values.  The method can handle these multi-line
       records.

       The method returns None when no more records exist.

       @returns  The fields from the next row.
       @rtype    list
    """
        try:
            return self.next()
        except StopIteration:
            return

        return