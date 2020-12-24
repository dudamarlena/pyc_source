# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/tagtomarkdown.py
# Compiled at: 2019-05-11 10:08:10
# Size of source mod 2**32: 28318 bytes
from markdown.extensions import Extension
from markdown.preprocessors import Preprocessor
from datetime import datetime
import os, sys

def makeExtension(*args, **kwargs):
    return TableTagExtension(**kwargs)


def version():
    return 'tagtomarkdown v.0.4.0, 2019-04-11'


class TableTagExtension(Extension):
    config = {}

    def __init__(self, **kwargs):
        (super(TableTagExtension, self).__init__)(**kwargs)

    def extendMarkdown(self, md, md_globals):
        md.registerExtension(self)
        md.preprocessors.add('tagtomarkdown', TagConverter(md), '_begin')


class TagConverter(Preprocessor):

    def __init__(self, substitutions):
        super().__init__()
        self.substitutions = substitutions

    def run(self, lines):
        documentElement = DocumentElement()
        documentElement.handleLines(lines, self.intPutConsole, self.intPutConsole)
        simpleConversions = SimpleConversions()
        simpleConversions.transform(documentElement, self.intPutConsole, self.intPutConsole)
        tableConversion = TableConversion()
        tableConversion.produceSymbolicNumbers(documentElement, self.intPutConsole, self.intPutConsole)
        orderedListConversion = OrderedListConversion()
        orderedListConversion.produceSymbolicNumbers(documentElement, self.intPutConsole, self.intPutConsole)
        documentElement.substituteSymbols(self.intPutConsole, self.intPutConsole)
        tableConversion.convertTable(documentElement, self.intPutConsole, self.intPutConsole)
        orderedListConversion.convertOrderedList(documentElement, self.intPutConsole, self.intPutConsole)
        return documentElement.getLines()

    def runProofOfConcept(self, lines):
        outLines = []
        for line in lines:
            if line.startswith('>br '):
                outLines.append('<p>%s</p>' % line[4:])
            else:
                outLines.append(line)

        return outLines

    def intPutConsole(self, text):
        print(text)

    def getTime(self):
        now = datetime.now()
        return now.isoformat(' ')[0:19]


