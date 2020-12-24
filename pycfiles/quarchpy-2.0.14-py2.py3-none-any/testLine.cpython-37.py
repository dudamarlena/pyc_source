# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Users\sboon\AppData\Local\Temp\pip-install-ptdbtr91\quarchpy\quarchpy\disk_test\testLine.py
# Compiled at: 2020-03-25 05:10:07
# Size of source mod 2**32: 2321 bytes
import xml.etree

class testLine:
    __doc__ = '\n    Init function taking all parameters\n    '

    def __init__(self):
        self.lineType = None
        self.testName = None
        self.moduleName = None
        self.paramList = {}

    def initFromXml(self, xmlTree):
        if xmlTree.tag != 'RemoteCommand':
            raise ValueError('XML tree does not contain the required root value (RemoteCommand)')
        self.lineType = xmlTree.find('LineType').text
        self.testName = xmlTree.find('Function').text
        self.moduleName = xmlTree.find('Module').text
        newItem = xmlTree.iter()
        newItem2 = []
        for elem in newItem:
            if 'key' in elem.tag or 'value' in elem.tag:
                newItem2.append(elem.text)

        skipElement = ''
        if newItem2:
            for x, elem in enumerate(newItem2):
                if skipElement == x:
                    continue
                self.paramList.update({elem: newItem2[(x + 1)]})
                skipElement = x + 1

        if self.lineType == None:
            raise ValueError("Remote command 'type' not set")
        if self.testName == None:
            raise ValueError("Remote command 'name' not set")
        if self.moduleName == None:
            raise ValueError("Remote command 'module' not set")