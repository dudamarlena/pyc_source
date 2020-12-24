# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-i686/egg/prettylogger/utils.py
# Compiled at: 2014-07-28 23:39:43
__options = {'p': '\x1b[95m', 'c': '\x1b[94m', 
   'y': '\x1b[93m', 
   'g': '\x1b[92m', 
   'r': '\x1b[91m', 
   'b': '\x1b[1m', 
   'x': '\x1b[0m'}

def prettify(thing, depth=4):
    if type(thing) is dict:
        formatted = '{'
        for key in thing:
            formatted += '\n' + ' ' * depth
            formatted += key + ': ' + prettify(thing[key], depth + 4) + ','

        formatted = formatted[:-1]
        formatted += '\n' + ' ' * (depth - 4) + '}'
        return formatted
    if type(thing) is tuple:
        formatted = '('
        for element in thing:
            formatted += '\n' + ' ' * depth
            formatted += prettify(element, depth + 4) + ','

        formatted += '\n' + ' ' * (depth - 4) + ')'
        return formatted
    if type(thing) is list:
        formatted = '['
        for element in thing:
            formatted += '\n' + ' ' * depth
            formatted += prettify(element, depth + 4) + ','

        formatted = formatted[:-1]
        formatted += '\n' + ' ' * (depth - 4) + ']'
        return formatted
    return str(thing)


def log(thing, options=''):
    options = [ __options[option] for option in options if option in __options ]
    prefix = ('').join(options)
    print prefix + prettify(thing) + __options['x']