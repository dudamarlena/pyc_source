# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/_nmf/widgets/OWPivotData.py
# Compiled at: 2013-02-14 09:13:46
"""
<name>Pivot Data</name>
<description>Pivot data</description>
<icon>icons/PivotIcon.png</icon>
<priority>30</priority>
"""
import numpy as np
from OWWidget import *
import OWGUI

class OWPivotData(OWWidget):
    settingsList = []

    def __init__(self, parent=None, signalManager=None):
        OWWidget.__init__(self, parent, signalManager, 'Pivot Data')
        self.inputs = [
         (
          'Data', ExampleTable, self.data)]
        self.outputs = [('Pivoted Data', ExampleTable)]
        self.loadSettings()
        box = OWGUI.widgetBox(self.controlArea, 'Info')
        self.infoa = OWGUI.widgetLabel(box, 'No data on input yet, waiting to get something.')
        self.infob = OWGUI.widgetLabel(box, '')
        OWGUI.separator(self.controlArea)
        OWGUI.button(self.controlArea, self, 'Pivot long', callback=self.pivotLong)
        OWGUI.button(self.controlArea, self, 'Pivot short', callback=self.pivotShort)
        self.resize(100, 50)

    def data(self, dataset):
        if dataset:
            self.dataset = dataset
            self.infoa.setText('%d variables in input data set' % len(dataset[0]))
            self.infob.setText('%d observations in input data set' % len(dataset))
        else:
            self.send('Pivoted Data', None)
            self.infoa.setText('No data on input yet, waiting to get something.')
            self.infob.setText('')
        return

    def pivotLong(self):
        self.outputData = []
        colVal = []
        colNames = []
        colID = []
        for j in range(0, len(self.dataset.domain)):
            for i in range(0, len(self.dataset)):
                colVal.append(self.dataset[i][j].value)
                colNames.append(self.dataset.domain[j].name)
                colID.append(self.dataset[i]['ID'].value)

        self.outputData = map(list, zip(*[colVal]))
        dom = [Orange.feature.Continuous('Value')]
        dom = Orange.data.Domain(dom, 0)
        dom.addmetas(self.dataset.domain.getmetas())
        newid = Orange.feature.Descriptor.new_meta_id()
        dom.add_meta(newid, Orange.feature.String('Names'))
        self.outputData = Orange.data.Table(dom, self.outputData)
        for i in range(0, len(self.outputData)):
            self.outputData[i]['ID'] = colID[i]
            self.outputData[i]['Names'] = colNames[i]

        self.send('Pivoted Data', self.outputData)

    def pivotShort(self):
        self.outputData = []
        domList = []
        nameMeta = self.dataset.domain.getmetas().values()
        if nameMeta[0].name == 'ID':
            nameMeta = nameMeta[1].name
        else:
            nameMeta = nameMeta[0].name
        i = 0
        while i < len(self.dataset):
            col = []
            nameCol = self.dataset[i][nameMeta].value
            domList.append(Orange.feature.Continuous(nameCol))
            while i < len(self.dataset) and self.dataset[i][nameMeta].value == nameCol:
                col.append(self.dataset[i][0].value)
                i += 1

            self.outputData.append(col)

        self.outputData = map(list, zip(*self.outputData))
        dom = Orange.data.Domain(domList, 0)
        dom.addmetas(self.dataset.domain.getmetas())
        dom.remove_meta(nameMeta)
        self.outputData = Orange.data.Table(dom, self.outputData)
        for i in range(0, len(self.outputData)):
            self.outputData[i]['ID'] = self.dataset[i]['ID']

        self.send('Pivoted Data', self.outputData)


if __name__ == '__main__':
    appl = QApplication(sys.argv)
    ow = OWPivotData()
    ow.show()
    dataset = orange.ExampleTable('C:/Users/Paul Fogel/Desktop/testPivot.tab')
    ow.data(dataset)
    appl.exec_()