class DocumentElement:
    outstandingSubstitutions = True
    substitutions = {}
    elements = []
    inDirName = ''
    fileName = ''
    parentDocumentElement = None
    globalSymbols = False

    def __init__(self, globalSymbols=False):
        self.outstandingSubstitutions = True
        self.substitutions = {}
        self.elements = []
        self.inDirName = ''
        self.parentDocumentElement = None
        self.globalSymbols = globalSymbols

    def handleLines(self, lines, consPrint, statusPrint):
        ignoreMode = False
        setBlockMode = False
        multiLineSymbolValue = []
        multiLineSymbolName = ''
        for lFull in lines:
            line = self.stripNewLine(lFull)
            words = line.split()
            if ignoreMode:
                if line.startswith('>/ignore'):
                    ignoreMode = False
                    continue
                    if setBlockMode:
                        if line.startswith('>/setblock'):
                            self.storeSubstitutionValue(multiLineSymbolName, multiLineSymbolValue)
                            multiLineSymbolValue = []
                            multiLineSymbolName = ''
                            setBlockMode = False
                        else:
                            multiLineSymbolValue.append(line)
                    else:
                        if line.startswith('>set '):
                            lineRemainder = ''
                            for i in range(2, len(words)):
                                if i > 2:
                                    lineRemainder += ' '
                                lineRemainder += words[i]

                            self.storeSubstitutionValue(words[1], lineRemainder)
                        else:
                            if line.startswith('>setblock'):
                                multiLineSymbolName = words[1]
                                setBlockMode = True
                            else:
                                if line.startswith('>#'):
                                    pass
                                else:
                                    if line.startswith('>ignore'):
                                        ignoreMode = True
                                    else:
                                        self.elements.append(line)

    def substituteSymbols(self, consPrint, statusPrint):
        self.outstandingSubstitutions = False
        i = 0
        while i < len(self.elements):
            line = self.elements[i]
            if isinstance(line, str):
                words = line.split()
                if line.startswith('>sub'):
                    substitutionString = self.lookupSymbol(words[1])
                    if len(substitutionString) < 1:
                        consPrint('Symbol %s not defined' % words[1])
                        self.outstandingSubstitutions = True
                    else:
                        if isinstance(substitutionString, str):
                            if len(words) > 2:
                                self.elements[i] = substitutionString + words[2]
                            else:
                                self.elements[i] = substitutionString
                        else:
                            del self.elements[i]
                            for l in substitutionString:
                                self.elements.insert(i, l)
                                i += 1

            else:
                if isinstance(line, DocumentElement):
                    line.substituteSymbols(consPrint, statusPrint)
                    if line.outstandingSubstitutions == True:
                        self.outstandingSubstitutions = True
                else:
                    consPrint('DocumentElement element of unknown type: %s.' % type(line).__name__)
                i += 1

    def getLines(self):
        return self.elements

    def getTime(self):
        now = datetime.now()
        return now.isoformat(' ')[0:19]

    def lookupSymbol(self, symbol):
        result = self.substitutions.get(symbol, '')
        if len(result) > 0:
            return result
        else:
            pDE = self.parentDocumentElement
            if isinstance(pDE, DocumentElement):
                result = pDE.lookupSymbol(symbol)
                if len(result) > 0:
                    return result
                else:
                    return ''
            else:
                return ''

    def stripNewLine(self, line):
        if len(line) > 0:
            if '\n' == line[(-1)]:
                return line[0:-1]
        return line

    def storeSubstitutionValue(self, symbolName, symbolValue):
        if self.globalSymbols:
            parent = self
            while parent != None:
                parentPrevious = parent
                parent = parent.parentDocumentElement
                parentPrevious.substitutions[symbolName] = symbolValue

        else:
            self.substitutions[symbolName] = symbolValue

    def printElements(self, recurseDepth):
        print('printElements() starting, %d elements, recurse depth: %d...' % (len(self.elements), recurseDepth))
        for line in self.elements:
            if isinstance(line, str):
                print('Str: %s' % line)
            else:
                if isinstance(line, DocumentElement):
                    print('DocumentElement child begin:')
                    line.printElements(recurseDepth + 1)
                    print('DocumentElement child end.')
                else:
                    print('DocumentElement element of unknown type: %s.' % type(line).__name__)

        print('printElements: substitutions:')
        for key in self.substitutions.keys():
            print('Key %s: %s' % (key, self.substitutions.get(key)))

    def writeElements(self, f, elements, consPrint, statusPrint):
        for line in elements:
            if isinstance(line, str):
                f.write('%s\n' % line)
            else:
                if isinstance(line, DocumentElement):
                    line.writeElements(f, line.elements, consPrint, statusPrint)
                else:
                    consPrint('DocumentElement element of unknown type: %s.' % type(line).__name__)


class SimpleConversions:

    def transform(self, documentElement, consPrint, statusPrint):
        i = 0
        while i < len(documentElement.elements):
            line = documentElement.elements[i]
            if isinstance(line, str):
                replacementString = ''
                if line.startswith('>datetime'):
                    replacementString = datetime.now().isoformat(' ')[0:19]
                else:
                    if line.startswith('>date'):
                        replacementString = datetime.now().isoformat(' ')[0:10]
                    else:
                        if line.startswith('>time'):
                            replacementString = datetime.now().isoformat(' ')[11:19]
                        else:
                            if line.startswith('>br'):
                                words = line.split()
                                l = words[0]
                                if len(l) == 3:
                                    replacementString = '<br />'
                                else:
                                    repetitionNoString = l[3:]
                                    if repetitionNoString.isnumeric():
                                        repetitionNo = int(repetitionNoString)
                                        while repetitionNo > 0:
                                            replacementString += '<br />'
                                            repetitionNo -= 1

                if len(replacementString) > 0:
                    words = line.split()
                    wordCount = 0
                    for word in words:
                        if wordCount == 1:
                            replacementString += word
                        if wordCount > 1:
                            replacementString += ' ' + word
                        wordCount += 1

                    documentElement.elements[i] = replacementString
            else:
                if isinstance(line, DocumentElement):
                    simpleConversions = SimpleConversions()
                    simpleConversions.transform(line, consPrint, statusPrint)
                else:
                    consPrint('DocumentElement element of unknown type: %s.' % type(line).__name__)
            i += 1


