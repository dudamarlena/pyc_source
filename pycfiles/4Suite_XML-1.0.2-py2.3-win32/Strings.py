# uncompyle6 version 3.7.4
# Python bytecode 2.3 (62011)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: \Ft\Xml\Xslt\Exslt\Strings.py
# Compiled at: 2006-12-26 13:39:48
"""
EXSLT - Strings

Copyright 2005 Fourthought, Inc. (USA).
Detailed license and copyright information: http://4suite.org/COPYRIGHT
Project home, documentation, distributions: http://4suite.org/
"""
import re, codecs
from Ft.Xml.XPath import Conversions, XPathTypes, NAMESPACE_NODE
from Ft.Xml.Xslt import XsltRuntimeException, Error
from Ft.Xml.Xslt.CopyOfElement import CopyNode
EXSL_STRINGS_NS = 'http://exslt.org/strings'

def Align(context, target, padding, alignment=''):
    """
    The str:align function aligns a string within another string.

    See http://exslt.org/str/functions/align/str.align.html for further
    explanation.
    """
    target = Conversions.StringValue(target)
    padding = Conversions.StringValue(padding)
    alignment = alignment and Conversions.StringValue(alignment)
    if len(target) > len(padding):
        return target[:len(padding)]
    if alignment == 'right':
        result = padding[:-len(target)] + target
    elif alignment == 'center':
        left = (len(padding) - len(target)) / 2
        right = left + len(target)
        result = padding[:left] + target + padding[right:]
    else:
        result = target + padding[len(target):]
    return result


def Concat(context, nodeset):
    """
    The str:concat function takes a node set and returns the concatenation of
    the string values of the nodes in that node set. If the node set is empty,
    it returns an empty string.
    """
    if type(nodeset) != type([]):
        raise XsltRuntimeException(Error.WRONG_ARGUMENT_TYPE, context.currentInstruction)
    strings = map(Conversions.StringValue, nodeset)
    return ('').join(strings)


def DecodeUri(context, uri, encoding='UTF-8'):
    """
    The str:decode-uri function decodes a percent-encoded string, such as
    one would find in a URI.
    """
    uri = Conversions.StringValue(uri)
    encoding = Conversions.StringValue(encoding)
    try:
        decoder = codecs.lookup(encoding)[1]
    except LookupError:
        return ''

    def repl(match, decoder=decoder):
        sequence = match.group()[1:]
        ordinals = sequence.split('%')
        characters = [ chr(int(ordinal, 16)) for ordinal in ordinals ]
        return decoder(('').join(characters), 'ignore')[0]

    return re.sub('(?:%[0-9a-fA-F]{2})+', repl, uri)


_unreserved = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-_.!~*'()%"
_reserved = ';/?:@&=+$,[]'

def EncodeUri(context, uri, escapeReserved, encoding='UTF-8'):
    """
    The str:encode-uri function percent-encodes a string for embedding in a URI.
    The second argument is a boolean indicating whether to escape reserved characters;
    if true, the given string can be a URI already, with just some of its characters
    needing to be escaped (not recommended, but users who don't understand the nuances
    of the URI syntax tend to prefer it over assembling a URI piece-by-piece).
    """
    uri = Conversions.StringValue(uri)
    escape_reserved = Conversions.BooleanValue(escapeReserved)
    encoding = Conversions.StringValue(encoding)
    try:
        encoder = codecs.lookup(encoding)[0]
    except LookupError:
        return ''

    uri = re.sub('%(?![0-9A-Fa-f]{2})', '%25', uri)
    safe = _unreserved
    if not escape_reserved:
        safe += _reserved
    res = list(uri)
    for i in xrange(len(res)):
        c = res[i]
        if c not in safe:
            try:
                if ord(c) > 127:
                    encoded = encoder(c, 'strict')[0]
                else:
                    encoded = chr(ord(c))
            except UnicodeError:
                encoded = '%3F'
            else:
                encoded = ('').join([ '%%%02X' % ord(c) for c in encoded ])

            res[i] = encoded

    return ('').join(res)


def Padding(context, length, chars=None):
    """
    The str:padding function creates a padding string of a certain length.

    The second argument gives a string to be used to create the padding.
    This string is repeated as many times as is necessary to create a string
    of the length specified by the first argument; if the string is more than
    a character long, it may have to be truncated to produce the required
    length. If no second argument is specified, it defaults to a space (' ').
    """
    length = int(Conversions.NumberValue(length))
    chars = chars and Conversions.StringValue(chars) or ' '
    return (chars * length)[:length]


