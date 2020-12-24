# uncompyle6 version 3.6.7
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: /Users/namanbharadwaj/en/lib/python2.6/site-packages/bobb/exceptions.py
# Compiled at: 2013-08-05 14:40:09


class BobbError(Exception):
    pass


class BobbfileNotFoundError(BobbError):

    def __init__(self):
        pass

    def __str__(self):
        return 'no bobbfile found'


class TargetConfigError(BobbError):

    def __init__(self, builder):
        self.builder = builder

    def __str__(self):
        return 'builder %s must build at least one target' % self.builder


class BuilderNotFoundError(BobbError):

    def __init__(self, target):
        self.target = target

    def __str__(self):
        return 'no builder registered to build target %s' % self.target


class BuilderError(BobbError):

    def __init__(self, target, builder):
        self.target = target
        self.builder = builder

    def __str__(self):
        return 'builder %s is expected to build target %s but does not' % (
         self.builder, self.target)


class TargetDeletionError(BobbError):

    def __init__(self, target):
        self.target = target

    def __str__(self):
        return 'target %s was built but no longer exists. this is probably a ' + 'bug in an unrelated builder' % self.target