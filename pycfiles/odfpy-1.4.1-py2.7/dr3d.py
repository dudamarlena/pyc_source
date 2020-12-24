# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/odf/dr3d.py
# Compiled at: 2020-01-18 11:47:38
import sys, os.path
sys.path.append(os.path.dirname(__file__))
from odf.namespaces import DR3DNS
from odf.element import Element
from odf.draw import StyleRefElement

def Cube(**args):
    return StyleRefElement(qname=(DR3DNS, 'cube'), **args)


def Extrude(**args):
    return StyleRefElement(qname=(DR3DNS, 'extrude'), **args)


def Light(Element):
    return StyleRefElement(qname=(DR3DNS, 'light'), **args)


def Rotate(**args):
    return StyleRefElement(qname=(DR3DNS, 'rotate'), **args)


def Scene(**args):
    return StyleRefElement(qname=(DR3DNS, 'scene'), **args)


def Sphere(**args):
    return StyleRefElement(qname=(DR3DNS, 'sphere'), **args)