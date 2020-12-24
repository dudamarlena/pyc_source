# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.7-x86_64/egg/_nmf/widgets/OWNMF.py
# Compiled at: 2013-02-14 09:13:08
"""
<name>NMF</name>
<description>Non negative matrix factorization</description>
<icon>icons/NMFicon.png</icon>
<priority>30</priority>
"""
import nimfa, numpy as np, scipy.stats
from OWWidget import *
import OWGUI, re, os.path
from exceptions import Exception

class OWNMF(OWWidget):
    settingsList = [
     'rank', 'nbIter', 'factorizationMethod', 'initialization', 'displayCluster', 'reorderingOption', 'saveOutputs', 'recentFiles', 'selectedFileName']
    savers = {'.txt': orange.saveTxt, '.tab': orange.saveTabDelimited, '.names': orange.saveC45, 
       '.test': orange.saveC45, '.data': orange.saveC45, '.csv': orange.saveCsv}
    registeredFileTypes = [ ft for ft in orange.getRegisteredFileTypes() if len(ft) > 3 if ft[3] if not ft[0] == 'C50' ]
    dlgFormats = 'Tab-delimited files (*.tab)\nHeaderless tab-delimited (*.txt)\nComma separated (*.csv)\nC4.5 files (*.data)\nRetis files (*.rda *.rdo)\n' + ('\n').join('%s (%s)' % ft[:2] for ft in registeredFileTypes) + '\nAll files(*.*)'
    savers.update(dict((lower(ft[1][1:]), ft[3]) for ft in registeredFileTypes))
    re_filterExtension = re.compile('\\(\\*(?P<ext>\\.[^ )]+)')

    def __init__(self, parent=None, signalManager=None):
        OWWidget.__init__(self, parent, signalManager, 'NMFV7')
        self.inputs = [
         (
          'Data', ExampleTable, self.dataX), ('Xd', ExampleTable, self.dataXd), ('Xa', ExampleTable, self.dataXa), ('Initial_W', ExampleTable, self.dataInitW), ('Initial_H', ExampleTable, self.dataInitH)]
        self.outputs = [('W', ExampleTable), ('H', ExampleTable), ('S', ExampleTable), ('WSH', ExampleTable), ('Residuals', ExampleTable), ('qqplot', ExampleTable), ('Reordered X', ExampleTable), ('Reordered WSH', ExampleTable), ('Reordered residuals', ExampleTable)]
        self.rank = 4
        self.nbIter = 200
        self.factorizationMethod = 0
        self.initialization = 0
        self.displayCluster = 0
        self.reorderingOption = 2
        self.saveOutputs = 1
        self.recentFiles = []
        self.selectedFileName = 'None'
        self.data = None
        self.filename = ''
        self.loadSettings()
        box = OWGUI.widgetBox(self.controlArea, 'Info')
        self.infoa = OWGUI.widgetLabel(box, 'No data on input yet, waiting to get something.')
        self.infob = OWGUI.widgetLabel(box, '')
        OWGUI.separator(self.controlArea)
        self.paramBox = OWGUI.widgetBox(self.controlArea, 'Parameters')
        OWGUI.spin(self.paramBox, self, 'rank', min=1, max=200, step=1, label='Rank', labelWidth=150)
        OWGUI.lineEdit(self.paramBox, self, 'nbIter', label='Number of iterations', labelWidth=150, orientation='horizontal')
        self.methodBox = OWGUI.widgetBox(self.controlArea, 'Factorization Method')
        OWGUI.radioButtonsInBox(self.methodBox, self, 'factorizationMethod', callback=self.setNbIter, btnLabels=[
         'NMF', 'LSNMF', 'SNMF', 'BMF'], tooltips=[
         'Standard Nonnegative Matrix Factorization',
         'Alternating Nonnegative Least Squares Matrix Factorization Using Projected Gradient (bound constrained optimization) method for each subproblem',
         'Sparse Nonnegative Matrix Factorization',
         'Binary Matrix Factorization'])
        self.initBox = OWGUI.widgetBox(self.controlArea, 'Initialization')
        OWGUI.radioButtonsInBox(self.initBox, self, 'initialization', btnLabels=[
         'random_vcol', 'NNDSVD', 'Fixed'], tooltips=[
         'Random initialization of factors',
         'Nonnegative Double Singular Value Decomposition',
         'Fixed (to be done)'])
        self.visualizationBox = OWGUI.widgetBox(self.controlArea, 'Visualization options')
        OWGUI.checkBox(self.visualizationBox, self, 'displayCluster', 'Display cluster in output data')
        self.reorderingBox = OWGUI.widgetBox(self.visualizationBox, 'Reorder')
        OWGUI.radioButtonsInBox(self.reorderingBox, self, 'reorderingOption', btnLabels=[
         'Rows', 'Columns', 'Both rows and columns'], tooltips=[
         'Reorder rows according to W', 'Reorder columns according to H', 'Reorder both rows and columns'])
        OWGUI.button(self.controlArea, self, 'Commit', callback=self.commit)
        self.saveBox = OWGUI.widgetBox(self.controlArea, 'Saving options')
        OWGUI.checkBox(self.saveBox, self, 'saveOutputs', 'Save outputs')
        rfbox = OWGUI.widgetBox(self.saveBox, 'Filename', orientation='horizontal', addSpace=True)
        self.filecombo = OWGUI.comboBox(rfbox, self, 'filename')
        self.filecombo.setMinimumWidth(200)
        button = OWGUI.button(rfbox, self, '...', callback=self.browseFile, disabled=0)
        button.setIcon(self.style().standardIcon(QStyle.SP_DirOpenIcon))
        button.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Fixed)
        self.resend = OWGUI.button(self.saveBox, self, 'Retrieve data', callback=self.resendData, default=True)
        OWGUI.rubber(self.controlArea)
        self.setFilelist()
        self.filecombo.setCurrentIndex(0)
        if self.selectedFileName != '':
            if os.path.exists(self.selectedFileName):
                self.openFile(self.selectedFileName)
            else:
                self.selectedFileName = ''
        self.infob = OWGUI.widgetLabel(box, '')
        self.paramBox.setDisabled(1)
        self.methodBox.setDisabled(1)
        self.initBox.setDisabled(1)
        self.visualizationBox.setDisabled(1)
        self.saveBox.setDisabled(1)
        self.resize(100, 50)
        return

    def dataX(self, dataset):
        if dataset:
            self.dataset = dataset
            self.infoa.setText('%d variables in input data set' % len(dataset[0]))
            self.infob.setText('%d observations in input data set' % len(dataset))
            self.paramBox.setDisabled(0)
            self.methodBox.setDisabled(0)
            self.initBox.setDisabled(0)
            self.visualizationBox.setDisabled(0)
            self.saveBox.setDisabled(0)
        else:
            self.send('W', None)
            self.send('H', None)
            self.send('WSH', None)
            self.send('S', None)
            self.send('Residuals', None)
            self.send('qqplot', None)
            self.send('Reordered X', None)
            self.send('Reordered WSH', None)
            self.send('Reordered residuals', None)
            self.infoa.setText('No data on input yet, waiting to get something.')
            self.infob.setText('')
        return

    def dataXd(self, dataset):
        if not dataset:
            self.Xd = None
        else:
            self.Xd = dataset
        return

    def dataXa(self, dataset):
        if not dataset:
            self.Xa = None
        else:
            self.Xa = dataset
        return

    def dataInitH(self, dataset):
        if not dataset:
            return
        H = dataset.toNumpy()
        H = np.matrix(H[0])
        self.initH = H.transpose

    def dataInitW(self, dataset):
        if not dataset:
            return
        W = dataset.toNumpy()
        W = np.matrix(W[0])
        self.initW = W

    def setNbIter(self):
        if self.factorizationMethod == 0:
            self.nbIter = 200
        elif self.factorizationMethod == 1:
            self.nbIter = 200
        elif self.factorizationMethod == 2:
            self.nbIter = 200
        else:
            self.nbIter = 200

    def runNMF(self):
        V = self.dataset.toNumpy()
        V = np.matrix(V[0])
        methodLabels = ['nmf', 'lsnmf', 'snmf', 'bmf']
        initLabels = ['random_vcol', 'nndsvd', 'fixed']
        if self.initialization == 2:
            fctr = nimfa.mf(V, seed=initLabels[self.initialization], method=methodLabels[self.factorizationMethod], rank=self.rank, max_iter=self.nbIter, W=self.initW, H=self.initH)
        elif self.factorizationMethod == 1:
            fctr = nimfa.mf(V, seed=initLabels[self.initialization], min_residuals=1e-15, method=methodLabels[self.factorizationMethod], rank=self.rank, max_iter=self.nbIter, sub_iter=20, inner_sub_iter=20)
        else:
            fctr = nimfa.mf(V, seed=initLabels[self.initialization], method=methodLabels[self.factorizationMethod], rank=self.rank, max_iter=self.nbIter)
        fctr_res = nimfa.mf_run(fctr)
        W = fctr_res.basis()
        H = fctr_res.coef()
        WH = W * H
        residuals = V - WH
        self.Wnorm = np.array(W)
        self.Hnorm = np.array(H)
        self.S = np.zeros([self.rank, 1])
        nbComp = self.Wnorm.shape[1]
        for j in range(0, nbComp):
            sumw = np.sqrt(sum(self.Wnorm[:, j] ** 2))
            sumh = np.sqrt(sum(self.Hnorm[j, :] ** 2))
            self.Wnorm[:, j] = self.Wnorm[:, j] / sumw
            self.Hnorm[j, :] = self.Hnorm[j, :] / sumh
            self.S[(j, 0)] = sumw * sumh

        self.residualsNP = residuals
        self.WHNP = np.array(WH)
        if self.displayCluster:
            self.clusterCol = np.matrix(self.Wnorm).argmax(1) + 1
            self.clusterCol = np.array(self.clusterCol)
        domainX = self.dataset.domain
        self.HNP = np.transpose(self.Hnorm)
        self.HH = Orange.data.Table(self.HNP)
        if hasattr(self, 'Xa') and self.Xa:
            self.HH = Orange.data.Table([self.HH, self.Xa])
        else:
            self.HH.domain.add_meta(Orange.feature.Descriptor.new_meta_id(), Orange.feature.String('Variable'))
            for i in range(0, len(domainX)):
                self.HH[i]['Variable'] = domainX[i].name

            newDomain = domainX
            domW = []
            for i in range(0, self.rank):
                domW.append(Orange.feature.Continuous('Component %i' % (i + 1)))

            domW = Orange.data.Domain(domW, 0)
            domW.addmetas(domainX.getmetas())
            self.WW = Orange.data.Table(domW, self.Wnorm)
            self.WSH = Orange.data.Table(newDomain, np.array(WH))
            self.S = Orange.data.Table(Orange.data.Domain([Orange.feature.Continuous('Scaling factor')], 0), self.S)
            self.residuals = Orange.data.Table(newDomain, np.array(residuals))
        if self.displayCluster:
            self.clusterCol = self.clusterCol.transpose()[0].tolist()
            for i in range(0, len(self.clusterCol)):
                self.clusterCol[i] = [
                 str(self.clusterCol[i])]

            val = []
            for i in range(1, self.rank + 1):
                val.append(str(i))

            domCluster = Orange.data.Domain([Orange.feature.Discrete('Cluster', values=val)])
            clusterTable = Orange.data.Table(domCluster, self.clusterCol)
            self.WW = Orange.data.Table([self.WW, clusterTable])
            self.WSH = Orange.data.Table([self.WSH, clusterTable])
            self.residuals = Orange.data.Table([self.residuals, clusterTable])
        if hasattr(self, 'Xd') and self.Xd:
            self.WW = Orange.data.Table([self.WW, self.Xd])
            self.WSH = Orange.data.Table([self.WSH, self.Xd])
            self.residuals = Orange.data.Table([self.residuals, self.Xd])
        else:
            for i in range(0, len(self.dataset)):
                self.WW[i]['ID'] = self.dataset[i]['ID']
                self.WSH[i]['ID'] = self.dataset[i]['ID']
                self.residuals[i]['ID'] = self.dataset[i]['ID']

    def calculateQQPlotValues(self):
        nbValues = self.residualsNP.shape[0] * self.residualsNP.shape[1]
        residualsVector = np.array(np.reshape(self.residualsNP, nbValues))[0]
        residualsVector.sort()
        normalQuantilesVector = scipy.stats.norm.ppf(np.linspace(1.0 / nbValues, 1 - 1.0 / nbValues, nbValues), loc=residualsVector.mean(), scale=residualsVector.std())
        self.qqplot = np.array([normalQuantilesVector, residualsVector])
        self.qqplot = self.qqplot.transpose()
        domQQPlot = Orange.data.Domain([Orange.feature.Continuous('normal quantiles'), Orange.feature.Continuous('residuals quantiles')], 0)
        self.qqplot = Orange.data.Table(domQQPlot, self.qqplot)

    def reorder(self):
        if self.reorderingOption == 0:
            orderLines = 1
            orderCol = 0
        elif self.reorderingOption == 1:
            orderLines = 0
            orderCol = 1
        else:
            orderLines = 1
            orderCol = 1
        self.Xordered = self.dataset.toNumpy()[0]
        self.WSHordered = self.WHNP
        self.residualsOrdered = np.array(self.residualsNP)
        varOrdered = Orange.data.Domain(self.dataset.domain)
        IDordered = self.dataset
        if hasattr(self, 'Xd') and self.Xd:
            Xdordered = self.Xd
        if orderLines:
            Wnorm = self.Wnorm
            nbComp = self.Wnorm.shape[1]
            cluster = Wnorm.argmax(1)
            ind = []
            for j in range(0, nbComp):
                ind.append(np.nonzero(cluster == j)[0])

            orderLin = []
            for j in range(0, nbComp):
                indComp = ind[j]
                orderLin.append(indComp[Wnorm[(indComp, j)].argsort()[::-1]])

            finalOrderLin = orderLin[0]
            for j in range(1, nbComp):
                finalOrderLin = np.concatenate((finalOrderLin, orderLin[j]), axis=0)

            self.Xordered = self.Xordered[finalOrderLin, :]
            self.WSHordered = self.WSHordered[finalOrderLin, :]
            self.residualsOrdered = self.residualsOrdered[finalOrderLin, :]
            if self.displayCluster:
                self.clusterCol = np.matrix(Wnorm).argmax(1) + 1
                self.clusterCol = self.clusterCol[finalOrderLin, :]
                self.clusterCol = np.array(self.clusterCol).transpose()[0].tolist()
                for i in range(0, len(self.clusterCol)):
                    self.clusterCol[i] = [
                     str(self.clusterCol[i])]

            finalOrderLin = finalOrderLin.tolist()
            IDordered = Orange.data.Table([self.dataset[finalOrderLin[0]]])
            for i in range(1, len(finalOrderLin)):
                IDordered.append(self.dataset[finalOrderLin[i]])

            if hasattr(self, 'Xd') and self.Xd:
                Xdordered = Orange.data.Table([self.Xd[finalOrderLin[0]]])
                for i in range(1, len(finalOrderLin)):
                    Xdordered.append(self.Xd[finalOrderLin[i]])

                Xdordered = Orange.data.Table(self.Xd.domain, Xdordered)
        if orderCol:
            Hnorm = self.Hnorm.T
            nbComp = Hnorm.shape[1]
            cluster = Hnorm.argmax(1)
            ind = []
            for j in range(0, nbComp):
                ind.append(np.nonzero(cluster == j)[0])

            orderCol = []
            for j in range(0, nbComp):
                indComp = ind[j]
                orderCol.append(indComp[Hnorm[(indComp, j)].argsort()[::-1]])

            finalOrderCol = orderCol[0]
            for j in range(1, nbComp):
                finalOrderCol = np.concatenate((finalOrderCol, orderCol[j]), axis=0)

            self.Xordered = self.Xordered[:, finalOrderCol]
            self.WSHordered = self.WSHordered[:, finalOrderCol]
            self.residualsOrdered = self.residualsOrdered[:, finalOrderCol]
            finalOrderCol = finalOrderCol.tolist()
            varOrdered = [self.dataset.domain[finalOrderCol[0]]]
            for i in range(1, len(self.dataset.domain)):
                varOrdered.append(self.dataset.domain[finalOrderCol[i]])

            varOrdered = Orange.data.Domain(varOrdered, 0)
            varOrdered.addmetas(self.dataset.domain.getmetas())
        if self.displayCluster:
            val = []
            for i in range(1, self.rank + 1):
                val.append(str(i))

            domCluster = Orange.data.Domain([Orange.feature.Discrete('Cluster', values=val)])
            clusterTable = Orange.data.Table(domCluster, self.clusterCol)
        self.Xordered = Orange.data.Table(varOrdered, np.array(self.Xordered))
        self.WSHordered = Orange.data.Table(varOrdered, np.array(self.WSHordered))
        self.residualsOrdered = Orange.data.Table(varOrdered, np.array(self.residualsOrdered))
        if self.displayCluster:
            self.Xordered = Orange.data.Table([self.Xordered, clusterTable])
            self.WSHordered = Orange.data.Table([self.WSHordered, clusterTable])
            self.residualsOrdered = Orange.data.Table([self.residualsOrdered, clusterTable])
        if hasattr(self, 'Xd') and self.Xd:
            self.Xordered = Orange.data.Table([self.Xordered, Xdordered])
            self.WSHordered = Orange.data.Table([self.WSHordered, Xdordered])
            self.residualsOrdered = Orange.data.Table([self.residualsOrdered, Xdordered])
        else:
            for i in range(0, len(self.dataset)):
                self.Xordered[i]['ID'] = IDordered[i]['ID']
                self.WSHordered[i]['ID'] = IDordered[i]['ID']
                self.residualsOrdered[i]['ID'] = IDordered[i]['ID']

    def browseFile(self):
        if self.recentFiles:
            startfile = self.recentFiles[0]
        else:
            startfile = os.path.expanduser('~/')
        filename, selectedFilter = QFileDialog.getSaveFileName(self, 'Save Orange Data File', startfile, self.dlgFormats), self.dlgFormats.splitlines()[0]
        filename = unicode(filename)
        if not filename or not os.path.split(filename)[1]:
            return
        ext = lower(os.path.splitext(filename)[1])
        if ext not in self.savers:
            filt_ext = self.re_filterExtension.search(str(selectedFilter)).group('ext')
            if filt_ext == '.*':
                filt_ext = '.tab'
            filename += filt_ext
        self.addFileToList(filename)
        if hasattr(self, 'WW') and self.WW:
            self.saveFile()

    def saveFile(self, *index):
        self.error()
        combotext = unicode(self.filecombo.currentText())
        if combotext == '(none)':
            QMessageBox.information(None, 'Error saving data', "Unable to save data. Select first a file name by clicking the '...' button.", QMessageBox.Ok + QMessageBox.Default)
            return
        else:
            filename = self.recentFiles[self.filecombo.currentIndex()]
            fileExt = lower(os.path.splitext(filename)[1])
            filenameWithoutExt = lower(os.path.splitext(filename)[0])
            WfileName = filenameWithoutExt + '_W' + '.tab'
            HfileName = filenameWithoutExt + '_H' + '.tab'
            SfileName = filenameWithoutExt + '_S' + '.tab'
            ResidualsfileName = filenameWithoutExt + '_Residuals' + '.tab'
            WSHfileName = filenameWithoutExt + '_WSH' + '.tab'
            QQplotfileName = filenameWithoutExt + '_QQplot' + '.tab'
            ReorderedXfileName = filenameWithoutExt + '_Reordered_X' + '.tab'
            ReorderedWSHfileName = filenameWithoutExt + '_Reordered_WSH' + '.tab'
            ReorderedResidualsfileName = filenameWithoutExt + '_Reordered_residuals' + '.tab'
            if fileExt == '':
                fileExt = '.tab'
            try:
                self.savers[fileExt](WfileName, self.WW)
                self.savers[fileExt](HfileName, self.HH)
                self.savers[fileExt](SfileName, self.S)
                self.savers[fileExt](ResidualsfileName, self.residuals)
                self.savers[fileExt](WSHfileName, self.WSH)
                self.savers[fileExt](QQplotfileName, self.qqplot)
                self.savers[fileExt](ReorderedXfileName, self.Xordered)
                self.savers[fileExt](ReorderedWSHfileName, self.WSHordered)
                self.savers[fileExt](ReorderedResidualsfileName, self.residualsOrdered)
            except Exception, errValue:
                self.error(str(errValue))
                return

            self.error()
            return

    def addFileToList(self, fn):
        if fn in self.recentFiles:
            self.recentFiles.remove(fn)
        self.recentFiles.insert(0, fn)
        self.setFilelist()

    def setFilelist(self):
        """Set the GUI filelist"""
        self.filecombo.clear()
        if self.recentFiles:
            self.filecombo.addItems([ os.path.split(file)[1] for file in self.recentFiles ])
        else:
            self.filecombo.addItem('(none)')

    def resendData(self):
        combotext = unicode(self.filecombo.currentText())
        if combotext == '(none)':
            QMessageBox.information(None, 'Error saving data', "Unable to send data. Select first a file name by clicking the '...' button.", QMessageBox.Ok + QMessageBox.Default)
            return
        else:
            filename = self.recentFiles[self.filecombo.currentIndex()]
            filenameWithoutExt = lower(os.path.splitext(filename)[0])
            self.runNMF()
            self.send('W', Orange.data.Table(filenameWithoutExt + '_W'))
            self.send('H', Orange.data.Table(filenameWithoutExt + '_H'))
            self.send('S', Orange.data.Table(filenameWithoutExt + '_S'))
            self.send('WSH', Orange.data.Table(filenameWithoutExt + '_WSH'))
            self.send('Residuals', Orange.data.Table(filenameWithoutExt + '_Residuals'))
            self.send('qqplot', Orange.data.Table(filenameWithoutExt + '_QQplot'))
            self.send('Reordered X', Orange.data.Table(filenameWithoutExt + '_Reordered_X'))
            self.send('Reordered WSH', Orange.data.Table(filenameWithoutExt + '_Reordered_WSH'))
            self.send('Reordered residuals', Orange.data.Table(filenameWithoutExt + '_Reordered_residuals'))
            return

    def commit(self):
        self.runNMF()
        self.send('W', self.WW)
        self.send('H', self.HH)
        self.send('S', self.S)
        self.send('WSH', self.WSH)
        self.send('Residuals', self.residuals)
        self.calculateQQPlotValues()
        self.send('qqplot', self.qqplot)
        self.reorder()
        self.send('Reordered X', self.Xordered)
        self.send('Reordered WSH', self.WSHordered)
        self.send('Reordered residuals', self.residualsOrdered)
        if self.saveOutputs:
            self.saveFile()


if __name__ == '__main__':
    appl = QApplication(sys.argv)
    ow = OWNMF()
    ow.show()
    dataset = orange.ExampleTable('C:/Users/Fajwel/Dropbox/Orange/data.tab')
    ow.dataX(dataset)
    appl.exec_()