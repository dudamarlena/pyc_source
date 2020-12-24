# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /users/payno/.local/share/virtualenvs/tomwer_venc/lib/python3.7/site-packages/tomwer/gui/reconstruction/ftserie/h5editor/rawh5parameditor.py
# Compiled at: 2019-12-11 09:05:53
# Size of source mod 2**32: 7628 bytes
__author__ = [
 'H. Payno']
__license__ = 'MIT'
__date__ = '08/02/2017'
from collections import OrderedDict
from silx.gui import qt
from tomwer.core.octaveh5editor import OctaveH5Editor
from tomwer.core.process.reconstruction.ftseries.params import fastsetupdefineglobals
from tomwer.core.log import TomwerLogger
logger = TomwerLogger(__name__)

class RawH5ParamEditor(OctaveH5Editor, qt.QTabWidget):
    __doc__ = '\n    This is a simple interface allowing the user to change values of an\n    h5 file\n\n    :param QObject parent: the parent widget\n    :param str h5File: the path of h5File to load on the editor\n    :param float readedOctaveVersion: the version which as write the h5File\n    '
    sigH5StructSettedToDefault = qt.Signal(list)

    def __init__(self, parent, h5File):
        OctaveH5Editor.__init__(self)
        qt.QWidget.__init__(self, parent)
        self._RawH5ParamEditor__initPalette = self.palette()
        self._loadH5File(h5File)
        self.defaultStructs = fastsetupdefineglobals.getAllDefaultStructures()

    def _loadH5File(self, h5File):
        """Main function to build the GUI"""
        self.h5File = h5File
        if self.h5File is None:
            return
        reader = fastsetupdefineglobals.FastSetupAll()
        reader.readAll(self.h5File, 3.8)
        self.loadReconsParams(reader.structures)

    def getInitialPalette(self):
        return self._RawH5ParamEditor__initPalette

    def getPalette(self, highlight=False):
        p = self.getInitialPalette()
        brush = qt.QBrush()
        p.setBrush(self.backgroundRole(), brush)
        if highlight:
            p.setColor(qt.QPalette.WindowText, qt.Qt.red)
            p.setColor(qt.QPalette.Text, qt.Qt.red)
            p.setColor(qt.QPalette.Window, qt.Qt.red)
        else:
            p.setColor(qt.QPalette.WindowText, qt.Qt.black)
            p.setColor(qt.QPalette.Text, qt.Qt.black)
            p.setColor(qt.QPalette.Window, qt.Qt.black)
        return p

    def getDefaultStruct(self, structID):
        if structID not in self.defaultStructs:
            raise ValueError('%s structure has no default value' % structID)
        else:
            return self.defaultStructs[structID]

    def getStructs(self):
        """Return a list of all the structures with their values"""
        res = {}
        for struct in self.structs:
            fields = {}
            for field in self.structs[struct]:
                self.structs[struct][field].text()
                fields[field] = self.structs[struct][field].text()

            res[struct] = fields

        return res

    def loadReconsParams(self, structures):
        structureIDs = [
         'FT', 'PYHSTEXE', 'FTAXIS', 'PAGANIN', 'BEAMGEO', 'DKRF']
        self.structs = {}
        settedToDefault = []
        for structID in structureIDs:
            highlightStruct = False
            highlightedVariables = []
            try:
                struct = structures[structID]
                FSDG = fastsetupdefineglobals.FastSetupAll()
                for variable in FSDG.defaultValues[structID]:
                    if variable not in struct:
                        highlightedVariables.append(variable)
                        struct[variable] = FSDG.defaultValues[structID][variable]
                        logger.info('%s variable in %s is missing' % (variable, struct))

            except ValueError:
                highlightStruct = True
                struct = self.getDefaultStruct(structID)
                settedToDefault.append(structID)
                warn = '%s structure not found in the given file, values setted to default' % struct
                logger.info(warn)

            self.structs[structID] = self._addStruct((OrderedDict(sorted((struct.items()), key=(lambda t: t[0])))),
              structID,
              highlight=highlightStruct,
              highlightedVariables=highlightedVariables)

        if len(settedToDefault) > 0:
            self.sigH5StructSettedToDefault.emit(settedToDefault)
            msg = qt.QMessageBox(self)
            msg.setIcon(qt.QMessageBox.Critical)
            text = "The following structure haven't been found in %s, you might check if setted values are corrects" % self.h5File
            for s in settedToDefault:
                text += '\n    - %s' % s

            msg.setText(text)
            msg.exec_()

    def _addStruct(self, struct, structID, highlight, highlightedVariables):
        """Add the given structure to the GUI"""
        newStruct = qt.QWidget()
        newStruct.setLayout(qt.QGridLayout())
        newStruct.setPalette(self.getPalette(highlight))
        self.addTab(newStruct, structID)
        dicoFieldToQLE = {}
        for i, field in enumerate(struct):
            dicoFieldToQLE[field] = self._addField(field, struct[field], newStruct, i, field in highlightedVariables)

        return OrderedDict(sorted((dicoFieldToQLE.items()), key=(lambda t: t[0])))

    def _addField(self, field, value, parent, index, highlighted=False):
        """Add the field to the widget

        :param str field: the ID of the new field to defined
        :param value: the value of the field
        :param parent: the Qt parent
        :param index: the index of the field
        :return: the line edit for the field
        """
        titleItem = qt.QLabel(field)
        titleItem.setPalette(self.getPalette(highlighted))
        parent.layout().addWidget(titleItem, index, 0)
        lineEdit = qt.QLineEdit(parent=parent, text=(str(value)))
        parent.layout().addWidget(lineEdit, index, 1)
        return lineEdit