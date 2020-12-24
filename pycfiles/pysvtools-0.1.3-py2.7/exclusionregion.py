# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.10-x86_64/egg/pysvtools/models/exclusionregion.py
# Compiled at: 2015-11-13 08:40:24


class ExclusionRegion(object):

    def __init__(self, chromosome, start, end, *args, **kwargs):
        self.chromosome = chromosome
        self.start = int(start)
        self.end = int(end)

    def overlaps(self, qChr, qPos):
        return qChr == self.chromosome and self.start <= qPos <= self.end

    def __eq__(self, other):
        pass

    def __repr__(self):
        return ('<ExclusionRegion {}:{}-{}>').format(self.chromosome, self.start, self.end)