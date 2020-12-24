# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\sboon\AppData\Local\Temp\pip-install-ptdbtr91\quarchpy\quarchpy\user_interface\user_interface.py
# Compiled at: 2020-03-25 05:10:07
# Size of source mod 2**32: 22006 bytes
"""
This module provides standard user interface elements to quarchpy functions, ensuring common style
and support for both terminal and TestCenter (quarch internal) execution

"""
from __future__ import print_function
import sys, os, math
from quarchpy.utilities import TestCenter

class User_interface:
    __doc__ = '\n    This class is a singleton pattern and provides common access to the user interace for user\n    interaction.  The UI can be the terminal or TestCenter\n    '
    instance = None

    class __user_interface:

        def __init__(self, ui):
            if ui in ('console', 'testcenter'):
                self.selectedInterface = ui
            else:
                raise ValueError('requested ui type not valid')

    def __init__(self, ui):
        """
        """
        if not User_interface.instance:
            User_interface.instance = User_interface._User_interface__user_interface(ui)
        else:
            User_interface.instance.selectedInterface = ui


def listSelection(title='', message='', selectionList=[], additionalOptions=[], nice=False, tableHeaders=[], indexReq=True, align='l'):
    if User_interface.instance != None:
        if User_interface.instance.selectedInterface == 'testcenter':
            return TestCenter.testPoint('Quarch_Host.ShowGenericDialog', 'Title=' + __formatForTestcenter(title), 'Message=' + __formatForTestcenter(message), 'ItemListString=' + __formatForTestcenter(selectionList), 'OptionListString=' + __formatForTestcenter(str(additionalOptions)))
    if message not in '':
        print(message)
    if nice is True:
        retVal = niceListSelection(selectionList, tableHeaders=tableHeaders, indexReq=indexReq, additionalOptions=additionalOptions, align=align)
        return retVal
    selectionList = selectionList.split(',')
    selectionList = [str(x).split('=') for x in selectionList]
    count = 1
    for item in selectionList:
        if len(item) > 1:
            print(str(count) + ' - ' + item[1])
        else:
            print(item[0])
        count += 1

    print('')
    while True:
        if sys.version_info.major >= 3:
            userStr = input('Please select an option:\n>')
        else:
            userStr = raw_input('Please select an option:\n>')
        try:
            userNumber = int(userStr)
            if userNumber <= len(selectionList):
                if userNumber >= 1:
                    break
        except:
            print('INVALID SELECTION!')

    return selectionList[(userNumber - 1)][0]


def niceListSelection(selectionList, title='', message='', tableHeaders=None, indexReq=True, additionalOptions=None, align='l'):
    try:
        selectionList = selectionList.copy()
        additionalOptions = additionalOptions.copy()
        tableHeaders = tableHeaders.copy()
    except:
        pass

    if additionalOptions is not None:
        if additionalOptions.__len__() > 0:
            if isinstance(additionalOptions, str):
                additionalOptions = additionalOptions.split(',')
            selectionList += additionalOptions
    elif isinstance(selectionList, str):
        selectionList = selectionList.split(',')
    else:
        if isinstance(selectionList, dict):
            selectionList = dictToList(selectionList)
    displayTable(selectionList, indexReq=indexReq, tableHeaders=tableHeaders, align=align)
    print('')
    while True:
        if sys.version_info.major >= 3:
            userStr = input('Please select an option:\n>')
        else:
            userStr = raw_input('Please select an option:\n>')
        try:
            userNumber = int(userStr)
            if userNumber <= len(selectionList):
                if userNumber >= 1:
                    break
        except:
            print('INVALID SELECTION!')

    return selectionList[(userNumber - 1)]


def printText(text, fillLine=False, terminalWidth=100, fill=' ', **kwargs):
    if User_interface.instance != None and User_interface.instance.selectedInterface == 'testcenter':
        if text.strip() != '':
            TestCenter.testPoint('Quarch_Host.LogComment', 'Message=' + __formatForTestcenter(text))
    elif fillLine:
        text += fill * (terminalWidth - len(text))
    elif kwargs != {}:
        print(text, **kwargs)
    else:
        print(text)


def showDialog(message='', title=''):
    if User_interface.instance != None and User_interface.instance.selectedInterface == 'testcenter':
        TestCenter.testPoint('Quarch_Host.ShowDialog', 'Title=' + __formatForTestcenter(title), 'Message=' + __formatForTestcenter(message))
    else:
        print(message)
        if sys.version_info.major >= 3:
            userStr = input('Press enter to continue\n>')
        else:
            userStr = raw_input('Press enter to continue\n>')