def Replace(context, s, searchNodes, replNodes):
    """
    The str:replace function converts a string to a node-set, with
    each instance of a substring from a given list (obtained from the
    string-values of nodes in the second argument) replaced by the
    node at the corresponding position of the node-set given as the
    third argument. Unreplaced substrings become text nodes.

    The second and third arguments can be any type of object; if
    either is not a node-set, it is treated as if it were a node-set
    of just one text node, formed from the object's string-value.

    Attribute and namespace nodes in the replacement set are
    erroneous but are treated as empty text nodes.

    All occurrences of the longest substrings are replaced first,
    and once a replacement is made, that span of the original string
    is no longer eligible for future replacements.

    An empty search string matches between every character of the
    original string.

    See http://exslt.org/str/functions/replace/str.replace.html for details.
    """
    s = Conversions.StringValue(s)
    if not isinstance(searchNodes, XPathTypes.NodesetType):
        search_set = [
         Conversions.StringValue(searchNodes)]
    else:
        search_set = map(Conversions.StringValue, searchNodes)
    if type(replNodes) is not type([]):
        replace_set = [
         context.node.rootNode.createTextNode(Conversions.StringValue(replNodes))]
    else:
        replace_set = [ (n.nodeType == n.ATTRIBUTE_NODE or n.nodeType == NAMESPACE_NODE) and context.node.createTextNode('') or n for n in replNodes ]
    replacements = map(None, search_set, replace_set)
    replacements = [ tup for tup in replacements if tup[0] ]
    replacements.sort(lambda a, b: cmp(len(a[0]), len(b[0])))
    processor = context.processor
    processor.pushResultTree(context.currentInstruction.baseUri)
    try:
        _replace(s, replacements, processor)
    finally:
        rtf = processor.popResult()
    return rtf.childNodes
    return


def _replace(s, replmap, processor):
    """
    Supports str:replace(). s is a string. replmap is a list of tuples,
    where each tuple is a search string and a replacement node or None.
    This recursive function will cause the original string to have
    occurrences of the search strings replaced with the corresponding
    node or deleted. When a replacement is made, that portion of the
    original string is no longer available for further replacements.
    All replacements are made for each search string before moving on
    to the next. Empty search strings match in between every character
    of the original string.
    """
    rm = replmap[:]
    if rm:
        sr = rm.pop()
        if sr[0]:
            nms = s.split(sr[0])
        else:
            nms = [ c for c in s ]
        last_i = len(nms) - 1
        for i in xrange(len(nms)):
            if nms[i]:
                _replace(nms[i], rm, processor)
            if i < last_i and sr[1]:
                CopyNode(processor, sr[1])

    else:
        processor.writer.text(s)
    return


def Split(context, string, pattern=' '):
    """
    The str:split function splits up a string and returns a node set of
    token elements, each containing one token from the string.

    The first argument is the string to be split. The second argument is a
    pattern string (default=' '). The string given by the first argument is
    split at any occurrence of this pattern. An empty string pattern will
    result in a split on every character in the string.
    """
    string = Conversions.StringValue(string)
    pattern = Conversions.StringValue(pattern)
    processor = context.processor
    processor.pushResultTree(context.currentInstruction.baseUri)
    try:
        if pattern:
            for token in string.split(pattern):
                processor.writer.startElement('token')
                processor.writer.text(token)
                processor.writer.endElement('token')

        for ch in string:
            processor.writer.startElement('token')
            processor.writer.text(ch)
            processor.writer.endElement('token')

    finally:
        rtf = processor.popResult()
    return rtf.childNodes


def Tokenize(context, string, delimiters='\t\n\r '):
    """
    The str:tokenize function splits up a string and returns a node set of
    'token' elements, each containing one token from the string.

    The first argument is the string to be tokenized. The second argument
    is a string consisting of a number of characters. Each character in
    this string is taken as a delimiting character. The string given by the
    first argument is split at any occurrence of any of these characters.
    """
    string = Conversions.StringValue(string)
    if delimiters:
        delimiters = Conversions.StringValue(delimiters)
        tokens = re.split('[%s]' % delimiters, string)
    else:
        tokens = string
    processor = context.processor
    processor.pushResultTree(context.currentInstruction.baseUri)
    try:
        for token in tokens:
            processor.writer.startElement('token')
            processor.writer.text(token)
            processor.writer.endElement('token')

    finally:
        rtf = processor.popResult()
    return rtf.childNodes


ExtNamespaces = {EXSL_STRINGS_NS: 'str'}
ExtFunctions = {(EXSL_STRINGS_NS, 'align'): Align, (EXSL_STRINGS_NS, 'concat'): Concat, (EXSL_STRINGS_NS, 'decode-uri'): DecodeUri, (EXSL_STRINGS_NS, 'encode-uri'): EncodeUri, (EXSL_STRINGS_NS, 'padding'): Padding, (EXSL_STRINGS_NS, 'replace'): Replace, (EXSL_STRINGS_NS, 'split'): Split, (EXSL_STRINGS_NS, 'tokenize'): Tokenize}
ExtElements = {}