# uncompyle6 version 3.7.4
# Python bytecode 3.6 (3379)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/tmiedema/.pyenv/versions/3.6.0/lib/python3.6/site-packages/holdmybeer/complex.py
# Compiled at: 2017-03-28 11:36:04
# Size of source mod 2**32: 4023 bytes
from .core import Bucket
from .exceptions import IncompatibleContainer

class RatioBucket(object):
    __doc__ = 'Has a collection of items that are given out in certain ratio.'

    def __init__(self, contenttype, ratios):
        """param ratios: dict(contenttype: ratio)"""
        self.contenttype = contenttype
        self.mylist = Bucketlist()
        self.ratios = ratios
        for contenttype in ratios.keys():
            self.mylist.append(Bucket(contenttype, 0, 0))

    def take(self, contenttype, amount):
        if contenttype == self.contenttype:
            bucket = RatioBucket(contenttype, self.ratios)
            for ctype, ratio in self.ratios.items():
                bucket.absorb(self.mylist.take(ctype, int(round(amount * ratio))))

            return bucket
        else:
            return self.mylist.take(contenttype, amount)

    def give(self, contenttype, amount, value):
        if contenttype == self.contenttype:
            ctypes = self.ratios.keys()
            ratios = [self.ratios[ctype] for ctype in ctypes]
            values = divide(amount, ratios)
            for i in range(len(values)):
                self.mylist.give(ctypes[i], int(round(amount * ratios[i])), values[i])

        else:
            self.mylist.give(contenttype, amount, value)

    def absorb(self, other):
        pass

    def has(self, contenttype):
        if contenttype == self.contenttype:
            return True
        else:
            return self.mylist.has(contenttype)

    @property
    def value(self):
        pass

    @property
    def amount(self):
        pass


class Bucketlist(object):
    __doc__ = 'Collection of buckets that can be accessed in one go.'

    def __init__(self, autocreate=False):
        self.mylist = []
        self.autocreate = autocreate

    def append(self, bucket):
        self.mylist.append(bucket)

    def take(self, contenttype, amount):
        for bucket in self.mylist:
            if bucket.has(contenttype):
                return bucket.take(contenttype, amount)

        raise IncompatibleContainer()

    def give(self, contenttype, amount, value):
        for bucket in self.mylist:
            if bucket.has(contenttype):
                bucket.give(contenttype, amount, value)
                return

        if self.autocreate:
            self.append(Bucket(contenttype, amount, value))
        else:
            raise IncompatibleContainer()

    def absorb(self, other):
        pass

    def has(self, contenttype):
        for bucket in self.mylist:
            if bucket.has(contenttype):
                return True

        return False


class Bucketcrate(Bucket):
    __doc__ = "Bucket of items that can be in packed together into a 'crate'. For example a trays of beer: they can either be counted in bottles or trays."

    def __init__(self, single_contenttype, crate_contenttype, per_crate, amount, value):
        super().__init__(single_contenttype, amount, value)
        self.crate_contenttype = crate_contenttype
        self.per_crate = per_crate

    def take(self, contenttype, amount):
        if contenttype == self.crate_contenttype:
            return super().take(self.contenttype, amount * self.per_crate)
        else:
            return super().take(contenttype, amount)

    def give(self, contenttype, amount, value):
        if contenttype == self.crate_contenttype:
            return super().give(self.contenttype, amount * self.per_crate, value)
        else:
            return super().give(contenttype, amount, value)

    def absorb(self, other):
        pass

    def has(self, contenttype):
        return contenttype == self.contenttype or contenttype == self.crate_contenttype