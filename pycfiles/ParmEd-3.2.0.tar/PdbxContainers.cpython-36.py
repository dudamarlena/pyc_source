# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/swails/src/ParmEd/parmed/formats/pdbx/PdbxContainers.py
# Compiled at: 2017-02-11 08:13:06
# Size of source mod 2**32: 29513 bytes
"""

A collection of container classes supporting the PDBx/mmCIF storage model.

A base container class is defined which supports common features of
data and definition containers.   PDBx data files are organized in
sections called data blocks which are mapped to data containers.
PDBx dictionaries contain definition sections and data sections
which are mapped to definition and data containes respectively.

Data in both PDBx data files and dictionaries are organized in
data categories. In the PDBx syntax individual items or data
identified by labels of the form '_categoryName.attributeName'.
The terms category and attribute in PDBx jargon are analogous
table and column in relational data model, or class and attribute
in an object oriented data model.

The DataCategory class provides base storage container for instance
data and definition meta data.

"""
__docformat__ = 'restructuredtext en'
__author__ = 'John Westbrook'
__email__ = 'jwest@rcsb.rutgers.edu'
__license__ = 'Creative Commons Attribution 3.0 Unported'
__version__ = 'V0.01'
from parmed.utils.six.moves import range
import re, sys, traceback

class CifName(object):
    __doc__ = ' Class of utilities for CIF-style data names -\n    '

    def __init__(self):
        pass

    @staticmethod
    def categoryPart(name):
        tname = ''
        if name.startswith('_'):
            tname = name[1:]
        else:
            tname = name
        i = tname.find('.')
        if i == -1:
            return tname
        else:
            return tname[:i]

    @staticmethod
    def attributePart(name):
        i = name.find('.')
        if i == -1:
            return
        else:
            return name[i + 1:]


class ContainerBase(object):
    __doc__ = ' Container base class for data and definition objects.\n    '

    def __init__(self, name):
        self._ContainerBase__name = name
        self._ContainerBase__objNameList = []
        self._ContainerBase__objCatalog = {}
        self._ContainerBase__type = None

    def getType(self):
        return self._ContainerBase__type

    def setType(self, type):
        self._ContainerBase__type = type

    def getName(self):
        return self._ContainerBase__name

    def setName(self, name):
        self._ContainerBase__name = name

    def exists(self, name):
        return name in self._ContainerBase__objCatalog

    def getObj(self, name):
        if name in self._ContainerBase__objCatalog:
            return self._ContainerBase__objCatalog[name]
        else:
            return

    def getObjNameList(self):
        return self._ContainerBase__objNameList

    def append(self, obj):
        """ Add the input object to the current object catalog. An existing object
            of the same name will be overwritten.
        """
        if obj.getName() is not None:
            if obj.getName() not in self._ContainerBase__objCatalog:
                self._ContainerBase__objNameList.append(obj.getName())
            self._ContainerBase__objCatalog[obj.getName()] = obj

    def replace(self, obj):
        """ Replace an existing object with the input object
        """
        if obj.getName() is not None:
            if obj.getName() in self._ContainerBase__objCatalog:
                self._ContainerBase__objCatalog[obj.getName()] = obj

    def printIt(self, fh=sys.stdout, type='brief'):
        fh.write('+ %s container: %30s contains %4d categories\n' % (
         self.getType(), self.getName(), len(self._ContainerBase__objNameList)))
        for nm in self._ContainerBase__objNameList:
            fh.write('--------------------------------------------\n')
            fh.write('Data category: %s\n' % nm)
            if type == 'brief':
                self._ContainerBase__objCatalog[nm].printIt(fh)
            else:
                self._ContainerBase__objCatalog[nm].dumpIt(fh)

    def rename(self, curName, newName):
        """ Change the name of an object in place -
        """
        try:
            i = self._ContainerBase__objNameList.index(curName)
            self._ContainerBase__objNameList[i] = newName
            self._ContainerBase__objCatalog[newName] = self._ContainerBase__objCatalog[curName]
            self._ContainerBase__objCatalog[newName].setName(newName)
            return True
        except:
            return False

    def remove(self, curName):
        """ Revmove object by name.  Return True on success or False otherwise.
        """
        try:
            if curName in self._ContainerBase__objCatalog:
                del self._ContainerBase__objCatalog[curName]
                i = self._ContainerBase__objNameList.index(curName)
                del self._ContainerBase__objNameList[i]
                return True
            else:
                return False
        except:
            pass

        return False


