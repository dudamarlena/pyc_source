# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/webias/gnosis/xml/pickle/util/_flags.py
# Compiled at: 2015-04-13 16:10:48
PARANOIA = 1

def setParanoia(val):
    global PARANOIA
    PARANOIA = val


def getParanoia():
    return PARANOIA


DEEPCOPY = 0

def setDeepCopy(val):
    global DEEPCOPY
    DEEPCOPY = val


def getDeepCopy():
    return DEEPCOPY


TYPE_IN_BODY = {}

def setInBody(typename, val):
    global TYPE_IN_BODY
    TYPE_IN_BODY[typename] = val


def getInBody(typename):
    return TYPE_IN_BODY.get(typename) or 0


CURRENT_PARSER = 'DOM'

def setParser(name):
    """Set current parser, by name"""
    global CURRENT_PARSER
    CURRENT_PARSER = name


def getParser():
    return CURRENT_PARSER


def enumParsers():
    """Return available parsers as a dictionary of (name: parser)"""
    dict = {}
    try:
        from gnosis.xml.pickle.parsers._dom import thing_from_dom
        dict['DOM'] = thing_from_dom
    except:
        pass

    try:
        from gnosis.xml.pickle.parsers._sax import thing_from_sax
        dict['SAX'] = thing_from_sax
    except:
        pass

    try:
        from gnosis.xml.pickle.parsers._cexpat import thing_from_cexpat
        dict['cEXPAT'] = thing_from_cexpat
    except:
        pass

    return dict


VERBOSE_XML = 0

def setVerbose(val):
    """Setting verbose to 0 will turn off some fields that
    aren't technically necessary (for example, the family field
    won't be included unless a mutated type is present).
    You need to set this to 1 if you're talking to a parser that
    requires that all fields be present."""
    global VERBOSE_XML
    VERBOSE_XML = val


def getVerbose():
    return VERBOSE_XML