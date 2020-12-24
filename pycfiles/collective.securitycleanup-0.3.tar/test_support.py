# uncompyle6 version 3.6.7
# Python bytecode 2.4 (62061)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
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