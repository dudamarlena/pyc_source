# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/gears_jsx/compiler.py
# Compiled at: 2014-05-08 06:07:41
import os
from gears.compilers import ExecCompiler

class JSXCompiler(ExecCompiler):
    result_mimetype = 'application/javascript'
    executable = 'node'
    params = [os.path.join(os.path.dirname(__file__), 'compiler.js')]