# uncompyle6 version 3.7.4
# Python bytecode 3.5 (3350)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/noval/python/analyzer.py
# Compiled at: 2019-08-16 02:55:35
# Size of source mod 2**32: 4446 bytes
from noval import GetApp
import noval.python.parser.codeparser as codeparser, threading, noval.python.parser.scope as scope, noval.util.utils as utils

class PythonModuleAnalyzer(object):
    __doc__ = 'description of class'
    STATUS_START_ANALYZING = 0
    STATUS_PARSING_SYNTAX = 1
    STATUS_LOADING_SYNTAX_TREE = 2
    STATUS_FINISH_ANALYZING = 3

    def __init__(self, mod_view):
        self._mod_view = mod_view
        self._status = self.STATUS_START_ANALYZING
        self._lock = threading.Lock()
        self._is_analyzing_stoped = False
        self._module_scope = None
        self._code_parser = codeparser.CodeParser()

    def LoadModule(self, filename):
        self._status = self.STATUS_PARSING_SYNTAX
        try:
            module = self._code_parser.ParsefileContent(self._mod_view.GetDocument().GetFilename(), self._mod_view.GetValue(), self._mod_view.GetDocument().file_encoding)
        except Exception as e:
            self._syntax_error_msg = str(e)
            self.FinishAnalyzing()
            return

        module_scope = scope.ModuleScope(module, self._mod_view.GetCtrl().GetLineCount())
        if not self.IsAnalyzingStopped():
            module_scope.MakeModuleScopes()
        else:
            utils.GetLogger().debug('analyze module file %s is canceled by user,will not make module scopes step', filename)
        if not self.IsAnalyzingStopped():
            module_scope.RouteChildScopes()
        else:
            utils.GetLogger().debug('analyze module file %s is canceled by user,will not route child scopes step', filename)
        self.ModuleScope = module_scope

    def AnalyzeModuleSynchronizeTree(self, view, outlineView, force, lineNum):
        self.LoadMouduleSynchronizeTree(view, outlineView, force, lineNum)

    def LoadMouduleSynchronizeTree(self, callback_view, outlineView, force, lineNum):
        with self._lock:
            if self.IsAnalyzing():
                utils.get_logger().debug('document %s is analyzing,will not analyze again', self._mod_view.GetDocument().GetFilename())
                return True
            else:
                document = self._mod_view.GetDocument()
                filename = document.GetFilename()
                if force:
                    self.LoadModule(filename)
                if not force and callback_view == self._mod_view:
                    return False
                self._status = self.STATUS_LOADING_SYNTAX_TREE
                if self.ModuleScope is not None:
                    if not self.IsAnalyzingStopped():
                        outlineView.LoadModuleAst(self.ModuleScope, self, lineNum)
                    else:
                        utils.GetLogger().debug('analyze module file %s is canceled by user,will not load and synchronize tree', filename)
                else:
                    outlineView._clear_tree()
                self.FinishAnalyzing()
                return True

    @property
    def ModuleScope(self):
        return self._module_scope

    @property
    def SyntaxError(self):
        return self._syntax_error_msg

    @ModuleScope.setter
    def ModuleScope(self, module_scope):
        self._module_scope = module_scope

    @property
    def View(self):
        return self._mod_view

    def StopAnalyzing(self):
        utils.get_logger().info('analyze module file %s is canceled by user,will stop analyzing', self._mod_view.GetDocument().GetFilename())
        self.FinishAnalyzing()
        self._is_analyzing_stoped = True

    def IsAnalyzingStopped(self):
        return self._is_analyzing_stoped

    def IsAnalyzing(self):
        return self._status == self.STATUS_PARSING_SYNTAX or self._status == self.STATUS_LOADING_SYNTAX_TREE

    def FinishAnalyzing(self):
        self._status = self.STATUS_FINISH_ANALYZING