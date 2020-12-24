# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/falkolab/cacheburster/metaconfigure.py
# Compiled at: 2010-12-17 11:51:49
import re, os.path, glob
from zope.configuration.exceptions import ConfigurationError
from zope.interface.declarations import implements
from falkolab.cacheburster.interfaces import IRuleFactory, IVersionRule
from zope.component.zcml import handler
from zope.browserresource.interfaces import IResource
from falkolab.cacheburster.rule import CacheBursterRule

class RuleFactory(object):
    implements(IRuleFactory)

    def __init__(self, cexpr, replacement, files, manager, name):
        self.__name = name
        self.__cexpr = cexpr
        self.__replacement = replacement
        self.__files = files
        self.__manager = manager

    def __call__(self, resource):
        rule = CacheBursterRule(resource, self.__cexpr, self.__replacement, self.__files, self.__manager)
        rule.__name__ = self.__name
        return rule


def cacheBurster(_context, from_, to, manager=None, fileset=None):
    files = None
    if fileset:
        files = set()
        for path in fileset:
            files = files | set(glob.glob(path))

        files = [ os.path.normcase(os.path.normpath(fileName)) for fileName in files ]
    flags = re.UNICODE
    fsCaseSensetive = os.path.normcase('Aa') == 'Aa'
    if not fsCaseSensetive:
        flags |= re.IGNORECASE
    try:
        cexpr = re.compile(raw(from_), flags)
    except:
        raise ConfigurationError("Can't compile rule expressions.")

    _context.action(discriminator=(
     'cacheBurster', from_), callable=cacheBusterHandler, args=(
     cexpr, raw(to), files, manager, from_, _context.info))
    return


def cacheBusterHandler(cexpr, replacement, files, manager, name, context_info):
    factory = RuleFactory(cexpr, replacement, files, manager, name)
    handler('registerAdapter', factory, (IResource,), IVersionRule, name=name, info=context_info)


escape_dict = {'\x07': '\\a', '\x08': '\\b', 
   '\\c': '\\c', 
   '\x0c': '\\f', 
   '\n': '\\n', 
   '\r': '\\r', 
   '\t': '\\t', 
   '\x0b': '\\v', 
   "'": "\\'", 
   '"': '\\"', 
   '\x00': '\\0', 
   '\x01': '\\1', 
   '\x02': '\\2', 
   '\x03': '\\3', 
   '\x04': '\\4', 
   '\x05': '\\5', 
   '\x06': '\\6', 
   '\x07': '\\7', 
   '\\8': '\\8', 
   '\\9': '\\9'}

def raw(text):
    """Returns a raw string representation of text"""
    return ('').join([ escape_dict.get(char, char) for char in text ])