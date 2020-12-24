# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /users/payno/.local/share/virtualenvs/tomwer_venc/lib/python3.7/site-packages/tomwer/gui/linksqobject.py
# Compiled at: 2019-08-19 02:52:33
# Size of source mod 2**32: 5173 bytes
__author__ = [
 'H. Payno']
__license__ = 'MIT'
__date__ = '14/03/2017'

class LinkQObject:
    __doc__ = 'Class used to store the QObject associated to an H5 parameter'

    def __init__(self, qobject):
        self.qobject = qobject


class LinkComboBox(LinkQObject):
    __doc__ = '\n    Class used to store the Combobox associated to an H5 parameter\n\n    :param qcombobox: the QCombobox in the interface to edit/display the\n        given h5ParamName\n    :param h5ParamName: the parameter ID in the H5 structure.\n    :param fitwithindex: true if we want to store the index in the h5File,\n        otherwise store the string\n    :param dic: if not None then instead for storing index or string we will\n        store the associated value with this key. Keys are the one displayed in\n        the QComboBox, values the one in the H5file\n    :param filters: filter to apply on the combobox value to get the requested\n        value (only apply on load/getting values)\n    :param setDefault: if value to set not found in the existing values then\n        set the default value, If False add the value to the QComboBox\n    '

    def __init__(self, qcombobox, fitwithindex, dic=None, filters=None, setDefault=True):
        LinkQObject.__init__(self, qcombobox)
        if not dic is None:
            assert type(dic) is dict
        if not filters is None:
            assert fitwithindex is False
        self.fitwithindex = fitwithindex
        self.dicCBtoH5 = dic
        self.dicH5ToCB = dict(((v, k) for k, v in iter(dic.items()))) if dic else None
        self.filters = filters
        self.setDefault = setDefault


class LinkCheckBox(LinkQObject):
    __doc__ = '\n    Class used to store the QCheckBox associated to an H5 parameter\n\n    :param qcheckbox: the QCheckBox in the interface to edit/display the\n        given h5ParamName\n    :param h5ParamName: the parameter ID in the H5 structure.\n    :param invert: true if we will not store the value state == checked but\n        state == unchecked\n    '

    def __init__(self, qcheckbox, invert):
        LinkQObject.__init__(self, qcheckbox)
        self.invert = invert


class LinkLineEdit(LinkQObject):
    __doc__ = '\n    Class used to store the QCheckBox associated to an H5 parameter\n\n    :param qlineedit: the QCheckBox in the interface to edit/display the\n        given h5ParamName\n    :param h5ParamName: the parameter ID in the H5 structure.\n    :param h5paramtype: Define the type of the output value\n    '

    def __init__(self, qlineedit, h5paramtype):
        LinkQObject.__init__(self, qlineedit)
        self.h5paramtype = h5paramtype


class LinkSelLineEdit(LinkQObject):
    __doc__ = '\n    Class used to store the QCheckBox associated to an H5 parameter\n\n    :param qlineedit: the QCheckBox in the interface to edit/display the\n        given h5ParamName\n    :param h5ParamName: the parameter ID in the H5 structure.\n    :param h5paramtype: Define the type of the output value\n    '

    def __init__(self, qlineedit, h5paramtype):
        LinkQObject.__init__(self, qlineedit)
        self.h5paramtype = h5paramtype


class LinkGroup(LinkQObject):
    __doc__ = '\n    Class used to store an H5 reconstruction parameter with a simple getter and\n    setter to call\n\n    :param qlineedit: the QCheckBox in the interface to edit/display the\n        given h5ParamName\n    :param h5ParamName: the parameter ID in the H5 structure.\n    :param setter: the function to set the variable in the GUI\n    :param getter: the function to get the variable value\n    '

    def __init__(self, group, getter, setter):
        LinkQObject.__init__(self, group)
        self.getter = getter
        self.setter = setter