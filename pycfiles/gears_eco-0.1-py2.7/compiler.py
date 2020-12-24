# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.8-x86_64/egg/gears_eco/compiler.py
# Compiled at: 2013-11-21 12:16:07
import os
from gears.compilers import ExecCompiler
SOURCE = '(function() { %(namespace)s || (%(namespace)s = {});\n    %(namespace)s["%(name)s"] = %(source)s;\n}).call(this);'

class EcoCompiler(ExecCompiler):
    result_mimetype = 'application/javascript'
    executable = 'node'
    params = [os.path.join(os.path.dirname(__file__), 'compiler.js')]

    def __call__(self, asset):
        super(EcoCompiler, self).__call__(asset)
        asset.processed_source = SOURCE % {'name': asset.attributes.path_without_suffix, 
           'source': asset.processed_source, 
           'namespace': 'this.JST'}