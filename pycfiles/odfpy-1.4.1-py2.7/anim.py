# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/odf/anim.py
# Compiled at: 2020-01-18 11:47:38
from odf.namespaces import ANIMNS
from odf.element import Element

def Animate(**args):
    return Element(qname=(ANIMNS, 'animate'), **args)


def Animatecolor(**args):
    return Element(qname=(ANIMNS, 'animateColor'), **args)


def Animatemotion(**args):
    return Element(qname=(ANIMNS, 'animateMotion'), **args)


def Animatetransform(**args):
    return Element(qname=(ANIMNS, 'animateTransform'), **args)


def Audio(**args):
    return Element(qname=(ANIMNS, 'audio'), **args)


def Command(**args):
    return Element(qname=(ANIMNS, 'command'), **args)


def Iterate(**args):
    return Element(qname=(ANIMNS, 'iterate'), **args)


def Par(**args):
    return Element(qname=(ANIMNS, 'par'), **args)


def Param(**args):
    return Element(qname=(ANIMNS, 'param'), **args)


def Seq(**args):
    return Element(qname=(ANIMNS, 'seq'), **args)


def Set(**args):
    return Element(qname=(ANIMNS, 'set'), **args)


def Transitionfilter(**args):
    return Element(qname=(ANIMNS, 'transitionFilter'), **args)