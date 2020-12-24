# uncompyle6 version 3.7.4
# Python bytecode 3.4 (3310)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.10-x86_64/egg/boto/pyami/helloworld.py
# Compiled at: 2015-11-24 05:02:18
# Size of source mod 2**32: 1238 bytes
from boto.pyami.scriptbase import ScriptBase

class HelloWorld(ScriptBase):

    def main(self):
        self.log('Hello World!!!')