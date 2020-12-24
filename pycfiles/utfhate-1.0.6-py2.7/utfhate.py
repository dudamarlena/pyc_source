# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/utfhate/utfhate.py
# Compiled at: 2015-07-24 10:27:18
import six

def continuation(integer):
    return byteliteral(integer)[-6:]


def binarycp(*args):
    """
    [internal!] utfhate.binarycp
    ------------------------------------------------
    Helper function which turns a number of integers
    into a list of binary strings. Works for a single
    argument (simple UTF-8 character) or many
    (multi-part with continuation bytes).

    May raise ValueError if input of an unexpected
    length  is encountered, e.g. not 0 < x < 7.
    ------------------------------------------------
    @param  args     list
                     integer
    @return          list
    """
    if not len(args):
        raise ValueError('UTF-8 sequence too short')
    else:
        if len(args) == 1:
            return [byteliteral(args[0])[-7:]]
        if len(args) < 7:
            leadbits = abs(len(args) - 7)
            return [
             byteliteral(args[0])[-leadbits:]] + map(continuation, args[1:])
        raise ValueError('UTF-8 continuation sequence too long')


def integercp(*args):
    return int(('').join(args), 2)


def htmlentity(integer):
    return '&#%d;' % integer


def hexliteral(integer):
    return hex(integer)[2:]


def byteliteral(integer):
    return bin(integer)[2:].zfill(8)


def utfentity(*args):
    return htmlentity(integercp(*binarycp(*args)))


def ascii(string):
    return six.text_type(string.encode('ascii'))


def multipart(char, iterable):
    """
    [internal!] utfhate.multipart
    ------------------------------------------------
    Helper function which handles multipart UTF-8
    characters and turns multiple input characters
    from iterable into a single output html entity.
    ------------------------------------------------
    @param  char     character
    @param  iterable iterable
    @return          (html entity, character)
    """
    bytes = [
     ord(char)]
    while True:
        try:
            char = iterable.next()
        except StopIteration:
            char = None
            break

        integer = ord(char)
        if integer in xrange(128, 192):
            bytes.append(integer)
        else:
            break

    entity = utfentity(*bytes)
    return (
     entity, char)


def htmlgenerator(chars, html_literal=False):
    """
    utfhate.htmlgenerator
    ------------------------------------------------
    From a unicode, byte-string or something that
    iterates over characters, safely create a valid
    string of html entities.

    Optionally set html_literal=True to receive an
    output with html encoded less than and greater
    than signs for (e.g.) rendering html as text.
    ------------------------------------------------
    @param  chars        string or iterable
    @param  html_literal boolean
    @return              generator
    """
    if not hasattr(chars, '__next__'):
        chars = iter(chars)

    def generate_htmlstring():
        char = None
        while True:
            char = char or chars.next()
            bytestring = isinstance(char, six.binary_type)
            integer = ord(char)
            if bytestring and integer in xrange(192, 256):
                entity, char = multipart(char, chars)
                yield entity
                continue
            elif integer > 127 or html_literal and integer in (60, 62):
                if bytestring:
                    yield utfentity(integer)
                else:
                    yield htmlentity(integer)
            else:
                yield ascii(char)
            char = None

        return

    return generate_htmlstring()


def htmlstring(chars, html_literal=False):
    """
    utfhate.htmlstring
    ------------------------------------------------
    See utfhate.htmlgenerator
    Consumes the generator and creates a string.
    ------------------------------------------------
    @param  chars        string or iterable
    @param  html_literal boolean
    @return              string
    """
    return ('').join(list(htmlgenerator(chars, html_literal=html_literal)))