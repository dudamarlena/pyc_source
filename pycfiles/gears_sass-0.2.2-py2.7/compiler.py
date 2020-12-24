# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.9-x86_64/egg/gears_sass/compiler.py
# Compiled at: 2014-04-29 09:04:07
import os
from gears.compilers import ExecCompiler

class SASSCompiler(ExecCompiler):
    result_mimetype = 'text/css'
    executable = 'node'
    params = [os.path.join(os.path.dirname(__file__), 'compiler.js')]

    def __init__(self, *args, **kwargs):
        self.paths = []
        super(SASSCompiler, self).__init__(*args, **kwargs)

    def __call__(self, asset):
        self.asset = asset
        super(SASSCompiler, self).__call__(asset)

    def run(self, src):
        return super(SASSCompiler, self).run(src)

    def get_args(self):
        args = super(SASSCompiler, self).get_args()
        args.append(os.path.dirname(self.asset.absolute_path))
        args.extend(self.asset.attributes.environment.paths)
        return args