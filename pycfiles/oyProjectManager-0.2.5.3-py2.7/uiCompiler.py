# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/oyProjectManager/ui/uiCompiler.py
# Compiled at: 2012-10-21 16:07:48
import os
os.environ['PATH'] = '/usr/bin:/usr/local/bin/:/usr/local/lib/python2.6/site-packages' + os.environ['PATH']
from PyQt4 import uic
import subprocess, oyProjectManager
uicFilePaths = []
pyFilePaths_PyQt4 = []
pyFilePaths_PySide = []
path = os.path.dirname(oyProjectManager.__file__)
ui_path = os.path.join(path, 'ui')
uicFilePaths.append(os.path.join(ui_path, 'version_creator.ui'))
pyFilePaths_PyQt4.append(os.path.join(ui_path, 'version_creator_UI_pyqt4.py'))
pyFilePaths_PySide.append(os.path.join(ui_path, 'version_creator_UI_pyside.py'))
for i, uicFilePath in enumerate(uicFilePaths):
    pyFilePath_PyQt4 = pyFilePaths_PyQt4[i]
    pyFilePath_PySide = pyFilePaths_PySide[i]
    print 'compiling %s to %s for PySide' % (uicFilePath, pyFilePath_PySide)
    subprocess.call(['pyside-uic', '-o', pyFilePath_PySide, uicFilePath])
    uicFile = file(uicFilePath)
    pyFile = file(pyFilePath_PyQt4, 'w')
    print 'compiling %s to %s for PyQt4' % (uicFilePath, pyFilePath_PyQt4)
    uic.compileUi(uicFile, pyFile)
    uicFile.close()
    pyFile.close()

print 'finished compiling'
# global pyFile ## Warning: Unused global
# global uicFile ## Warning: Unused global