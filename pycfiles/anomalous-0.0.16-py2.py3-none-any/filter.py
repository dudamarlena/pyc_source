# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.linux-x86_64/egg/anolislib/processes/filter.py
# Compiled at: 2011-08-30 06:36:54
from lxml import cssselect

def filter(ElementTree, **kwargs):
    if 'filter' not in kwargs or kwargs['filter'] == None:
        return
    selector = cssselect.CSSSelector(kwargs['filter'])
    for element in selector(ElementTree.getroot()):
        element.getparent().remove(element)

    return