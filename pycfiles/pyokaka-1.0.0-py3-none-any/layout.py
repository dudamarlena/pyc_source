# uncompyle6 version 3.6.7
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build\bdist.win32\egg\pyojo\js\dijit\layout.py
# Compiled at: 2013-06-09 06:06:20
__doc__ = ' Page layout widgets.\n'
from ..dijit import Dijit

class ContentPane(Dijit):
    """ Simple panel.
    """
    require = [
     'dojo/ready',
     'dijit/layout/ContentPane']

    def add(self, target):
        return self.add_loc('%s.addChild(%s);' % (target, self.name))

    def select(self, target):
        return self.add_loc('%s.selectChild(%s);' % (target, self.name))


class BorderContainer(Dijit):
    """ A parent panel who contains other panels.
    """
    require = [
     'dojo/ready',
     'dijit/layout/BorderContainer',
     'dijit/layout/ContentPane']

    def init(self):
        style = 'height: 100%; width: 100%;background-color:rgb(239, 239, 239);'
        self.member.update({'style': style, 'gutters': False})

    def panel(self, region='center', name=None, style=None, **kwargs):
        if name is None:
            name = self.name + '_' + region
        if style is None:
            style = 'padding:0px; margin:0px;'
        new = ContentPane(name, region=region, style=style, **kwargs).new(False)
        self.loc += '%s.addChild(%s);' % (self.name, new)
        return


class DijitPanelMixin(object):
    """ Provides the panel method for containers.
    """

    def init(self):
        self.member.update({'style': 'height: 100%; width: 100%;'})

    def panel(self, name=None, title='', style=None, **kwargs):
        if style is None:
            style = 'padding:0px; margin:0px;'
        new = ContentPane(name, title=title, style=style, **kwargs).new(False)
        self.loc += '%s.addChild(%s);' % (self.name, new)
        return


class AccordionContainer(DijitPanelMixin, Dijit):
    require = [
     'dojo/ready',
     'dijit/layout/AccordionContainer',
     'dijit/layout/ContentPane']


class TabContainer(DijitPanelMixin, Dijit):
    require = [
     'dojo/ready',
     'dijit/layout/TabContainer',
     'dijit/layout/ContentPane']