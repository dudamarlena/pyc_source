# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build\bdist.win32\egg\webchuan\__init__.py
# Compiled at: 2008-10-22 07:35:12
from webchuan.element import Element
from webchuan.base import GetPage, Parser, If, DoNothing, FunctionHandler
from webchuan.decorator import Decorator, Retry
from webchuan.bin import Bin, Pipeline, Dispatcher
__version__ = '0.0.1'
__all__ = [
 'Element',
 'GetPage', 'Parser', 'If', 'DoNothing', 'FunctionHandler',
 'Decorator', 'Retry',
 'Bin', 'Pipeline', 'Dispatcher',
 'createPipeline']

def createPipeline(name, *args):
    """Create simple pipeline, for example 
    
    ::
    
        pipeline = Pipeline('pipeline')
        pipeline.add(element1)
        pipeline.add(element2)
        pipeline.add(element3)
        pipeline.link(element1, element2, element3)
        pipeline.first = element1
        pipeline.last = element3
        
    Code like this can be replace by
    
    ::
    
        pipeline = createPipeline('pipeline', element1, element2, element3)

    """
    pipeline = Pipeline(name)
    for element in args:
        pipeline.add(element)

    if len(args) >= 2:
        pipeline.link(*args)
    pipeline.first = args[0]
    pipeline.last = args[(-1)]
    return pipeline