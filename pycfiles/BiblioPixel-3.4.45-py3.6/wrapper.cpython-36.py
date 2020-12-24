# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/bibliopixel/animation/wrapper.py
# Compiled at: 2019-08-11 12:22:47
# Size of source mod 2**32: 584 bytes
from .indexed import Indexed

class Wrapper(Indexed):
    __doc__ = '\n    Wraps a single Animation.\n\n    ``Wrapper`` is used as a base class for Pytho Animation classes that control\n    or process other animations.\n    '

    @staticmethod
    def pre_recursion(desc):
        if 'animations' in desc:
            raise ValueError('Cannot specify animations in a Wrapper')
        desc['animations'] = [
         desc.pop('animation')]
        return Indexed.pre_recursion(desc)

    @property
    def animation(self):
        return self.animations[0]