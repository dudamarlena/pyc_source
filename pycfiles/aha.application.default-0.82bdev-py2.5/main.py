# uncompyle6 version 3.7.4
# Python bytecode 2.5 (62131)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.3-i386/egg/application/controller/main.py
# Compiled at: 2010-10-24 22:00:57
"""
The main controller for sample application.

$Id: main.py 650 2010-08-16 07:45:11Z ats $
"""
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