# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/seq2annotation/preprocess_hooks/hook_base.py
# Compiled at: 2019-07-30 09:27:42
# Size of source mod 2**32: 93 bytes


class HookBase(object):

    def __call__(self, sentence):
        return NotImplementedError