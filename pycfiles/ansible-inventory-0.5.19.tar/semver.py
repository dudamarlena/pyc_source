# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /work/ansible/ansible-extras/filter_plugins/semver.py
# Compiled at: 2018-10-04 13:55:43
import re

def semver(args):
    ver = 0
    sem = 10000000
    args = re.sub('[^0-9.]', '', args)
    for arg in args.split('.'):
        if arg == '':
            continue
        ver += int(arg) * sem
        sem = sem / 100

    return ver


class FilterModule(object):
    """Returns a semver based number suitable for sorting """

    def filters(self):
        return {'semver': semver}


if __name__ == '__main__':
    assert semver('1.0.8') < semver('1.0.9')
    assert semver('1.0.9') < semver('1.0.19')
    assert semver('1.0.8.GA') < semver('1.0.9.GA')
    assert semver('1.0.9') < semver('1.0.19')