class TableConversion:

    def __init__(self):
        pass

    def produceSymbolicNumbers(self, documentElement, consPrint, statusPrint):
        tableRowCounter = 0
        i = 0
        while i < len(documentElement.elements):
            line = documentElement.elements[i]
            if isinstance(line, str):
                words = line.split()
                if line.startswith('>cell'):
                    if len(words) > 1:
                        command = words[1]
                        if command.startswith('*'):
                            if command == '*start':
                                tableRowCounter = 1
                                documentElement.elements[i] = '>cell %s' % tableRowCounter
                            else:
                                if command == '*incr':
                                    tableRowCounter += 1
                                    documentElement.elements[i] = '>cell %s' % tableRowCounter
                            if len(words) > 2:
                                symbol = words[2]
                                documentElement.substitutions[symbol] = '%d' % tableRowCounter
            else:
                if isinstance(line, DocumentElement):
                    self.produceSymbolicNumbers(line, consPrint, statusPrint)
                else:
                    consPrint('DocumentElement element of unknown type: %s.' % type(line).__name__)
            i += 1

    def convertTable(self, documentElement, consPrint, statusPrint):
        currColNo = 0
        noOfCols = 0
        cellContents = ''
        rowContents = ''
        caption = ''
        tableNo = 0
        tableMode = False
        linesIn = []
        i = 0
        while i < len(documentElement.elements):
            line = documentElement.elements[i]
            if isinstance(line, str):
                words = line.split()
                if tableMode:
                    del documentElement.elements[i]
                    i -= 1
                    if len(line.strip()) < 1 or line.startswith('>/row'):
                        savedContents = self.closeCell(cellContents)
                        cellContents = ''
                        if len(savedContents) > 0:
                            rowContents += savedContents
                        if noOfCols > 0:
                            while currColNo < noOfCols:
                                rowContents += '&nbsp;|'
                                currColNo += 1

                        if len(rowContents) > 0:
                            linesIn.append(rowContents)
                            linesIn.append('')
                            rowContents = ''
                        if line.startswith('>/row'):
                            caption = ''
                            if len(words) > 1:
                                for j in range(1, len(words)):
                                    if j == 1:
                                        if words[j].strip() == '*tableno':
                                            tableNo += 1
                                        else:
                                            caption += words[j].strip()
                                    else:
                                        caption += ' '
                                        caption += words[j].strip()

                                if tableNo > 0:
                                    linesIn.append('**Table %d: %s**' % (tableNo, caption))
                                else:
                                    linesIn.append('**%s**' % caption)
                        for line in linesIn:
                            i += 1
                            documentElement.elements.insert(i, line)

                        currColNo = 0
                        tableMode = False
                        linesIn = []
                    else:
                        if line.startswith('>row'):
                            savedContents = self.closeCell(cellContents)
                            cellContents = ''
                            if len(savedContents) > 0:
                                rowContents += savedContents
                            if noOfCols > 0:
                                while currColNo < noOfCols:
                                    rowContents += '&nbsp;|'
                                    currColNo += 1

                            linesIn.append(rowContents)
                            rowContents = '|'
                            currColNo = 0
                        else:
                            if line.startswith('>cell'):
                                savedContents = self.closeCell(cellContents)
                                cellContents = ''
                                if len(savedContents) > 0:
                                    rowContents += savedContents
                                lineRemainder = ''
                                if len(words) > 1:
                                    for j in range(1, len(words)):
                                        if j > 1:
                                            lineRemainder += ' '
                                        lineRemainder += words[j].strip()

                                    cellContents = lineRemainder
                                else:
                                    cellContents = '&nbsp;'
                                currColNo += 1
                            else:
                                if len(cellContents) > 0:
                                    if cellContents == '&nbsp;':
                                        cellContents = ''
                                    else:
                                        cellContents += ' '
                else:
                    cellContents += line.strip()
            elif line.startswith('>row'):
                del documentElement.elements[i]
                i -= 1
                cellContents = ''
                tableMode = True
                if len(words) > 1:
                    noOfCols = int(words[1])
                else:
                    noOfCols = 0
                currColNo = 0
                rowContents = '|'
            else:
                if isinstance(line, DocumentElement):
                    tableConversion = TableConversion()
                    tableConversion.convertTable(line, consPrint, statusPrint)
                else:
                    consPrint('TableConversion: DocumentElement element of unknown type: %s.' % type(line).__name__)
            i += 1

    def closeCell(self, cellContents):
        if len(cellContents) == 0:
            return ''
        else:
            return cellContents + '|'


