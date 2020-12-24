# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\xicam\plugins\hipgisaxs\featuremanager.py
# Compiled at: 2018-09-13 20:32:23
from PySide.QtUiTools import QUiLoader
from PySide import QtGui
from PySide import QtCore
import models, ui, customwidgets, display, hig
features = []
functionTree = None
layout = None

def clearFeatures():
    global features
    while features:
        feature = features[(-1)]
        features.remove(feature)
        feature.deleteLater()


def addSubstrate():
    if not sum([ type(feature) is customwidgets.substrate for feature in features ]):
        features.insert(0, customwidgets.substrate())
    update()


def addLayer():
    features.append(customwidgets.layer())
    update()


def addParticle():
    features.append(customwidgets.particle())
    update()


def removeFeature(index):
    del features[index]
    update()


def layercount():
    return sum([ type(feature) is customwidgets.layer for feature in features ])


def particlecount():
    return sum([ type(feature) is customwidgets.particle for feature in features ])


def update():
    assert isinstance(layout, QtGui.QVBoxLayout)
    for i in range(layout.count()):
        if layout.itemAt(i) not in features:
            layout.itemAt(i).parent = None

    for i, item in enumerate(features[::-1]):
        layout.insertWidget(i, item)

    if display.viewWidget:
        display.redraw()
    return


def loadform(path):
    guiloader = QUiLoader()
    f = QtCore.QFile(path)
    f.open(QtCore.QFile.ReadOnly)
    form = guiloader.load(f)
    f.close()
    return form


def load():
    layout.setAlignment(QtCore.Qt.AlignBottom)
    addSubstrate()
    addParticle()


# global functionTree ## Warning: Unused global