def progressBar(iteration, total, prefix='', suffix='', decimals=1, fill='█', fullWidth=100):
    if iteration >= 0:
        if total > 0:
            if User_interface.instance != None and User_interface.instance.selectedInterface == 'testcenter':
                TestCenter.testPoint('Quarch_Host.ShowTaskProgress', 'Title=Task Progress', 'Iteration=' + str(iteration), 'Total=' + str(total))
            else:
                percent = ('{0:.' + str(decimals) + 'f}').format(100 * (iteration / float(total)))
                length = fullWidth - (len(prefix) + len(suffix) + len(percent) + 4)
                filledLength = int(length * iteration // total)
                bar = fill * filledLength + '-' * (length - filledLength)
                print(('%s|%s|%s%%%s' % (prefix, bar, percent, suffix)), end='\r')
                if iteration >= total:
                    print()


def startTestBlock(text):
    if User_interface.instance != None:
        if User_interface.instance.selectedInterface == 'testcenter':
            return TestCenter.beginTestBlock(__formatForTestcenter(text))
    print('')
    print(text)
    return


def endTestBlock():
    if User_interface.instance != None:
        if User_interface.instance.selectedInterface == 'testcenter':
            return TestCenter.endTestBlock()
    return


def logCalibrationResult(title, report):
    if User_interface.instance != None and User_interface.instance.selectedInterface == 'testcenter':
        if report['result']:
            TestCenter.testPoint('Quarch_Host.LogTestPoint', 'Test=' + __formatForTestcenter(title), 'Result=True', 'Message=' + __formatForTestcenter(title) + ' Passed, worst case: ' + __formatForTestcenter(report['worst case']))
            for line in report['report'].splitlines():
                TestCenter.testPoint('Quarch_Host.LogComment', 'Message=' + __formatForTestcenter(line))

            TestCenter.endTestBlock()
        else:
            TestCenter.testPoint('Quarch_Host.LogTestPoint', 'Test=' + __formatForTestcenter(title), 'Result=False', 'Message=' + __formatForTestcenter(title) + ' Failed, worst case: ' + __formatForTestcenter(report['worst case']))
            for line in report['report'].splitlines():
                TestCenter.testPoint('Quarch_Host.LogComment', 'Message=' + __formatForTestcenter(line))

            TestCenter.endTestBlock()
    else:
        if report['result']:
            print('\t' + title + ' Passed')
            print('\tworst case: ' + report['worst case'])
        else:
            print('\t' + title + ' Failed')
            print('')
            data = report['report']
            print(data)


def logSimpleResult(title, result):
    if User_interface.instance != None:
        if User_interface.instance.selectedInterface == 'testcenter':
            if result:
                TestCenter.testPoint('Quarch_Host.LogTestPoint', 'Test=' + __formatForTestcenter(title), 'Result=True', 'Message=' + __formatForTestcenter(title))
        else:
            TestCenter.testPoint('Quarch_Host.LogTestPoint', 'Test=' + __formatForTestcenter(title), 'Result=False', 'Message=' + __formatForTestcenter(title))
    elif result:
        print('\t' + title + ' Passed')
    else:
        print('\t' + title + ' Failed')


def logResults(test, notes):
    if User_interface.instance != None and User_interface.instance.selectedInterface == 'testcenter':
        TestCenter.testPoint('Quarch_Host.ResultDialog', 'Test=' + __formatForTestcenter(test), 'Notes=' + __formatForTestcenter(notes))
    else:
        print(notes)


def storeDeviceInfo(**kwargs):
    if User_interface.instance != None:
        if User_interface.instance.selectedInterface == 'testcenter':
            if 'serial' in kwargs:
                TestCenter.testPoint('Quarch_Internal.StoreSerial', 'Serial=' + kwargs['serial'])
            if 'idn' in kwargs:
                IDNString = '|'.join(kwargs['idn'].splitlines())
                TestCenter.testPoint('Quarch_Internal.StoreDutActualIdn', 'Idn=' + IDNString)


def requestDialog(title='', message='', desiredType=None, minRange=None, maxRange=None, defaultUserInput=''):
    validValue = False
    if desiredType != None:
        if desiredType.lower() == 'string':
            desiredType = None
    while validValue == False:
        if User_interface.instance != None and User_interface.instance.selectedInterface == 'testcenter':
            userStr = TestCenter.testPoint('Quarch_Host.ShowRequestDialog', 'Title= ' + __formatForTestcenter(title), 'Message=' + __formatForTestcenter(message))
        else:
            if sys.version_info.major >= 3:
                userStr = input(message + '\n>')
            else:
                userStr = raw_input(message + '\n>')
        if userStr == '':
            userStr = defaultUserInput
        validValue = validateUserInput(userStr, desiredType, minRange, maxRange)

    return userStr


def validateUserInput(userStr, desiredType, minRange, maxRange):
    validValue = False
    if desiredType == None:
        validValue = True
    if desiredType == 'float':
        try:
            userStr = float(userStr)
            if not minRange != None or maxRange != None and (userStr < minRange or userStr > maxRange):
                validValue = False
            else:
                validValue = True
        except:
            pass

    else:
        if desiredType == 'int':
            try:
                userStr = int(userStr)
                if not minRange != None or maxRange != None and (userStr < minRange or userStr > maxRange):
                    validValue = False
                else:
                    validValue = True
            except:
                pass

        else:
            if desiredType == 'path':
                if os.path.isdir(userStr) == False:
                    validValue = False
                else:
                    validValue = True
            elif validValue == False:
                printText(str(userStr) + ' is not a valid ' + str(desiredType))
                if minRange != None and maxRange != None:
                    printText('Please enter a ' + str(desiredType) + ' between ' + str(minRange) + ' and ' + str(maxRange))
                else:
                    printText('Please enter a valid ' + str(desiredType))
            return validValue


def userRangeIntSelection(inputString, intLength=3):
    inputList = inputString.split(',')
    returnList = []
    for item in inputList:
        if '-' in item:
            myRange = item.split('-')
            myRange = range(int(myRange[0]), int(myRange[1]) + 1)
            returnList.extend(myRange)

    for i, item in enumerate(returnList):
        returnList[i] = str(item)
        if intLength != None:
            returnList[i] = returnList[i].zfill(intLength)

    return returnList


def displayTable(tableData=[
 [
  '']], message='', tableHeaders=None, indexReq=False, printToConsole=True, align='l'):
    retVal = ''
    try:
        tableData = tableData.copy()
        if tableHeaders is not None:
            tableHeaders = tableHeaders.copy()
    except:
        pass

    if isinstance(tableData, str):
        tableData = tableData.split(',')
    else:
        if isinstance(tableData, dict):
            tableData = dictToList(tableData)
        else:
            try:
                if not isinstance(tableData[0], tuple):
                    if not isinstance(tableData[0], list):
                        if not isinstance(tableData[0], dict):
                            tempList = list()
                            for item in tableData:
                                tempList.append(list([item]))

                            tableData = tempList
            except:
                pass

        if message != '':
            print(message)
        if indexReq:
            if tableHeaders is not None:
                tableHeaders.insert(0, '#')
            counter = 1
            for rows in tableData:
                rows.insert(0, counter)
                counter += 1

        columnWidths = []
        itemLegnth = 0
        for rowData in tableData:
            index = 0
            for item in rowData:
                itemLegnth = len(str(item))
                try:
                    if columnWidths[index] < itemLegnth:
                        columnWidths[index] = itemLegnth
                except:
                    columnWidths.append(itemLegnth)

                index += 1

        if tableHeaders is not None:
            index = 0
            for item in tableHeaders:
                itemLegnth = len(str(item))
                try:
                    if columnWidths[index] < itemLegnth:
                        columnWidths[index] = itemLegnth
                except:
                    columnWidths.append(itemLegnth)

                index += 1

        topEdge = '╔'
        middleEdge = '╠'
        bottomEdge = '╚'
        firstLoop = True
        for columnWidth in columnWidths:
            if firstLoop is False:
                topEdge += '╦'
                middleEdge += '╬'
                bottomEdge += '╩'
            topEdge += '═' * (columnWidth + 2)
            middleEdge += '═' * (columnWidth + 2)
            bottomEdge += '═' * (columnWidth + 2)
            firstLoop = False

        topEdge = topEdge + '╗'
        middleEdge = middleEdge + '╣'
        bottomEdge = bottomEdge + '╝'
        if tableHeaders is not None:
            rowString = '║'
            index = 0
            retVal += topEdge + '\r\n'
            for item in tableHeaders:
                spaces = columnWidths[index] - len(str(item)) + 2
                if align.lower() in 'l':
                    rowString += str(item) + ' ' * spaces + '║'
                else:
                    if align.lower() in 'c':
                        prefix = ' ' * math.floor(spaces / 2)
                        suffix = ' ' * math.ceil(spaces / 2)
                        rowString += prefix + str(item) + suffix + '║'
                    else:
                        if align.lower() in 'r':
                            rowString += ' ' * spaces + str(item) + '║'
                        index += 1

            retVal += rowString + '\r\n'
        retVal += middleEdge + '\r\n'
        for rowData in tableData:
            index = 0
            rowString = '║'
            for item in rowData:
                spaces = columnWidths[index] - len(str(item)) + 2
                if align.lower() in 'l':
                    rowString += str(item) + ' ' * spaces + '║'
                else:
                    if align.lower() in 'c':
                        prefix = ' ' * math.floor(spaces / 2)
                        suffix = ' ' * math.ceil(spaces / 2)
                        rowString += prefix + str(item) + suffix + '║'
                    else:
                        if align.lower() in 'r':
                            rowString += ' ' * spaces + str(item) + '║'
                        index += 1

            retVal += rowString + '\r\n'

        retVal += bottomEdge
        if printToConsole:
            printText(retVal)
        return retVal


def dictToList(tableData):
    tempList = []
    tempEl = []
    for k, v in tableData.items():
        tempEl = []
        tempEl.append(v)
        tempEl.append(k)
        tempList.append(tempEl)

    tableData = tempList
    return tableData


def __formatForTestcenter(text):
    text = text.replace('\\', '\\\\')
    text = text.replace('\x07', '')
    text = '|'.join(text.splitlines())
    return text