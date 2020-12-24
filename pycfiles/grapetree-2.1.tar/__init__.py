# uncompyle6 version 3.7.4
# Python bytecode 2.7 (62211)
# Decompiled from: Python 3.6.9 (default, Apr 18 2020, 01:56:04) 
# [GCC 8.4.0]
# Embedded file name: /home/zhemin/software/GrapeTree/module/__init__.py
# Compiled at: 2019-03-06 20:09:44
from flask import Flask
import sys, os
from . import config
if getattr(sys, 'frozen', False):
    template_folder = sys._MEIPASS
    static_folder = os.path.join(sys._MEIPASS, 'static')
    app = Flask(__name__, template_folder=template_folder, static_folder=static_folder)
else:
    app = Flask(__name__, template_folder=os.path.dirname(os.path.dirname(os.path.abspath(__file__))), static_folder=os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'static'))
app.config.from_object(config)
from . import views