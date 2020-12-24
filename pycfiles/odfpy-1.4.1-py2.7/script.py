# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/odf/script.py
# Compiled at: 2020-01-18 11:47:38
from odf.namespaces import SCRIPTNS
from odf.element import Element

def EventListener(**args):
    return Element(qname=(SCRIPTNS, 'event-listener'), **args)