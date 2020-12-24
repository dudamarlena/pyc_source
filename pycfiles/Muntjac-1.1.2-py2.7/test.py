# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/muntjac/demo/sampler/test.py
# Compiled at: 2013-04-04 15:36:38
from muntjac.main import muntjac
from muntjac.application import Application
from muntjac.ui.window import Window
from muntjac.demo.sampler.features.dragndrop.DragDropServerValidationExample import DragDropServerValidationExample as Example

class App(Application):

    def init(self):
        main = Window('Muntjac')
        main.setTheme('sampler-reindeer')
        self.setMainWindow(main)
        main.addComponent(Example())


if __name__ == '__main__':
    muntjac(App, nogui=True, forever=True, debug=True)