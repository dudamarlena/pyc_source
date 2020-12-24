# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: c:\users\billingtonm\dropbox\code\pydiagrams\build\lib\pydiagrams\helpers\helper.py
# Compiled at: 2019-10-15 16:53:25
# Size of source mod 2**32: 1249 bytes
shape = {}
comment_format = '/* {text} */\n'

class helper(object):
    __doc__ = " \n    The Helper class stores the methods specific to a diagram language.\n    It's passed to the FlowchartBase object to be used when rendering code\n    "
    extension = ''
    name = ''

    @staticmethod
    def shape(in_shape, **kwargs):
        """ Translate a shape to this one recognized by the helper """
        return shape.get(in_shape, in_shape)

    @staticmethod
    def node(id, label=None, **kwargs):
        pass

    @staticmethod
    def edge(fromId, toId, label=None, **kwargs):
        pass

    @staticmethod
    def startDiagram(*args):
        """ Called first during the render to initialise a diagram """
        pass

    @staticmethod
    def endDiagram(*args):
        """ Called last uring the render to finalise a diagram """
        pass

    @staticmethod
    def startSubdiagram(id, **kwargs):
        pass

    @staticmethod
    def endSubdiagram(id, **kwargs):
        pass

    @staticmethod
    def comment(text):
        return comment_format.format(text=text)