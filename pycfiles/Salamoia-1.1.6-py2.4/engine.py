# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/salamoia/tales/engine.py
# Compiled at: 2007-12-02 16:26:58
"""Expression engine configuration and registration.

Each expression engine can have its own expression types and base names.

$Id: engine.py 30451 2005-05-20 04:54:15Z fdrake $
"""
from salamoia.tales.tales import ExpressionEngine
from salamoia.tales.expressions import PathExpr, StringExpr, NotExpr, DeferExpr
from salamoia.tales.expressions import SimpleModuleImporter
from salamoia.tales.pythonexpr import PythonExpr

def Engine():
    e = ExpressionEngine()
    reg = e.registerType
    for pt in PathExpr._default_type_names:
        reg(pt, PathExpr)

    reg('string', StringExpr)
    reg('python', PythonExpr)
    reg('not', NotExpr)
    reg('defer', DeferExpr)
    e.registerBaseName('modules', SimpleModuleImporter())
    return e


Engine = Engine()
from salamoia.tests import *
runDocTests()