class DefinitionContainer(ContainerBase):

    def __init__(self, name):
        super(DefinitionContainer, self).__init__(name)
        self.setType('definition')

    def isCategory(self):
        if self.exists('category'):
            return True
        else:
            return False

    def isAttribute(self):
        if self.exists('item'):
            return True
        else:
            return False

    def printIt(self, fh=sys.stdout, type='brief'):
        fh.write('Definition container: %30s contains %4d categories\n' % (
         self.getName(), len(self.getObjNameList())))
        if self.isCategory():
            fh.write('Definition type: category\n')
        else:
            if self.isAttribute():
                fh.write('Definition type: item\n')
            else:
                fh.write('Definition type: undefined\n')
        for nm in self.getObjNameList():
            fh.write('--------------------------------------------\n')
            fh.write('Definition category: %s\n' % nm)
            if type == 'brief':
                self.getObj(nm).printIt(fh)
            else:
                self.getObj(nm).dumpId(fh)


class DataContainer(ContainerBase):
    __doc__ = ' Container class for DataCategory objects.\n    '

    def __init__(self, name):
        super(DataContainer, self).__init__(name)
        self.setType('data')
        self._DataContainer__globalFlag = False

    def invokeDataBlockMethod(self, type, method, db):
        self._DataContainer__currentRow = 1
        exec(method.getInline())

    def setGlobal(self):
        self._DataContainer__globalFlag = True

    def getGlobal(self):
        return self._DataContainer__globalFlag


class DataCategoryBase(object):
    __doc__ = ' Base object definition for a data category -\n    '

    def __init__(self, name, attributeNameList=None, rowList=None):
        self._name = name
        if rowList is not None:
            self._rowList = rowList
        else:
            self._rowList = []
        if attributeNameList is not None:
            self._attributeNameList = attributeNameList
        else:
            self._attributeNameList = []
        self._catalog = {}
        self._numAttributes = 0
        self._DataCategoryBase__setup()

    def __setup(self):
        self._numAttributes = len(self._attributeNameList)
        self._catalog = {}
        for attributeName in self._attributeNameList:
            attributeNameLC = attributeName.lower()
            self._catalog[attributeNameLC] = attributeName

    def setRowList(self, rowList):
        self._rowList = rowList

    def setAttributeNameList(self, attributeNameList):
        self._attributeNameList = attributeNameList
        self._DataCategoryBase__setup()

    def setName(self, name):
        self._name = name

    def get(self):
        return (
         self._name, self._attributeNameList, self._rowList)


