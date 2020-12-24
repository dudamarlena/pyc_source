# uncompyle6 version 3.7.4
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/collective/sectionsubskin/test_support.py
# Compiled at: 2008-07-18 06:49:04
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile
from collective.sectionsubskin.browser.subskin import SubSkin
from collective.sectionsubskin.interfaces import ISubskinDefinition
from collective.sectionsubskin.definition import BaseDefinition

class IRedSkin(ISubskinDefinition):
    __module__ = __name__


class IBlueSkin(ISubskinDefinition):
    __module__ = __name__


class RedSkin(BaseDefinition):
    __module__ = __name__
    title = 'RedSkin'
    colour = 'FF0000'
    type_interface = IRedSkin


class BlueSkin(BaseDefinition):
    __module__ = __name__
    title = 'BlueSkin'
    colour = '0000FF'
    type_interface = IBlueSkin


class colours(SubSkin):
    """ Colours. """
    __module__ = __name__

    def render(self):
        """ Render the CSS. """
        try:
            return 'html { background-color: #%s; }' % self.subskin.colour
        except:
            return ''

    __call__ = render