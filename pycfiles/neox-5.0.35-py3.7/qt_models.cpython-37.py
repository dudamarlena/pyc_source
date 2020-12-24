# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/neox/commons/qt_models.py
# Compiled at: 2019-05-28 11:35:24
# Size of source mod 2**32: 730 bytes
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QStandardItemModel, QStandardItem

def get_simple_model(obj, data, header=[]):
    model = QStandardItemModel(0, len(header), obj)
    if header:
        i = 0
        for head_name in header:
            model.setHeaderData(i, Qt.Horizontal, head_name)
            i += 1

    _insert_items(model, data)
    return model


def _insert_items(model, data):
    for d in data:
        row = []
        for val in d:
            itemx = QStandardItem(str(val))
            itemx.setFlags(Qt.ItemIsEnabled | Qt.ItemIsSelectable)
            row.append(itemx)

        model.appendRow(row)

    model.sort(0, Qt.AscendingOrder)


def set_selection_model(tryton_model, args):
    pass