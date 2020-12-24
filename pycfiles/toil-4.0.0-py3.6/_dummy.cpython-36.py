# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/toil/lib/encryption/_dummy.py
# Compiled at: 2020-04-03 17:41:24
# Size of source mod 2**32: 1070 bytes
overhead = 0

def encrypt(message, keyPath):
    _bail()


def decrypt(ciphertext, keyPath):
    _bail()


def _bail():
    raise NotImplementedError("Encryption support is not installed. Consider re-installing toil with the 'encryption' extra along with any other extras you might want, e.g. 'pip install toil[encryption,...]'.")