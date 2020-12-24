# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/_nmf/widgets/OWMissingValues.py
# Compiled at: 2013-02-14 09:12:45
"""
<name>Missing Values Indicator</name>
<description>Detection of Missing Values</description>
<icon>icons/MissingIcon.png</icon>
<priority>30</priority>
"""
import numpy as np
from OWWidget import *
import OWGUI

class OWMissingValues(OWWidget):
    settingsList = []

    def __init__(self, parent=None, signalManager=None):
        OWWidget.__init__(self, parent, signalManager, 'Missing Values Indicator')
        self.inputs = [
         (
          'Data', ExampleTable, self.data)]
        self.outputs = [('Missing Values Indicator', ExampleTable)]
        self.loadSettings()
        box = OWGUI.widgetBox(self.controlArea, 'Info')
        self.infoa = OWGUI.widgetLabel(box, 'No data on input yet, waiting to get something.')
        self.infob = OWGUI.widgetLabel(box, '')
        OWGUI.separator(self.controlArea)
        OWGUI.button(self.controlArea, self, 'Commit', callback=self.commit)
        self.resize(100, 50)

    def data(self, dataset):
        if dataset:
            self.dataset = dataset
            self.infoa.setText('%d variables in input data set' % len(dataset[0]))
            self.infob.setText('%d observations in input data set' % len(dataset))
        else:
            self.send('Missing Values Indicator', None)
            self.infoa.setText('No data on input yet, waiting to get something.')
            self.infob.setText('')
        return

    def commit(self):
        indic = np.ones([len(self.dataset), len(self.dataset[0])])
        for i in range(0, len(self.dataset)):
            for j in range(0, len(self.dataset[0])):
                if self.dataset[i][j].isSpecial():
                    indic[i][j] = 0

        self.outputData = indic
        domainX = self.dataset.domain
        self.outputData = Orange.data.Table(domainX, np.array(self.outputData))
        for i in range(0, len(self.dataset)):
            self.outputData[i]['ID'] = self.dataset[i]['ID']

        self.send('Missing Values Indicator', self.outputData)


if __name__ == '__main__':
    appl = QApplication(sys.argv)
    ow = OWMissingValues()
    ow.show()
    dataset = orange.ExampleTable('C:/Users/Fajwel/Dropbox/Orange/testMissingData.txt')
    ow.data(dataset)
    appl.exec_()