class DataCategory(DataCategoryBase):
    __doc__ = '  Methods for creating, accessing, and formatting PDBx cif data categories.  \n    '

    def __init__(self, name, attributeNameList=None, rowList=None):
        super(DataCategory, self).__init__(name, attributeNameList, rowList)
        self._DataCategory__lfh = sys.stdout
        self._DataCategory__currentRowIndex = 0
        self._DataCategory__currentAttribute = None
        self._DataCategory__avoidEmbeddedQuoting = False
        self._DataCategory__wsRe = re.compile('\\s')
        self._DataCategory__wsAndQuotesRe = re.compile('[\\s\'\\"]')
        self._DataCategory__nlRe = re.compile('[\\n\\r]')
        self._DataCategory__sqRe = re.compile("[']")
        self._DataCategory__sqWsRe = re.compile("('\\s)|(\\s')")
        self._DataCategory__dqRe = re.compile('["]')
        self._DataCategory__dqWsRe = re.compile('("\\s)|(\\s")')
        self._DataCategory__intRe = re.compile('^[0-9]+$')
        self._DataCategory__floatRe = re.compile('^-?(([0-9]+)[.]?|([0-9]*[.][0-9]+))([(][0-9]+[)])?([eE][+-]?[0-9]+)?$')
        self._DataCategory__dataTypeList = [
         'DT_NULL_VALUE', 'DT_INTEGER', 'DT_FLOAT', 'DT_UNQUOTED_STRING', 'DT_ITEM_NAME',
         'DT_DOUBLE_QUOTED_STRING', 'DT_SINGLE_QUOTED_STRING', 'DT_MULTI_LINE_STRING']
        self._DataCategory__formatTypeList = ['FT_NULL_VALUE', 'FT_NUMBER', 'FT_NUMBER', 'FT_UNQUOTED_STRING',
         'FT_QUOTED_STRING', 'FT_QUOTED_STRING', 'FT_QUOTED_STRING', 'FT_MULTI_LINE_STRING']

    def __getitem__(self, x):
        """  Implements list-type functionality - 
             Implements op[x] for some special cases -
                x=integer - returns the row in category (normal list behavior)
                x=string  - returns the value of attribute 'x' in first row.
        """
        if isinstance(x, int):
            return self._rowList[x]
        else:
            if isinstance(x, str):
                try:
                    ii = self.getAttributeIndex(x)
                    return self._rowList[0][ii]
                except (IndexError, KeyError) as e:
                    raise KeyError(str(e))

            assert False, 'Should not be here'

    def getCurrentAttribute(self):
        return self._DataCategory__currentAttribute

    def getRowIndex(self):
        return self._DataCategory__currentRowIndex

    def getRowList(self):
        return self._rowList

    def getRowCount(self):
        return len(self._rowList)

    def getRow(self, index):
        try:
            return self._rowList[index]
        except:
            return []

    def removeRow(self, index):
        try:
            if index >= 0:
                if index < len(self._rowList):
                    del self._rowList[index]
                    if self._DataCategory__currentRowIndex >= len(self._rowList):
                        self._DataCategory__currentRowIndex = len(self._rowList) - 1
                    return True
        except:
            pass

        return False

    def getFullRow(self, index):
        """ Return a full row based on the length of the the attribute list.
        """
        try:
            if len(self._rowList[index]) < self._numAttributes:
                for ii in range(self._numAttributes - len(self._rowList[index])):
                    self._rowList[index].append('?')

            return self._rowList[index]
        except:
            return ['?' for ii in range(self._numAttributes)]

    def getName(self):
        return self._name

    def getAttributeList(self):
        return self._attributeNameList

    def getAttributeCount(self):
        return len(self._attributeNameList)

    def getAttributeListWithOrder(self):
        oL = []
        for ii, att in enumerate(self._attributeNameList):
            oL.append((att, ii))

        return oL

    def getAttributeIndex(self, attributeName):
        try:
            return self._attributeNameList.index(attributeName)
        except:
            return -1

    def hasAttribute(self, attributeName):
        return attributeName in self._attributeNameList

    def getIndex(self, attributeName):
        try:
            return self._attributeNameList.index(attributeName)
        except:
            return -1

    def getItemNameList(self):
        itemNameList = []
        for att in self._attributeNameList:
            itemNameList.append('_' + self._name + '.' + att)

        return itemNameList

    def append(self, row):
        self._rowList.append(row)

    def appendAttribute(self, attributeName):
        attributeNameLC = attributeName.lower()
        if attributeNameLC in self._catalog:
            i = self._attributeNameList.index(self._catalog[attributeNameLC])
            self._attributeNameList[i] = attributeName
            self._catalog[attributeNameLC] = attributeName
        else:
            self._attributeNameList.append(attributeName)
            self._catalog[attributeNameLC] = attributeName
        self._numAttributes = len(self._attributeNameList)

    def appendAttributeExtendRows(self, attributeName):
        attributeNameLC = attributeName.lower()
        if attributeNameLC in self._catalog:
            i = self._attributeNameList.index(self._catalog[attributeNameLC])
            self._attributeNameList[i] = attributeName
            self._catalog[attributeNameLC] = attributeName
            self._DataCategory__lfh.write('Appending existing attribute %s\n' % attributeName)
        else:
            self._attributeNameList.append(attributeName)
            self._catalog[attributeNameLC] = attributeName
        if len(self._rowList) > 0:
            for row in self._rowList:
                row.append('?')

        self._numAttributes = len(self._attributeNameList)

    def getValue(self, attributeName=None, rowIndex=None):
        if attributeName is None:
            attribute = self._DataCategory__currentAttribute
        else:
            attribute = attributeName
        if rowIndex is None:
            rowI = self._DataCategory__currentRowIndex
        else:
            rowI = rowIndex
        if isinstance(attribute, str):
            if isinstance(rowI, int):
                try:
                    return self._rowList[rowI][self._attributeNameList.index(attribute)]
                except IndexError:
                    raise IndexError

        raise IndexError(str(attribute))

    def setValue(self, value, attributeName=None, rowIndex=None):
        if attributeName is None:
            attribute = self._DataCategory__currentAttribute
        else:
            attribute = attributeName
        if rowIndex is None:
            rowI = self._DataCategory__currentRowIndex
        else:
            rowI = rowIndex
        if isinstance(attribute, str) and isinstance(rowI, int):
            try:
                for ii in range(rowI + 1 - len(self._rowList)):
                    self._rowList.append(self._DataCategory__emptyRow())

                ll = len(self._rowList[rowI])
                ind = self._attributeNameList.index(attribute)
                if ind >= ll:
                    self._rowList[rowI].extend([None for ii in range(2 * ind - ll)])
                self._rowList[rowI][ind] = value
            except IndexError:
                self._DataCategory__lfh.write('DataCategory(setvalue) index error category %s attribute %s index %d value %r\n' % (
                 self._name, attribute, rowI, value))
                traceback.print_exc(file=(self._DataCategory__lfh))
            except ValueError:
                self._DataCategory__lfh.write('DataCategory(setvalue) value error category %s attribute %s index %d value %r\n' % (
                 self._name, attribute, rowI, value))
                traceback.print_exc(file=(self._DataCategory__lfh))

    def __emptyRow(self):
        return [None for ii in range(len(self._attributeNameList))]

    def replaceValue(self, oldValue, newValue, attributeName):
        numReplace = 0
        if attributeName not in self._attributeNameList:
            return numReplace
        else:
            ind = self._attributeNameList.index(attributeName)
            for row in self._rowList:
                if row[ind] == oldValue:
                    row[ind] = newValue
                    numReplace += 1

            return numReplace

    def replaceSubstring(self, oldValue, newValue, attributeName):
        ok = False
        if attributeName not in self._attributeNameList:
            return ok
        else:
            ind = self._attributeNameList.index(attributeName)
            for row in self._rowList:
                val = row[ind]
                row[ind] = val.replace(oldValue, newValue)
                if val != row[ind]:
                    ok = True

            return ok

    def invokeAttributeMethod(self, attributeName, type, method, db):
        self._DataCategory__currentRowIndex = 0
        self._DataCategory__currentAttribute = attributeName
        self.appendAttribute(attributeName)
        ind = self._attributeNameList.index(attributeName)
        if len(self._rowList) == 0:
            row = [None for ii in range(len(self._attributeNameList) * 2)]
            row[ind] = None
            self._rowList.append(row)
        for row in self._rowList:
            ll = len(row)
            if ind >= ll:
                row.extend([None for ii in range(2 * ind - ll)])
                row[ind] = None
            exec(method.getInline())
            self._DataCategory__currentRowIndex += 1

    def invokeCategoryMethod(self, type, method, db):
        self._DataCategory__currentRowIndex = 0
        exec(method.getInline())

    def getAttributeLengthMaximumList(self):
        mList = [0 for i in len(self._attributeNameList)]
        for row in self._rowList:
            for indx, val in enumerate(row):
                mList[indx] = max(mList[indx], len(val))

        return mList

    def renameAttribute(self, curAttributeName, newAttributeName):
        """ Change the name of an attribute in place -
        """
        try:
            i = self._attributeNameList.index(curAttributeName)
            self._attributeNameList[i] = newAttributeName
            del self._catalog[curAttributeName.lower()]
            self._catalog[newAttributeName.lower()] = newAttributeName
            return True
        except:
            return False

    def printIt(self, fh=sys.stdout):
        fh.write('--------------------------------------------\n')
        fh.write('  Category: %s attribute list length: %d\n' % (
         self._name, len(self._attributeNameList)))
        for at in self._attributeNameList:
            fh.write('  Category: %s attribute: %s\n' % (self._name, at))

        fh.write('  Row value list length: %d\n' % len(self._rowList))
        for row in self._rowList[:2]:
            if len(row) == len(self._attributeNameList):
                for ii, v in enumerate(row):
                    fh.write('        %30s: %s ...\n' % (self._attributeNameList[ii], str(v)[:30]))

            else:
                fh.write('+WARNING - %s data length %d attribute name length %s mismatched\n' % (
                 self._name, len(row), len(self._attributeNameList)))

    def dumpIt(self, fh=sys.stdout):
        fh.write('--------------------------------------------\n')
        fh.write('  Category: %s attribute list length: %d\n' % (
         self._name, len(self._attributeNameList)))
        for at in self._attributeNameList:
            fh.write('  Category: %s attribute: %s\n' % (self._name, at))

        fh.write('  Value list length: %d\n' % len(self._rowList))
        for row in self._rowList:
            for ii, v in enumerate(row):
                fh.write('        %30s: %s\n' % (self._attributeNameList[ii], v))

    def __formatPdbx(self, inp):
        """ Format input data following PDBx quoting rules - 
        """
        try:
            if inp is None:
                return ('?', 'DT_NULL_VALUE')
            else:
                if isinstance(inp, int) or self._DataCategory__intRe.search(str(inp)):
                    return ([str(inp)], 'DT_INTEGER')
                else:
                    if isinstance(inp, float) or self._DataCategory__floatRe.search(str(inp)):
                        return (
                         [
                          str(inp)], 'DT_FLOAT')
                    else:
                        if inp == '.' or inp == '?':
                            return ([inp], 'DT_NULL_VALUE')
                        else:
                            if inp == '':
                                return (
                                 [
                                  '.'], 'DT_NULL_VALUE')
                            else:
                                if not self._DataCategory__wsAndQuotesRe.search(inp):
                                    if inp.startswith('_'):
                                        return (self._DataCategory__doubleQuotedList(inp), 'DT_ITEM_NAME')
                                    else:
                                        return (
                                         [
                                          str(inp)], 'DT_UNQUOTED_STRING')
                                else:
                                    if self._DataCategory__nlRe.search(inp):
                                        return (
                                         self._DataCategory__semiColonQuotedList(inp), 'DT_MULTI_LINE_STRING')
                                    if self._DataCategory__avoidEmbeddedQuoting:
                                        if not self._DataCategory__dqRe.search(inp):
                                            if not self._DataCategory__sqWsRe.search(inp):
                                                return (
                                                 self._DataCategory__doubleQuotedList(inp), 'DT_DOUBLE_QUOTED_STRING')
                                        if not self._DataCategory__sqRe.search(inp):
                                            if not self._DataCategory__dqWsRe.search(inp):
                                                return (
                                                 self._DataCategory__singleQuotedList(inp), 'DT_SINGLE_QUOTED_STRING')
                                        return (
                                         self._DataCategory__semiColonQuotedList(inp), 'DT_MULTI_LINE_STRING')
                                    elif not self._DataCategory__dqRe.search(inp):
                                        return (
                                         self._DataCategory__doubleQuotedList(inp), 'DT_DOUBLE_QUOTED_STRING')
                            return self._DataCategory__sqRe.search(inp) or (
                             self._DataCategory__singleQuotedList(inp), 'DT_SINGLE_QUOTED_STRING')
                    return (
                     self._DataCategory__semiColonQuotedList(inp), 'DT_MULTI_LINE_STRING')
        except:
            traceback.print_exc(file=(self._DataCategory__lfh))

    def __dataTypePdbx(self, inp):
        """ Detect the PDBx data type - 
        """
        if inp is None:
            return 'DT_NULL_VALUE'
        else:
            if isinstance(inp, int) or self._DataCategory__intRe.search(str(inp)):
                return 'DT_INTEGER'
            else:
                if isinstance(inp, float) or self._DataCategory__floatRe.search(str(inp)):
                    return 'DT_FLOAT'
                else:
                    if inp == '.' or inp == '?':
                        return 'DT_NULL_VALUE'
                    else:
                        if inp == '':
                            return 'DT_NULL_VALUE'
                        else:
                            if not self._DataCategory__wsAndQuotesRe.search(inp):
                                if inp.startswith('_'):
                                    return 'DT_ITEM_NAME'
                                else:
                                    return 'DT_UNQUOTED_STRING'
                            else:
                                if self._DataCategory__nlRe.search(inp):
                                    return 'DT_MULTI_LINE_STRING'
                                if self._DataCategory__avoidEmbeddedQuoting:
                                    if not self._DataCategory__sqRe.search(inp):
                                        if not self._DataCategory__dqWsRe.search(inp):
                                            return 'DT_DOUBLE_QUOTED_STRING'
                                    if not self._DataCategory__dqRe.search(inp):
                                        if not self._DataCategory__sqWsRe.search(inp):
                                            return 'DT_SINGLE_QUOTED_STRING'
                                    return 'DT_MULTI_LINE_STRING'
                                elif not self._DataCategory__sqRe.search(inp):
                                    return 'DT_DOUBLE_QUOTED_STRING'
                        return self._DataCategory__dqRe.search(inp) or 'DT_SINGLE_QUOTED_STRING'
                return 'DT_MULTI_LINE_STRING'

    def __singleQuotedList(self, inp):
        l = []
        l.append("'")
        l.append(inp)
        l.append("'")
        return l

    def __doubleQuotedList(self, inp):
        l = []
        l.append('"')
        l.append(inp)
        l.append('"')
        return l

    def __semiColonQuotedList(self, inp):
        l = []
        l.append('\n')
        if inp[(-1)] == '\n':
            l.append(';')
            l.append(inp)
            l.append(';')
            l.append('\n')
        else:
            l.append(';')
            l.append(inp)
            l.append('\n')
            l.append(';')
            l.append('\n')
        return l

    def getValueFormatted(self, attributeName=None, rowIndex=None):
        if attributeName is None:
            attribute = self._DataCategory__currentAttribute
        else:
            attribute = attributeName
        if rowIndex is None:
            rowI = self._DataCategory__currentRowIndex
        else:
            rowI = rowIndex
        if isinstance(attribute, str):
            if isinstance(rowI, int):
                try:
                    list, type = self._DataCategory__formatPdbx(self._rowList[rowI][self._attributeNameList.index(attribute)])
                    return ''.join(list)
                except IndexError:
                    self._DataCategory__lfh.write('attributeName %s rowI %r rowdata %r\n' % (attributeName, rowI, self._rowList[rowI]))
                    raise IndexError

        raise TypeError(str(attribute))

    def getValueFormattedByIndex(self, attributeIndex, rowIndex):
        try:
            list, type = self._DataCategory__formatPdbx(self._rowList[rowIndex][attributeIndex])
            return ''.join(list)
        except IndexError:
            raise IndexError

    def getAttributeValueMaxLengthList(self, steps=1):
        mList = [0 for i in range(len(self._attributeNameList))]
        for row in self._rowList[::steps]:
            for indx in range(len(self._attributeNameList)):
                val = row[indx]
                mList[indx] = max(mList[indx], len(str(val)))

        return mList

    def getFormatTypeList(self, steps=1):
        try:
            curDataTypeList = ['DT_NULL_VALUE' for i in range(len(self._attributeNameList))]
            for row in self._rowList[::steps]:
                for indx in range(len(self._attributeNameList)):
                    val = row[indx]
                    dType = self._DataCategory__dataTypePdbx(val)
                    dIndx = self._DataCategory__dataTypeList.index(dType)
                    cType = curDataTypeList[indx]
                    cIndx = self._DataCategory__dataTypeList.index(cType)
                    cIndx = max(cIndx, dIndx)
                    curDataTypeList[indx] = self._DataCategory__dataTypeList[cIndx]

            curFormatTypeList = []
            for dt in curDataTypeList:
                ii = self._DataCategory__dataTypeList.index(dt)
                curFormatTypeList.append(self._DataCategory__formatTypeList[ii])

        except:
            self._DataCategory__lfh.write('PdbxDataCategory(getFormatTypeList) ++Index error at index %d in row %r\n' % (indx, row))

        return (curFormatTypeList, curDataTypeList)

    def getFormatTypeListX(self):
        curDataTypeList = ['DT_NULL_VALUE' for i in range(len(self._attributeNameList))]
        for row in self._rowList:
            for indx in range(len(self._attributeNameList)):
                val = row[indx]
                dType = self._DataCategory__dataTypePdbx(val)
                dIndx = self._DataCategory__dataTypeList.index(dType)
                cType = curDataTypeList[indx]
                cIndx = self._DataCategory__dataTypeList.index(cType)
                cIndx = max(cIndx, dIndx)
                curDataTypeList[indx] = self._DataCategory__dataTypeList[cIndx]

        curFormatTypeList = []
        for dt in curDataTypeList:
            ii = self._DataCategory__dataTypeList.index(dt)
            curFormatTypeList.append(self._DataCategory__formatTypeList[ii])

        return (
         curFormatTypeList, curDataTypeList)