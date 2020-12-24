# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
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