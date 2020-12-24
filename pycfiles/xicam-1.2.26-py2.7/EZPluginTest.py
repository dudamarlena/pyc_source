# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win-amd64\egg\xicam\plugins\EZPluginTest.py
# Compiled at: 2018-08-27 17:21:07
import base

def runtest():
    import numpy as np
    img = np.random.random((100, 100, 100))
    EZTest.setImage(img)
    hist = np.histogram(img, 100)
    EZTest.plot(hist[1][:-1], hist[0])


def opentest(filepaths):
    import fabio
    for filepath in filepaths:
        img = fabio.open(filepath).data
        EZTest.setImage(img)


EZTest = base.EZplugin(name='EZTest', toolbuttons=[
 (
  'xicam/gui/icons_34.png', runtest)], parameters=[{'name': 'Test', 'value': 10, 'type': 'int'}, {'name': 'Fooo', 'value': True, 'type': 'bool'}], openfileshandler=opentest)