# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.darwin-8.9.1-i386/egg/classproperty.py
# Compiled at: 2006-05-29 15:25:16


class classpropertytype(property):
    __module__ = __name__

    def __init__(self, name, bases=(), members={}):
        return super(classpropertytype, self).__init__(members.get('__get__'), members.get('__set__'), members.get('__delete__'), members.get('__doc__'))


classproperty = classpropertytype('classproperty')
if __name__ == '__main__':
    import doctest
    doctest.testfile('classproperty.txt')