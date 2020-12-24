# uncompyle6 version 3.7.4
# Python bytecode 3.8 (3413)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: c:\users\billingtonm\dropbox\code\pydiagrams\build\lib\pydiagrams\helpers\PUML.py
# Compiled at: 2019-10-20 20:24:48
# Size of source mod 2**32: 3393 bytes
from pydiagrams.helpers.constants import *
from pydiagrams.helpers import helper
helper.shape = {'Cloud':'cloud', 
 'Database':'database', 
 'Folder':'folder', 
 'Frame':'frame', 
 'Node':'node', 
 'Package':'package', 
 'Rectangle':'rectangle', 
 'Component':'component', 
 'Interface':'interface', 
 'Diamond':'interface', 
 'Table':'rectangle', 
 'View':'rectangle', 
 'Package':'package', 
 'File':'folder', 
 'Integration':'interface', 
 'System':'cloud', 
 'Task':'component'}
helper.comment_format = "' {text}\n"

class Helper(helper.helper):
    __doc__ = " \n    The Helper class stores the methods specific to a diagram language.\n    It's passed to the FlowchartBase object to be used when rendering code\n    "
    extension = 'puml'
    name = 'PUML'
    arrows = {'vertical':'-->', 
     'horizontal':'->', 
     'right':'-right->', 
     'left':'-left->', 
     'up':'-up->', 
     'down':'-down->', 
     'hline':'-', 
     'vline':'--', 
     'vdotted':'..>'}

    @staticmethod
    def node(id, label, **kwargs):
        n = Helper.shape(kwargs.get('shape', 'rectangle'))
        if label or label != '':
            n += ' "{}"'.format(label)
        n += ' as {} '.format(id)
        if fillcolor in kwargs:
            FILLCOLOR = kwargs[fillcolor]
            if not FILLCOLOR.startswith('#'):
                n += '#'
            n += FILLCOLOR
        if 'note' in kwargs:
            n += '\nnote right of {id}\n{note}\nend note'.format(id=id, note=(kwargs['note']))
        return n

    @staticmethod
    def edge(fromId, toId, label=None, **kwargs):
        dir = kwargs.get('dir', None)
        if not dir:
            dir = 'vertical'
        edge = '{} {} {}'.format(fromId, Helper.arrows[dir], toId)
        if label:
            edge += ' : ' + label
        return edge

    @staticmethod
    def startDiagram(*args):
        """ Called first during the render to initialise a diagram """
        return '@startuml {filename}\n!include w:\\plantuml\\theme-blue.iuml\n        '.format(filename=(args[0]))

    @staticmethod
    def endDiagram(*args):
        """ Called last uring the render to finalise a diagram """
        return '@enduml'

    @staticmethod
    def startSubdiagram(id, label, **kwargs):
        shape = Helper.shape(kwargs.get('shape', 'rectangle'))
        t = shape
        if label:
            if label != '':
                t += ' "{}" '.format(label)
        color = str(kwargs.get('fillcolor', ''))
        if color:
            if not color.startswith('#'):
                t += '#'
            t += str(color)
        return t + ' {\n'

    @staticmethod
    def endSubdiagram(id, label, **kwargs):
        return '\n}} \n'.format(id=id)