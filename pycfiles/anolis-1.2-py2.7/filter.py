# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
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