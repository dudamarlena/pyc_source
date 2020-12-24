# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.darwin-8.8.0-Power_Macintosh/egg/econ/data/tabular.py
# Compiled at: 2007-04-18 06:57:54
"""
Tools for dealing with tabular data
"""
import econ.log
logger = econ.log.get_logger()

class TabularData(object):
    """Holder for tabular data

    Assume data organized in rows
    No type conversion so all data will be strings
    Properties:
        data: data itself provided as array of arrays
        header: associated header columns (if they exist)
    TODO: handling of large datasets (iterators?)
    """
    __module__ = __name__

    def __init__(self, data=None, header=None):
        """
        Initialize object. If data or header not set they are defaulted to
        empty list.
        
        NB: must use None as default value for arguments rather than []
        because [] is mutable and using it will result in subtle bugs. See:
        'Default parameter values are evaluated when the function definition
        is executed.' [http://www.python.org/doc/current/ref/function.html]
        """
        self.data = []
        self.header = []
        if data is not None:
            self.data = data
        if header is not None:
            self.header = header
        return


import csv

class ReaderCsv(object):
    """Read data from a csv file into a TabularData structure
    """
    __module__ = __name__

    def read(self, fileobj):
        """Read in a csv file and return a TabularData object
        @param: fileobj: file like object
        """
        tabData = TabularData()
        sample = fileobj.read()
        sniffer = csv.Sniffer()
        hasHeader = sniffer.has_header(sample)
        fileobj.seek(0)
        reader = csv.reader(fileobj, skipinitialspace=True)
        if hasHeader:
            tabData.header = reader.next()
        for row in reader:
            tabData.data.append(row)

        return tabData


import re

class WriterHtml:
    """
    Write tabular data to xhtml
    """
    __module__ = __name__

    def __init__(self, table_attributes={'class': 'data'}, decimal_places=2, do_pretty_print=False):
        """
        @do_pretty_print: whether to pretty print (indent) output
        @attributes: dictionary of html attribute name/value pairs to be
        added to the table element
        @decimal_places: number of decimal places to use when rounding numerical 
                        values when textifying for table
        """
        self.do_pretty_print = do_pretty_print
        self.table_attributes = table_attributes
        self.decimal_places = decimal_places

    def write(self, tabulardata, caption='', rowHeadings=[]):
        """
        Write matrix of data to xhtml table.
        Allow for addition of row and column headings
        
        @return xhtml table containing data
        
        @param data: table of data that makes up table
        @param caption: the caption for the table (if empty no caption created)
        """
        columnHeadings = tabulardata.header
        data = tabulardata.data
        haveRowHeadings = len(rowHeadings) > 0
        htmlTable = '<table'
        for (key, value) in self.table_attributes.items():
            htmlTable += ' %s="%s"' % (key, value)

        htmlTable += '>'
        if caption != '':
            htmlTable += self._writeTag('caption', caption)
        numColHeads = len(columnHeadings)
        if numColHeads > 0:
            if haveRowHeadings and numColHeads == len(data[0]):
                columnHeadings.insert(0, '')
            htmlTable += self.writeHeading(columnHeadings)
        htmlTable += '<tbody>'
        for ii in range(0, len(data)):
            if haveRowHeadings:
                htmlTable += self.writeRow(data[ii], rowHeadings[ii])
            else:
                htmlTable += self.writeRow(data[ii])

        htmlTable += '</tbody></table>'
        if self.do_pretty_print:
            return self.prettyPrint(htmlTable)
        else:
            return htmlTable

    def writeHeading(self, row):
        """
        Write heading for html table (<thead>)
        """
        result = '<thead><tr>'
        result += self.writeGeneralRow(row, 'th')
        result += '</tr></thead>'
        return result

    def writeRow(self, row, rowHeading=''):
        result = ''
        if rowHeading != '':
            result = self._writeTag('th', rowHeading)
        result += self.writeGeneralRow(row, 'td')
        result = self._writeTag('tr', result)
        return result

    def writeGeneralRow(self, row, tagName):
        result = ''
        for ii in range(len(row)):
            result += self._writeTag(tagName, row[ii])

        return result

    def prettyPrint(self, html):
        """pretty print html using HTMLTidy"""
        import mx.Tidy
        return self.tabify(mx.Tidy.tidy(html, None, None, wrap=0, indent='yes')[2])

    def tabify(self, instr, tabsize=2):
        """
        tabify text by replacing spaces of size tabSize by tabs
        """
        whitespace = tabsize * ' '
        return re.sub(whitespace, '\t', instr)

    def _writeTag(self, tagName, value):
        return '<' + tagName + '>' + self._processTagValueToText(value) + '</' + tagName + '>'

    def _processTagValueToText(self, tagValue):
        if type(tagValue) != type('text'):
            roundedResult = str(round(tagValue, self.decimal_places))
            if len(str(tagValue)) < len(roundedResult):
                return str(tagValue)
            else:
                return roundedResult
        else:
            return str(tagValue)