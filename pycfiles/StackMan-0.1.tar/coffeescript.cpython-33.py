# uncompyle6 version 3.7.4
# Python bytecode 3.3 (3230)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /Users/coltonprovias/Development/zymio/stackman/stackman/common/coffeescript.py
# Compiled at: 2013-12-13 03:36:54
# Size of source mod 2**32: 689 bytes
"""
StackMan
Colton J. Provias - cj@coltonprovias.com
"""
from stackman.stack import StackItem

class CoffeeScript(StackItem):
    __doc__ = "\n    Watches your Coffee so you don't have to!\n\n    Arguments:\n    * base_command str Base Command\n                       Default: coffee\n    * input_dir str Input Directory\n                    Default: static/coffee\n    * output_dir str Output Directory\n                     Default: static/js\n    "
    ready_text = 'compiled'

    @property
    def command(self):
        i = self.input_dir + '/*.coffee'
        fmap = {'in': i,  'command': self.base_command,  'out': self.output_dir}
        return '{command} -w -c -o {out} {in}'.format_map(fmap)