# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/swails/src/ParmEd/parmed/formats/pdbx/PdbxReader.py
# Compiled at: 2019-02-23 13:42:47
# Size of source mod 2**32: 16561 bytes
"""
PDBx/mmCIF dictionary and data file parser.

Acknowledgements:

 The tokenizer used in this module is modeled after the clever parser design
 used in the PyMMLIB package.
 
 PyMMLib Development Group
 Authors: Ethan Merritt: merritt@u.washington.ed  & Jay Painter: jay.painter@gmail.com
 See:  http://pymmlib.sourceforge.net/

"""
import re
from parmed.exceptions import PdbxError, PdbxSyntaxError
from parmed.formats.pdbx.PdbxContainers import DataCategory, DefinitionContainer, DataContainer

class PdbxReader(object):
    __doc__ = ' PDBx reader for data files and dictionaries.\n    \n    '

    def __init__(self, ifh):
        """  ifh - input file handle returned by open()
        """
        self._PdbxReader__curLineNumber = 0
        self._PdbxReader__ifh = ifh
        self._PdbxReader__stateDict = {'data':'ST_DATA_CONTAINER',  'loop':'ST_TABLE', 
         'global':'ST_GLOBAL_CONTAINER', 
         'save':'ST_DEFINITION', 
         'stop':'ST_STOP'}

    def read(self, containerList):
        """
        Appends to the input list of definition and data containers.
        
        """
        self._PdbxReader__curLineNumber = 0
        try:
            self._PdbxReader__parser(self._PdbxReader__tokenizer(self._PdbxReader__ifh), containerList)
        except StopIteration:
            pass
        except (RuntimeError, DeprecationWarning) as e:
            if 'StopIteration' not in str(e):
                raise
        else:
            raise PdbxError()

    def __syntaxError(self, errText):
        raise PdbxSyntaxError(self._PdbxReader__curLineNumber, errText)

    def __getContainerName(self, inWord):
        """ Returns the name of the data_ or save_ container
        """
        return str(inWord[5:]).strip()

    def __getState(self, inWord):
        """Identifies reserved syntax elements and assigns an associated state.  

           Returns: (reserved word, state)
           where - 
              reserved word -  is one of CIF syntax elements:
                               data_, loop_, global_, save_, stop_
              state - the parser state required to process this next section.
        """
        i = inWord.find('_')
        if i == -1:
            return (None, 'ST_UNKNOWN')
        try:
            rWord = inWord[:i].lower()
            return (rWord, self._PdbxReader__stateDict[rWord])
        except:
            return (None, 'ST_UNKNOWN')

    def __parser(self, tokenizer, containerList):
        """ Parser for PDBx data files and dictionaries.

            Input - tokenizer() reentrant method recognizing data item names (_category.attribute)
                    quoted strings (single, double and multi-line semi-colon delimited), and unquoted
                    strings.

                    containerList -  list-type container for data and definition objects parsed from
                                     from the input file.

            Return:
                    containerList - is appended with data and definition objects - 
        """
        curContainer = None
        categoryIndex = {}
        curCategory = None
        curRow = None
        state = None
        while 1:
            curCatName, curAttName, curQuotedString, curWord = next(tokenizer)
            if curWord is None:
                continue
            reservedWord, state = self._PdbxReader__getState(curWord)
            if reservedWord is not None:
                break

        while 1:
            if curCatName is not None:
                state = 'ST_KEY_VALUE_PAIR'
            else:
                if curWord is not None:
                    reservedWord, state = self._PdbxReader__getState(curWord)
                else:
                    self._PdbxReader__syntaxError('Miscellaneous syntax error')
                    return
            if state == 'ST_KEY_VALUE_PAIR':
                try:
                    curCategory = categoryIndex[curCatName]
                except KeyError:
                    curCategory = categoryIndex[curCatName] = DataCategory(curCatName)
                    try:
                        curContainer.append(curCategory)
                    except AttributeError:
                        self._PdbxReader__syntaxError('Category cannot be added to  data_ block')
                        return
                    else:
                        curRow = []
                        curCategory.append(curRow)
                else:
                    try:
                        curRow = curCategory[0]
                    except IndexError:
                        self._PdbxReader__syntaxError('Internal index error accessing category data')
                        return

                    if curAttName in curCategory.getAttributeList():
                        self._PdbxReader__syntaxError('Duplicate attribute encountered in category')
                        return
                    curCategory.appendAttribute(curAttName)
                    tCat, tAtt, curQuotedString, curWord = next(tokenizer)
                    if tCat is not None or curQuotedString is None and curWord is None:
                        self._PdbxReader__syntaxError('Missing data for item _%s.%s' % (curCatName, curAttName))
                    if curWord is not None:
                        reservedWord, state = self._PdbxReader__getState(curWord)
                        if reservedWord is not None:
                            self._PdbxReader__syntaxError('Unexpected reserved word: %s' % reservedWord)
                        curRow.append(curWord)
                    else:
                        if curQuotedString is not None:
                            curRow.append(curQuotedString)
                        else:
                            self._PdbxReader__syntaxError('Missing value in item-value pair')
                    curCatName, curAttName, curQuotedString, curWord = next(tokenizer)
                    continue
            if state == 'ST_TABLE':
                curCatName, curAttName, curQuotedString, curWord = next(tokenizer)
                if curCatName is None or curAttName is None:
                    self._PdbxReader__syntaxError('Unexpected token in loop_ declaration')
                    return
                if curCatName in categoryIndex:
                    self._PdbxReader__syntaxError('Duplicate category declaration in loop_')
                    return
                curCategory = DataCategory(curCatName)
                try:
                    curContainer.append(curCategory)
                except AttributeError:
                    self._PdbxReader__syntaxError('loop_ declaration outside of data_ block or save_ frame')
                    return
                else:
                    curCategory.appendAttribute(curAttName)
                    while True:
                        curCatName, curAttName, curQuotedString, curWord = next(tokenizer)
                        if curCatName is None:
                            break
                        if curCatName != curCategory.getName():
                            self._PdbxReader__syntaxError('Changed category name in loop_ declaration')
                            return
                        curCategory.appendAttribute(curAttName)

                    if curWord is not None:
                        reservedWord, state = self._PdbxReader__getState(curWord)
                        if reservedWord is not None:
                            if reservedWord == 'stop':
                                return
                            self._PdbxReader__syntaxError('Unexpected reserved word after loop declaration: %s' % reservedWord)
                    while 1:
                        curRow = []
                        curCategory.append(curRow)
                        for tAtt in curCategory.getAttributeList():
                            if curWord is not None:
                                curRow.append(curWord)
                            else:
                                if curQuotedString is not None:
                                    curRow.append(curQuotedString)
                            curCatName, curAttName, curQuotedString, curWord = next(tokenizer)

                        if curCatName is not None:
                            break
                        if curWord is not None:
                            reservedWord, state = self._PdbxReader__getState(curWord)
                            if reservedWord is not None:
                                break

                continue
            elif state == 'ST_DEFINITION':
                sName = self._PdbxReader__getContainerName(curWord)
                if len(sName) > 0:
                    curContainer = DefinitionContainer(sName)
                    containerList.append(curContainer)
                    categoryIndex = {}
                    curCategory = None
                curCatName, curAttName, curQuotedString, curWord = next(tokenizer)
            elif state == 'ST_DATA_CONTAINER':
                dName = self._PdbxReader__getContainerName(curWord)
                if len(dName) == 0:
                    dName = 'unidentified'
                curContainer = DataContainer(dName)
                containerList.append(curContainer)
                categoryIndex = {}
                curCategory = None
                curCatName, curAttName, curQuotedString, curWord = next(tokenizer)
            else:
                if state == 'ST_STOP':
                    return
                if state == 'ST_GLOBAL':
                    curContainer = DataContainer('blank-global')
                    curContainer.setGlobal()
                    containerList.append(curContainer)
                    categoryIndex = {}
                    curCategory = None
                    curCatName, curAttName, curQuotedString, curWord = next(tokenizer)
                else:
                    if state == 'ST_UNKNOWN':
                        self._PdbxReader__syntaxError('Unrecogized syntax element: ' + str(curWord))
                        return

    def __tokenizer(self, ifh):
        """ Tokenizer method for the mmCIF syntax file - 

            Each return/yield from this method returns information about
            the next token in the form of a tuple with the following structure.

            (category name, attribute name, quoted strings, words w/o quotes or white space)

            Differentiated the regular expression to the better handle embedded quotes.

        """
        mmcifRe = re.compile('(?:(?:_(.+?)[.](\\S+))|(?:[\'](.*?)(?:[\']\\s|[\']$))|(?:["](.*?)(?:["]\\s|["]$))|(?:\\s*#.*$)|(\\S+))')
        fileIter = iter(ifh)
        while True:
            line = next(fileIter)
            self._PdbxReader__curLineNumber += 1
            if line.startswith('#'):
                pass
            else:
                if line.startswith(';'):
                    mlString = [
                     line[1:]]
                    while True:
                        line = next(fileIter)
                        self._PdbxReader__curLineNumber += 1
                        if line.startswith(';'):
                            break
                        mlString.append(line)

                    mlString[-1] = mlString[(-1)].rstrip()
                    yield (
                     None, None, ''.join(mlString), None)
                    line = line[1:]
                for it in mmcifRe.finditer(line):
                    tgroups = it.groups()
                    if tgroups != (None, None, None, None, None):
                        if tgroups[2] is not None:
                            qs = tgroups[2]
                        else:
                            if tgroups[3] is not None:
                                qs = tgroups[3]
                            else:
                                qs = None
                        groups = (
                         tgroups[0], tgroups[1], qs, tgroups[4])
                        yield groups

    def __tokenizerOrg(self, ifh):
        """ Tokenizer method for the mmCIF syntax file - 

            Each return/yield from this method returns information about
            the next token in the form of a tuple with the following structure.

            (category name, attribute name, quoted strings, words w/o quotes or white space)

        """
        mmcifRe = re.compile('(?:(?:_(.+?)[.](\\S+))|(?:[\'"](.*?)(?:[\'"]\\s|[\'"]$))|(?:\\s*#.*$)|(\\S+))')
        fileIter = iter(ifh)
        while True:
            line = next(fileIter)
            self._PdbxReader__curLineNumber += 1
            if line.startswith('#'):
                pass
            else:
                if line.startswith(';'):
                    mlString = [
                     line[1:]]
                    while True:
                        line = next(fileIter)
                        self._PdbxReader__curLineNumber += 1
                        if line.startswith(';'):
                            break
                        mlString.append(line)

                    mlString[-1] = mlString[(-1)].rstrip()
                    yield (
                     None, None, ''.join(mlString), None)
                    line = line[1:]
                for it in mmcifRe.finditer(line):
                    groups = it.groups()
                    if groups != (None, None, None, None):
                        yield groups