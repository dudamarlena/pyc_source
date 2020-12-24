# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/epscApp/scmProject.py
# Compiled at: 2009-05-29 13:49:24
import cPickle

class ScmProject:
    """  save current working data to the specified file and restore it when user open

        """

    def __init__(self, parent):
        self.parent = parent
        self.flag = False
        self.fullPath = ''

    def open(self, prjFile):
        inf = open(prjFile)
        self.parent.controller.epscData = cPickle.load(inf)
        self.parent.controller.epscOpt.epscData = self.parent.controller.epscData
        self.parent.controller.epscOpt.colData.epscData = self.parent.controller.epscData
        self.fullPath = prjFile
        self.flag = True

    def saveAs(self, prjFile):
        outf = open(prjFile, 'w')
        cPickle.dump(self.parent.controller.epscData, outf)
        outf.close()
        self.fullPath = prjFile
        self.flag = True

    def save(self):
        outf = open(self.fullPath, 'w')
        cPickle.dump(self.parent.controller.epscData, outf)
        outf.close()

    def close(self):
        self.flag = False