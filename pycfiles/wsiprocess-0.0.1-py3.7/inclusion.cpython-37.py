# uncompyle6 version 3.7.4
# Python bytecode 3.7 (3394)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.14-x86_64/egg/wsiprocess/inclusion.py
# Compiled at: 2019-11-21 06:51:45
# Size of source mod 2**32: 644 bytes


class Inclusion:

    def __init__(self, path):
        with open(path, 'r') as (f):
            self.inclusion_file = f.readlines()
        self.read_inclusion()

    def read_inclusion(self):
        self.inclusion = {}
        for line in self.inclusion_file:
            line_ = [i.strip() for i in line.split(' ')]
            base, exclude = line_[0], line_[1:]
            setattr(self, base, exclude)