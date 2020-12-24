# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: C:\Anaconda2\lib\site-packages\pySAXS\guisaxs\qt\pluginFAI.py
# Compiled at: 2018-02-14 09:13:28
from pySAXS.guisaxs.qt import plugin
from pySAXS.guisaxs.qt import dlgQtFAI
from pySAXS.guisaxs.qt import dlgQtFAITest
from pySAXS.guisaxs.qt import dlgSurveyor
classlist = [
 'pluginFAI', 'pluginTestFAI', 'pluginSurveyorXeuss']

class pluginFAI(plugin.pySAXSplugin):
    menu = 'Data Treatment'
    subMenu = 'Image'
    subMenuText = 'Fast Radial Averaging'
    icon = 'imshow.png'
    toolbar = True

    def execute(self):
        parameterfile = self.parent.pref.get('parameterfile', 'pyFAI')
        ouputdir = self.parent.pref.get('outputdir', 'pyFAI')
        self.dlgFAI = dlgQtFAI.FAIDialog(self.parent, parameterfile, ouputdir)
        self.dlgFAI.show()


class pluginTestFAI(plugin.pySAXSplugin):
    menu = 'Data Treatment'
    subMenu = 'Image'
    subMenuText = 'Test Radial Averaging parameters'
    icon = 'image.png'

    def execute(self):
        parameterfile = self.parent.pref.get('parameterfile', 'pyFAI')
        ouputdir = self.parent.pref.get('outputdir', 'pyFAI')
        self.dlgFAI = dlgQtFAITest.FAIDialogTest(self.parent, parameterfile, ouputdir)
        self.dlgFAI.show()


class pluginSurveyorXeuss(plugin.pySAXSplugin):
    menu = 'Data Treatment'
    subMenu = 'Image'
    subMenuText = 'SAXS Image Surveyor'
    icon = 'eye.png'
    toolbar = True

    def execute(self):
        parameterfile = self.parent.pref.get('parameterfile', 'pyFAI')
        self.dlg = dlgSurveyor.SurveyorDialog(self.parent, parameterfile)
        self.dlg.show()