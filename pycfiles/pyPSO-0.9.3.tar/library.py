# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/dswistowski/pso/pypso/src/pypso/library.py
# Compiled at: 2007-06-30 10:30:50
"""
Biblioteka, w tym module są przechowywana załadowane strategie, oraz funkcje.
"""
(FUNCTION, NAME, DOCUMENTATION) = range(3)

class _library:

    def __init__(self):
        self.__elements = []
        self.__elements_index = {}

    def register(self, element, name=None, documentation=None):
        if name == None:
            name = element.__name__
        if documentation == None:
            documentation = element.__doc__
        el = (
         element, name, documentation)
        self.__elements.append(el)
        self.__elements_index[name] = el
        return

    def get(self, name=None, function=None):
        if name != None:
            return self.__elements_index[name]
        if function != None:
            for element in self.__elements:
                if element[0] == function:
                    return element

            return
        return self.__elements


function_library = _library()
strategy_library = _library()