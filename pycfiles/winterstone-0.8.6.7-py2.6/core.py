# uncompyle6 version 3.7.4
# Python bytecode 2.6 (62161)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.linux-i686/egg/winter_project/core.py
# Compiled at: 2011-04-27 02:55:02
from PyQt4.QtGui import *
from PyQt4.QtCore import *
from winterstone.baseQt import API
from winterstone.winterBug import try_this

class Core(object):
    """
        Store all your app logic here
    """

    def _afterInit(self):
        """
            when application totally init
        """
        self.api = API()

    def main(self):
        """
            dummy for main core method. no autorun
        """
        pass

    def test(self):
        """
            try execute in debug line "core.test"
        """
        self.api.info('Test success!')