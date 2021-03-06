# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/salamoia/utility/tpgext.py
# Compiled at: 2007-12-02 16:26:55
from tpg import *
import salamoia.utility, os

class DynamicParser(object):
    __module__ = __name__

    def __new__(cls, grammar):
        return ParserMetaClass(cls.__name__, (Parser,), {'__doc__': grammar})()


class ExternParserMetaClass(ParserMetaClass):
    __module__ = __name__

    def __init__(cls, name, bases, dict):
        super(ExternParserMetaClass, cls).__init__(name, bases, dict)
        try:
            filename = dict['filename'] + '.tpg'
            base = __import__(cls.__module__).__path__[0]
            print base
            grammar = file(base + '/frontends/' + filename).read()
        except KeyError:
            pass
        else:
            parser = TPGParser(sys._getframe(1).f_globals)
            for (attribute, source, code) in parser(grammar):
                setattr(cls, attribute, code)


class ExternParser(Parser):
    __module__ = __name__
    __metaclass__ = ExternParserMetaClass


class ExternVerboseParser(VerboseParser):
    __module__ = __name__
    __metaclass__ = ExternParserMetaClass


def GenerateParser(externParser):
    cls = externParser
    base = __import__(cls.__module__).__path__[0]
    basefilename = base + '/frontends/' + externParser.filename
    filename = basefilename + '.tpg'
    outfilename = basefilename + '.py'
    print 'generating parser', externParser.__name__
    grammar = file(filename).read()
    out = file(outfilename, 'w')
    parser = TPGParser(sys._getframe(1).f_globals)
    print >> out, 'import salamoia.utility'
    print >> out, 'import salamoia.utility.tpg'
    print >> out, 'class %s(salamoia.utility.tpg.Parser):' % cls.__name__
    print >> out, '  generated = True'
    print >> out, '  __metaclass__ = type'
    for (attribute, source, code) in parser(grammar):
        print >> out, ' ', source

    out.close()


import os

def ImportParser(packname, modname, classname, glb, basemodule):
    fallbackClass = ExternParser
    path = basemodule.__path__[0]
    fullname = path + '/' + packname + '/' + modname
    if not os.path.exists(fullname + '.py'):
        print 'generated parser', classname, 'does not exist at', fullname + '.py', '. generating at runtime'
        return fallbackClass
    if os.path.exists(fullname + '.tpg') and os.path.getmtime(fullname + '.tpg') > os.path.getmtime(fullname + '.py'):
        print fullname + '.tpg', fullname + '.py'
        print 'generated parser', classname, 'older than source, not importing'
        return fallbackClass
    try:
        m = __import__(packname + '.' + modname, glb, [], [modname])
        m.__dict__.update(glb)
        cls = getattr(m, classname)
        return cls
    except ImportError:
        return fallbackClass


from salamoia.tests import *
runDocTests()