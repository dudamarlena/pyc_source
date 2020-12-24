# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/_multitarget/widgets/OWBinaryRelevance.py
# Compiled at: 2012-11-23 17:14:54
"""
<name>Binary Relevance</name>
<description>Binary relevance learner wrapper</description>
<priority>1000</priority>
<category>Multitarget</category>
<tags>multitarget,binary,relevance,wrapper</tags>
<icon>icons/BinaryRelevance.png</icon>

"""
import Orange, Orange.multitarget
from OWWidget import *
import OWGUI

class OWBinaryRelevance(OWWidget):
    settingsList = [
     'name']

    def __init__(self, parent=None, signalManager=None, title='Binary Relevance'):
        OWWidget.__init__(self, parent, signalManager, title, wantMainArea=False)
        self.inputs = [
         (
          'Data', Orange.data.Table, self.set_data),
         (
          'Base Learner', Orange.classification.Learner,
          self.set_learner)]
        self.outputs = [
         (
          'Learner', Orange.classification.Learner),
         (
          'Classifier', Orange.classification.Classifier)]
        self.name = 'Binary Relevance'
        self.loadSettings()
        box = OWGUI.widgetBox(self.controlArea, 'Learner/Classifier Name')
        OWGUI.lineEdit(box, self, 'name')
        OWGUI.button(self.controlArea, self, '&Apply', callback=self.apply, autoDefault=True)
        self.base_learner = None
        self.data = None
        self.apply()
        return

    def set_data(self, data=None):
        self.error([0])
        if data is not None and not data.domain.class_vars:
            data = None
            self.error(0, 'Input data must have multi target domain.')
        self.data = data
        return

    def set_learner(self, base_learner=None):
        self.base_learner = base_learner

    def handleNewSignals(self):
        self.apply()

    def apply(self):
        learner = None
        if self.base_learner is not None:
            learner = Orange.multitarget.binary.BinaryRelevanceLearner(name=self.name, learner=self.base_learner)
        classifier = None
        if self.data is not None and learner is not None:
            classifier = learner(self.data)
            classifier.name = self.name
        self.send('Learner', learner)
        self.send('Classifier', classifier)
        return


if __name__ == '__main__':
    app = QApplication([])
    w = OWBinaryRelevance()
    data = Orange.data.Table('multitarget:emotions.tab')
    base_learner = Orange.classification.bayes.NaiveLearner()
    w.set_data(data)
    w.set_learner(base_learner)
    w.set_data(None)
    w.set_data(data)
    w.show()
    app.exec_()
    w.saveSettings()