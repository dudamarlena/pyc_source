# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.5-ppc/egg/oldowan/mitomotifs/polymorphism.py
# Compiled at: 2008-08-24 10:54:34


class Polymorphism(object):

    def __init__(self, position, insert, value, reference=''):
        self.position = position
        self.insert = insert
        self.value = value
        self.reference = reference

    def __cmp__(self, other):
        if self.position == other.position:
            if self.insert == other.insert:
                return cmp(self.value, other.value)
            return cmp(self.insert, other.insert)
        return cmp(self.position, other.position)

    def __str__(self):
        if self.insert == 0:
            if self.value == '-':
                return '%s%s' % (self.position, 'd')
            else:
                return '%s%s' % (self.position, self.value)
        return '%s.%s%s' % (self.position, self.insert, self.value)

    def __repr__(self):
        return str(self)

    def is_substitution(self):
        return self.insert == 0 and self.value != '-'

    def is_transition(self):
        changes = [
         self.value, self.reference]
        changes.sort()
        change = ('%s%s' % tuple(changes)).upper()
        return self.is_substitution() and change in ('AG', 'CT')

    def is_transversion(self):
        return self.is_substitution() and not self.is_transition()

    def is_insertion(self):
        return self.insert > 0

    def is_deletion(self):
        return self.value in ('-', )