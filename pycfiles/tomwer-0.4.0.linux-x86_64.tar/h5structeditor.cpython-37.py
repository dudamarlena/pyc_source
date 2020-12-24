# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /users/payno/.local/share/virtualenvs/tomwer_venc/lib/python3.7/site-packages/tomwer/gui/reconstruction/ftserie/h5editor/h5structeditor.py
# Compiled at: 2019-12-11 09:05:53
# Size of source mod 2**32: 6086 bytes
__author__ = [
 'H. Payno']
__license__ = 'MIT'
__date__ = '08/02/2017'
from tomwer.core.log import TomwerLogger
from tomwer.gui.reconstruction.ftserie.h5editor import H5StructsEditor
logger = TomwerLogger(__name__)

class H5StructEditor(H5StructsEditor):
    __doc__ = 'simple class which link an interface with an h5 struct used for pyhst'

    def __init__(self, structID):
        self.structID = structID
        H5StructsEditor.__init__(self, (self.structID,))

    def linkComboboxWithH5Variable(self, qcombobox, h5ParamName, fitwithindex=False, dic=None, filters=None, setDefault=True):
        """

        :param qcombobox: the QCombobox in the interface to edit/display the
            given h5ParamName
        :param h5ParamName: the parameter ID in the H5 structure.
        :param fitwithindex: true if we want to store the index in the h5File,
            otherwise store the string
        :param filters: filter to apply on the string to get the requested
            value
        """
        return H5StructsEditor.linkComboboxWithH5Variable(self, qcombobox=qcombobox,
          structID=(self.structID),
          h5ParamName=h5ParamName,
          fitwithindex=fitwithindex,
          dic=dic,
          filters=filters,
          setDefault=setDefault)

    def linkCheckboxWithH5Variable(self, qcheckbox, h5ParamName, invert=False):
        """

        :param qcheckbox: the QCheckBox in the interface to edit/display the
            given h5ParamName
        :param h5ParamName: the parameter ID in the H5 structure.
        :param invert: true if we will not store the value state == checked but
            state == unchecked
        :param structID: the structID associated with the param ID
        """
        return H5StructsEditor.linkCheckboxWithH5Variable(self, qcheckbox=qcheckbox,
          structID=(self.structID),
          h5ParamName=h5ParamName,
          invert=invert)

    def LinkLineEditWithH5Variable(self, qlineedit, h5ParamName, h5paramtype=str):
        """

        :param qlineedit: the QLineEdit in the interface to edit/display the
            given h5ParamName
        :param h5ParamName: the parameter ID in the H5 structure.
        :param h5ParamName: the parameter ID in the H5 structure.
        """
        return H5StructsEditor.LinkLineEditWithH5Variable(self, qlineedit=qlineedit,
          h5ParamName=h5ParamName,
          structID=(self.structID),
          h5paramtype=h5paramtype)

    def LinkSelectionLineEditWithH5Variable(self, qlineedit, h5ParamName, h5paramtype=str):
        """

        :param qlineedit: the QLineEdit in the interface to edit/display the
            given h5ParamName
        :param h5ParamName: the parameter ID in the H5 structure.
        :param h5ParamName: the parameter ID in the H5 structure.
        """
        return H5StructsEditor.LinkSelectionLineEditWithH5Variable(self, qlineedit=qlineedit,
          h5ParamName=h5ParamName,
          structID=(self.structID),
          h5paramtype=h5paramtype)

    def linkGroupWithH5Variable(self, group, h5ParamName, getter, setter):
        return H5StructsEditor.linkGroupWithH5Variable(self, group=group,
          structID=(self.structID),
          h5ParamName=h5ParamName,
          getter=getter,
          setter=setter)