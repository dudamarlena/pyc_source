# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/swails/src/ParmEd/parmed/formats/pdbx/PdbxWriter.py
# Compiled at: 2017-02-11 08:13:06
# Size of source mod 2**32: 6974 bytes
"""
Classes for writing data and dictionary containers in PDBx/mmCIF format.

"""
__docformat__ = 'restructuredtext en'
__author__ = 'John Westbrook'
__email__ = 'jwest@rcsb.rutgers.edu'
__license__ = 'Creative Commons Attribution 3.0 Unported'
__version__ = 'V0.01'
from parmed.utils.six.moves import range
from parmed.formats.pdbx.PdbxContainers import DefinitionContainer, DataContainer
from parmed.exceptions import PdbxError
import sys

class PdbxWriter(object):
    __doc__ = 'Write PDBx data files or dictionaries using the input container\n       or container list.\n    '

    def __init__(self, ofh=sys.stdout):
        self._PdbxWriter__ofh = ofh
        self._PdbxWriter__containerList = []
        self._PdbxWriter__MAXIMUM_LINE_LENGTH = 2048
        self._PdbxWriter__SPACING = 2
        self._PdbxWriter__INDENT_DEFINITION = 3
        self._PdbxWriter__indentSpace = ' ' * self._PdbxWriter__INDENT_DEFINITION
        self._PdbxWriter__doDefinitionIndent = False
        self._PdbxWriter__rowPartition = None

    def setRowPartition(self, numRows):
        """ Maximum number of rows checked for value length and format
        """
        self._PdbxWriter__rowPartition = numRows

    def write(self, containerList):
        self._PdbxWriter__containerList = containerList
        for container in self._PdbxWriter__containerList:
            self.writeContainer(container)

    def writeContainer(self, container):
        indS = ' ' * self._PdbxWriter__INDENT_DEFINITION
        if isinstance(container, DefinitionContainer):
            self._PdbxWriter__write('save_%s\n' % container.getName())
            self._PdbxWriter__doDefinitionIndent = True
            self._PdbxWriter__write(indS + '#\n')
        else:
            if isinstance(container, DataContainer):
                if container.getGlobal():
                    self._PdbxWriter__write('global_\n')
                    self._PdbxWriter__doDefinitionIndent = False
                    self._PdbxWriter__write('\n')
                else:
                    self._PdbxWriter__write('data_%s\n' % container.getName())
                    self._PdbxWriter__doDefinitionIndent = False
                    self._PdbxWriter__write('#\n')
        for nm in container.getObjNameList():
            obj = container.getObj(nm)
            objL = obj.getRowList()
            if len(objL) == 0:
                continue
            else:
                if len(objL) == 1:
                    self._PdbxWriter__writeItemValueFormat(obj)
                elif len(objL) > 1:
                    if len(obj.getAttributeList()) > 0:
                        self._PdbxWriter__writeTableFormat(obj)
                else:
                    raise PdbxError()
            if self._PdbxWriter__doDefinitionIndent:
                self._PdbxWriter__write(indS + '#')
            else:
                self._PdbxWriter__write('#')

        if isinstance(container, DefinitionContainer):
            self._PdbxWriter__write('\nsave_\n')
        self._PdbxWriter__write('#\n')

    def __write(self, st):
        self._PdbxWriter__ofh.write(st)

    def __writeItemValueFormat(self, myCategory):
        attributeNameLengthMax = 0
        for attributeName in myCategory.getAttributeList():
            attributeNameLengthMax = max(attributeNameLengthMax, len(attributeName))

        itemNameLengthMax = self._PdbxWriter__SPACING + len(myCategory.getName()) + attributeNameLengthMax + 2
        lineList = []
        lineList.append('#\n')
        for attributeName, iPos in myCategory.getAttributeListWithOrder():
            if self._PdbxWriter__doDefinitionIndent:
                lineList.append(self._PdbxWriter__indentSpace)
            itemName = '_%s.%s' % (myCategory.getName(), attributeName)
            lineList.append(itemName.ljust(itemNameLengthMax))
            lineList.append(myCategory.getValueFormatted(attributeName, 0))
            lineList.append('\n')

        self._PdbxWriter__write(''.join(lineList))

    def __writeTableFormat(self, myCategory):
        lineList = []
        lineList.append('#\n')
        if self._PdbxWriter__doDefinitionIndent:
            lineList.append(self._PdbxWriter__indentSpace)
        else:
            lineList.append('loop_')
            for attributeName in myCategory.getAttributeList():
                lineList.append('\n')
                if self._PdbxWriter__doDefinitionIndent:
                    lineList.append(self._PdbxWriter__indentSpace)
                itemName = '_%s.%s' % (myCategory.getName(), attributeName)
                lineList.append(itemName)

            self._PdbxWriter__write(''.join(lineList))
            if self._PdbxWriter__rowPartition is not None:
                numSteps = max(1, myCategory.getRowCount() / self._PdbxWriter__rowPartition)
            else:
                numSteps = 1
        formatTypeList, dataTypeList = myCategory.getFormatTypeList(steps=numSteps)
        maxLengthList = myCategory.getAttributeValueMaxLengthList(steps=numSteps)
        spacing = ' ' * self._PdbxWriter__SPACING
        for iRow in range(myCategory.getRowCount()):
            lineList = []
            lineList.append('\n')
            if self._PdbxWriter__doDefinitionIndent:
                lineList.append(self._PdbxWriter__indentSpace + '  ')
            for iAt in range(myCategory.getAttributeCount()):
                formatType = formatTypeList[iAt]
                maxLength = maxLengthList[iAt]
                if formatType == 'FT_UNQUOTED_STRING' or formatType == 'FT_NULL_VALUE':
                    val = myCategory.getValueFormattedByIndex(iAt, iRow)
                    lineList.append(val.ljust(maxLength))
                else:
                    if formatType == 'FT_NUMBER':
                        val = myCategory.getValueFormattedByIndex(iAt, iRow)
                        lineList.append(val.rjust(maxLength))
                    else:
                        if formatType == 'FT_QUOTED_STRING':
                            val = myCategory.getValueFormattedByIndex(iAt, iRow)
                            lineList.append(val.ljust(maxLength + 2))
                        else:
                            if formatType == 'FT_MULTI_LINE_STRING':
                                val = myCategory.getValueFormattedByIndex(iAt, iRow)
                                lineList.append(val)
                lineList.append(spacing)

            self._PdbxWriter__write(''.join(lineList))

        self._PdbxWriter__write('\n')