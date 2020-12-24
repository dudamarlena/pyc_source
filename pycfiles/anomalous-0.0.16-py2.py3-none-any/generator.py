# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/anolislib/generator.py
# Compiled at: 2013-02-15 13:25:53
from __future__ import unicode_literals
import html5lib
from html5lib import treebuilders, treewalkers
from html5lib.serializer import htmlserializer
import lxml.html
from lxml import etree

def process(tree, processes=[
 b'sub', b'toc', b'xref'], **kwargs):
    """ Process the given tree. """
    for process in processes:
        try:
            process_module = getattr(__import__(b'processes', globals(), locals(), [str(process)], -1), process)
        except AttributeError:
            process_module = __import__(process, globals(), locals(), [], -1)

        getattr(process_module, process)(tree, **kwargs)


def fromFile(input, processes=set([b'sub', b'toc', b'xref']), parser=b'html5lib', profile=False, **kwargs):
    if False:
        tree = etree.parse(input)
    elif parser == b'lxml.html':
        tree = lxml.html.parse(input)
    else:
        builder = treebuilders.getTreeBuilder(b'lxml', etree)
        try:
            parser = html5lib.HTMLParser(tree=builder, namespaceHTMLElements=False)
        except TypeError:
            parser = html5lib.HTMLParser(tree=builder)

        tree = parser.parse(input)
    input.close()
    if profile:
        import os, tempfile
        statfile = tempfile.mkstemp()[1]
        try:
            import cProfile, pstats
            cProfile.runctx(b'process(tree, processes, **kwargs)', globals(), locals(), statfile)
            stats = pstats.Stats(statfile)
        except None:
            import hotshot, hotshot.stats
            prof = hotshot.Profile(statfile)
            prof.runcall(process, tree, processes, **kwargs)
            prof.close()
            stats = hotshot.stats.load(statfile)

        stats.strip_dirs()
        stats.sort_stats(b'time')
        stats.print_stats()
        os.remove(statfile)
    else:
        process(tree, processes, **kwargs)
    return tree


def toString(tree, output_encoding=b'utf-8', serializer=b'html5lib', **kwargs):
    if False:
        rendered = etree.tostring(tree, encoding=output_encoding)
    elif serializer == b'lxml.html':
        rendered = lxml.html.tostring(tree, encoding=output_encoding)
    else:
        walker = treewalkers.getTreeWalker(b'lxml')
        s = htmlserializer.HTMLSerializer(**kwargs)
        rendered = s.render(walker(tree), encoding=output_encoding)
    return rendered


def toFile(tree, output, output_encoding=b'utf-8', serializer=b'html5lib', **kwargs):
    rendered = toString(tree, output_encoding=output_encoding, serializer=serializer, **kwargs)
    output.write(rendered)


def fromToFile(input, output, **kwargs):
    tree = fromFile(input, **kwargs)
    toFile(tree, output, **kwargs)