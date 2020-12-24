# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/xix/utils/tools/parse.py
# Compiled at: 2006-03-02 13:58:59
__author__ = 'Drew Smathers'
__contact__ = 'andrew.smathers@turner.com'
from xix.utils.tools.options import OptionException, Option
from xix.utils.tools.options import OptionCollection
from xix.utils.tools.interfaces import IParser
from xix.utils.comp.interface import implements
import re
CONT_CHAR_PATT = re.compile('^[a-zA-Z_]')
VALUE_PATT = re.compile('"([^"]*)"')
VAR_NAME = re.compile('^[a-zA-Z_]\\w*$')

class OptionParser:
    """Implement IParser

    >>> from zope.interface.verify import verifyClass
    >>> int(verifyClass(IParser, OptionParser))
    1
    """
    __module__ = __name__
    implements(IParser)

    def parse(self, text):
        pass


class OptionParserException(Exception):
    """Generic parse exception for OptionParser object. Raised
    on known exception in parse method of parser.
    """
    __module__ = __name__


class TextualOptionParser(OptionParser):
    """Parser for plain text configuration for options.  Plain
    text configuration provides subset of optparse API.
    
    Example:

    >>> from zope.interface.verify import verifyClass
    >>> int(verifyClass(IParser, TextualOptionParser))
    1
    """
    __module__ = __name__
    START = 0
    READING_OPTION = 1

    def __init__(self):
        raise NotImplementedError

    def parse(self, input):
        state = self.START
        nothing = self.__isnothing
        comment = self.__isacomment
        cont = self.__isacont
        start = self.__isastart
        options = OptionCollection()
        curried = None
        if hasattr(input, 'readlines'):
            lines = input
        else:
            lines = input.split('\n')
        for line in lines:
            if nothing(line) or comment(line):
                continue
            elif start(line):
                if curried:
                    option = Option(**curried)
                    options.append(option)
                    curried = None
                curried = self.__build_options(line)
            elif cont(line):
                if curried is None:
                    errmsg = 'Cannot parse: %s' % line
                    raise OptionParserException, errmsg
                self.__build_options(line, curried=curried)
            else:
                errmsg = 'Cannot parse: %s' % line
                raise OptionParserException, errmsg

        if curried:
            option = Option(**curried)
            options.append(option)
        return options

    def __build_options(self, line, curried=None):
        l = line.strip()
        tokens = l.split()
        if not curried:
            (short, long) = tokens[:2]
            if not (short[0] == '-' or long[0] != '-'):
                errmsg = 'No short/long flags given'
                raise OptionParserException, errmsg
            if short[:2] == '--':
                if long[0] == '-':
                    errmsg = 'Short flag should be given before long flag'
                    raise OptionParserException, errmsg
                long = short
                args = tokens[1:]
            elif short[:1] == '-':
                if long[:2] != '--':
                    args = tokens[1:]
                    long = ''
                else:
                    args = tokens[2:]
            else:
                errmsg = (
                 'Invalid token sequence: ', (',').join(tokens))
                raise OptionParserException, errmsg
            curried = {'short_desc': short, 'long_desc': long}
        else:
            args = tokens
        pairs = self.__validargs(args)
        for (name, value) in pairs:
            curried[name] = value

        return curried

    def __isnothing(self, line):
        l = line.strip()
        return l == ''

    def __isastart(self, line):
        l = line.strip()
        return l[0] == '-'

    def __isacomment(self, line):
        l = line.strip()
        return l == '#'

    def __isacont(self, line):
        l = line.strip()
        return CONT_CHAR_PATT.match(l) is not None

    def __isastr(self, value):
        return VALUE_PATT.match(value) is not None

    def __getvalue(self, text):
        if self.__isacont(text):
            return VALUE_PATT.match(text).groups()[0]
        else:
            return text

    def __validargs(self, args):
        try:
            pairs = [ (name, self.__getvalue(value)) for (name, value) in [ arg.split('=') for arg in args ] ]
            for (name, value) in pairs:
                if VAR_NAME.match(name) is None:
                    errmsg = 'Invlaid name in assignment: %s= ...' % name
                    raise OptionParserException, errmsg

        except Exception, e:
            errmsg = 'invalid argument structure: %s. (%s)' % (args, e)
            raise OptionParserException, errmsg

        return pairs


_TEST_OPTIONS_TEXTUAL = '\n-s --host dest="host" default="example.com"\n            help="name of host"\n            \n-z --zoo dest="zoo" default=\'atl\'\n   # This is a comment\n            help=\'where animals live"\n\n--recurring action="store_true" dest="recurring_only"\nhelp="let it be recurring"\n            \n# This is a comment\n            \n-p --path dest="path" default="/home"\n            help="the yellow brick road"\n'

def _testTextualOptionParser():
    """Example:

    #>>> parser = TextualOptionParser()
    #>>> o = parser.parse(_TEST_OPTIONS_TEXTUAL)
    #>>> print o.zoo
    #atl
    #>>> print o._data['zoo'].help
    #where animals live
    #>>> print o._data['zoo'].short_desc
    #-z
    #>>> print o._data['zoo'].long_desc
    #--zoo
    #>>> print o._data['recurring_only'].help
    #let it be recurring
    #>>> print o._data['recurring_only'].long_desc
    #--recurring
    #>>> print o._data['recurring_only'].short_desc
    #None

    >>> try:
    ...     parser = TextualOptionParser()
    ... except NotImplementedError:
    ...     print 'TextualOptionParser is not complete'
    ...
    TextualOptionParser is not complete
    """
    pass