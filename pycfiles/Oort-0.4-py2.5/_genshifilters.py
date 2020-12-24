# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-fat/egg/oort/util/_genshifilters.py
# Compiled at: 2007-09-29 15:43:43
from genshi import XML
from genshi.core import Stream
START, END = Stream.START, Stream.END
XML_LANG = '{http://www.w3.org/XML/1998/namespace}lang'
RDF_WRAPPER = 'rdf-wrapper'

def language_filtered_xml(valueOrList, lang, fragment=True, encoding=None):
    if isinstance(valueOrList, unicode):
        return langXML(valueOrList, lang, fragment, encoding)
    else:
        events = []
        for value in valueOrList:
            if value:
                events.extend(langXML(value, lang, fragment, encoding).events)

        return Stream(events)


def langXML(text, lang, fragment=True, encoding=None):
    if text.startswith('<?xml ') or text.startswith('<!DOCTYPE '):
        fragment = False
    if fragment:
        text = '<xml>%s</xml>' % text
    if isinstance(text, unicode):
        encoding = 'utf-16'
        text = text.encode(encoding)
    stream = XML(text)
    lang_filter = filter_language(lang)
    if fragment:
        return stream | skip_outer | lang_filter
    else:
        return stream | lang_filter


def skip_outer(stream):
    """A filter that doesn't actually do anything with the stream."""
    istream = iter(stream)
    istream.next()
    last = None
    for content in istream:
        if last:
            yield last
        last = content

    return


def filter_language(lang):

    def filter_lang(stream):
        depth = 0
        eating = False
        for (kind, data, pos) in stream:
            if kind == START and lang:
                elemLang = get_elem_lang(data)
                if elemLang:
                    if elemLang != lang:
                        eating = True
            if eating == True:
                if kind == START:
                    depth += 1
                elif kind == END:
                    depth -= 1
                    if depth == 0:
                        eating = False
                continue
            if kind == START and data[0] == RDF_WRAPPER:
                continue
            elif kind == END and data == RDF_WRAPPER:
                continue
            else:
                yield (
                 kind, data, pos)

    return filter_lang


def get_elem_lang(data):
    for (name, value) in data[1]:
        if name in (XML_LANG, 'lang'):
            return value