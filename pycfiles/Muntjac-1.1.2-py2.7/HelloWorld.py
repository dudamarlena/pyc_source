# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-x86_64/egg/muntjac/demo/HelloWorld.py
# Compiled at: 2013-04-04 15:36:38
from muntjac.api import Application, Window, Label

class HelloWorld(Application):

    def init(self):
        """Init is invoked on application load (when a user accesses
        the application for the first time).
        """
        main = Window('Hello window')
        self.setMainWindow(main)
        main.addComponent(Label('Hello World!'))