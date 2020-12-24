# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: build/bdist.macosx-10.13-intel/egg/flask_boot/project/application/core/app.py
# Compiled at: 2018-09-06 06:26:33
import sys
from flask import Flask
from application.api import api_init
from application.core.signal import signal
reload(sys)
sys.setdefaultencoding('utf-8')

class ApplicationApp(Flask):

    def init(self, settings):
        self.config.update(**settings.FLASK)
        api_init(self)
        signal(self)