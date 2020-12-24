# uncompyle6 version 3.6.7
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.8.2 (tags/v3.8.2:7b3ab59, Feb 25 2020, 23:03:10) [MSC v.1916 64 bit (AMD64)]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/application/controller/main.py
# Compiled at: 2010-10-24 22:00:57
__doc__ = '\nThe main controller for sample application.\n\n$Id: main.py 650 2010-08-16 07:45:11Z ats $\n'
__author__ = 'Atsushi Shibata <shibata@webcore.co.jp>'
__docformat__ = 'plaintext'
__licence__ = 'BSD'
from aha.controller.basecontroller import BaseController
from aha.controller.decorator import expose

class MainController(BaseController):
    """
    The Main Controller.
    """

    @expose
    def index(self):
        """
        A method to say 'Aha :-).'.
        """
        self.render('Aha :-).')