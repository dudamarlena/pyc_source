# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/web2py_utils/menu.py
# Compiled at: 2010-05-22 13:48:28
from gluon.html import OL, UL, LI, A

class MenuManager:
    """
    Manages menu's for blogitizor.

    Example usage

    menu = MenuManager()
    main_menu = MenuItem(
        title, url
        activewhen(
            controller ==
            application ==
            action ==
        )
    """
    TITLE_INDEX = 0
    URL_INDEX = 1
    ACTIVE_INDEX = 2

    def __init__(self, request):
        self.menus = {}
        self.request = request

    def add_menu_item(self, menu, title, url, activewhen=dict(c=None, f=None, a=None, custom=None)):
        if not self.menus.has_key(menu):
            self.menus[menu] = []
        self.menus[menu].append([
         title, url, self.iam(activewhen)])

    def render_menu(self, menu, type='ol'):
        if type == 'ol':
            xml = OL(_id=menu, _class='menu')
        else:
            xml = UL(_id=menu, _class='menu')
        if self.menus.has_key(menu):
            for item in self.menus[menu]:
                if item[MenuManager.ACTIVE_INDEX]:
                    c = 'active'
                else:
                    c = None
                xml.append(LI(A(item[MenuManager.TITLE_INDEX], _href=item[MenuManager.URL_INDEX]), _class=c))

        else:
            xml = ''
        return xml

    def is_active_menu(self, when):
        c = when.get('c', None)
        f = when.get('f', None)
        a = when.get('a', None)
        custom = when.get('custom', None)
        i = False
        if c:
            if c == self.request.controller:
                i = True
            else:
                i = False
        if f:
            fs = f.split('|')
            onehit = False
            for fps in fs:
                if fps == self.request.function:
                    onehit = True

            i = onehit and i
        if a:
            if a == self.request.args:
                i = True and i
            else:
                i = False
        if custom:
            for lambfunc in custom:
                i = lambfunc(i)

        return i

    iam = is_active_menu