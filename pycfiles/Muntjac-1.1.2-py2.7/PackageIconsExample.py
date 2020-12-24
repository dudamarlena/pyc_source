# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/muntjac/demo/sampler/features/commons/PackageIconsExample.py
# Compiled at: 2013-04-04 15:36:38
from muntjac.api import VerticalLayout, TabSheet, GridLayout, Embedded, Label, Alignment
from muntjac.ui.themes import Reindeer
from muntjac.terminal.theme_resource import ThemeResource

class PackageIconsExample(VerticalLayout):

    def __init__(self):
        super(PackageIconsExample, self).__init__()
        self._icons = [
         'arrow-down.png', 'arrow-left.png', 'arrow-right.png',
         'arrow-up.png', 'attention.png', 'calendar.png', 'cancel.png',
         'document.png', 'document-add.png', 'document-delete.png',
         'document-doc.png', 'document-image.png', 'document-pdf.png',
         'document-ppt.png', 'document-txt.png', 'document-web.png',
         'document-xsl.png', 'email.png', 'email-reply.png',
         'email-send.png', 'folder.png', 'folder-add.png',
         'folder-delete.png', 'globe.png', 'help.png', 'lock.png',
         'note.png', 'ok.png', 'reload.png', 'settings.png', 'trash.png',
         'trash-full.png', 'user.png', 'users.png']
        self._sizes = [
         '16', '32', '64']
        self.setSpacing(True)
        tabSheet = TabSheet()
        tabSheet.setStyleName(Reindeer.TABSHEET_MINIMAL)
        for size in self._sizes:
            iconsSideBySide = 2 if size == '64' else 3
            grid = GridLayout(iconsSideBySide * 2, 1)
            grid.setSpacing(True)
            grid.setMargin(True)
            tabSheet.addTab(grid, size + 'x' + size, None)
            tabSheet.addComponent(grid)
            for icon in self._icons:
                res = ThemeResource('../runo/icons/' + size + '/' + icon)
                e = Embedded(None, res)
                e.setWidth(size + 'px')
                e.setHeight(size + 'px')
                name = Label(icon)
                if size == '64':
                    name.setWidth('185px')
                else:
                    name.setWidth('150px')
                grid.addComponent(e)
                grid.addComponent(name)
                grid.setComponentAlignment(name, Alignment.MIDDLE_LEFT)

        self.addComponent(tabSheet)
        return