# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/dap/responses/das.py
# Compiled at: 2008-03-31 07:43:18
"""DAS DAP response.

This module implements the DAS DAP response, building it
dynamically from datasets objects.
"""
__author__ = 'Roberto De Almeida <rob@pydap.org>'
from dap.lib import INDENT, __dap__, encode_atom, to_list
from dap.dtypes import *
from dap.dtypes import _basetypes

def build(self, constraints=None):
    dataset = self._parseconstraints(None)
    headers = [
     ('Content-description', 'dods_das'),
     (
      'XDODS-Server', 'dods/%s' % ('.').join([ str(i) for i in __dap__ ])),
     ('Content-type', 'text/plain')]
    output = _dispatch(dataset)
    return (
     headers, output)


typeconvert = {basestring: 'String', unicode: 'String', 
   str: 'String', 
   float: 'Float64', 
   long: 'Int32', 
   int: 'Int32'}

def _recursive_build(attr, values, level=0):
    """
    Recursive function to build the DAS.
    
    This function checks for attribute nodes that do not belong to any
    variable, and append them as metadata.
    """
    if isinstance(values, dict):
        yield '%s%s {\n' % ((level + 1) * INDENT, attr)
        for (k, v) in values.items():
            for line in _recursive_build(k, v, level + 1):
                yield line

        yield '%s}\n' % ((level + 1) * INDENT)
    else:
        values = to_list(values)
        if not isinstance(values, list):
            values = [values]
        attrtype = typeconvert[type(values[0])]
        values = [ encode_atom(v) for v in values ]
        values = (', ').join(values)
        yield '%s%s %s %s;\n' % ((level + 1) * INDENT, attrtype, attr.replace(' ', '_'), values)


def _dispatch(dapvar, level=0):
    func = {DatasetType: _dataset, StructureType: _structure, 
       SequenceType: _sequence, 
       GridType: _grid, 
       ArrayType: _array, 
       BaseType: _base}[type(dapvar)]
    return func(dapvar, level)


def _dataset(dapvar, level=0):
    yield '%sAttributes {\n' % (level * INDENT)
    for (attr, values) in dapvar.attributes.items():
        for line in _recursive_build(attr, values, level):
            yield line

    for var in dapvar.walk():
        for line in _dispatch(var, level=level + 1):
            yield line

    yield '%s}\n' % (level * INDENT)


def _structure(dapvar, level=0):
    yield '%s%s {\n' % (level * INDENT, dapvar.name)
    for (attr, values) in dapvar.attributes.items():
        for line in _recursive_build(attr, values, level):
            yield line

    for var in dapvar.walk():
        for line in _dispatch(var, level=level + 1):
            yield line

    yield '%s}\n' % (level * INDENT)


_sequence = _structure

def _grid(dapvar, level=0):
    yield '%s%s {\n' % (level * INDENT, dapvar.name)
    for (attr, values) in dapvar.attributes.items():
        for line in _recursive_build(attr, values, level):
            yield line

    yield '%s}\n' % (level * INDENT)


def _array(dapvar, level=0):
    yield '%s%s {\n' % (level * INDENT, dapvar.name)
    for (attr, values) in dapvar.attributes.items():
        for line in _recursive_build(attr, values, level):
            yield line

    yield '%s}\n' % (level * INDENT)


_base = _array

def _test():
    import doctest
    doctest.testmod()


if __name__ == '__main__':
    _test()