# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/decocare/scan.py
# Compiled at: 2016-04-27 23:26:51
import glob

class ID:
    VENDOR = 2593
    PRODUCT = 32769

    @classmethod
    def template(Klass, prefix):
        postfix = '*'
        usb_id = '%04x_%04x' % (ID.VENDOR, ID.PRODUCT)
        candidate = ('').join([prefix, usb_id, postfix])
        return candidate


def scan(prefix='/dev/serial/by-id/*-', template=ID.template):
    candidate = template(prefix)
    results = glob.glob(candidate)
    return (results[0:1] or ['']).pop()


if __name__ == '__main__':
    candidate = scan()
    print candidate