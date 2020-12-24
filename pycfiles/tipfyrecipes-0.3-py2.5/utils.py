# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/tipfyrecipes/utils.py
# Compiled at: 2011-08-05 19:07:14
import hashlib, os
TRUE_VALUES = ('yes', 'true', '1', 'on')

def get_bool_option(option):
    return option.strip().lower() in TRUE_VALUES


def get_checksum(path, hashtype='sha1'):
    if not os.path.isfile(path):
        return
    func = getattr(hashlib, hashtype)
    checksum = func()
    f = open(path, 'rb')
    try:
        chunk = f.read(65536)
        while chunk:
            checksum.update(chunk)
            chunk = f.read(65536)

        return checksum.hexdigest()
    finally:
        f.close()

    return