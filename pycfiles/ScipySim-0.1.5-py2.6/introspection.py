# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/scipysim/gui/introspection.py
# Compiled at: 2010-04-22 06:03:43


def interrogate(item):
    """Print lots of useful information about a python object."""
    result = ''
    if hasattr(item, '__name__'):
        result += 'Name:  %s\n' % item.__name__
    if hasattr(item, '__class__'):
        result += 'Class: %s\n' % item.__class__.__name__
    result += 'ID:    %d\n' % id(item)
    result += 'Type:  %s\n' % type(item)
    result += 'Value: %s\n' % repr(item)
    result += 'Callable: %s\n' % ('Yes' if callable(item) else 'No')
    if hasattr(item, '__doc__'):
        doc = getattr(item, '__doc__')
        result += 'Documentation: \n%s\n' % doc
    result += 'DIR: %s\n' % dir(item)
    return result


if __name__ == '__main__':
    print interrogate(interrogate)