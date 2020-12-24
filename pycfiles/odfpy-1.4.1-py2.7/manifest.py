# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/odf/manifest.py
# Compiled at: 2020-01-18 11:47:38
import sys, os.path
sys.path.append(os.path.dirname(__file__))
from odf.namespaces import MANIFESTNS
from odf.element import Element

def Manifest(**args):
    return Element(qname=(MANIFESTNS, 'manifest'), **args)


def FileEntry(**args):
    return Element(qname=(MANIFESTNS, 'file-entry'), **args)


def EncryptionData(**args):
    return Element(qname=(MANIFESTNS, 'encryption-data'), **args)


def Algorithm(**args):
    return Element(qname=(MANIFESTNS, 'algorithm'), **args)


def KeyDerivation(**args):
    return Element(qname=(MANIFESTNS, 'key-derivation'), **args)