class OrderedListConversion:

    def __init__(self):
        pass

    def produceSymbolicNumbers(self, documentElement: DocumentElement, consPrint, statusPrint):
        listItemCounter = 0
        i = 0
        insideListItem = False
        while i < len(documentElement.elements):
            line = documentElement.elements[i]
            if isinstance(line, str):
                words = line.split()
                if line.startswith('>li'):
                    insideListItem = True
                    if len(words) > 1:
                        command = words[1]
                        if command.startswith('*'):
                            if command == '*start':
                                listItemCounter = 1
                                documentElement.elements[i] = '%s. ' % listItemCounter
                            else:
                                if command == '*incr':
                                    listItemCounter += 1
                                    documentElement.elements[i] = '%s. ' % listItemCounter
                            if len(words) > 2:
                                symbol = words[2]
                                documentElement.substitutions[symbol] = '%d' % listItemCounter
                        else:
                            listItemCounter += 1
                            documentElement.elements[i] = '%s. %s' % (listItemCounter, self.fetchRemainder(words))
                    else:
                        listItemCounter += 1
                        documentElement.elements[i] = '%s. ' % listItemCounter
                else:
                    if line.startswith('>/li'):
                        insideListItem = False
                        del documentElement.elements[i]
                        i -= 1
                    else:
                        if insideListItem:
                            documentElement.elements[(i - 1)] += line
                            del documentElement.elements[i]
                            i -= 1
                            insideListItem = False
            else:
                if isinstance(line, DocumentElement):
                    self.produceSymbolicNumbers(line, consPrint, statusPrint)
                else:
                    consPrint('OrderedListConverision: DocumentElement element of unknown type: %s.' % type(line).__name__)
            i += 1

    def convertOrderedList(self, documentElement: DocumentElement, consPrint, statusPrint):
        orderedListMode = False
        linesIn = []
        i = 0
        while i < len(documentElement.elements):
            line = documentElement.elements[i]
            if isinstance(line, str):
                words = line.split()
                if line.startswith('>li'):
                    linesIn.append(self.fetchRemainder(words))
                else:
                    if line.startswith('>/li'):
                        pass
                    else:
                        linesIn.append(line)
            else:
                if isinstance(line, DocumentElement):
                    orderedListConversion = OrderedListConversion()
                    orderedListConversion.convertOrderedList(line, consPrint, statusPrint)
                else:
                    consPrint('OrderedListConversion: DocumentElement element of unknown type: %s.' % type(line).__name__)
            i += 1

    def fetchRemainder(self, words):
        lineRemainder = ''
        if len(words) > 1:
            for j in range(1, len(words)):
                if j > 1:
                    lineRemainder += ' '
                lineRemainder += words[j].strip()

        return lineRemainder