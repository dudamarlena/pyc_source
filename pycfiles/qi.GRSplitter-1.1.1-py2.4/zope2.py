# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/qi/GRSplitter/zope2.py
# Compiled at: 2008-07-02 04:09:18
from Products.ZCTextIndex.PipelineFactory import element_factory
from qi.GRSplitter.GRSplitter import GRSplitter

def initialize(context):
    """Initializer called when used as a Zope 2 product."""
    try:
        element_factory.registerFactory('Word Splitter', 'GR splitter', GRSplitter)
    except ValueError:
        pass